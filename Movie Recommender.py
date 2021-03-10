# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 12:46:39 2020

@author: Nobody
"""

import json
import requests


def get_movie_recommendations(ls):
    '''
    Takes a list of movie(s) as input and upon getting related movies and their infos
    from get_related_movies() and get_data_from_OMDB() respectively, it gives movie suggestions
    sorted by rating
    '''
    
    movies_info_list = []
    movie_list = get_related_movies(ls)
    for movie in movie_list:
        movie_info = get_data_from_OMDB(movie)
        movies_info_list.append(movie_info)
      
    #sorting movies based on rating
    sorted_rating_and_movie = sorted(movies_info_list, reverse = True)
    sorted_movie_list = [(title,genre,imdb,meta,plot) for (imdb,meta,title,genre,plot) in sorted_rating_and_movie]
    if len(sorted_movie_list) <1:
        print ("No movies found. Please check for typo or determiner :)")
    
    print("___________________________________________")
    for tup in sorted_movie_list:
        (title,genre,imdb,meta,plot) = tup
        print("")
        print("Movie name: ",title)
        print("Genre: ",genre)
        print("Ratings: IMDB- {}   Metascore- {}".format(imdb,meta))
        print("Plot: ",plot)
        print("___________________________________________")
    
       
def get_data_from_tastedive(movie_name):
    '''
    Takes movie name as input and gets the related movie title by sending 
    json object to get_movie_titles()
    returns the movie titles
    '''
    
    #Request pattern https://tastedive.com/read/api
    #Please replace your API key in place of "Your_API_Key_here"
    parameters  = {"q":movie_name, "type": "movies", "limit":10, "k":"Your_API_Key_here"}
    testdive_response = requests.get("https://tastedive.com/api/similar",params=parameters)
    #url = testdive_response.url
    #print(url)
    
    #the text of the response
    returned_object = json.loads(testdive_response.text)

    titles = get_movie_titles(returned_object)
    return titles


def get_movie_titles(dic):
    '''
    Takes a json object as input and gets the related movie title 
    returns the movie title list
    '''
    #extracting the list of similar movies
    movie_list = dic["Similar"]["Results"]
    movie_title = []
    for movies in movie_list:
        movie_title.append(movies["Name"])
    return movie_title                    


def get_related_movies(ls):
    '''
    Takes a movie list and gets related movies from get_data_from_tastedive
    returns the unique similar movie list
    '''
    combined_movies = []
    for i in range(len(ls)):
        similar_movies = get_data_from_tastedive(ls[i])
        
        #list of unique movies
        for movie in similar_movies:
            if movie not in combined_movies:
                combined_movies.append(movie)
    return combined_movies
            

def get_data_from_OMDB(movie_name):
    '''
    Takes a movie name as input and returns the infos of the movie by passing
    a json object to get_info()
    returns movie info
    '''
    #Request format https://www.omdbapi.com/
    #Please replace your API key in place of "Your_API_Key_here"
    parameters = {"t":movie_name ,"r":"json", "apikey":"Your_API_Key_here"}
    OMDB_response = requests.get("https://www.omdbapi.com/",params=parameters)
    returned_object = json.loads(OMDB_response.text)
    #print(OMDB_response.url)
    
    movie_info = get_info(returned_object)
    return movie_info
    

def get_info(dic):
    '''
    Takes a json object and returns relevant info as a tuple
    returns a tuple of movie info
    '''
    movie_title = dic["Title"]
    movie_genre = dic["Genre"]
    movie_plot = dic["Plot"]
    imdb_rating = dic["imdbRating"]
    metacritic_rating = dic["Metascore"]

   
        
    return(imdb_rating,metacritic_rating,movie_title,movie_genre,movie_plot)
 
get_recommended_movies = []   
user_input = input("Please give movie name: ")
get_recommended_movies.append(user_input)
while(1):
    more_input = input("Any more movies to add? If no, please press 1: ")
    if(more_input == "1"):
        break
    get_recommended_movies.append(more_input)
get_movie_recommendations(get_recommended_movies)
#get_movie_recommendations(["One flew over the cuckoo's nest"])

    
