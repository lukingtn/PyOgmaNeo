// ----------------------------------------------------------------------------
// PyOgmaNeo
//  Copyright(c) 2016 Ogma Intelligent Systems Corp. All rights reserved.
//
//  This copy of PyOgmaNeo is licensed to you under the terms described
//  in the PYOGMANEO_LICENSE.md file included in this distribution.
// ----------------------------------------------------------------------------

%begin %{
#include <cmath>
#include <iostream>
%}
%module ogmaneo

%{
#include "system/SharedLib.h"
#include "system/ComputeSystem.h"
#include "system/ComputeProgram.h"
#include "OgmaNeo.h"
#include "neo/LayerDescs.h"
#include "neo/Hierarchy.h"
#include "neo/Agent.h"
#include "neo/ScalarEncoder.h"
%}

%include "std_string.i"
%include "std_vector.i"

namespace std {
    %template(vectorld) vector<ogmaneo::LayerDescs>;
    %template(vectorf) vector<float>;
};

%include "system/SharedLib.h"
%include "system/ComputeSystem.h"
%include "system/ComputeProgram.h"
%include "OgmaNeo.h"
%include "neo/LayerDescs.h"
%include "neo/Hierarchy.h"
%include "neo/Agent.h"
%include "neo/ScalarEncoder.h"