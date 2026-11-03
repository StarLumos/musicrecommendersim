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

```text
Loading songs from data/songs.csv...
Loaded songs: 20

========================================================================
 TOP 5 RECOMMENDATIONS
 Profile: lofi / chill
========================================================================

 #1  Midnight Coding  by LoRoom
     Score: 7.88 / 8.00
     Why:
       * genre match: lofi (+2.00)
       * mood match: chill (+1.00)
       * energy 0.42 vs target 0.4 (+1.47)
       * acousticness 0.71 vs target 0.75 (+0.96)
       * valence 0.56 vs target 0.58 (+0.98)
       * danceability 0.62 vs target 0.6 (+0.73)
       * tempo_bpm 78 vs target 80 (+0.73)
------------------------------------------------------------------------

 #2  Library Rain  by Paper Lanterns
     Score: 7.71 / 8.00
     Why:
       * genre match: lofi (+2.00)
       * mood match: chill (+1.00)
       * energy 0.35 vs target 0.4 (+1.42)
       * acousticness 0.86 vs target 0.75 (+0.89)
       * valence 0.6 vs target 0.58 (+0.98)
       * danceability 0.58 vs target 0.6 (+0.73)
       * tempo_bpm 72 vs target 80 (+0.68)
------------------------------------------------------------------------

 #3  Focus Flow  by LoRoom
     Score: 6.96 / 8.00
     Why:
       * genre match: lofi (+2.00)
       * energy 0.4 vs target 0.4 (+1.50)
       * acousticness 0.78 vs target 0.75 (+0.97)
       * valence 0.59 vs target 0.58 (+0.99)
       * danceability 0.6 vs target 0.6 (+0.75)
       * tempo_bpm 80 vs target 80 (+0.75)
------------------------------------------------------------------------

 #4  Spacewalk Thoughts  by Orbit Bloom
     Score: 5.27 / 8.00
     Why:
       * mood match: chill (+1.00)
       * energy 0.28 vs target 0.4 (+1.32)
       * acousticness 0.92 vs target 0.75 (+0.83)
       * valence 0.65 vs target 0.58 (+0.93)
       * danceability 0.41 vs target 0.6 (+0.61)
       * tempo_bpm 60 vs target 80 (+0.59)
------------------------------------------------------------------------

 #5  Dust Road Home  by Cedar Hollow
     Score: 4.68 / 8.00
     Why:
       * energy 0.48 vs target 0.4 (+1.38)
       * acousticness 0.74 vs target 0.75 (+0.99)
       * valence 0.58 vs target 0.58 (+1.00)
       * danceability 0.61 vs target 0.6 (+0.74)
       * tempo_bpm 102 vs target 80 (+0.57)
------------------------------------------------------------------------
```

## Sample Recommendation Output for Adversarial or Edge Cafe User Profiles
```
Loading songs from data/songs.csv...
Loaded songs: 20

### Late-night study session

========================================================================
 TOP 5 RECOMMENDATIONS
 Profile: lofi / chill
========================================================================

 #1  Midnight Coding  by LoRoom
     Score: 7.88 / 8.00
     Why:
       * genre match: lofi (+2.00)
       * mood match: chill (+1.00)
       * energy 0.42 vs target 0.4 (+1.47)
       * acousticness 0.71 vs target 0.75 (+0.96)
       * valence 0.56 vs target 0.58 (+0.98)
       * danceability 0.62 vs target 0.6 (+0.73)
       * tempo_bpm 78 vs target 80 (+0.73)
------------------------------------------------------------------------

 #2  Library Rain  by Paper Lanterns
     Score: 7.71 / 8.00
     Why:
       * genre match: lofi (+2.00)
       * mood match: chill (+1.00)
       * energy 0.35 vs target 0.4 (+1.42)
       * acousticness 0.86 vs target 0.75 (+0.89)
       * valence 0.6 vs target 0.58 (+0.98)
       * danceability 0.58 vs target 0.6 (+0.73)
       * tempo_bpm 72 vs target 80 (+0.68)
------------------------------------------------------------------------

 #3  Focus Flow  by LoRoom
     Score: 6.96 / 8.00
     Why:
       * genre match: lofi (+2.00)
       * energy 0.4 vs target 0.4 (+1.50)
       * acousticness 0.78 vs target 0.75 (+0.97)
       * valence 0.59 vs target 0.58 (+0.99)
       * danceability 0.6 vs target 0.6 (+0.75)
       * tempo_bpm 80 vs target 80 (+0.75)
------------------------------------------------------------------------

 #4  Spacewalk Thoughts  by Orbit Bloom
     Score: 5.27 / 8.00
     Why:
       * mood match: chill (+1.00)
       * energy 0.28 vs target 0.4 (+1.32)
       * acousticness 0.92 vs target 0.75 (+0.83)
       * valence 0.65 vs target 0.58 (+0.93)
       * danceability 0.41 vs target 0.6 (+0.61)
       * tempo_bpm 60 vs target 80 (+0.59)
------------------------------------------------------------------------

 #5  Dust Road Home  by Cedar Hollow
     Score: 4.68 / 8.00
     Why:
       * energy 0.48 vs target 0.4 (+1.38)
       * acousticness 0.74 vs target 0.75 (+0.99)
       * valence 0.58 vs target 0.58 (+1.00)
       * danceability 0.61 vs target 0.6 (+0.74)
       * tempo_bpm 102 vs target 80 (+0.57)
------------------------------------------------------------------------

### Sad but pumped

========================================================================
 TOP 5 RECOMMENDATIONS
 Profile: pop / sad
========================================================================

 #1  Gym Hero  by Max Pulse
     Score: 3.79 / 8.00
     Why:
       * genre match: pop (+2.00)
       * energy 0.93 vs target 0.9 (+1.46)
       * valence 0.77 vs target 0.1 (+0.33)
------------------------------------------------------------------------

 #2  Sunrise City  by Neon Echo
     Score: 3.64 / 8.00
     Why:
       * genre match: pop (+2.00)
       * energy 0.82 vs target 0.9 (+1.38)
       * valence 0.84 vs target 0.1 (+0.26)
------------------------------------------------------------------------

 #3  Iron Cathedral  by Black Meridian
     Score: 2.27 / 8.00
     Why:
       * energy 0.97 vs target 0.9 (+1.40)
       * valence 0.22 vs target 0.1 (+0.88)
------------------------------------------------------------------------

 #4  Storm Runner  by Voltline
     Score: 2.10 / 8.00
     Why:
       * energy 0.91 vs target 0.9 (+1.48)
       * valence 0.48 vs target 0.1 (+0.62)
------------------------------------------------------------------------

 #5  Night Drive Loop  by Neon Echo
     Score: 1.88 / 8.00
     Why:
       * energy 0.75 vs target 0.9 (+1.27)
       * valence 0.49 vs target 0.1 (+0.61)
------------------------------------------------------------------------

### Melancholic but pumped

========================================================================
 TOP 5 RECOMMENDATIONS
 Profile: pop / melancholic
========================================================================

 #1  Gym Hero  by Max Pulse
     Score: 3.79 / 8.00
     Why:
       * genre match: pop (+2.00)
       * energy 0.93 vs target 0.9 (+1.46)
       * valence 0.77 vs target 0.1 (+0.33)
------------------------------------------------------------------------

 #2  Sunrise City  by Neon Echo
     Score: 3.64 / 8.00
     Why:
       * genre match: pop (+2.00)
       * energy 0.82 vs target 0.9 (+1.38)
       * valence 0.84 vs target 0.1 (+0.26)
------------------------------------------------------------------------

 #3  Crossroads Monday  by Delta Slim
     Score: 2.61 / 8.00
     Why:
       * mood match: melancholic (+1.00)
       * energy 0.46 vs target 0.9 (+0.84)
       * valence 0.33 vs target 0.1 (+0.77)
------------------------------------------------------------------------

 #4  Nocturne in Rain  by Elena Marchetti
     Score: 2.33 / 8.00
     Why:
       * mood match: melancholic (+1.00)
       * energy 0.22 vs target 0.9 (+0.48)
       * valence 0.25 vs target 0.1 (+0.85)
------------------------------------------------------------------------

 #5  Iron Cathedral  by Black Meridian
     Score: 2.27 / 8.00
     Why:
       * energy 0.97 vs target 0.9 (+1.40)
       * valence 0.22 vs target 0.1 (+0.88)
------------------------------------------------------------------------

### Loud and unplugged

========================================================================
 TOP 5 RECOMMENDATIONS
 Profile: - / -
========================================================================

 #1  Rooftop Lights  by Indigo Parade
     Score: 1.74 / 8.00
     Why:
       * energy 0.76 vs target 0.9 (+1.29)
       * acousticness 0.35 vs target 0.9 (+0.45)
------------------------------------------------------------------------

 #2  Dust Road Home  by Cedar Hollow
     Score: 1.71 / 8.00
     Why:
       * energy 0.48 vs target 0.9 (+0.87)
       * acousticness 0.74 vs target 0.9 (+0.84)
------------------------------------------------------------------------

 #3  Coffee Shop Stories  by Slow Stereo
     Score: 1.69 / 8.00
     Why:
       * energy 0.37 vs target 0.9 (+0.70)
       * acousticness 0.89 vs target 0.9 (+0.99)
------------------------------------------------------------------------

 #4  Storm Runner  by Voltline
     Score: 1.68 / 8.00
     Why:
       * energy 0.91 vs target 0.9 (+1.48)
       * acousticness 0.1 vs target 0.9 (+0.20)
------------------------------------------------------------------------

 #5  Sunrise City  by Neon Echo
     Score: 1.66 / 8.00
     Why:
       * energy 0.82 vs target 0.9 (+1.38)
       * acousticness 0.18 vs target 0.9 (+0.28)
------------------------------------------------------------------------

### Genre vs. numbers

========================================================================
 TOP 5 RECOMMENDATIONS
 Profile: metal / angry
========================================================================

 #1  Iron Cathedral  by Black Meridian
     Score: 3.43 / 8.00
     Why:
       * genre match: metal (+2.00)
       * mood match: angry (+1.00)
       * energy 0.97 vs target 0.2 (+0.34)
       * acousticness 0.04 vs target 0.95 (+0.09)
       * tempo_bpm 168 vs target 60 (+0.00)
------------------------------------------------------------------------

 #2  Nocturne in Rain  by Elena Marchetti
     Score: 3.15 / 8.00
     Why:
       * energy 0.22 vs target 0.2 (+1.47)
       * acousticness 0.97 vs target 0.95 (+0.98)
       * tempo_bpm 66 vs target 60 (+0.70)
------------------------------------------------------------------------

 #3  Spacewalk Thoughts  by Orbit Bloom
     Score: 3.10 / 8.00
     Why:
       * energy 0.28 vs target 0.2 (+1.38)
       * acousticness 0.92 vs target 0.95 (+0.97)
       * tempo_bpm 60 vs target 60 (+0.75)
------------------------------------------------------------------------

 #4  Porch Light Lullaby  by Willow & Pine
     Score: 2.97 / 8.00
     Why:
       * energy 0.3 vs target 0.2 (+1.35)
       * acousticness 0.93 vs target 0.95 (+0.98)
       * tempo_bpm 74 vs target 60 (+0.64)
------------------------------------------------------------------------

 #5  Library Rain  by Paper Lanterns
     Score: 2.84 / 8.00
     Why:
       * energy 0.35 vs target 0.2 (+1.28)
       * acousticness 0.86 vs target 0.95 (+0.91)
       * tempo_bpm 72 vs target 60 (+0.65)
------------------------------------------------------------------------

### Wrong scale

========================================================================
 TOP 5 RECOMMENDATIONS
 Profile: - / -
========================================================================

 #1  Spacewalk Thoughts  by Orbit Bloom
     Score: 0.27 / 8.00
     Why:
       * energy 0.28 vs target 9 (+0.00)
       * tempo_bpm 60 vs target 0.8 (+0.27)
------------------------------------------------------------------------

 #2  Nocturne in Rain  by Elena Marchetti
     Score: 0.22 / 8.00
     Why:
       * energy 0.22 vs target 9 (+0.00)
       * tempo_bpm 66 vs target 0.8 (+0.22)
------------------------------------------------------------------------

 #3  Crossroads Monday  by Delta Slim
     Score: 0.19 / 8.00
     Why:
       * energy 0.46 vs target 9 (+0.00)
       * tempo_bpm 70 vs target 0.8 (+0.19)
------------------------------------------------------------------------

 #4  Library Rain  by Paper Lanterns
     Score: 0.17 / 8.00
     Why:
       * energy 0.35 vs target 9 (+0.00)
       * tempo_bpm 72 vs target 0.8 (+0.17)
------------------------------------------------------------------------

 #5  Porch Light Lullaby  by Willow & Pine
     Score: 0.15 / 8.00
     Why:
       * energy 0.3 vs target 9 (+0.00)
       * tempo_bpm 74 vs target 0.8 (+0.15)
------------------------------------------------------------------------

### Messy categories

========================================================================
 TOP 5 RECOMMENDATIONS
 Profile: Hip-Hop /  chill 
========================================================================

 #1  Coffee Shop Stories  by Slow Stereo
     Score: 0.00 / 8.00
     Why:
       * 
------------------------------------------------------------------------

 #2  Concrete Crown  by Rhyme Atlas
     Score: 0.00 / 8.00
     Why:
       * 
------------------------------------------------------------------------

 #3  Crossroads Monday  by Delta Slim
     Score: 0.00 / 8.00
     Why:
       * 
------------------------------------------------------------------------

 #4  Dust Road Home  by Cedar Hollow
     Score: 0.00 / 8.00
     Why:
       * 
------------------------------------------------------------------------

 #5  Focus Flow  by LoRoom
     Score: 0.00 / 8.00
     Why:
       * 
------------------------------------------------------------------------

### Empty profile

========================================================================
 TOP 5 RECOMMENDATIONS
 Profile: - / -
========================================================================

 #1  Coffee Shop Stories  by Slow Stereo
     Score: 0.00 / 8.00
     Why:
       * 
------------------------------------------------------------------------

 #2  Concrete Crown  by Rhyme Atlas
     Score: 0.00 / 8.00
     Why:
       * 
------------------------------------------------------------------------

 #3  Crossroads Monday  by Delta Slim
     Score: 0.00 / 8.00
     Why:
       * 
------------------------------------------------------------------------

 #4  Dust Road Home  by Cedar Hollow
     Score: 0.00 / 8.00
     Why:
       * 
------------------------------------------------------------------------

 #5  Focus Flow  by LoRoom
     Score: 0.00 / 8.00
     Why:
       * 
------------------------------------------------------------------------

### Categorical only

========================================================================
 TOP 5 RECOMMENDATIONS
 Profile: lofi / chill
========================================================================

 #1  Library Rain  by Paper Lanterns
     Score: 3.00 / 8.00
     Why:
       * genre match: lofi (+2.00)
       * mood match: chill (+1.00)
------------------------------------------------------------------------

 #2  Midnight Coding  by LoRoom
     Score: 3.00 / 8.00
     Why:
       * genre match: lofi (+2.00)
       * mood match: chill (+1.00)
------------------------------------------------------------------------

 #3  Focus Flow  by LoRoom
     Score: 2.00 / 8.00
     Why:
       * genre match: lofi (+2.00)
------------------------------------------------------------------------

 #4  Spacewalk Thoughts  by Orbit Bloom
     Score: 1.00 / 8.00
     Why:
       * mood match: chill (+1.00)
------------------------------------------------------------------------

 #5  Coffee Shop Stories  by Slow Stereo
     Score: 0.00 / 8.00
     Why:
       * 
------------------------------------------------------------------------

### Average listener

========================================================================
 TOP 5 RECOMMENDATIONS
 Profile: - / -
========================================================================

 #1  Tidal Daydream  by Glass Meadow
     Score: 4.79 / 8.00
     Why:
       * energy 0.5 vs target 0.5 (+1.50)
       * acousticness 0.4 vs target 0.5 (+0.90)
       * valence 0.57 vs target 0.5 (+0.93)
       * danceability 0.55 vs target 0.5 (+0.71)
       * tempo_bpm 100 vs target 100 (+0.75)
------------------------------------------------------------------------

 #2  Dust Road Home  by Cedar Hollow
     Score: 4.55 / 8.00
     Why:
       * energy 0.48 vs target 0.5 (+1.47)
       * acousticness 0.74 vs target 0.5 (+0.76)
       * valence 0.58 vs target 0.5 (+0.92)
       * danceability 0.61 vs target 0.5 (+0.67)
       * tempo_bpm 102 vs target 100 (+0.73)
------------------------------------------------------------------------

 #3  Midnight Coding  by LoRoom
     Score: 4.34 / 8.00
     Why:
       * energy 0.42 vs target 0.5 (+1.38)
       * acousticness 0.71 vs target 0.5 (+0.79)
       * valence 0.56 vs target 0.5 (+0.94)
       * danceability 0.62 vs target 0.5 (+0.66)
       * tempo_bpm 78 vs target 100 (+0.57)
------------------------------------------------------------------------

 #4  Crossroads Monday  by Delta Slim
     Score: 4.34 / 8.00
     Why:
       * energy 0.46 vs target 0.5 (+1.44)
       * acousticness 0.67 vs target 0.5 (+0.83)
       * valence 0.33 vs target 0.5 (+0.83)
       * danceability 0.52 vs target 0.5 (+0.73)
       * tempo_bpm 70 vs target 100 (+0.51)
------------------------------------------------------------------------

 #5  Velvet Hours  by Amara Vale
     Score: 4.33 / 8.00
     Why:
       * energy 0.52 vs target 0.5 (+1.47)
       * acousticness 0.3 vs target 0.5 (+0.80)
       * valence 0.68 vs target 0.5 (+0.82)
       * danceability 0.76 vs target 0.5 (+0.55)
       * tempo_bpm 92 vs target 100 (+0.68)
------------------------------------------------------------------------

### Tie-breaker

========================================================================
 TOP 5 RECOMMENDATIONS
 Profile: lofi / -
========================================================================

 #1  Focus Flow  by LoRoom
     Score: 3.50 / 8.00
     Why:
       * genre match: lofi (+2.00)
       * energy 0.4 vs target 0.4 (+1.50)
------------------------------------------------------------------------

 #2  Midnight Coding  by LoRoom
     Score: 3.47 / 8.00
     Why:
       * genre match: lofi (+2.00)
       * energy 0.42 vs target 0.4 (+1.47)
------------------------------------------------------------------------

 #3  Library Rain  by Paper Lanterns
     Score: 3.42 / 8.00
     Why:
       * genre match: lofi (+2.00)
       * energy 0.35 vs target 0.4 (+1.42)
------------------------------------------------------------------------

 #4  Coffee Shop Stories  by Slow Stereo
     Score: 1.46 / 8.00
     Why:
       * energy 0.37 vs target 0.4 (+1.46)
------------------------------------------------------------------------

 #5  Crossroads Monday  by Delta Slim
     Score: 1.41 / 8.00
     Why:
       * energy 0.46 vs target 0.4 (+1.41)
------------------------------------------------------------------------

### Wrong type
  CRASHED: TypeError: unsupported operand type(s) for -: 'float' and 'str'
```

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



