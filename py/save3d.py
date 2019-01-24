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
JUMP_DIST = 0.2

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

class Vector3D:
	def __init__(self, x = 0.0, y = 0.0, z = 0.0):
		self.x = x
		self.y = y
		self.z = z
	def __add__(self, other):
		return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
	def __sub__(self, other):
		return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)
	def __mul__(self, num: float):
		return Vector3D(self.x *num, self.y *num, self.z *num)
	def len(self):
		return (self.x**2 + self.y**2 + self.z**2)**0.5

def tichngoai(a, b, c):
	return Vector3D(a.y*b.z-a.z*b.y, a.x*b.z-a.z*b.x, a.x*b.y-a.y*b.x)

class MyStrategy:
	def act(self, me: Robot, rules: Rules, game: Game, action: Action):

		#dist = me to ball
		dist = ((me.x - game.ball.x)**2 + (me.y - game.ball.y)**2 + (me.z - game.ball.z)**2)**0.5

		is_attack = False
		for robot in Robot:
			robot: Robot = robot
			if robot.is_teammate and robot.id != me.id:
				dist2 = ((robot.x - game.ball.x)**2 + (robot.y - game.ball.y)**2 + (robot.z - game.ball.z)**2)**0.5
				if dist2 > dist:
					is_attack = True

#ATTACK
		if is_attack:
			

	def custom_rendering(self):
		return ""
