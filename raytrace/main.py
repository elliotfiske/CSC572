from math import *
import numpy as np
import scipy.misc as smp


IMG_WIDTH = 400
IMG_HEIGHT = 400


class Point:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def __str__(self):
		return "{} {} {}".format(self.x, self.y, self.z)

	def __mul__(self, other):
		if isinstance(other, Point):
			return Point(self.x * other.x, self.y * other.y, self.z * other.z)
		else:
			return Point(self.x * other, self.y * other, self.z * other)

	def __rmul__(self, other):
		if isinstance(other, Point):
			return Point(self.x * other.x, self.y * other.y, self.z * other.z)
		else:
			return Point(self.x * other, self.y * other, self.z * other)

	def __add__(self, other):
		return Point(self.x + other.x, self.y + other.y, self.z + other.z)

class Sphere:
	def __init__(self, center, radius, ambient, diffuse):
		self.center = center
		self.r = radius
		self.ambient = ambient
		self.diffuse = diffuse

	

spheres = [
	Sphere(Point(0, 0, 7), 1, Point(0.06, 0.08, 0.04), Point(0.2, 0.9, 0.9)),
	Sphere(Point(1, 0, 5), 0.8, Point(0.06, 0.08, 0.04), Point(0.9, 0.9, 0.9)),
	Sphere(Point(0, -2, 2), 0.5, Point(0.06, 0.08, 0.04), Point(0.9, 0.4, 0.9)),
	Sphere(Point(-1, 2, 5), 1, Point(0.06, 0.08, 0.04), Point(0.2, 0.2, 0.9)),
]

light = Point(1, 4, 3)
lightColor = Point(1.0, 1.0, 1.0)

camera = Point(0, 0, 0)

def magnitude(vec):
	return sqrt(vec.x*vec.x + vec.y*vec.y + vec.z*vec.z)

# return a - b
def subPoint(a, b): 
	return Point(a.x - b.x, a.y - b.y, a.z - b.z)

# return a dot b
def dotProd(a, b): 
	return a.x * b.x + a.y * b.y + a.z * b.z

def normalize(vec):
	length = magnitude(vec)
	return Point(vec.x/length, vec.y/length, vec.z/length)

def reflect(I, N):
	return I + -2.0 * dotProd(N, I) * N

def clamp(a, low, hi):
	if a < low:
		return low
	if a > hi:
		return hi
	return a
	
# `d` is the unit vector of the ray
def intersectRaySphere(D, sphere):
	L = subPoint(sphere.center, camera)
	tca = dotProd(L, D)

	if tca < 0:
		print("Should never get here", tca, str(L))
		return None

	d_2 = dotProd(L, L) - tca*tca
	if d_2 > sphere.r*sphere.r:
		return None

	thc = sqrt(sphere.r*sphere.r - d_2)
	t0 = tca - thc
	t1 = tca + thc

	# Ambient
	ambient = lightColor * sphere.ambient

	# Diffuse
	intersection = camera + t1 * D
	N = normalize(subPoint(sphere.center, intersection))
	lightDir = normalize(subPoint(light, intersection))
	diff = max(dotProd(N, lightDir), 0)
	diffuse = lightColor * (diff * sphere.diffuse)

	# Specular
	viewDir = normalize(subPoint(camera, intersection))
	reflectDir = reflect(-1 * lightDir, N)
	spec = pow(max(dotProd(viewDir, reflectDir), 0), 32)
	specular = 0.5 * spec * lightColor;

	

	color = ambient + diffuse + specular

	return color
		
# Create a 1024x1024x3 array of 8 bit unsigned integers
data = np.zeros( (IMG_WIDTH,IMG_HEIGHT,3), dtype=np.uint8 )

# Camera is at (0, 0, 0)
for x in range(0, IMG_WIDTH):
	for y in range(0, IMG_HEIGHT):
		# Create ray unit vector
		rayX = x / float(IMG_WIDTH)  * 2 - 1
		rayY = y / float(IMG_HEIGHT) * 2 - 1
		rayPoint = Point(rayX, rayY, 1)
		rayPoint = normalize(rayPoint)

		color = None
		sphereNdx = 0
		while color is None and sphereNdx < len(spheres):
			color = intersectRaySphere(rayPoint, spheres[sphereNdx])
			sphereNdx += 1

		if color is not None:
			color = color * 255
			color.x = int(min(color.x, 255))
			color.y = int(min(color.y, 255))
			color.z = int(min(color.z, 255))
			data[x,y] = [color.x, color.y, color.z]



img = smp.toimage( data )       # Create a PIL image
img.show()                      # View in default viewer
