import cv2

class ShapeDetector:
	def __init__(self):
		pass

    # Algorithm is based on the split-merge algorithm, essentially treats shape as a curve, performs linear curve fit on it
	def detect(self, contour):
		# Initialize the shape name and approximate the contour
		shape = "Unknown"

		perimeter = cv2.arcLength(contour, True)

        # Second parameter controls how aggresive the curve fitting is, makes it more linear
		approximation = cv2.approxPolyDP(contour, 0.04 * perimeter, True)

		# Try to guess the shape based on the number of edges the shape has
		if len(approximation) == 3:
			shape = "triangle"

        # Use aspect ratio to determine whether or not it is a square or rectangle
		elif len(approximation) == 4:
			# Compute the bounding box of the contour
			(x, y, w, h) = cv2.boundingRect(approximation)

			aspectratio = w/float(h)

            # Aspect ratio of 1 indicates a perfect square
			if aspectratio >= 0.95 and aspectratio <= 1.05:
				shape = "square"
			else:
				shape = "rectangle"
		elif len(approximation) == 5:
			shape = "pentagon"
		elif len(approximation) == 6:
			shape = "hexagon"
		elif len(approximation) == 7:
			shape = "heptagon"
		elif len(approximation) == 8:
			shape = "octagon"
		elif len(approximation) == 10:
			shape = "star"
		elif len(approximation) == 12:
			shape = "cross"
		# otherwise, we assume the shape is a circle
		else:
			# Compute the bounding box of the contour
			(x, y, w, h) = cv2.boundingRect(approximation)

			aspectratio = w/float(h)

            # Aspect ratio of 1 indicates a perfect circle
			if aspectratio >= 0.95 and aspectratio <= 1.05:
				shape = "circle"
			else:
				shape = "semicircle"
				
		# Return the name of the shape
		return shape