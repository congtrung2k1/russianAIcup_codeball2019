import math
from model.action import Action
from model.game import Game
from model.robot import Robot
from model.rules import Rules

EPS = 1e-5
ROBOT_MIN_RADIUS = 1
ROBOT_MAX_RADIUS = 1.05
ROBOT_MAX_JUMP_SPEED = 15
ROBOT_ACCELERATION = 100
ROBOT_NITRO_ACCELERATION = 30
ROBOT_MAX_GROUND_SPEED = 30
ROBOT_ARENA_E = 0
ROBOT_RADIUS = 1
ROBOT_MASS = 2
TICKS_PER_SECOND = 60
MICROTICKS_PER_TICK = 100
RESET_TICKS = 2 * TICKS_PER_SECOND
BALL_ARENA_E = 0.7
BALL_RADIUS = 2
BALL_MASS = 1
MIN_HIT_E = 0.4
MAX_HIT_E = 0.5
MAX_ENTITY_SPEED = 100
MAX_NITRO_AMOUNT = 100
START_NITRO_AMOUNT = 50
NITRO_POINT_VELOCITY_CHANGE = 0.6
NITRO_PACK_X = 20
NITRO_PACK_Y = 1
NITRO_PACK_Z = 30
NITRO_PACK_RADIUS = 0.5
NITRO_PACK_AMOUNT = 100
NITRO_PACK_RESPAWN_TICKS = 10 * TICKS_PER_SECOND
GRAVITY = 30
JUMP_DIST = 0.3

class Vector2D:
    def __init__(self, x = 0.0, z = 0.0):
        self.x = x
        self.z = z
    def __add__(self, other):
        return Vector2D(self.x + other.x, self.z + other.z)
    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.z - other.z)
    def __mul__(self, num: float):
        return Vector2D(num * self.x, num * self.z)
    def len(self):
        return (self.x * self.x + self.z * self.z) ** 0.5
    def normalize(self):
        return Vector2D(self.x/self.len(), self.z/self.len())

class MyStrategy:
    def act(self, me: Robot, rules: Rules, game: Game, action: Action):

        GOAL = rules.arena.goal_width / 2.0 - rules.arena.goal_side_radius

        if not me.touch:
            action.target_velocity_x = 0.0
            action.target_velocity_y = -MAX_ENTITY_SPEED
            action.target_velocity_z = 0.0
            action.jump_speed = 0.0
            action.use_nitro = True
            return

        #dist = me to ball
        dist = ((me.x - game.ball.x)**2 + (me.z - game.ball.z)**2)**0.5

        #jump to ball
        jump = (dist <= BALL_RADIUS + ROBOT_MAX_RADIUS + JUMP_DIST) and (me.z < game.ball.z)

        #set robot for attacker
        is_attacker = len(game.robots) == 2
        for robot in game.robots:
            robot: Robot = robot
            if robot.is_teammate and (robot.id != me.id):
                dist2 = ((robot.x - game.ball.x)**2 + (robot.z - game.ball.z)**2)**0.5
                if dist2 > dist:
                    is_attacker = True
                elif robot.z < me.z:
                    is_attacker = True

#ATTACK
        if is_attacker:
            for i in range(1,21):
                t = i * 0.1
                ball_x = game.ball.x
                ball_z = game.ball.z
                ball_vel_x = game.ball.velocity_x
                ball_vel_z = game.ball.velocity_z
                ball_pos = Vector2D(ball_x, ball_z) + Vector2D(ball_vel_x, ball_vel_z) * t

                to_ball = Vector2D(ball_pos.x, ball_pos.z) - Vector2D(me.x, me.z)
                speed = to_ball.len() / t
                
                target_velocity = to_ball.normalize() * speed
                action.target_velocity_x = target_velocity.x
                action.target_velocity_y = 0.0
                action.target_velocity_z = target_velocity.z
                action.jump_speed = ROBOT_MAX_JUMP_SPEED if jump else 0.0
                action.use_nitro = False
                return

#DEFEND             
        jump = 0.0
        t = 1
        def_pos = Vector2D(0.0, -rules.arena.depth / 2.0)

        if game.ball.velocity_z < -EPS:
            t = (def_pos.z - game.ball.z) / game.ball.velocity_z
            def_pos.x = game.ball.x + game.ball.velocity_x * t

        if def_pos.x < -GOAL:
            def_pos.x = -GOAL
        elif GOAL < def_pos.x:
            def_pos.x = GOAL

        to_pos = Vector2D(def_pos.x - me.x, def_pos.z - me.z)
        speed = min(to_pos.len() / t, ROBOT_MAX_GROUND_SPEED)
        def_velocity = to_pos.normalize() * speed

        if (game.ball.z + game.ball.velocity_z * t <= -rules.arena.depth / 2.0) and (me.z == def_pos.z):
            if game.ball.y + game.ball.velocity_y * t > 0:
                jump = ROBOT_MAX_JUMP_SPEED

        if game.ball.z <= -rules.arena.depth / 4.0:
            for i in range(1,101):
                t = i * 0.1
                ball_x = game.ball.x
                ball_z = game.ball.z
                ball_vel_x = game.ball.velocity_x
                ball_vel_z = game.ball.velocity_z
                ball_pos = Vector2D(ball_x, ball_z) + Vector2D(ball_vel_x, ball_vel_z) * t

                to_ball = Vector2D(ball_pos.x, ball_pos.z) - Vector2D(me.x, me.z)
                speed = to_ball.len() / t

                target_velocity = to_ball.normalize() * speed
                action.target_velocity_x = target_velocity.x
                action.target_velocity_y = 0.0
                action.target_velocity_z = target_velocity.z
                action.jump_speed = ROBOT_MAX_JUMP_SPEED if jump else 0.0
                action.jump_speed = 0.0
                action.use_nitro = False
                return

        action.target_velocity_x = def_velocity.x
        action.target_velocity_y = 0.0
        action.target_velocity_z = def_velocity.z
        action.jump_speed = jump
        action.use_nitro = False

    def custom_rendering(self):
        return ""
