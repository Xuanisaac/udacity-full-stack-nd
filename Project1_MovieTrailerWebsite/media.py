import fresh_tomatoes


class Movie():
    """ This id DocStrings for Movie class

    Attributes:
        title (str): the title of movie_title
        storyline (str):
        trailer_youtube_url (str): the youtube link of the trailer_youtube_url
        poster_image_url (str) : the poster image link of the movie
    """

    def __init__(self, movie_title, movie_storyline, poster_image, trailer_youtube):
        self.title = movie_title
        self.storyline = movie_storyline
        self.trailer_youtube_url = trailer_youtube
        self.poster_image_url = poster_image

    def show_trailer(self):
        webbrowswer.open(self.trailer_link)
