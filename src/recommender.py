import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file into dicts, converting numeric columns to int/float."""
    print(f"Loading songs from {csv_path}...")

    songs: List[Dict] = []

    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            for key in ("energy", "valence", "danceability", "acousticness"):
                row[key] = float(row[key])
            songs.append(row)

    print(f"Loaded songs: {len(songs)}")
    
    return songs

# Max points per feature (total = 8.0). See "Algorithm Recipe" in README.md.
WEIGHTS = {
    "genre": 2.0,
    "mood": 1.0,
    "energy": 1.5,
    "acousticness": 1.0,
    "valence": 1.0,
    "danceability": 0.75,
    "tempo_bpm": 0.75,
}

# Largest possible gap for each numeric feature. The 0-1 features span 1.0;
# tempo spans the BPM column (60 to 152).
NUMERIC_SPANS = {
    "energy": 1.0,
    "acousticness": 1.0,
    "valence": 1.0,
    "danceability": 1.0,
    "tempo_bpm": 92.0,
}

# Maps each numeric song column to its key in the user's taste profile.
NUMERIC_TARGET_KEYS = {
    "energy": "target_energy",
    "acousticness": "target_acousticness",
    "valence": "target_valence",
    "danceability": "target_danceability",
    "tempo_bpm": "target_tempo_bpm",
}

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores one song out of 8.0, returning (score, reasons); skips features missing from user_prefs."""
    score = 0.0
    reasons: List[str] = []

    # Categorical features: all-or-nothing.
    for feature, pref_key in (("genre", "favorite_genre"), ("mood", "favorite_mood")):
        favorite = user_prefs.get(pref_key)
        if favorite is None:
            continue
        if str(song[feature]).lower() == str(favorite).lower():
            points = WEIGHTS[feature]
            score += points
            reasons.append(f"{feature} match: {song[feature]} (+{points:.2f})")

    # Numeric features: points scale with closeness to the user's target.
    for feature, target_key in NUMERIC_TARGET_KEYS.items():
        target = user_prefs.get(target_key)
        
        if target is None:
            continue
        
        gap = abs(song[feature] - target)
        closeness = max(0.0, 1.0 - gap / NUMERIC_SPANS[feature])
        points = WEIGHTS[feature] * closeness
        
        score += points
        
        reasons.append(
            f"{feature} {song[feature]:g} vs target {target:g} (+{points:.2f})"
        )

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Returns the top k (song, score, explanation) tuples, highest score first."""
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    # Highest score first; ties fall back to title so output is stable.
    ranked = sorted(scored, key=lambda item: (-item[1], item[0]["title"]))

    return [(song, score, "; ".join(reasons)) for song, score, reasons in ranked[:k]]
