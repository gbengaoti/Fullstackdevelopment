import actor_friends
import fresh_tomatoes

rebel = actor_friends.Friend("Rebel Wilson",  
	"https://upload.wikimedia.org/wikipedia/commons/7/75/Rebel_Wilson_2019.png",
    "https://www.youtube.com/watch?v=_j5hwooOHVE")

melissa = actor_friends.Friend("Melissa McCarthy",  
	"https://upload.wikimedia.org/wikipedia/commons/a/ab/Melissa_McCarthy_in_2018_%28cropped%29.jpg",
    "https://www.youtube.com/watch?v=uO12W35DpsQ")

anna = actor_friends.Friend("Anna Kendrick",  
	"https://upload.wikimedia.org/wikipedia/commons/b/b8/AnnaKendrick09TIFF-cropped.jpg",
    "https://www.youtube.com/watch?v=8dItOM6eYXY")

columbiana = actor_friends.Friend("Zoe Saldana",  
	"https://upload.wikimedia.org/wikipedia/commons/9/99/Zoe_Saldana_at_82nd_Academy_Awards_%28cropped%29.jpg",
    "https://www.youtube.com/watch?v=N_0R5mvrZ28")

tatiana = actor_friends.Friend("Tatiana Maslany",  
	"https://upload.wikimedia.org/wikipedia/commons/1/17/Tatiana_Maslany_%28derivative_image%29.jpg",
    "https://www.youtube.com/watch?v=do_BCA-vR9E")

aisha = actor_friends.Friend("Aisha Dee",  
	"https://www.advocate.com/sites/advocate.com/files/2019/04/09/aisha750x.jpg",
    "https://www.youtube.com/watch?v=q9Evo8pJTV0")

friends = [rebel, melissa, anna, columbiana, tatiana, aisha]

fresh_tomatoes.open_movies_page(friends)

