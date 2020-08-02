# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 11:17:11 2020

@author: Nagul
"""


import pandas as pd
from scipy import sparse

ratings = pd.read_csv('ratings.csv')
movies = pd.read_csv('movies.csv')
ratings = pd.merge(movies,ratings).drop(['genres','timestamp'],axis=1)
print(ratings.shape)
ratings.head()

userRatings = ratings.pivot_table(index=['userId'],columns=['title'],values='rating')
print(userRatings.shape)

#Removing movies based on threshold
userRatings = userRatings.dropna(thresh=10, axis=1).fillna(0,axis=1)
print(userRatings.shape)

#Pearson method
corrMatrix = userRatings.corr(method='pearson')
corrMatrix.head(50)

def get_similar(movie_name,rating):
    similar_ratings = corrMatrix[movie_name]*(rating-2.5) #For movies with rating less than 2.5 to appear below the top rated movies or the disliked movies should be below 
    similar_ratings = similar_ratings.sort_values(ascending=False)
    #print(type(similar_ratings))
    return similar_ratings



romantic_lover = [("(500) Days of Summer (2009)",5),("Alice in Wonderland (2010)",3),("Aliens (1986)",1),("2001: A Space Odyssey (1968)",2)]
similar_movies = pd.DataFrame()
for movie,rating in romantic_lover:
    similar_movies = similar_movies.append(get_similar(movie,rating),ignore_index = True)

similar_movies.head(5)

similar_movies.sum().sort_values(ascending=False).head(20)

action_lover = [("Amazing Spider-Man, The (2012)",5),("Mission: Impossible III (2006)",4),("Toy Story 3 (2010)",2),("2 Fast 2 Furious (Fast and the Furious 2, The) (2003)",4)]
similar_movies = pd.DataFrame()
for movie,rating in action_lover:
    similar_movies = similar_movies.append(get_similar(movie,rating),ignore_index = True)

similar_movies.head(10)
similar_movies.sum().sort_values(ascending=False).head(20)