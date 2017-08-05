import media
import sys
from argparse import ArgumentParser
import urllib
import json


def main():

    movies_list = list()

    # Input several movies title
    p = ArgumentParser()
    p.add_argument('read', nargs='+',
                   help='movies title, no blank spaces in one movie title is allowed, use + instead')
    mainargs = p.parse_args()
    num = len((mainargs.read))

    # Three web service queries url
    url = "http://www.omdbapi.com/?t=deadbeaf&y=&plot=short&r=json"
    imdb_query = "https://api.themoviedb.org/3/find/deadbeaf?api_key=05802e91a1d715299c9896d6d6343f77&language=en-US&external_source=imdb_id"
    youtube_query = "https://api.themoviedb.org/3/movie/deadbeaf/videos?api_key=05802e91a1d715299c9896d6d6343f77&language=en-US"

    for i in range(1,num):
        # The first argument is 'read' as shown in line 14 so the first movie title starts at index 1

        youtube_link = ''
        title = ''
        image = ''
        storyline = ''
        # Clear variables
        movie_title = mainargs.read[i]
        # Query the movie data using movie title supported by omdbapi.com
        url_movie = url.replace("deadbeaf", movie_title)
        response = urllib.urlopen(url_movie)
        data = json.loads(response.read())

        if (data["Response"] == "False"):
            # Handle unfound movie case
            print "the movie " + movie_title + " is not found"
            continue
        else:
            # Movie found
            title = data["Title"]
            storyline = data["Plot"]
            image = data["Poster"]

            imdb_id = data["imdbID"]

            # Find the movie id in the data base of themoviedb.org
            imdb_query_url = imdb_query.replace("deadbeaf", imdb_id)
            imdb_query_result = urllib.urlopen(imdb_query_url)
            db_data = json.loads(imdb_query_result.read())

            if db_data["movie_results"] == []:
                # Handle unfound movie case
                continue
            else:
                # Query themoviedb.org database to find the movie link in youtube.com
                db_id = str(db_data["movie_results"][0]["id"])
                youtube_query_url = youtube_query.replace("deadbeaf", db_id)
                youtube_q_response = urllib.urlopen(youtube_query_url)
                youtube_data = json.loads(youtube_q_response.read())

                if youtube_data["results"] != []:
                    youtube_key = youtube_data["results"][0]["key"]
                    youtube_link = "https://www.youtube.com/watch?v=" + youtube_key

            # Make a movie object and append it in list
            movie_entry = media.Movie(title, storyline, image, youtube_link)
            movies_list.append(movie_entry)

    media.fresh_tomatoes.open_movies_page(movies_list)

if __name__ == "__main__":
    main()
