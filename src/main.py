"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


# Keys match UserProfile.
PROFILES = {
    # Distinct, realistic taste profiles
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.90,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.40,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.92,
        "likes_acoustic": False,
    },
    # Adversarial / edge-case profiles
    "Adversarial: Energetic but Sad": {
        "favorite_genre": "pop",
        "favorite_mood": "sad",  # no song in the catalog has this mood
        "target_energy": 0.90,
        "likes_acoustic": False,
    },
    "Adversarial: Unknown Genre (k-pop)": {
        "favorite_genre": "k-pop",  # not in the catalog
        "favorite_mood": "happy",
        "target_energy": 0.80,
        "likes_acoustic": False,
    },
    "Adversarial: Calm Metal Fan": {
        "favorite_genre": "metal",
        "favorite_mood": "angry",
        "target_energy": 0.05,  # conflicts with metal/angry songs
        "likes_acoustic": True,
    },
}


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, user_prefs in PROFILES.items():
        print(f"\n=== {name} ===")
        print(f"Prefs: {user_prefs}\n")

        for song, score, explanation in recommend_songs(user_prefs, songs, k=5):
            print(f"{song['title']} ({song['genre']}/{song['mood']}, energy {song['energy']}) - Score: {score:.2f}")
            print(f"Because: {explanation}")
            print()


if __name__ == "__main__":
    main()
