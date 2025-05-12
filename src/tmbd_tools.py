import requests
import pandas as pd # type: ignore
import os

# Set API key
API_KEY = os.getenv('TMDB_API_KEY')  # safer way
BASE_URL = 'https://api.themoviedb.org/3'

# Set up paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, '../data')

def search_movies_by_year(year, country='GB'): 
    # ireland = 'IE' , check https://en.wikipedia.org/wiki/ISO_3166-2 for others
    url = f"{BASE_URL}/discover/movie"
    
    params = {
        'api_key': API_KEY,
        'primary_release_year': year,
        'region': country,
        'with_original_language': 'en'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200: #200 successful HTTP response 
        data = response.json()
    else:
        print(f"Error fetching data for region {country}: {response.status_code}")

    return data

def get_movie_details(movie_id): #https://developer.themoviedb.org/reference/movie-details
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {'api_key': API_KEY}
    response = requests.get(url, params=params)
    return response.json()

def get_movie_credits(movie_id): #https://developer.themoviedb.org/reference/movie-credits
    url = f"{BASE_URL}/movie/{movie_id}/credits"
    params = {'api_key': API_KEY}
    response = requests.get(url, params=params)
    return response.json()

def get_movie_external_ids(movie_id): #https://developer.themoviedb.org/reference/movie-external-ids
    # imbd, fb, insta, twitter, wiki
    url = f"{BASE_URL}/movie/{movie_id}/external_ids"
    params = {'api_key': API_KEY}
    response = requests.get(url, params=params)
    return response.json()

def get_movie_watch_providers(movie_id): # https://api.themoviedb.org/3/movie/{movie_id}/watch/providers
    url = f"{BASE_URL}/movie/{movie_id}/watch/providers"
    params = {'api_key': API_KEY}
    response = requests.get(url, params=params)
    return response.json()

def get_person_details(person_id): #https://developer.themoviedb.org/reference/person-details
    url = f"{BASE_URL}/person/{person_id}"
    params = {'api_key': API_KEY}
    response = requests.get(url, params=params)
    return response.json()

def get_person_movie_credits(person_id): #https://developer.themoviedb.org/reference/person-movie-credits
    url = f"{BASE_URL}/person/{person_id}/movie_credits"
    params = {'api_key': API_KEY}
    response = requests.get(url, params=params)
    return response.json()