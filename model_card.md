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

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
