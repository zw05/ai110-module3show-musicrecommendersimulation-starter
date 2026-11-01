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
