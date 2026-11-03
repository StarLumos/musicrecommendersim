# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0** 

MuseMatcher

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

MuseMatcher suggests the top 5 songs from a small catalog of 20 songs for one listener at a time. Each suggestion comes with a score out of 8 and a plain-language list of reasons, such as "genre match" or "energy close to target", so the user can see why a song was picked. It assumes the listener can describe their taste up front as a single profile: one favorite genre, one favorite mood, and an ideal value for energy, tempo, valence, danceability, and acousticness. It also assumes that taste is stable and that songs close to those targets are what the listener wants, so it does not learn from skips, replays, or other users. This is a classroom exploration project, not a product for real listeners. It is meant for learning how recommenders turn data into rankings and for examining their trade-offs, and it is too small and too simple to rely on for actual music discovery.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

Think of MuseMatcher as a judge handing out points. The listener tells it their favorite genre and mood, plus their ideal level of energy, tempo, happiness (valence), danceability, and acousticness. Then the judge goes through every song in the catalog, one at a time, and awards points for how well that song fits. Each song can earn up to 8 points.

Genre and mood are all-or-nothing: a matching genre earns 2 points and a matching mood earns 1 point, while a mismatch earns nothing. The other five features are about closeness instead of a match. A song earns the full points for a feature if it sits right on the listener's target, and fewer points the further away it is. Energy is worth up to 1.5 points, acousticness and valence up to 1 point each, and danceability and tempo up to 0.75 each. Tempo is measured against the full range of tempos in the catalog, so a gap of a few beats per minute does not count more heavily than a gap in the other features. Once every song has a total, the songs are ranked from highest to lowest and the top 5 are shown, with ties broken alphabetically by title. Along with each score, the model lists the points each feature contributed, so the listener can see exactly why a song ranked where it did.

The starter code only had empty placeholders for loading songs, scoring them, and ranking them, so the scoring approach is new. I set the weights myself, giving genre the most weight because it is the strongest single signal and mood a smaller one. I also replaced the starter profile's single "likes acoustic" yes/no idea with numeric targets for every feature, so the listener's taste can be described more precisely. Every recommendation now comes with its reasons, which the starter did not provide.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The catalog has 20 songs. The starter file had 10, and I added 10 more to cover genres and moods the original set left out. Each song has a genre, a mood, and five numeric features: energy, tempo, valence, danceability, and acousticness. There are 17 distinct genres, but only lofi (3 songs) and pop (2 songs) appear more than once, so 14 genres are represented by a single song. Moods are similar: 15 distinct moods, with chill the most common (3 songs) and happy, intense, and melancholic at 2 each. Energy is uneven, with 7 songs below 0.45, 8 at 0.75 or above, and almost nothing between 0.56 and 0.74. Much of taste is missing: there is no Latin, K-pop, or Afrobeats, no non-English music, and nothing that is both loud and acoustic. With one song per genre, a listener whose favorite genre has a single song only ever gets one genre match.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The system works best for listeners with a coherent, well-covered taste, such as the "Late-night study session" profile (lofi, chill, low energy, high acousticness). Its top 3 were Midnight Coding (7.88 / 8), Library Rain (7.71), and Focus Flow (6.96), all lofi and all matching the quiet, slow, acoustic feel I described. Spacewalk Thoughts and Dust Road Home followed at #4 and #5 with no genre match. They are different genres that share the same low-key vibe, so the numeric features are doing real work there, not just the labels. The "Average listener" profile, with no genre or mood, also gave sensible results: Tidal Daydream, which sits closest to the middle on every feature, ranked first. Because the model lists the points each feature contributed, I could check every ranking against my intuition and see why it came out that way.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

**Weakness discovered: the genre label overrides what the user's numbers say they want.** An exact genre match is worth 2.0 points, more than the entire energy feature (1.5), so a single label can outweigh a large mismatch on every other axis. In the "Sad but pumped" profile (pop, energy 0.9, valence 0.1), Gym Hero scores about 3.79 because of its genre match, while Iron Cathedral, a much closer fit on energy and valence, scores only about 2.27. The problem is made worse by the catalog: 14 of its 17 genres have a single song, and matching is all-or-nothing, so "pop" earns nothing for "indie pop" or "dream pop". Listeners whose taste is better described by vibe than by genre label are therefore pushed toward whichever song happens to share their label, and the numeric features mostly act as tie-breakers.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

I tested 12 profiles: one realistic listener ("Late-night study session") and 11 adversarial or edge-case ones ("Sad but pumped", "Melancholic but pumped", "Loud and unplugged", "Genre vs. numbers", "Wrong scale", "Messy categories", "Empty profile", "Categorical only", "Average listener", "Tie-breaker", "Wrong type"). I checked whether the top 5 matched what each profile asked for and whether the listed reasons explained the ranking. I compared them in six pairs, using each profile once, to see what each preference actually changes:

- **Study session vs. Average listener:** Study targets quiet, slow, acoustic lofi and returns Midnight Coding, Library Rain, and Focus Flow. The average listener's mid-range targets favor mid-energy songs (Tidal Daydream, Velvet Hours). Dust Road Home and Midnight Coding appear in both lists, which makes sense since they sit near the middle too.
- **Sad but pumped vs. Melancholic but pumped:** Only the mood differs. "Sad" isn't in the catalog, so it earns nothing, while "melancholic" is. The top 2 (Gym Hero, Sunrise City) are identical, but melancholic pulls in Crossroads Monday and Nocturne in Rain, which are quiet songs, ahead of Storm Runner. A mood match (+1.0) is worth more than the energy gap (about 0.66), so this follows from the weights, though it is wrong for someone who wants "pumped".
- **Loud and unplugged vs. Genre vs. numbers:** Both have conflicting preferences, in different ways. Loud and unplugged has no labels and asks for a combination no song has, so it tops out at 1.74 with a list split between loud and acoustic songs. In Genre vs. numbers the metal label contradicts the quiet, acoustic numbers. Iron Cathedral wins at 3.43 on labels alone, and ranks 2 to 5 follow the numbers. With a label, one song gets lifted. Without one, the list is just a compromise.
- **Categorical only vs. Tie-breaker:** Categorical only ties Library Rain and Midnight Coding at 3.00, and the #5 slot is a 0.00 song picked alphabetically. Adding one energy target (0.4) in Tie-breaker puts Focus Flow first and fills ranks 4 and 5 with the songs closest in energy (Coffee Shop Stories, Crossroads Monday) instead of arbitrary zeros.
- **Messy categories vs. Empty profile:** The output is identical, all 0.00 and alphabetical. "Hip-Hop" and " chill " only count if they're formatted exactly like the catalog, so the typos silently turned a real user into an empty one.
- **Wrong scale vs. Wrong type:** Both have a broken energy target. Wrong scale (energy 9) silently gives energy 0 points and lets tempo pick the winner, so the results look valid but aren't. Wrong type ("0.9") crashes with a TypeError. The crash is arguably the better failure because it can't be mistaken for a real recommendation.

What surprised me most was how little the energy gap mattered. A 0.7 gap costs only about 1 point, and a genre match more than repays it. The system works well for ordinary, genre-consistent taste and breaks down when a listener's genre label and numeric targets disagree.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

**Additional features.** I would add more song data, like artist, language, and release year. I would also let users list several favorite genres and moods instead of one. A user could also name genres or moods they want to avoid.

**Better scoring.** I would lower the genre weight so it cannot beat the numbers so easily. I would also give partial credit for related genres, so "pop" earns something for "indie pop". Mood could work the same way, so "sad" would be close to "melancholic".

**Better input handling.** The system should clean up typos and extra spaces, like " chill " or "Hip-Hop". It should also reject values on the wrong scale, like an energy of 9. Bad input should give a clear error, not a quiet wrong answer.

**More diversity.** Right now the top 5 can all sound alike. I would add a rule that limits how many songs share one genre or artist.

**Better explanations.** I would show why a song missed out, not just why it ranked. I would also say when a profile is too vague to give a good answer.

**More complex taste.** Real listeners change with the time of day and their mood. I would let users pick a context, like "study" or "workout". I would also learn from skips and replays.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

My biggest learning moment was testing the odd profiles. The "Wrong scale" profile gave results that looked fine but were not. The "Wrong type" profile crashed, and that was the better failure. A system that fails quietly is hard to trust. I also learned that a recommender is mostly a set of choices about weights. I gave genre 2.0 points, and that one choice shaped almost every result.

AI helped me move fast. It helped me draft the scoring code, think up edge-case profiles, and write up my notes. But it was not always right. I had to check the song counts, the genre counts, and the scores against the real data and the real output. I also had to check that the weights in the write-up matched the weights in the code. The AI sounded sure even when a number was off. So I treated its answers as drafts, not facts.

I was surprised how real the output felt. The model only adds up points. Yet the study profile gave a list that matched the mood I had in mind. The "Average listener" profile even picked a song that sat in the middle on every feature. Listing the reasons for each score made it feel smarter than it is. It also showed me where the logic broke. One thing that did not feel real was how little the energy gap mattered. A big gap cost about 1 point, and a genre match paid it back.

For improvements, first, I would lower the genre weight and give partial credit for related genres and moods. Then I would clean up and check user input. After that, I would add a rule so the top 5 are not all alike. I would also like to add more songs and more genres. Last, I would let users pick a context like "study" or "workout". Then I would try learning from skips and replays.

Music apps now look different to me. Their suggestions are not neutral. Someone chose what to count and how much. A small catalog or a heavy genre weight can keep a listener in one narrow lane. I want to learn more about what real apps measure.
