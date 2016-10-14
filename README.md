<!---
  PyOgmaNeo
  Copyright(c) 2016 Ogma Intelligent Systems Corp. All rights reserved.

  This copy of PyOgmaNeo is licensed to you under the terms described
  in the PYOGMANEO_LICENSE.md file included in this distribution.
--->

# Python bindings for OgmaNeo

[![Build Status](https://travis-ci.org/ogmacorp/PyOgmaNeo.svg?branch=master)](https://travis-ci.org/ogmacorp/PyOgmaNeo)

## Introduction

PyOgmaNeo contains Python [SWIG](http://www.swig.org/) bindings to the main [OgmaNeo](https://github.com/ogmacorp/OgmaNeo) C++ library.

These bindings provide an interface into the C++ library. Allowing Python scripts to gain access to the OgmaNeo CPU and GPU accelerated algorithms. Implementation(s) of Online Predictive Hierarchies, as described in arXiv.org paper: [Feynman Machine: The Universal Dynamical Systems Computer](http://arxiv.org/abs/1609.03971).

## Installation

Once the PyOgmaNeo requirements have been setup. The following command will download and build the OgmaNeo library, process the SWiG bindings, and install PyOgmaNeo into a local site-packages location.

```
python setup.py install --user
```

## Importing and Setup

The PyOgmaNeo module can be imported into Python using:

```python
import ogmaneo
```

Two interfaces are used to setup PyOgmaNeo. The `ComputeSystemInterface` is used to setup the OgmaNeo C++ library and OpenCL. The `ComputeProgramInterface` is used to load default packaged OpenCL kernel code. For example:
```python
csi = ogmaneo.ComputeSystemInterface()  
cs = csi.create(ogmaneo.ComputeSystem._gpu)  # or _cpu

cpi = ogmaneo.ComputeProgramInterface()  
cpi.loadMainKernel(csi)
```

Layer properties can be accessed via `LayerDescs`. With the main hierarchy accessed through `Hierarchy`. For example:
```python
layer_desc = [ogmaneo.LayerDescs(256, 256), ogmaneo.LayerDescs(256, 256)]  

input_width, input_height = 16, 16  
hierarchy = ogmaneo.Hierarchy(csi(), prog(), input_width, input_height, layer_desc, -0.01, 0.01, 1234)  
```

`Hierarchy.simStep` is used to pass input into the hierarchy and run through one prediction step. For example:
```python
hierarchy.simStep(inputs[i], True)  
```

`Hierarchy.getPrediction()` is used to obtain prediction after a `simStep` has taken place.
```python
prediction = hierarchy.getPrediction()  
```

A hierarchy can be saved and loaded as follows:
```python
hierarchy.save(csi(), "filename.opr")  
hierarchy.load(csi(), cpi(), "filename.opr")
```

The above example Python code can be found in the `Example.py` file.

## Requirements

The same requirements that OgmaNeo has, are required for PyOgmaNeo: a C++1x compiler, [CMake](https://cmake.org/), and an OpenCL SDK.

Additionally PyOgmaNeo requires an installation of [SWIG](http://www.swig.org/) and the Khronos `cl2.hpp` header file.

PyOgmaNeo has been tested using:

| Distribution | Operating System (Compiler) |
| --- | ---:|
| Python 2.7 | Linux (GCC 4.8+) |
| Python 2.7 | Mac OSX |
| Anaconda Python 2.7 3.4 & 3.5 | Linux (GCC 4.8+) |
| Anaconda Python 3.5 | Windows (MSVC 2015) |

Further information on Python compatible Windows compilers can be found [here](https://wiki.python.org/moin/WindowsCompilers).

#### [SWIG](http://www.swig.org/)

- Linux requires SWIG installed via, for example, ```sudo apt-get install swig``` command (or via ```yum```).
- Windows requires installation of SWIG (2.0.1+). With the SourceForge Zip expanded, and the PATH environment variable updating to include the SWIG installation binary directory (for example `C:\Program Files (x86)\swigwin-3.0.8`).

#### [cl2.hpp](http://github.khronos.org/OpenCL-CLHPP/)

The `cl2.hpp` header file can be downloaded from Github https://github.com/KhronosGroup/OpenCL-CLHPP/releases and needs to be placed alongside your OpenCL header files.

## Examples

#### `Sequence.py`  
A sequence prediction example that shows the following:
- imports the PyOgmaNeo module
- instantiate the main compute system (enabling _cpu or _gpu processing)
- load the default OpenCL packaged kernel code
- changing internal layer parameters
- construct a predictive hierarchy
- training a predictive hierarchy with a repeatitive sequence
- monitoring the predictions of the hierarchy

## OgmaNeo Developers

By default PyOgmaNeo uses the `CMake/FindOgmaNeo.cmake` script to find an existing installation of the OgmaNeo library. If it cannot find the library, CMake automatically clones the OgmaNeo master repository and builds the library in place.

Two options exist for OgmaNeo library developers that can redirect this process:

- The `CMakeLists.txt` file can be modified locally to point to a fork of an OgmaNeo repository, and also clone a particular branch from a fork. The `GIT_REPOSITORY` line in `CMakeLists.txt` file can be changed to point to a fork location. An additional `GIT_TAG` line can be added to obtain a particular branch from a fork.

- If you require PyOgmaNeo to use a local clone of OgmaNeo, the `setup.cfg` file can be modified locally to achieve this. An extra line can be added to specify optional CMake arguments.  
Similar to the following, but with `<repo_dir>` changed to point to your OgmanNeo root directory, or to appropriate system wide locations. This assumes that the OgmaNeo CMAKE_INSTALL_PREFIX has been set to `<repo_dir>/install` and that a `make install` build step has been performed before running the `python setup.py install --user` command. Make sure to use `/` as a path seperator.  
> [build_ext]  
> inplace=0  
> extra-cmake-args=-DOGMANEO_LIBRARY=\<repo_dir\>/install/lib/OgmaNeo.lib -DOGMANEO_INCLUDE_DIR=\<repo_dir\>/install/include  

## Contributions

Refer to the PyOgmaNeo [CONTRIBUTING.md](https://github.com/ogmacorp/PyOgmaNeo/blob/master/CONTRIBUTING.md) file for details about contributing to PyOgmaNeo. The same instructions apply for contributing to OgmaNeo, including the signing of the [Ogma Contributor Agreement](https://ogma.ai/wp-content/uploads/2016/09/OgmaContributorAgreement.pdf).

## License and Copyright

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />The work in this repository is licensed under the <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>. See the [PYOGMANEO_LICENSE.md](https://github.com/ogmacorp/PyOgmaNeo/blob/master/PYOGMANEO_LICENSE.md) and [LICENSE.md](https://github.com/ogmacorp/PyOgmaNeo/blob/master/LICENSE.md) file for further information.

Contact Ogma Intelligent Systems Corp licenses@ogmacorp.com to discuss commercial use and licensing options.

PyOgmanNeo Copyright (c) 2016 [Ogma Intelligent Systems Corp](https://ogmacorp.com). All rights reserved.
