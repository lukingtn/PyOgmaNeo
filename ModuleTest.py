# ----------------------------------------------------------------------------
#  PyOgmaNeo
#  Copyright(c) 2016 Ogma Intelligent Systems Corp. All rights reserved.
#
#  This copy of PyOgmaNeo is licensed to you under the terms described
#  in the PYOGMANEO_LICENSE.md file included in this distribution.
# ----------------------------------------------------------------------------

# -*- coding: utf-8 -*-

import ogmaneo

import pkg_resources
print("OgmaNeo version: " + pkg_resources.get_distribution("ogmaneo").version)

csi = ogmaneo.ComputeSystemInterface()
cs = csi.create(ogmaneo.ComputeSystem._cpu)

cpi = ogmaneo.ComputeProgramInterface()
cpi.loadMainKernel(csi)

print("Done")
