from math import *
import numpy as np
import scipy.misc as smp


IMG_WIDTH = 500
IMG_HEIGHT = 500


class Point:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def __str__(self):
		return "{} {} {}".format(self.x, self.y, self.z)

class Sphere:
	def __init__(self, center, radius, color):
		self.center = center
		self.r = radius
		self.color = color

spheres = [
	Sphere(Point(0, 0, 4), 2, Point(255, 0, 0))
]

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
	
# `d` is the unit vector of the ray
def intersectRaySphere(D, sphere):
	L = subPoint(sphere.center, camera)
	tca = dotProd(L, D)
	#	print(str(L), str(D), "tca", tca)

	if tca < 0:
		print("Should never get here", tca, str(L))
		return None

	d_2 = dotProd(L, L) - tca*tca
	if d_2 > sphere.r*sphere.r:
		print("Hahahah", d_2)
		return None

	print("hohoh")
	thc = sqrt(sphere.r*sphere.r - d_2)
	t0 = tca - thc
	t1 = tca + thc

	return True
		
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

		if intersectRaySphere(rayPoint, spheres[0]):
			data[x,y] = [x % 255, y % 255, (x * y) % 255]


img = smp.toimage( data )       # Create a PIL image
img.show()                      # View in default viewer
