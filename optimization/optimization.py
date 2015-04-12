from math import sqrt
from PIL import Image

NUM_SLICES = 151				#number of slices
SAMPLE_FREQ = 10				#frequency at which to output image
sliceRange = range(NUM_SLICES)	#frenquently used range throughtout this program

#driver method for this program
def main():

	#get a 3D array of pixels from the different slices
	slices = [ [ line.split('  ') for line in open( "./hw1/slices" + str(i+1) ).read().splitlines() ] for i in sliceRange ]
	
	#initialize order list which will maintain the order of slices as it is changed throughout this program
	order = [ i for i in sliceRange ]

	#compute the disagreement matrix. 
	#This matrix is computed via the two-norm of adjacent pixel vectors for every possible combination of slices.
	D = computeD( slices )

	#initialize hill climbing algorithm to rearrange slices
	hillClimb( D, order, slices )

#hill climbing algorith to rearrange slices
def hillClimb( D, order, slices ):

	#counters
	counter = 0
	imgCounter = 0

	#output an image of how the data looks before algorithm
	toImage( order, slices, imgCounter )

	#initialize algorithm parameters
	minDisagreement = computeOrderDisagreement( D, order )
	bestMin = minDisagreement
	minOrder = order[:]

	done = False
	while not done:

		#determine the neighbor state which minimizes disagreement
		#a neighbor is considered as any state in which one slice is placed at a different location than the current
		minOrder, minDisagreement = minNeighbor( D, order, minDisagreement, minOrder )

		#ensure progress is being made
		if bestMin - minDisagreement > 0:

			#store new minima
			bestMin = minDisagreement
			order = minOrder[:]

			#if counter reaches 10 output image
			counter = counter + 1
			if counter == SAMPLE_FREQ:
				imgCounter = imgCounter + 1
				toImage( order, slices, imgCounter )
				counter = 0

		#is no progress was made, output image and end
		else:
			imgCounter = imgCounter + 1
			toImage( order, slices, imgCounter )
			done = True

#determines the neighbor state which minimizes disagreement
#a neighbor is considered as any state in which one slice is placed at a different location than the current
def minNeighbor ( D, order, lastMinDisagreement, lastMinOrder ):

	#initializations
	minDisagreement = lastMinDisagreement
	minOrder = lastMinOrder[:]

	#look for the rearrangement of a slice the minimizes disagreement
	#i will be the index to be repositioned
	#j will be the index to which i is being repositioned
	for i in sliceRange:
		for j in sliceRange:

			if i == j:				#no change will occur
				continue

			#temp variable
			possibleOrder = order[:]

			#perform the shift of the slice
			if j > i:
				for k in range(i,j,1):
					possibleOrder[k], possibleOrder[k+1] = possibleOrder[k+1], possibleOrder[k]
			elif j < i:
				for k in range(i,j,-1):
					possibleOrder[k-1], possibleOrder[k] = possibleOrder[k], possibleOrder[k-1]

			#determine disagreement of possible order
			orderDisagreement = computeOrderDisagreement( D, possibleOrder )

			#update parameters if necessary
			if minDisagreement - orderDisagreement > 0:
				minDisagreement = orderDisagreement
				minOrder = possibleOrder[:]

	return minOrder, minDisagreement

#compute pairwise disagreement of a particular ordering of slices
def computeOrderDisagreement( D, order ):

	orderDisagreement = 0
	for i in range(NUM_SLICES - 1):
		orderDisagreement = orderDisagreement + D[ order[i] ][ order[i+1] ]
	return orderDisagreement

#compute disagreement matrix of any possible pair of slices
def computeD( slices ):

	D = [[0.0 for col in sliceRange] for row in sliceRange]
	for i in sliceRange:
		for j in sliceRange:
			D[i][j] = computeDisagreement( slices[i], slices[j] )
	return D

#compute disagreement of slices by computing the two-norm of adjacent pixel vectors
#slice1 is assumed to be on the left of slice2
def computeDisagreement( slice1, slice2 ):
	
	disagreement = 0.0
	height = len( slice1 )
	width = len( slice1[1] )

	#sum up the square differences between pixels
	for i in range( height ):
		diff = float( slice1[i][width-1] ) - float( slice2[i][1] )
		disagreement = disagreement + pow(diff, 2.0)

	#compute two-norm and return
	disagreement = sqrt( disagreement )
	return disagreement

#output slice order into an image
def toImage( order, slices, imgCounter ):

	height = len( slices[0] )
	width = len( slices[0][0] ) - 1

	#new grayscale image
	img = Image.new( "L", (width * NUM_SLICES, height) )
	pixels = img.load()

	#loop through slices in correct order (note first index of slices is given by order[k]) and write pixel values
	for k in sliceRange:
		for i in range(height):
			for j in range(width):
				pixels[j + k * width, i] = float( slices[order[k]][i][j+1] )

	#output image
	img.save( "./snapshot" + str(imgCounter) + ".jpg", "JPEG" )

main()