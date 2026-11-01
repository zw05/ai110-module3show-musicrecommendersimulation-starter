# Data Flow Map

```
 INPUT                        PROCESS                              OUTPUT
 -----                        -------                              ------

 User Prefs (dict)            The Loop (recommend_songs)           The Ranking
 ┌──────────────────┐         ┌──────────────────────────────┐     ┌──────────────────────────┐
 │ favorite_genre   │         │ for song in songs:           │     │ sort by score, desc      │
 │ favorite_mood    │──┐      │     score, reasons =         │     │ take top k               │
 │ target_energy    │  │      │         score_song(prefs,    │     │                          │
 │ likes_acoustic   │  ├────▶ │                    song)     │───▶ │ [(song, score, why), ...]│
 └──────────────────┘  │      │     keep (song, score, why)  │     │                          │
                       │      └──────────────────────────────┘     │ printed by main.py       │
 songs.csv             │                                           └──────────────────────────┘
 ┌──────────────────┐  │
 │ load_songs()     │──┘
 │ -> list of dicts │
 │ id, title, genre,│
 │ mood, energy,    │
 │ tempo, valence,  │
 │ danceability,    │
 │ acousticness     │
 └──────────────────┘
```

## 1. Input
- **User prefs**: `favorite_genre`, `favorite_mood`, `target_energy`, `likes_acoustic` (set in `src/main.py`).
- **Song catalog**: `data/songs.csv` loaded by `load_songs()` into a list of dicts (numeric columns converted to `int`/`float`).

## 2. Process: the loop
`recommend_songs()` judges **every** song in the catalog with `score_song(user_prefs, song)`, which returns `(score, reasons)`.

Planned scoring logic (one score per song, built from simple parts):

| Signal | Rule | Notes |
|---|---|---|
| Genre | +points if `song.genre == favorite_genre` | exact match |
| Mood | +points if `song.mood == favorite_mood` | exact match |
| Energy | `1 - abs(song.energy - target_energy)` | closer = higher, range 0-1 |
| Acousticness | if `likes_acoustic`: reward high `acousticness`, else reward low | scaled 0-1 |

Each rule that fires also appends a human-readable string to `reasons` (e.g. `"genre match (lofi)"`), which becomes the explanation.

## 3. Output: the ranking
1. Collect `(song, score, explanation)` for all songs.
2. Sort by `score`, highest first.
3. Return the first `k` entries (default `k=5`).
4. `main.py` prints each title, score, and "Because: ..." explanation.

## Functions to implement (`src/recommender.py`)
- `load_songs(csv_path)`: CSV -> list of dicts
- `score_song(user_prefs, song)`: one song -> `(score, reasons)`
- `recommend_songs(user_prefs, songs, k)`: loop + sort + top k
