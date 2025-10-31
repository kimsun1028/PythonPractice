# This example is not working in Spyder directly (F5 or Run)
# Please type '!python turtle_runaway.py' on IPython console in your Spyder.
import tkinter as tk
import turtle, random
import time
from math import atan2, degrees

# 실제 게임 실행하는 함수
class RunawayGame:
    def __init__(self, canvas, runner, chasers,lifepoint = 3, catch_radius=40, remain_time = 60):
        # 데이터 필드, 멤버 변수
        self.canvas = canvas       
        self.runner = runner                    # 도망치는 거북이(플레이어)      
        self.catch_radius2 = catch_radius**2    # 잡는 판정을 할 제곱 거리
        self.remain_time = remain_time          # 게임 플레이 시간
        self.lifepoint = lifepoint              # 플레이어 목숨
        self.invincible_time = 0                # 무적 시간 변수 초기화
        self.start_time = time.time()           # 남은 시간 계산을 위한 시작 시간 

        # Initialize 'runner' and 'chaser'
        self.runner.shape('runnerturtle.gif')   # 플레이어 거북이 사진 설정
        self.runner.penup()                     # 펜 들기
        self.runner.hideturtle()                # 플레이어 가려놓기

        self.chasers = chasers                  # 쫓아가는 거북이(상대편) 리스트
        for chaser in chasers:                  
            chaser.shape('chaserturtle.gif')    # 상대편 거북이 사진 설정
            chaser.penup()                      # 펜 들기
            chaser.hideturtle()                 # 상대편 가려놓기

        # Instantiate another turtle for drawing
        self.drawer = turtle.RawTurtle(canvas)      # 글씨 출력을 위한  drawer 거북이 선언
        self.drawer.hideturtle()                    # 펜 들기
        self.drawer.penup()                         # 가려 놓기


    def remainlife(self):                           # 플레이어 거북이가 잡혔는지 판별하는 함수
        if self.invincible_time >0:                 # 이미 라이프가 감소해 무적 시간이 양수면
            self.invincible_time -= 1               # 프레임마다 하나씩 감소
            return self.lifepoint , True            # 무적 시간이므로 True도 반환
        p = self.runner.pos()                       # p = 플레이어 위치
        for chaser in self.chasers:                 # 상대편 리스트에서
            q = chaser.pos()                        
            dx, dy = p[0] - q[0], p[1] - q[1]
            if dx**2 + dy**2 < self.catch_radius2:  # 플레이어와의 제곱거리 < 설정된 거리이면
                self.lifepoint -= 1                 # 라이프 감소
                self.invincible_time = 2            # 무적 시간 설정
                return self.lifepoint , True        # 무적 시간이므로 True도 반환
            
        return self.lifepoint , False               # 무적 시간이 아니므로 False 반환
             

            
    def explain_and_start(self):                    # 설명 후 시작하는 함수
        self.drawer.clear()                         
        self.drawer.setpos(-350,0)                  # drawer 위치 설정 및 설명 작성
        self.drawer.write("전진 : W , 회전 : A,D , 후진 : S , 폭탄 설치/폭발 : 마우스 왼클릭 \n게임을 시작하려면 엔터를 누르세요 : ", font=("Arial",20,"bold"))
        self.canvas.onkey(lambda: self.start_game(),"Return")   # 엔터 입력받으면 게임 시작
        self.canvas.listen()

    def start_game(self):                           # 게임 시작하는 함수
        self.drawer.clear()
        self.start()

 
    def start(self, init_dist=400, ai_timer_msec=100):      # 게임 시작    
        self.runner.showturtle()                            # 플레이어 위치와 방향 설정
        self.runner.setpos((0, 0))
        self.runner.setheading(0)
        for i, chaser in enumerate(self.chasers):           # 상대방 위치와 방향 설정
            chaser.showturtle()
            if i % 2 == 1:
                chaser.setpos((init_dist * (-1)**(i//2)),0)
                chaser.setheading(90 * (i+1))
            else:
                chaser.setpos(0,(init_dist* (-1)**(i//2 + 1)))
                chaser.setheading(90 * (i+1))

        self.ai_timer_msec = ai_timer_msec
        self.canvas.ontimer(self.step, self.ai_timer_msec)  # msec 후에 step 함수 실행



    def step(self):                                         # 프레임 단위 발동되는 함수
        for chaser in self.chasers:
            chaser.chase_ai(self.runner.pos(), self.runner.heading())   # Chaser가 프레임 단위마다 ai에 따라 이동
        # TODO) You can do something here and follows.
        elapsed = time.time() - self.start_time                         # 지난 시간 계산
        self.remain_time = 60 - elapsed                                 # 남은 시간 계산
        remainlife , isInvincible = self.remainlife()                   # 남은 라이프, 무적 유무 
        if isInvincible:                                                # 무적 시간일 경우 외형 변경
            self.runner.shape("invincibleturtle.gif")
        else:
            self.runner.shape("runnerturtle.gif")                       # 무적 시간이 끝날 경우 외형 복구

        self.drawer.clear()                                             # 남은 시간, 라이프,  남은 적의 수, 점수 출력
        self.drawer.penup()
        self.drawer.setpos(-700, 400)
        self.drawer.write(f'남은 시간 : {int(self.remain_time)}s, 라이프 : {remainlife}, 남은 적 : {len(self.chasers)}, 점수 : {25*(4 - len(self.chasers))}', font=("Arial",15,"bold"))

        # Note) The following line should be the last of this function to keep the game playing
        if (remainlife > 0) and (self.remain_time > 0) and (len(self.chasers) > 0):     # 라이프 > 0 and 남은 시간 > 0 and 남은 적 수 > 0 일 경우
            self.canvas.ontimer(self.step, self.ai_timer_msec)                          # msec 후 step 발동
        elif len(self.chasers) == 0:                                                    # 남은 적이 0일 경우
            self.drawer.setpos(-150,0)                                                  # 승리 선언
            self.drawer.write("You Win!!", font=("Arial",50,"bold"))                    
        else:                                                                           # 패배 선언
            self.drawer.setpos(-200,0)
            self.drawer.write("Game Over", font=("Arial",50,"bold")) 
        

class ManualMover(turtle.RawTurtle):                                # 플레이어 움직임 함수
    def __init__(self, canvas, chasers, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn
        self.chasers = chasers
        self.bomb = Bomb(canvas,self.chasers)                       # 폭탄

        # Register event handlers
        canvas.onkey(lambda: self.forward(self.step_move), 'w')     # wasd로 움직임 구현
        canvas.onkey(lambda: self.backward(self.step_move), 's')
        canvas.onkey(lambda: self.left(self.step_turn), 'a')
        canvas.onkey(lambda: self.right(self.step_turn), 'd')

        canvas.onscreenclick(lambda x, y : self.active(),1)         # 클릭 시 폭탄 설치&폭발

        canvas.listen()

    def active(self):
        if not self.bomb.isplaced:                                  # 폭탄 설치가 안 되있을 시 설치
            self.bomb.place(self.xcor(),self.ycor())
        else:                                                       # 되어 있을 시 폭발
            self.bomb.explode()                                     

    def run_ai(self, opp_pos, opp_heading):                         
        pass

class ChaserMover(turtle.RawTurtle):                                # 상대방 움직임 구현
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

# 고쳐야 할 코드 : Runner의 위치에 따른 Chaser의 움직임 구현
    def chase_ai(self, opp_pos, opp_heading):                       # 한 프레임당 turn 한번, 전진 한번
        dx = opp_pos[0] - self.xcor()
        dy = opp_pos[1] - self.ycor()
        angle_to_opp = degrees(atan2(dy, dx))                       # angle_to_opp = 상대방 위치 -> 플레이어 위치 벡터의 각도 (-180 ~ 180)
        # angle_to_opp - self.heading() = 현재 방향에서 상대방까지의 각도 차이, 이를 -180 ~ 180도 범위로 변환
        if (((angle_to_opp - self.heading()) + 180) % 360 - 180) > 0:   # 양수면 왼쪽으로 
            self.left(self.step_turn)
        else:                                                           # 음수면 오른쭉으로 회전
            self.right(self.step_turn)
        self.forward(self.step_move)                                    # 앞으로 전진

class Bomb(turtle.RawTurtle):                       # 플레이어의 무기 : 폭탄
    def __init__(self,canvas,chasers,exploderange = 30):  
        super().__init__(canvas)
        self.chasers = chasers                      # 상대방 리스트                      
        self.shape("bomb.gif")                      # 폭탄 외형 설정
        self.canvas = canvas
        self.penup()                                
        self.hideturtle()
        self.isplaced = False                       # 초기 상태 = 설치 X
        self.exploderange = exploderange            # 폭발 범위 설정

    def place(self,x,y):                            # 폭탄 설치 함수
        self.setpos(x,y)                            # 플레이어 위치에 설치
        self.shape("bomb.gif")                      # 폭탄 외형 초기화
        self.showturtle()                           
        self.isplaced = True                        # 폭탄 설치 

    def explode(self):                              # 폭탄 폭발 함수
        if not self.isplaced:                       # 설치가 안되어있으면 False return
            return False
        else:
            self.shape("explode.gif")                   # 폭발 외형 설정
            self.canvas.ontimer(self.hideturtle,200)    # 외형 유지 시간 설정
            self.isplaced = False                       # 폭탄 설치 해제
    
            for i in reversed(range(len(self.chasers))):        # 폭탄에 맞은 상대방 설정
                chaser = self.chasers[i]      
                dx = self.xcor() - chaser.xcor()
                dy = self.ycor() - chaser.ycor()
                if (dx**2 + dy**2) < (self.exploderange)**2:    # 폭탄에 맞았으면
                    chaser.shape("dieturtle.gif")               # 외형 설정
                    self.chasers.pop(i)                         # 상대방 리스트 뒷IDX부터 에서 pop
        

# 메인 코드
if __name__ == '__main__':
    # Use 'TurtleScreen' instead of 'Screen' to prevent an exception from the singleton 'Screen'
    root = tk.Tk()
    canvas = tk.Canvas(root, width=1500, height=900)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)
    screen.addshape("runnerturtle.gif")                 # 외형(사진) 추가
    screen.addshape("bomb.gif")
    screen.addshape("explode.gif")
    screen.addshape("chaserturtle.gif")
    screen.addshape("dieturtle.gif")
    screen.addshape("invincibleturtle.gif")
    screen.bgpic("gamefield.gif")                       # 배경 사진 설정
    # TODO) Change the follows to your turtle if necessary
    chasers = [ChaserMover(screen) for _ in range(4)]   # 상대방 리스트 생성
    runner = ManualMover(screen,chasers)                # 플레이어 생성
    game = RunawayGame(screen, runner, chasers)         # 게임 생성
    game.explain_and_start()                            # 설명 후 시작!
    screen.mainloop()
