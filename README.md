# content_based_movie_recommender
The Gist of the algo is to embed the plots and the titles, and use their combined embeddings and cosine similarity to retrieve the nearest neighbors of each given query movie. Then, the recommendations that do not match the metadata (genre, year, language, country, length) are dropped. The top remainder reocmmendations are returned. See details in the notebook.

The filtering code is thus explained: 
Each recommendation must have a matching genre, language and country, so that we Batman in English doesn't
    get "Batman XXX: a porn Parody", nor a Batman movie in Hindi, nor a Batman movie from India. 
    Each recommendation must also be release with 30y of the query movie,
    in order not to jump between eras, e.g., Batman of 1966 is not like the Batman of the 2000s.
    Finally, the recommendtion feature length must be within 10x of the query movie's length, in order not to mix shorts with feature films, (not sure about this).    
    
FYI this use of the criteria rules is honed for avoiding bad recommendations, at the expense of some recall. 

# instructions
cd into the repo folder
run "pip install requirements.txt"
unzip the train file, into the same repo folder
run the notebook (this may take over an hour if you run on a CPU, on my GPU it took ~10min)
run "python app.py"
use this URL to get similar movies: "http://localhost:105/your favorite movie title"

# Future work
tune the reduced dimension size of the titles (50), against a labelled dataset of movie similarities.

reduce dimensionality of the combined_vecs, for better speed and smaller memory footprint.

notice there is a small amount of irregular release dates that we did not parse (<10%), as well as a bit of similar noise in other columns, and we will clean them in future work.

replace the 'movies_df.csv' with a dict, in order to remove the pandas import in app.py

need to tune the manual metadata criteria, ideally flex them as much as possible so as not to overfit.
