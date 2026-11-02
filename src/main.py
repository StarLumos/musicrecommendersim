"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import WEIGHTS, load_songs, recommend_songs


def main() -> None:
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

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print_recommendations(user_prefs, recommendations)


def print_recommendations(user_prefs: dict, recommendations: list) -> None:
    """Prints each recommendation as a numbered card: title, score, and reasons."""
    width = 72
    max_score = sum(WEIGHTS.values())

    print()
    print("=" * width)
    print(f" TOP {len(recommendations)} RECOMMENDATIONS")
    print(f" Profile: {user_prefs['favorite_genre']} / {user_prefs['favorite_mood']}")
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
