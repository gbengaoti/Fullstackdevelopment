# turtle min project , drawing a flower
import turtle

def draw_triangle():
	
	tri = turtle.Turtle()
	tri.shape("turtle")

	tri.forward(120)

	i = 0
	while(i < 36):
		tri.forward(120)
		tri.right(145)
		tri.left(20)
		i += 1

def main():
	window = turtle.Screen()
	window.bgcolor("blue")
	draw_triangle()
	window.exitonclick()

main()