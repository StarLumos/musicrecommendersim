"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


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

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
