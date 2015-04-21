Renato Pereyra
COMP 590 - Artificial Intelligence & Machine Learning HW1

Overview:

Take a "shredded" image and organize the pixel strips to produce the original image.

Execution

Execute with the python interpreter. This project unscrambles pixel slices to generate a whole image that minimizes pixel disagreement between slices. The algorithm will not always finish because it may get stuck in a local minimum during the minimization process.

	$ python optimization.py
	$ python optimization_extra.py

	Note: The assignment script (optimization.py) runs within a reasonable amount of time (7 min on my Fedora VM) and produces the snapshots in the results folder.

	The extra credit script (optimization_extra.py) takes much longer to run (somewhere in the order of 4 hours) and produces the snapshots in the results_extra_credit folder.

-------------------------------------------------------------------------------

Design

CONSTANTS:

	1) NUM_SLICES: The number of slices to be analyzed.
	2) SAMPLE_FREQ: The frequency at which to sample the ordering of slices.

METHODS:

	There are seven functions submitted in each python script. They are described below at a high level.

	main:
		Driver method. Obtains the pixel slices from the hw1 directory, computes the disagreement matrix D, and calls the hillclimbing algorithm.

	hillClimb:
		Runs a loop attempting to find the ordering of slices which minimizes the disagreement between pixels. To do this, it calls on the minNeighbor function, which will provide it with the neighbor configuration with lowest possible disagreement.

	minNeighbor:
		Determines the neighbor configuration with lowest possible disagreement by looping through ALL possible on-move rearrangements and returning the order with minimum disagreement.

	computeOrderDiasgreement:
		Computes the pairwise disagreement of a given ordering of slices. Called when determining the minNeighbor.

	computeD:
		Computes the disagreement matrix for any possible pairing of slices.

	computeDisagreement:
		Computes the disagreement between two slices. Only called when building the D matrix.

	toImage:
		Outputs the current ordering of slices into an image.
