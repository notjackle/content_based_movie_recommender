# content_based_movie_recommender
The Gist of the algo is to embed the plots and the titles, and use their combined embeddings to retrieve the nearest neighbors of each given query movie. Then, the recommendations that do not match the metadata (genre, year, language, country, length) are dropped. The top remainder reocmmendations are returned. See details in the notebook.
