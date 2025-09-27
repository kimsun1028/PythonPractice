# This example is not working in Spyder directly (F5 or Run)
# Please type '!python turtle_runaway.py' on IPython console in your Spyder.
import tkinter as tk
import turtle, random
from math import atan2, degrees

class RunawayGame:
    def __init__(self, canvas, runner, chaser, catch_radius=50, remain_time = 60):
        # 데이터 필드, 멤버 변수
        self.canvas = canvas        # 캔버스 변수
        self.runner = runner        # 도망치는 거북이
        self.chaser = chaser        # 쫓아가는 거북이
        self.catch_radius2 = catch_radius**2 # 잡는 판정을 할 제곱 거리
        self.remain_time = remain_time

        # Initialize 'runner' and 'chaser'
        self.runner.shape('turtle')
        self.runner.color('blue')
        self.runner.penup()
        self.runner.hideturtle()

        self.chaser.shape('turtle')
        self.chaser.color('red')
        self.chaser.penup()
        self.chaser.hideturtle()

        # Instantiate another turtle for drawing
        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()



    def is_catched(self):   # 거북이가 잡혔는지 판별하는 함수
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2


    def explain_and_start(self):
        self.drawer.clear()
        self.drawer.setpos(0,0)
        self.drawer.write("게임을 시작하려면 엔터를 누르세요 : ")
        self.canvas.onkey(lambda: self.start_game(),"Return")
        self.canvas.listen()

    def start_game(self):
        self.drawer.clear()
        self.start()

    # 게임 시작    
    def start(self, init_dist=400, ai_timer_msec=100):
        self.runner.showturtle()
        self.chaser.showturtle()
        self.runner.setpos((-init_dist / 2, 0))
        self.runner.setheading(0)
        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)

        # TODO) You can do something here and follows.
        self.ai_timer_msec = ai_timer_msec
        self.canvas.ontimer(self.step, self.ai_timer_msec) #msec 후에 step 함수 실행



    def step(self):
        self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
        self.chaser.chase_ai(self.runner.pos(), self.runner.heading())

        # TODO) You can do something here and follows.
        is_catched = self.is_catched()
        self.drawer.clear()
        self.drawer.penup()
        self.drawer.setpos(-300, 300)
        self.remain_time -= self.ai_timer_msec / 1000
        self.drawer.write(f'Time left : {int(self.remain_time)}s, Is catched? {is_catched}')

        # Note) The following line should be the last of this function to keep the game playing
        self.canvas.ontimer(self.step, self.ai_timer_msec)

class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn
        self.bomb = Bomb(canvas)

        # Register event handlers
        canvas.onkey(lambda: self.forward(self.step_move), 'w')
        canvas.onkey(lambda: self.backward(self.step_move), 's')
        canvas.onkey(lambda: self.left(self.step_turn), 'a')
        canvas.onkey(lambda: self.right(self.step_turn), 'd')

        canvas.onscreenclick(lambda x, y : self.active(),1)

        canvas.listen()

    def active(self):
        if not self.bomb.isplaced:
            self.bomb.place(self.xcor(),self.ycor())
        else:
            self.bomb.explode()   
            self.bomb.exploderange += 0.2 

    def run_ai(self, opp_pos, opp_heading):
        pass

class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

# 고쳐야 할 코드 : Chaser의 위치에 따른 Runner의 움직임 구현
    def chase_ai(self, opp_pos, opp_heading):
        dx = opp_pos[0] - self.xcor()
        dy = opp_pos[1] - self.ycor()
        angle_to_opp = degrees(atan2(dy, dx))
        if ((angle_to_opp - self.heading() + 180) % 360 - 180) > 0:
            self.left(self.step_turn)
        else:
            self.right(self.step_turn)
        self.forward(self.step_move)

class Bomb(turtle.RawTurtle):
    def __init__(self,canvas,radius = 50):
        super().__init__(canvas)
        self.radius = radius
        self.shape("circle")
        self.color("orange")
        self.shapesize(0.5,0.5)
        self.canvas = canvas
        self.penup()
        self.hideturtle()
        self.isplaced = False
        self.exploderange = 1.5

    def place(self,x,y):
        self.setpos(x,y)
        self.shapesize(0.5,0.5)
        self.showturtle()
        self.isplaced = True

    def explode(self):
        if not self.isplaced:
            return False
        else:
            self.shapesize(self.exploderange,self.exploderange)
            self.canvas.ontimer(self.hideturtle,200)
            self.isplaced = False
        

# 메인 코드
if __name__ == '__main__':
    # Use 'TurtleScreen' instead of 'Screen' to prevent an exception from the singleton 'Screen'
    root = tk.Tk()
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)

    # TODO) Change the follows to your turtle if necessary
    runner = ManualMover(screen)
    chaser = RandomMover(screen)

    game = RunawayGame(screen, runner, chaser)
    game.explain_and_start()
   
    screen.mainloop()
