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
        """Store the song catalog that recommendations are drawn from."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs for the given user profile."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a short text explaining why a song was recommended to the user."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into a list of dicts with numeric fields converted."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            for key in ("energy", "tempo_bpm", "valence", "danceability", "acousticness"):
                row[key] = float(row[key])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences, returning the score and match reasons."""
    target_energy = user_prefs["target_energy"]
    target_acoustic = 0.8 if user_prefs["likes_acoustic"] else 0.2
    target_valence = 0.5

    # Tempo is normalized to 0-1 over 60-180 BPM; the energy target stands in
    # for the danceability and tempo targets since the profile has neither.
    tempo_norm = min(max((song["tempo_bpm"] - 60) / 120, 0.0), 1.0)

    score = 0.0
    reasons = []

    if song["mood"] == user_prefs["favorite_mood"]:
        score += 0.30
        reasons.append("mood matches")

    energy_close = 1 - abs(song["energy"] - target_energy)
    score += 0.25 * energy_close
    if energy_close >= 0.85:
        reasons.append("energy is close")

    acoustic_close = 1 - abs(song["acousticness"] - target_acoustic)
    score += 0.15 * acoustic_close
    if acoustic_close >= 0.85:
        reasons.append("acousticness fits")

    valence_close = 1 - abs(song["valence"] - target_valence)
    score += 0.15 * valence_close
    if valence_close >= 0.85:
        reasons.append("valence is neutral")

    if song["genre"] == user_prefs["favorite_genre"]:
        score += 0.10
        reasons.append("genre matches")

    dance_close = 1 - abs(song["danceability"] - target_energy)
    tempo_close = 1 - abs(tempo_norm - target_energy)
    score += 0.025 * dance_close + 0.025 * tempo_close

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Return the top k songs as (song, score, explanation) tuples, best first."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons) if reasons else "general fit"
        scored.append((song, score, explanation))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
