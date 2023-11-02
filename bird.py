# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, load_font, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT
from ball import Ball, BigBall
import game_world
import game_framework
import random
# Bird Run Speed

# 549 / 2 CM , 537 / 2 CM
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 3 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour 시속 10키로미터
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
# fill here

# Bird Action Speed
# fill here
TIME_PER_ACTION = 0.8
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5


class Run:
    @staticmethod
    def enter(bird):
        bird.dir, bird.action, bird.face_dir = 1, 1, 1

    @staticmethod
    def exit(bird):
        pass

    @staticmethod
    def do(bird):
        bird.frame = (bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        bird.x += bird.dir * RUN_SPEED_PPS * game_framework.frame_time
        if (bird.x > 1600 or bird.x < 0):
            bird.dir *= -1
        if(bird.frame == 0):
            bird.action += 1
            bird.action %= 3
        if(bird.action == 0 and bird.frame == 4):
            bird.frame +=1

    @staticmethod
    def draw(bird):
        if bird.dir == 1:
            bird.image.clip_draw(int(bird.frame) * 183, bird.action * 169 , 183, 169, bird.x, bird.y,
                                 183 / 2, 169 / 2)
        else:
            bird.image.clip_composite_draw(int(bird.frame) * 183, bird.action * 169 , 183, 169, 0,
                                           'h', bird.x, bird.y, 183 / 2, 169 / 2)


class StateMachine:
    def __init__(self, bird):
        self.bird = bird
        self.cur_state = Run

    def start(self):
        self.cur_state.enter(self.bird)

    def update(self):
        self.cur_state.do(self.bird)

    def handle_event(self):
        # for check_event, next_state in self.transitions[self.cur_state].items():
        #    if check_event(e):
        #        self.cur_state.exit(self.boy, e)
        #        self.cur_state = next_state
        #        self.cur_state.enter(self.boy, e)
        #        return True

        return False

    def draw(self):
        self.cur_state.draw(self.bird)


class Bird:
    def __init__(self):
        self.x, self.y = random.randint(1,1400), random.randint(400,500)
        self.frame = 0
        self.frame2 = 0
        self.action = 0
        self.face_dir = 1
        self.dir = 1
        self.image = load_image('bird_animation.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event()

    def draw(self):
        self.state_machine.draw()
