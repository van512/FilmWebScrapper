import pandas as pd # type: ignore
from tmbd_tools import *
import time


def process_people(crew_list, cast_list, movie_id, top_n_cast=3):
    # Find Director
    directors = [member for member in crew_list if member.get('job') == 'Director']
    producers = [member for member in crew_list if member.get('job') == 'Producer']
    main_cast = cast_list[:top_n_cast]
    people = []

    for group, role in [(directors, 'Director'), (producers, 'Producer'), (main_cast, 'Actor')]:
        for person in group:
            person_id = person['id']
            #person_details = get_person_details(person_id)
            credits = get_person_movie_credits(person_id)

            years = []
            for credit in credits.get('cast', []) + credits.get('crew', []):
                if credit.get('release_date'):
                    try:
                        years.append(int(credit['release_date'][:4]))
                    except:
                        continue
            debut_year = min(years) #if years else None

            sorted_credits = sorted(
                credits.get('cast', []) + credits.get('crew', []),
                key=lambda x: x.get('release_date', '0000-00-00'),
                reverse=True
            )
            last_five = sorted_credits[:5]

            last_five_titles = "; ".join([
                f"{film.get('title')} ({film.get('release_date', '')[:4]}) as {film.get('job', 'Actor')}"
                for film in last_five
            ])

            last_five_ids = "; ".join([
                f"{film.get('id')}"
                for film in last_five
            ])

            person_record = {
                'movie_id': movie_id,
                'person_name': person.get('name'),
                'role': role,
                'debut_year': debut_year,
                'years_active': 2025 - debut_year if debut_year else None,
                'last_five_films': last_five_titles,
                'last_five_ids': last_five_ids
            }

            people.append(person_record)
            time.sleep(0.25)  # Respect API limits

    return people


def scrape_movie_and_people(movie_id):
    movie_details = get_movie_details(movie_id)
    credits = get_movie_credits(movie_id)
    crew = credits.get('crew', [])  #if crew empty returns [] and not error
    cast = credits.get('cast', [])
    movie_watch_providers = get_movie_watch_providers(movie_id)

    movie_record = {
    'movie_id': movie_id,
    'title': movie_details.get('title'),
    'revenue': movie_details.get('revenue'),  # global box office performance (national not available in tmdb)
    'vote_average': movie_details.get('vote_average'),  # tmdb score
    'vote_count': movie_details.get('vote_count'),  # tmdb nbr of user ratings
    'watch_providers': ", ".join([provider.get('provider_name', '') for provider in movie_watch_providers.get('results', {}).get('GB', {}).get('flatrate', [])]),  # Join all provider names by comma
    'genres': ", ".join([g['name'] for g in movie_details.get('genres', [])]),  # genres
    'budget': movie_details.get('budget'),  # budget
    'runtime': movie_details.get('runtime'),  # length in minutes
    'original_language': movie_details.get('original_language'),  # language
    'adult': movie_details.get('adult'),  # equivalent to Movie rating (e.g., PG, R) or certification in release_dates
    'shooting_format': None,  # Shooting format (e.g., Digital, 35mm, 70mm, IMAX), not available in tmdb
    'release_year': movie_details.get('release_date').split('-')[0],  # (Production and) release year
    'number_screens_release': None,  # Number of screens at release not available in tmdb
    'overview': movie_details.get('overview'),  # synopsis
    'movie_script': None,  # not available in tmdb
    'script_writer': ", ".join([member.get('name', '') for member in crew if member.get('job') == 'Screenwriter']),  # All scriptwriters (joined by comma)
    'distributors': ", ".join([company.get('name', '') for company in movie_details.get('production_companies', [])]),  # All distributors (joined by comma)
    'director': ", ".join([member.get('name', '') for member in crew if member.get('job') == 'Director']),  # All directors (joined by comma)
    'producers': ", ".join([member.get('name', '') for member in crew if member.get('job') == 'Producer']),  # All producers (joined by comma)
    'main_cast': ", ".join([actor['name'] for actor in cast[:3]]),  # Top 3 cast members (joined by comma)
}

    people_records = process_people(crew, cast, movie_id)

    return movie_record, people_records


# discover movies from 2015 to 2025 in the UK and scrape their metadata and people, 
# not yet rescraping metadata from movies associated to people
# first 20 results for each year (page)

def main():
    movie_data = []
    people_data = []

    for year in range(2015, 2026):
        print(f"Fetching movies from {year}...")
        data = search_movies_by_year(year) # default country is GB

        for movie in data.get('results', []): #[:2] (default is 20 results)
            movie_id = movie.get('id')
            print(f"Scraping movie ID {movie_id}...")
            movie_record, people_records = scrape_movie_and_people(movie_id)
            movie_data.append(movie_record)
            people_data.extend(people_records)
            time.sleep(0.5)

     # Save to CSV
    movie_df = pd.DataFrame(movie_data)
    people_df = pd.DataFrame(people_data)

    #os.makedirs('../data', exist_ok=True)
    movie_df.to_csv(f'{data_path}/movies.csv', index=False)
    people_df.to_csv(f'{data_path}/people.csv', index=False)

if __name__ == "__main__":
    main()