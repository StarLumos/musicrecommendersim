"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from typing import Any, Dict

from recommender import WEIGHTS, load_songs, recommend_songs


def main() -> None:
    """Loads the catalog, recommends songs for the sample profile, and prints them."""
    songs = load_songs("data/songs.csv") 

    # Taste profile: "Late-night study session" listener.
    # "favorite_*" keys are exact-match against the genre/mood columns in songs.csv.
    # "target_*" keys are ideal values on the same scale as the matching CSV column;
    # songs score higher the closer they are to each target.
    user_prefs = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.40,         # low-key, background-friendly (0-1)
        "target_tempo_bpm": 80,        # slow, steady pace
        "target_valence": 0.58,        # neutral-to-slightly-positive, not euphoric or dark
        "target_danceability": 0.60,   # gentle groove, not club-oriented
        "target_acousticness": 0.75,   # prefers organic/soft textures over synthetic
    }

    # Adversarial / edge-case profiles: each tries to trick the scoring logic.
    sad_but_pumped: Dict[str, Any] = {
        "favorite_genre": "pop",
        "favorite_mood": "sad",        # not in the catalog (closest: "melancholic")
        "target_energy": 0.9,
        "target_valence": 0.1,
    }

    melancholic_but_pumped: Dict[str, Any] = {
        "favorite_genre": "pop",
        "favorite_mood": "melancholic",  # real mood, but conflicts with high energy
        "target_energy": 0.9,
        "target_valence": 0.1,
    }

    loud_and_unplugged = {
        "target_energy": 0.9,
        "target_acousticness": 0.9,    # no song has both
    }

    genre_vs_numbers: Dict[str, Any] = {
        "favorite_genre": "metal",
        "favorite_mood": "angry",
        "target_energy": 0.2,          # numbers describe a quiet, acoustic song
        "target_acousticness": 0.95,
        "target_tempo_bpm": 60,
    }

    wrong_scale: Dict[str, Any] = {
        "target_energy": 9,            # should be 0-1
        "target_tempo_bpm": 0.8,       # should be BPM
    }

    messy_categories = {
        "favorite_genre": "Hip-Hop",   # catalog uses "hip hop"
        "favorite_mood": " chill ",    # .lower() but no .strip()
    }

    empty_profile: Dict[str, Any] = {}

    categorical_only = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",      # no numeric targets, so max score is 3.0
    }

    average_listener: Dict[str, Any] = {
        "target_energy": 0.5,
        "target_valence": 0.5,
        "target_danceability": 0.5,
        "target_acousticness": 0.5,
        "target_tempo_bpm": 100,
    }

    tie_breaker: Dict[str, Any] = {
        "favorite_genre": "lofi",
        "target_energy": 0.4,          # Focus Flow matches exactly; ties fall back to title
    }

    wrong_type = {
        "target_energy": "0.9",        # string instead of float
    }

    profiles: Dict[str, Dict[str, Any]] = {
        "Late-night study session": user_prefs,
        "Sad but pumped": sad_but_pumped,
        "Melancholic but pumped": melancholic_but_pumped,
        "Loud and unplugged": loud_and_unplugged,
        "Genre vs. numbers": genre_vs_numbers,
        "Wrong scale": wrong_scale,
        "Messy categories": messy_categories,
        "Empty profile": empty_profile,
        "Categorical only": categorical_only,
        "Average listener": average_listener,
        "Tie-breaker": tie_breaker,
        "Wrong type": wrong_type,
    }

    for name, prefs in profiles.items():
        print(f"\n### {name}")
        try:
            recommendations = recommend_songs(prefs, songs, k=5)
        except Exception as exc:
            print(f"  CRASHED: {type(exc).__name__}: {exc}")
            continue
        print_recommendations(prefs, recommendations)


def print_recommendations(user_prefs: Dict[str, Any], recommendations: list) -> None:
    """Prints each recommendation as a numbered card: title, score, and reasons."""
    width = 72
    max_score = sum(WEIGHTS.values())

    print()
    print("=" * width)
    print(f" TOP {len(recommendations)} RECOMMENDATIONS")
    print(f" Profile: {user_prefs.get('favorite_genre', '-')} / {user_prefs.get('favorite_mood', '-')}")
    print("=" * width)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print()
        print(f" #{rank}  {song['title']}  by {song['artist']}")
        print(f"     Score: {score:.2f} / {max_score:.2f}")
        print("     Why:")
        for reason in explanation.split("; "):
            print(f"       * {reason}")
        print("-" * width)


if __name__ == "__main__":
    main()
