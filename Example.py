# ----------------------------------------------------------------------------
#  PyOgmaNeo
#  Copyright(c) 2016 Ogma Intelligent Systems Corp. All rights reserved.
#
#  This copy of PyOgmaNeo is licensed to you under the terms described
#  in the PYOGMANEO_LICENSE.md file included in this distribution.
# ----------------------------------------------------------------------------

# -*- coding: utf-8 -*-

import numpy as np
import os.path
import ogmaneo

import pkg_resources
print("OgmaNeo version: " + pkg_resources.get_distribution("ogmaneo").version)

serializationEnabled = True

layer_desc = [ogmaneo.LayerDescs(256, 256), ogmaneo.LayerDescs(256, 256)]
for l in layer_desc:
    print("Layer sizes: " + str(l._width) + " x " + str(l._width))

csi = ogmaneo.ComputeSystemInterface()
cs = csi.create(ogmaneo.ComputeSystem._gpu)

cpi = ogmaneo.ComputeProgramInterface()
cpi.loadMainKernel(csi)

w, h = 16, 16
hierarchy = ogmaneo.Hierarchy(csi(), cpi(), w, h, layer_desc, -0.01, 0.01, 1337)

if (serializationEnabled and os.path.exists("example.opr")):
    print("Loading hierarchy from example.opr")
    hierarchy.load(csi(), cpi(), "example.opr")

num_inputs = 100
inputs = [[x for x in range(w*h)] for y in range(num_inputs)]

for i in range(0, num_inputs):
    hierarchy.simStep(inputs[i], True)
    prediction = hierarchy.getPrediction()
    print("Input:", inputs[i])
    print("Predt:", prediction)

if (serializationEnabled):
    print("Saving hierachy to example.opr")
    hierarchy.save(csi(), "example.opr")

print("Done")
