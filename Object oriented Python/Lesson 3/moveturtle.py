import turtle

def draw_square():
	
	conrad = turtle.Turtle()
	conrad.shape("turtle")
	conrad.color("red")
	conrad.speed(3)

	i = 0
	while(i < 4):
		conrad.forward(200)
		conrad.right(90)
		i += 1

def draw_circle():
	
	niki = turtle.Turtle()
	niki.circle(50)

def draw_triangle():
	
	tri = turtle.Turtle()
	tri.shape("turtle")

	i = 0
	while(i < 3):
		tri.forward(135)
		tri.right(145)
		i += 1

def main():
	window = turtle.Screen()
	window.bgcolor("blue")
	
	draw_square()
	draw_circle()
	draw_triangle()
	window.exitonclick()

main()