# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world platforms like Spotify and YouTube predict what you'll love next with a multi-stage pipeline. They first narrow millions of tracks to a few hundred candidates, then rank those with a learned model. Their strongest signal is collaborative filtering, which learns from the behavior of millions of users (plays, skips, saves, playlist adds), and it is blended with content-based signals such as audio features and metadata, which help when a song or user is new. Our version is purely content-based and works on a small catalog, so it has no other users' behavior to learn from. It compares each song's attributes to a single user's taste profile and prioritizes **energy** most heavily, scored by how close a song is to the user's target rather than by how high or low it is. It then adds smaller contributions from **mood**, **genre**, **valence**, and **danceability**. Each song gets a score from this weighted sum, and the top-scoring songs are returned along with the reasons they matched.

### Features

**`Song`** (one row of `data/songs.csv`)

| Field | Type | Used in scoring? | Notes |
|---|---|---|---|
| `id` | int | No | Identifier |
| `title` | str | No | Shown in output |
| `artist` | str | No | Shown in output |
| `genre` | str | **Yes** (2.0 pts) | Compared to `favorite_genre` |
| `mood` | str | **Yes** (1.0 pt) | Compared to `favorite_mood` |
| `energy` | float, 0 to 1 | **Yes** (1.5 pts) | Closeness to `target_energy` |
| `acousticness` | float, 0 to 1 | **Yes** (1.0 pt) | Closeness to `target_acousticness` |
| `valence` | float, 0 to 1 | **Yes** (1.0 pt) | Closeness to `target_valence` |
| `danceability` | float, 0 to 1 | **Yes** (0.75 pts) | Closeness to `target_danceability` |
| `tempo_bpm` | float | **Yes** (0.75 pts) | Closeness to `target_tempo_bpm`, scaled by 92 |

**`UserProfile`** (the listener's taste profile)

| Field | Type | Matched against | Example ("late-night study") |
|---|---|---|---|
| `favorite_genre` | str | `Song.genre` | `"lofi"` |
| `favorite_mood` | str | `Song.mood` | `"chill"` |
| `target_energy` | float, 0 to 1 | `Song.energy` | `0.40` |
| `target_tempo_bpm` | float | `Song.tempo_bpm` | `80` |
| `target_valence` | float, 0 to 1 | `Song.valence` | `0.58` |
| `target_danceability` | float, 0 to 1 | `Song.danceability` | `0.60` |
| `target_acousticness` | float, 0 to 1 | `Song.acousticness` | `0.75` |

### Data Flow

```
INPUT                      PROCESS                               OUTPUT
user_prefs  ─┐
             ├─▶ for song in songs:                  ─▶ sort by score (desc)
songs.csv   ─┘      score_song(prefs, song)               take top k
(load_songs)        → (score, reasons)                     → [(song, score, explanation), ...]
```

1. **Input:** `load_songs` reads the CSV into a list of dicts, and `main.py` supplies the user's taste profile.
2. **Process:** `recommend_songs` loops over *every* song and calls `score_song`, which returns a score and the reasons behind it. No songs are filtered out beforehand.
3. **Output:** Songs are sorted by score (highest first), with ties broken deterministically, and the top `k` are returned with their explanations.

### Algorithm Recipe

Each song earns points out of a maximum of **8.0**:

| Feature | Type | Max points | How points are earned |
|---|---|---|---|
| genre | categorical | **2.0** | Exact match = 2.0, otherwise 0 |
| mood | categorical | **1.0** | Exact match = 1.0, otherwise 0 |
| energy | numeric | **1.5** | `1.5 × (1 − abs(song − target))` |
| acousticness | numeric | **1.0** | `1.0 × (1 − abs(song − target))` |
| valence | numeric | **1.0** | `1.0 × (1 − abs(song − target))` |
| danceability | numeric | **0.75** | `0.75 × (1 − abs(song − target))` |
| tempo_bpm | numeric | **0.75** | `0.75 × max(0, 1 − abs(song − target) / 92)` |
| **Total** | | **8.0** | |

- Tempo is divided by 92, the spread of the BPM column (60 to 152), so a BPM gap is scaled the same as the 0 to 1 features.
- Genre is worth twice as much as mood. Energy is the strongest numeric feature because it varies most across the catalog and best separates calm songs from intense ones.
- Danceability and tempo get lower weights because they overlap with energy.
- Each component appends a reason (e.g. `"genre match (+2.0)"`) so every recommendation can explain itself.
- Weights live in a single dict so they are easy to tweak and compare.

### Expected Biases and Limitations

- **Genre over-prioritization.** Genre carries twice the weight of mood, so a song with the right genre but the wrong feel can outrank a great mood and energy match from another genre. For example, a mellow jazz track could rank below an upbeat lofi track.
- **Exact-match categories.** Mood and genre are all-or-nothing, so near-misses like "relaxed" vs. "chill" or "indie pop" vs. "pop" earn zero. This penalizes songs that are close in spirit.
- **Rare categories.** If the user's favorite genre has only a couple of songs in the catalog, the genre bonus makes the top of the list nearly fixed, and the system keeps recommending the same few songs.
- **Single-point taste.** A user is modeled as one target value per feature, so someone who likes both calm acoustic songs and high-energy workout songs will be matched to neither well.
- **Content-only and small catalog.** With no listening history or other users' behavior, the system can't learn from skips or discover surprising matches, and it will tend to recommend songs similar to what the user already says they like (a filter bubble).
- **Hand-picked weights.** The point values reflect our judgment, not learned data, and they treat every user the same way even though real users weigh genre and mood differently.

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
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

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



