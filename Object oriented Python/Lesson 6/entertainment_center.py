import media
import fresh_tomatoes

toy_story = media.Movie("Toy story", 
	"A story of a boy and his toys that come to life", 
	"http://upload.wikimedia.org/wikipedia/en/1/13/Toy_Story.jpg",
    "https://www.youtube.com/watch?v=vwyZH85NQC4")

#print(toy_story.storyline)

avatar = media.Movie("Avatar",
					"A marine on an alien planet",
					"http://upload.wikimedia.org/wikipedia/id/b/b0/Avatar-Teaser-Poster.jpg",
					"https://www.youtube.com/watch?v=5PSNL1qE6VY")

columbiana = media.Movie("Columbiana",
					"A smart young girl kills many people",
					"https://upload.wikimedia.org/wikipedia/en/thumb/b/bc/Colombiana.jpg/220px-Colombiana.jpg",
					"https://www.youtube.com/watch?v=N_0R5mvrZ28")


movies = [toy_story, avatar, columbiana]
columbiana.show_trailer()

#fresh_tomatoes.open_movies_page(movies)

# print(media.Movie.__doc__)
# print(media.Movie.__name__)
# print(media.Movie.__name__)

#print(columbiana.title)