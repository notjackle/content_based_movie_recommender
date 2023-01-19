# content_based_movie_recommender

A RESTful micro service to hand you content based movie recommendations. For example:

For "Batman" you'd get these recommendations (for 2 separate movies with that title):

```json
{
  "Batman (United States of America, 1966)": [
    "Batman (United States of America/United Kingdom, 1989)",
    "Batman Returns (United States of America/United Kingdom, 1992)",
    "Adventures of Captain Marvel (United States of America, 1941)"
  ],
  "Batman (United States of America/United Kingdom, 1989)": [
    "Batman (United States of America, 1966)",
    "Batman Begins (United States of America/United Kingdom, 2005)",
    "Batman & Robin (United States of America/United Kingdom, 1997)"
  ]
}
```

For "Titanic":
```json
{
  "Titanic (United States of America, 1953)": [
    "The Chambermaid on the Titanic (, )",
    "Lifeboat (United States of America, 1944)",
    "Submarine (United States of America, 1928)"
  ],
  "Titanic (United States of America/Canada, 1996)": [
    "The Chambermaid on the Titanic (, )",
    "Overboard (United States of America, 1987)",
    "Submarine (United States of America/England/United Kingdom, 2010)"
  ]
}
```

# The Gist of the algo 
To embed the plots and the titles, and use their combined embeddings and cosine similarity to retrieve the nearest neighbors of each given query movie. Then, the recommendations that do not match the metadata (genre, year, language, country, length) are dropped. The top remainder reocmmendations are returned. See details in the notebook.

The filtering code is thus explained: 
Each recommendation must have a matching genre, language and country, so that we Batman in English doesn't
    get "Batman XXX: a porn Parody", nor a Batman movie in Hindi, nor a Batman movie from India. 
    Each recommendation must also be release with 30y of the query movie,
    in order not to jump between eras, e.g., Batman of 1966 is not like the Batman of the 2000s.
    Finally, the recommendtion feature length must be within 10x of the query movie's length, in order not to mix shorts with feature films, (not sure about this).    
    
FYI this use of the criteria rules is honed for avoiding bad recommendations, at the expense of some recall. 

# instructions
1. clone the repo, cd into the repo folder
2. run "pip install requirements.txt"
3. unzip the train file, into the same repo folder
4. run the notebook (this may take over an hour if you run on a CPU, on my GPU it took ~10min)
5. run "python app.py"
6. use this URL to get similar movies: "http://localhost:105/your favorite movie title"

# Future work
tune the reduced dimension size of the titles (50), against a labelled dataset of movie similarities.

reduce dimensionality of the combined_vecs, for better speed and smaller memory footprint.

notice there is a small amount of irregular release dates that we did not parse (<10%), as well as a bit of similar noise in other columns, and we will clean them in future work.

replace the 'movies_df.csv' with a dict, in order to remove the pandas import in app.py

need to tune the manual metadata criteria, ideally flex them as much as possible so as not to overfit.
