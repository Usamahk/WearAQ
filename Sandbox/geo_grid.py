#!/usr/bin/python
import math

def makeGrid(maxLat, maxLon, minLat, minLon, resX, resY):
	"""
	makeGrid generates a grid of <resX> x <resY> resolution
	mapped on a boundig box described by <maxLat>, <maxLon>, <minLat>, <minLon>
	"""

	# TO VALIDATE!
	# latitude ranages from -90 to +90
	# latitude ranages from -180 to +180

	# the grid array
	grid = []

	# find lat absolute distance
	totolLat = abs(minLat) + abs(maxLat)
	
	# find lon absolute distance
	totolLon = abs(minLon) + abs(maxLon)

	# divide distances by gurd resolution
	gridBlockWidth = totolLat/resX
	gridBlockHeight = totolLon/resY

	# get grid blocks coordinates
	for i in range(resY):
		for j in range(resX):
			x1 = minLat + (gridBlockWidth * j)
			x2 = minLat + (gridBlockWidth * (j+1))

			y1 = maxLon - (gridBlockHeight * i)
			y2 = maxLon - (gridBlockHeight * (i+1))

			currentBlock = { 'minX': roundTo3DecimalP(x1), 'minY': roundTo3DecimalP(y1), 'maxX': roundTo3DecimalP(x2), 'maxY': roundTo3DecimalP(y2) }

			grid.append(currentBlock)


	return grid

def roundTo3DecimalP(c):

	return math.ceil(c*1000)/1000