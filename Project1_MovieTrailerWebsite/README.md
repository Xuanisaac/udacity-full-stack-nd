# Project 1 for Udaicty Full Stack Nanodegree
## Movie Trailer Website Project
The interactive movie trailer website can contain a list of your favorite movies. On clicking the poster on the website, the trailer window will be popped open. This project is developed for the Udacity Full Stack Nanodegree program.
### License
The contents are supported by [omdbapi.com](http://www.omdbapi.com/), [themoviedb.org](https://www.themoviedb.org). All content licensed under CC BY-NC 4.0.
### Project Details
##### Usage
By running `python html_generator.py read movie_title1 [movie_title2] [...]`, a movie trailer website will be generated
 and opened with your favorite movies. In running the command line, please treat each movie title as a single word, for exmaple **the matrix** should be **the+matrix**.

The functionality is defined in the file `html_page_generator.py`. The movie class is defined in `media.py`. Extra attributes of movie can be added by changing movie class in `media.py` and modifying `html_generator.py` to contain corresponding contents.
