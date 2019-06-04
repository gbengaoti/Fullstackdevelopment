import webbrowser

class Video():
	def __init__(self, video_title, trailer_youtube, poster_image):
		self.title = video_title
		self.trailer_youtube_url = trailer_youtube
		self.poster_image_url = poster_image

	def show_trailer(self):
		webbrowser.open(self.trailer_youtube_url)

class Movie(Video):

	"""This class contains information about movies"""
	VALID_RATINGS = ["G", "PG", "PG-13", "R"]	
	def __init__(self, movie_title, movie_storyline, poster_image, trailer_youtube):
		Video.title = movie_title	
		Video.trailer_youtube_url = trailer_youtube
		Video.poster_image_url = poster_image
		self.storyline = movie_storyline	

	def show_trailer(self):
		Video.show_trailer(self)


class TvShow(Video):

	"""This class contains information about tv shows"""	
	def __init__(self, movie_title, episode_no, season_no, poster_image, trailer_youtube):
		Video.title = movie_title	
		Video.trailer_youtube_url = trailer_youtube	
		Video.poster_image_url = poster_image
		self.episode = episode_no
		self.season = season_no
		

	