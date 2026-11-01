# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

In this current version of the music recommender, the user inputs their own
preferences of music based on the current features. The application then takes 
the music that it has in its database and gives a score for each song that 
best fits the users preferences. It then returns at list of songs that 
best match the preferences. 


Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

Each of the songs have 10 fields:
id, title, artist, genre, mood, energy, tempo_bpm, valence, danceability and acousticness.

But not all of them are used to be scored upon.
The way I plan on scoring the fields are as follows:
- Used heavily: mood, energy, acousticness, valence
- Used lightly: genre, danceability, tempo_bpm
- Display only: id, title, artist

Each UserProfile stores 4 things:
- favorite_mood (e.g. "chill")
- target_energy (a number from 0 to 1)
- favorite_genre (e.g. "lofi")
- likes_acoustic (True or False)

The profile is a small snapshot of what the user wants right now. For scoring,
likes_acoustic becomes an acousticness target of about 0.8 if True and about 0.2
if False. Valence has no field in the profile, so it uses a neutral target of 0.5.

The Recommender scores every song by comparing it to the profile and adding up
weighted results:

| Feature | How it is compared | Weight |
|---|---|---|
| mood | 1 if it matches, else 0 | 0.30 |
| energy | 1 - abs(song - target) | 0.25 |
| acousticness | closeness to the target | 0.15 |
| valence | closeness to the target | 0.15 |
| genre | 1 if it matches, else 0 | 0.10 |
| danceability / tempo_bpm | closeness (tempo is normalized first) | 0.05 |

The final score is the weighted sum, between 0 and 1. The scorer also keeps short
reasons (like "mood matches" or "energy is close") so each recommendation can be
explained.

To choose which songs to recommend:

1. Score every song in the CSV against the user's profile.
2. Sort the songs by score, highest first.
3. Return the top k songs (default 5) with their scores and reasons.

```
songs.csv -> load songs -> score each vs. UserProfile -> sort high to low -> top k + explanation
```

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
Loaded songs: 25

Top recommendations:

Midnight Coding - Score: 0.96
Because: mood matches, energy is close, acousticness fits, valence is neutral, genre matches

Library Rain - Score: 0.95
Because: mood matches, energy is close, acousticness fits, valence is neutral, genre matches

Spacewalk Thoughts - Score: 0.82
Because: mood matches, energy is close, acousticness fits, valence is neutral

Deep Blue Drift - Score: 0.81
Because: mood matches, acousticness fits, valence is neutral

Focus Flow - Score: 0.67
Because: energy is close, acousticness fits, valence is neutral, genre matches
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

I defined six user profiles in `src/main.py` (`PROFILES`): three realistic ones and three adversarial edge cases designed to try to trick the scoring logic. Run them with `python src/main.py`. Top 5 results for each are below (catalog: 25 songs).

### Standard profiles

**High-Energy Pop** (`pop`, `happy`, energy 0.90, not acoustic)

```
Sunrise City (pop/happy, energy 0.82) - Score: 0.91
Because: mood matches, energy is close, acousticness fits, genre matches

Dancefloor Fever (pop/happy, energy 0.9) - Score: 0.91
Because: mood matches, energy is close, acousticness fits, genre matches

Rooftop Lights (indie pop/happy, energy 0.76) - Score: 0.78
Because: mood matches, energy is close, acousticness fits

Golden Hour Drive (indie pop/happy, energy 0.7) - Score: 0.76
Because: mood matches, acousticness fits

Gym Hero (pop/intense, energy 0.93) - Score: 0.62
Because: energy is close, acousticness fits, genre matches
```

**Chill Lofi** (`lofi`, `chill`, energy 0.40, likes acoustic)

```
Midnight Coding (lofi/chill, energy 0.42) - Score: 0.96
Because: mood matches, energy is close, acousticness fits, valence is neutral, genre matches

Library Rain (lofi/chill, energy 0.35) - Score: 0.95
Because: mood matches, energy is close, acousticness fits, valence is neutral, genre matches

Spacewalk Thoughts (ambient/chill, energy 0.28) - Score: 0.82
Because: mood matches, energy is close, acousticness fits, valence is neutral

Deep Blue Drift (ambient/chill, energy 0.22) - Score: 0.81
Because: mood matches, acousticness fits, valence is neutral

Focus Flow (lofi/focused, energy 0.4) - Score: 0.67
Because: energy is close, acousticness fits, valence is neutral, genre matches
```

**Deep Intense Rock** (`rock`, `intense`, energy 0.92, not acoustic)

```
Storm Runner (rock/intense, energy 0.91) - Score: 0.97
Because: mood matches, energy is close, acousticness fits, valence is neutral, genre matches

Concrete Pulse (hip hop/intense, energy 0.85) - Score: 0.84
Because: mood matches, energy is close, acousticness fits, valence is neutral

Gym Hero (pop/intense, energy 0.93) - Score: 0.83
Because: mood matches, energy is close, acousticness fits

Static Bloom (rock/moody, energy 0.8) - Score: 0.63
Because: energy is close, acousticness fits, valence is neutral, genre matches

Night Drive Loop (synthwave/moody, energy 0.75) - Score: 0.54
Because: acousticness fits, valence is neutral
```

### Adversarial / edge-case profiles

**Energetic but Sad** (`pop`, `sad`, energy 0.90, not acoustic): conflicting preferences, and no song in the catalog has the mood `sad`.

```
Gym Hero (pop/intense, energy 0.93) - Score: 0.62
Because: energy is close, acousticness fits, genre matches

Sunrise City (pop/happy, energy 0.82) - Score: 0.61
Because: energy is close, acousticness fits, genre matches

Dancefloor Fever (pop/happy, energy 0.9) - Score: 0.61
Because: energy is close, acousticness fits, genre matches

Storm Runner (rock/intense, energy 0.91) - Score: 0.57
Because: energy is close, acousticness fits, valence is neutral

Concrete Pulse (hip hop/intense, energy 0.85) - Score: 0.55
Because: energy is close, acousticness fits, valence is neutral
```

**Unknown Genre** (`k-pop`, `happy`, energy 0.80, not acoustic): the genre is not in the catalog.

```
Sunrise City (pop/happy, energy 0.82) - Score: 0.83
Because: mood matches, energy is close, acousticness fits

Rooftop Lights (indie pop/happy, energy 0.76) - Score: 0.81
Because: mood matches, energy is close, acousticness fits

Golden Hour Drive (indie pop/happy, energy 0.7) - Score: 0.79
Because: mood matches, energy is close, acousticness fits

Dancefloor Fever (pop/happy, energy 0.9) - Score: 0.78
Because: mood matches, energy is close, acousticness fits

Night Drive Loop (synthwave/moody, energy 0.75) - Score: 0.57
Because: energy is close, acousticness fits, valence is neutral
```

**Calm Metal Fan** (`metal`, `angry`, energy 0.05, likes acoustic): the genre and mood point at the loudest song while the energy target points at the quietest.

```
Iron Horizon (metal/angry, energy 0.97) - Score: 0.60
Because: mood matches, genre matches

Deep Blue Drift (ambient/chill, energy 0.22) - Score: 0.51
Because: acousticness fits, valence is neutral

Sunday Morning Piano (classical/peaceful, energy 0.18) - Score: 0.51
Because: energy is close

Spacewalk Thoughts (ambient/chill, energy 0.28) - Score: 0.49
Because: acousticness fits, valence is neutral

Library Rain (lofi/chill, energy 0.35) - Score: 0.49
Because: acousticness fits, valence is neutral
```

### Observations

- **Standard profiles behave sensibly.** Each one's top results match its genre, mood and energy, and the top scores are 0.91 to 0.97.
- **Missing mood is silently ignored.** For "Energetic but Sad", the 0.30 mood weight can never fire, so the system falls back to energy and genre. It recommends upbeat pop with no signal that it couldn't honor the request.
- **Unknown genre degrades gracefully.** Without a genre match, mood and energy carry the ranking and the results are reasonable. Nothing tells the user their genre wasn't found, though.
- **Conflicting preferences expose the weights.** For "Calm Metal Fan", the 0.40 weight on mood plus genre puts Iron Horizon (energy 0.97, target 0.05) first even though its energy is nearly the opposite of what was requested. Its score of 0.60 is low, but the system still presents it as the top pick.
- **Closest-energy matching rewards the loudest songs for high-energy targets.** `Gym Hero` (pop/intense) shows up for pop, rock and sad profiles alike because its energy is high and its genre or mood overlaps.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



