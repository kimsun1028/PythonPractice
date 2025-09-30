# This example is not working in Spyder directly (F5 or Run)
# Please type '!python turtle_runaway.py' on IPython console in your Spyder.
import tkinter as tk
import turtle, random
import time
from math import atan2, degrees

# 실제 게임 실행하는 함수
class RunawayGame:
    def __init__(self, canvas, runner, chasers,lifepoint = 3, catch_radius=30, remain_time = 60):
        # 데이터 필드, 멤버 변수
        self.canvas = canvas        # 캔버스 변수
        self.runner = runner        # 도망치는 거북이      
        self.catch_radius2 = catch_radius**2 # 잡는 판정을 할 제곱 거리
        self.remain_time = remain_time
        self.lifepoint = lifepoint
        self.invincible_time = 0
        self.start_time = time.time()

        # Initialize 'runner' and 'chaser'
        self.runner.shape('turtle')
        self.runner.color('blue')
        self.runner.penup()
        self.runner.hideturtle()

        self.chasers = chasers # 쫓아가는 거북이 리스트
        for chaser in chasers:    
            chaser.shape('turtle')
            chaser.color('red')
            chaser.penup()
            chaser.hideturtle()

        # Instantiate another turtle for drawing
        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()


    def remainlife(self):   # 플레이어 거북이가 잡혔는지 판별하는 함수
        if self.invincible_time >0:
            self.invincible_time -= 1
            return self.lifepoint
        p = self.runner.pos()
        for chaser in self.chasers:
            q = chaser.pos()
            dx, dy = p[0] - q[0], p[1] - q[1]
            if dx**2 + dy**2 < self.catch_radius2:
                self.lifepoint -= 1
                self.invincible_time = 10
                break
        return self.lifepoint
             

            
    def explain_and_start(self):
        self.drawer.clear()
        self.drawer.setpos(-350,0)
        self.drawer.write("전진 : W , 회전 : A,D , 후진 : S , 폭탄 설치/폭발 : 마우스 왼클릭 \n게임을 시작하려면 엔터를 누르세요 : ", font=("Arial",20,"bold"))
        self.canvas.onkey(lambda: self.start_game(),"Return")
        self.canvas.listen()

    def start_game(self):
        self.drawer.clear()
        self.start()

    # 게임 시작    
    def start(self, init_dist=400, ai_timer_msec=100):
        self.runner.showturtle()
        self.runner.setpos((0, 0))
        self.runner.setheading(0)
        for i, chaser in enumerate(self.chasers):
            chaser.showturtle()
            if i % 2 == 1:
                chaser.setpos((init_dist * (-1)**(i//2)),0)
                chaser.setheading(90 * (i))
            else:
                chaser.setpos(0,(init_dist* (-1)**(i//2 + 1)))
                chaser.setheading(90 * (i))
        

        # TODO) You can do something here and follows.
        self.ai_timer_msec = ai_timer_msec
        self.canvas.ontimer(self.step, self.ai_timer_msec) #msec 후에 step 함수 실행



    def step(self):
        for chaser in self.chasers:
            chaser.chase_ai(self.runner.pos(), self.runner.heading())

        # TODO) You can do something here and follows.
        elapsed = time.time() - self.start_time
        self.remain_time = 60 - elapsed
        remainlife = self.remainlife() 
        self.drawer.clear()
        self.drawer.penup()
        self.drawer.setpos(-700, 400)
        self.drawer.write(f'남은 시간 : {int(self.remain_time)}s, 라이프 = {remainlife}', font=("Arial",15,"bold"))

        # Note) The following line should be the last of this function to keep the game playing
        if (remainlife > 0) and (self.remain_time > 0):
            self.canvas.ontimer(self.step, self.ai_timer_msec)
        else:
            self.drawer.clear()
            self.drawer.penup()
            self.drawer.setpos(-200,0)
            self.drawer.write('GAME OVER!')
            return 0

class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn
        self.bomb = Bomb(canvas,self.chasers)

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

    def run_ai(self, opp_pos, opp_heading):
        pass

class ChaserMover(turtle.RawTurtle):
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
    def __init__(self,canvas,chasers,radius = 50):
        super().__init__(canvas)
        self.chasers = chasers
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
            return[(self.xcor(),self.ycor()),self.exploderange]
        

# 메인 코드
if __name__ == '__main__':
    # Use 'TurtleScreen' instead of 'Screen' to prevent an exception from the singleton 'Screen'
    root = tk.Tk()
    canvas = tk.Canvas(root, width=1500, height=900)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)

    # TODO) Change the follows to your turtle if necessary
    runner = ManualMover(screen)
    chasers = [ChaserMover(screen) for _ in range(4)]
    game = RunawayGame(screen, runner, chasers)
    game.explain_and_start()
   
    screen.mainloop()
