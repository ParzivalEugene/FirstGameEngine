import turtle

# screen settings
WIDTH, HEIGHT = 1600, 900
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.screensize(10 * WIDTH, 10 * HEIGHT)
screen.bgcolor('black')
screen.delay(0)
# turtle settings
leo = turtle.Turtle()
leo.pensize(3)
leo.speed(0)
leo.setpos(-WIDTH, -HEIGHT)
leo.color('gold')
# l-system settings
gens = 9
axiom = 'F'
chr_1, rule_1 = 'F', 'F-G+F+G-F'
chr_2, rule_2 = 'G', 'GG'
step = 8
angle = 120


def apply_rules(axiom):
    return ''.join([rule_1 if chr == chr_1 else rule_2 if chr == chr_2 else chr for chr in axiom])


def get_result(gens, axiom):
    for gen in range(gens):
        axiom = apply_rules(axiom)
    return axiom


turtle.pencolor('white')
turtle.goto(-WIDTH // 2 + 60, HEIGHT // 2 - 100)
turtle.clear()
turtle.write(f'generation: {gens}', align="left", font=("Arial", 60, "normal"))

axiom = get_result(gens, axiom)
for chr in axiom:
    if chr == chr_1 or chr == chr_2:
        leo.forward(step)
    elif chr == '+':
        leo.right(angle)
    elif chr == '-':
        leo.left(angle)
screen.exitonclick()
