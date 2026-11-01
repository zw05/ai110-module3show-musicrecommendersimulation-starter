# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

This recommender application is a judge giving every song in the catalog a grade out of 100 for a listener's preferences, then handing back the five songs with the highest grades that match the preferences..

**What the listener tells us.** A listener gives us four things: their favorite genre, their favorite mood, how energetic they want their music to feel (from 0 for very calm to 1 for very intense), and whether they like acoustic, instrument-driven sound.

**What we know about each song.** Every song in the catalog has a genre, a mood, and some numbers describing how it sounds: energy, tempo, how positive it feels (valence), how danceable it is, and how acoustic it is.

**How the grade is built.** The song earns points in several categories, and the categories are not equally important:

- **Mood match (up to 30 points):** the biggest single factor. A song gets the full 30 if its mood is the same as the listener's favorite, and nothing otherwise.
- **Energy (up to 25 points):** the closer the song's energy is to what the listener wants, the more points it earns. A perfect match earns all 25 and a big miss earns close to none.
- **Acoustic feel (up to 15 points):** listeners who like acoustic music are treated as wanting a mostly acoustic sound, and everyone else as wanting a mostly produced, electronic sound. Songs closer to that target score higher.
- **Positivity (up to 15 points):** we assume most people want music that is neither very gloomy nor very cheerful, so songs with a middle-of-the-road feel score best here.
- **Genre match (up to 10 points):** a small bonus when the song's genre is the listener's favorite. Genre counts for less than mood on purpose, so a great song from a neighboring genre can still do well.
- **Danceability and tempo (up to 5 points together):** small tie-breakers. Since the listener doesn't tell us how danceable or fast they want things, we use their energy preference as a stand-in, on the idea that high-energy listeners probably like fast, danceable songs.

Add the points up and each song has a grade between 0 and 100. We then sort all the songs from highest to lowest grade and show the top five. Alongside each song we list the reasons it scored well (for example, "mood matches, energy is close"), so the listener can see why it was picked.

---

## 4. Data  

The catalog in `data/songs.csv` has 25 songs, expanded from the starter set in a recent commit, covering 13 genres (lofi, pop, indie pop, jazz, synthwave, ambient, rock, metal, hip hop, folk, EDM, country, classical) and 11 moods (such as happy, chill, focused, moody, intense and peaceful). Most genres have only one to four songs, and some moods have just one, so each listener's pool of good matches is small. Missing from the data are moods like "sad", many world and regional genres (for example k-pop or Latin), and anything about lyrics, language or era.

---

## 5. Strengths  

The system works best for listeners whose taste lines up with a well-represented genre and mood, such as Chill Lofi, High-Energy Pop and Deep Intense Rock, where the top results scored 0.91 to 0.97 and matched what I would have picked by hand. Weighting mood above genre lets close neighbors show up sensibly, like ambient tracks for a lofi fan or a hip hop track for a rock fan who wants intensity. The "because" reasons also make each result easy to check against intuition.

---

## 6. Limitations and Bias 

The system ignores tempo preferences, lyrics, artist, language and listening history, and it assumes everyone wants a neutral, middling positivity level. Because mood is worth 30% of the grade, a listener who asks for a mood the catalog lacks (like "sad") gets no mood signal at all, and a listener with conflicting wishes (like a calm metal fan) is pulled toward whichever labels carry the most weight. The scoring also favors users whose taste matches the catalog's best-covered genres, while fans of one-song genres have almost nothing to choose from.

---

## 7. Evaluation  

I ran six profiles through the recommender: three realistic ones (High-Energy Pop, Chill Lofi, Deep Intense Rock) and three adversarial ones (Energetic but Sad, Unknown Genre, Calm Metal Fan), and compared each top 5 against what I expected. The realistic profiles matched expectations, but I was surprised that the adversarial ones never failed visibly: a missing mood or genre was silently ignored, and the Calm Metal Fan still got an extremely loud song as its top pick. The full outputs are in the README under "Experiments You Tried".

---

## 8. Future Work  

Next I would let listeners set their own tempo, positivity and danceability targets instead of using stand-ins, and warn them when a requested mood or genre isn't in the catalog. I would also add a diversity step so the top five aren't all near-duplicates, and allow several favorite genres or moods per listener to handle mixed tastes. Finally, a larger and more varied catalog would make every one of these improvements easier to test.

---

## 9. Personal Reflection  

The biggest thing I learned is how simple it can be to recommend something to someone. With just a few preferences and a weighted score, the system produced believable results, which made me realize that recommendations on shopping sites like Amazon probably rest on the same basic idea, only with far more signals behind it.

Something interesting I noticed is that the more data the system has, the better it gets at ranking items. With only 25 songs, a listener often had just one or two real matches and the rest of the top five were filler, while a bigger catalog and richer information about each listener would give the scoring more to work with. It also changed how I see recommendation apps: the suggestions feel personal, but they come from a handful of design choices, like which features to count and how much each one is worth, and those choices decide who gets good results.

