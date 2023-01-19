from flask import Flask
from flask import jsonify
import numpy as np
import torch
import pickle
from typing import List


# load artifacts
combined_vecs = torch.load('combined_vecs.pt')
with open('title2indices.pickle', 'rb') as f:
    title2indices = pickle.load(f)
with open('index2metadata.pickle', 'rb') as f:
    index2metadata = pickle.load(f)

    
def get_similar_movies(movie_ndx: int, num_recommendations: int=3) -> List[str]:
    """
    get (an index to) a movie, and return (the display names of) its #{num_recommendations} most similar movies, by content.
    
    First, use dot product similarity (equivalent to cosine) to retrieve the movie's nearest neighbors among the combined_vecs.
    
    Second, filter the results according to metadata: each recommendation must have a matching genre, language and country, so that we Batman in English doesn't
    get "Batman XXX: a porn Parody", nor a Batman movie in Hindi, nor a Batman movie from India. 
    Each recommendation must also be release with 30y of the query movie,
    in order not to jump between eras, e.g., Batman of 1966 is not like the Batman of the 2000s.
    Finally, the recommendtion feature length must be within 10x of the query movie's length, in order not to mix shorts with feature films, (not sure about this).    
    
    Future work: need to fine tune these criteria, ideally flex them as much as possible so as not to overfit. 
    """
    # 1. get most similar movie indices, by dot product (cosine) similarity
    vec = combined_vecs[movie_ndx]
    similarities = np.inner(vec, combined_vecs)
    top_indices = list(reversed(np.argsort(similarities)))[1:] # remove #1 most similar, b/c it's (probably) the original title

    # 2. filter the recommendations by matching the metadata 
    top_similar_display_names = []
    query_movie = index2metadata[movie_ndx]
    genres = query_movie['genres']
    countries = query_movie['countries']
    languages = query_movie['languages']
    year = query_movie['year']
    feature_length = query_movie['feature_length']
    i = 0
    while (len(top_similar_display_names) < num_recommendations) and (i < len(top_indices)):
        recommendation = index2metadata[top_indices[i]]
        recom_genres = recommendation['genres']
        recom_countries = recommendation['countries']
        recom_langugaes = recommendation['languages']
        recom_year = recommendation['year']
        recom_feature_length = recommendation['feature_length']
                
        if (   ((not genres) or (not recom_genres) or set.intersection(genres, recom_genres))
           and ((not languages) or (not recom_langugaes) or set.intersection(languages, recom_langugaes))
           and ((not countries) or (not recom_countries) or set.intersection(countries, recom_countries))
           and ((not year) or (not recom_year) or (abs(year - recom_year) <= 30))
           and ((not feature_length) or (not recom_feature_length) or (0.1 < (feature_length / recom_feature_length) < 10))
           ):
            top_similar_display_names.append(recommendation['display'])
        i += 1
    
    return top_similar_display_names


app = Flask(__name__)


app = Flask(__name__)

@app.route('/<string:movie>/', methods=['GET', 'POST'])
def get_similar_movies_(movie, num_recommendations=3):
    title_indices = title2indices.get(movie)
    if title_indices is None:
        return f'Title is misspelled/unknown: {movie}'
    return jsonify(
        {index2metadata[i]['display']: get_similar_movies(i, num_recommendations)
         for i in title_indices})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)