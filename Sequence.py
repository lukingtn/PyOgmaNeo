# ----------------------------------------------------------------------------
#  PyOgmaNeo
#  Copyright(c) 2016 Ogma Intelligent Systems Corp. All rights reserved.
#
#  This copy of PyOgmaNeo is licensed to you under the terms described
#  in the PYOGMANEO_LICENSE.md file included in this distribution.
# ----------------------------------------------------------------------------

# -*- coding: utf-8 -*-

import ogmaneo
import numpy as np
from copy import copy

sequence = [[ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0 ],
            [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0 ],
            [ 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0 ],
            [ 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0 ],
            [ 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0 ],
            [ 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0 ],
            [ 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0 ],
            [ 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0 ],
            [ 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0 ],
            [ 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0 ],
            [ 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0 ],
            [ 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0 ],
            [ 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0 ],
            [ 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0 ],
            [ 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0 ],
            [ 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0 ],
            [ 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0 ],
            [ 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0 ],
            [ 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0 ],
            [ 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0 ],
            [ 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0 ],
            [ 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0 ],
            [ 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0 ],
            [ 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0 ],
            [ 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0 ],
            [ 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0 ],
            [ 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0 ],
            [ 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0 ],
            [ 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0 ],
            [ 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0 ],
            [ 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0 ],
            [ 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0 ],
            [ 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0 ],
            [ 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]]

def arrToList(mat):
    return ogmaneo.vectorf(mat.astype(np.float32).tolist())

trainIter = 1500 # Number of songs to iterate over

csi = ogmaneo.ComputeSystemInterface()
cs = csi.create(ogmaneo.ComputeSystem._cpu) # Use _gpu instead of _cpu

prog = ogmaneo.ComputeProgramInterface()
prog.loadMainKernel(csi) # Load default kernels

# Create Neo Hierarchy
layerDescs = [ ogmaneo.LayerDescs(16, 16), ogmaneo.LayerDescs(16, 16), ogmaneo.LayerDescs(16, 16), ogmaneo.LayerDescs(16, 16) ]

# Some settings
for l in layerDescs:
    l._spFeedForwardWeightAlpha = 0.2
    l._spPredictionWeightAlpha = 0.2
    l._spBiasAlpha = 0.004
    l._spActiveRatio = 0.04
    l._feedForwardRadius = 6
    l._inhibitionRadius = 5
    l._predictionRadius = 6

# Hierarchy parameters
rootSize = int(np.ceil(np.sqrt(len(sequence[0])))) # Fit notes into a square
inputWidth = rootSize
inputHeight = rootSize
totalInputSize = inputWidth * inputHeight
leftovers = totalInputSize - len(sequence[0])
initMinWeight = -0.01
initMaxWeight = 0.01
seed = 23423

h = ogmaneo.Hierarchy(csi(), prog(), inputWidth, inputHeight, layerDescs, initMinWeight, initMaxWeight, seed)

for i in range(0, trainIter):
    resized = copy(sequence[i % len(sequence)])

    for j in range(0, leftovers):
        resized.append(0.0)

    h.simStep(resized, True)

    match = True

    res = []

    for j in range(0, len(sequence[0])):
        if (h.getPrediction()[j] > 0.5) != (sequence[(i + 1) % len(sequence)][j] > 0.5):
            match = False

        res.append(float(h.getPrediction()[j] > 0.5))

    print(match)
