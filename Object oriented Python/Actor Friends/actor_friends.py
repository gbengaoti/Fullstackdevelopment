import webbrowser

class Friend():
	def __init__(self, actor_name, actor_image, actor_trailer):
		self.name = actor_name		
		self.poster_image_url = actor_image
		self.trailer_youtube_url = actor_trailer

	def show_trailer(self):
		webbrowser.open(self.trailer_youtube_url)