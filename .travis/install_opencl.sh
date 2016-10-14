#!/bin/sh

# OgmaNeo
# Copyright(c) 2016 Ogma Intelligent Systems Corp. All rights reserved.
#
# This copy of OgmaNeo is licensed to you under the terms described
# in the OGMANEO_LICENSE.md file included in this distribution.

set -ex

#----------------------------------------
# Install POCL (Linux only)

if [ $TRAVIS_OS_NAME == 'linux' ]; then
    cd $TRAVIS_BUILD_DIR

    sudo apt install libhwloc-dev ocl-icd-opencl-dev libglew-dev
    sudo apt install zlib1g-dev libedit-dev libltdl-dev opencl-headers

    # Check to see if POCL cache folder is empty
    if [ ! -d "$HOME/.local/pocl" ]; then
        sudo apt install clang-3.8 libclang-3.8-dev

        git clone https://github.com/pocl/pocl.git
        cd pocl

        git checkout release_0_13
        mkdir build-pocl; cd build-pocl

        CC=gcc-4.8 CXX=g++-4.8 $HOME/.local/cmake/bin/cmake -DCMAKE_INSTALL_PREFIX=$HOME/.local/pocl -DWITH_LLVM_CONFIG=/usr/bin/llvm-config-3.8 -DSTATIC_LLVM=1 -DENABLE_ICD=1 ..

        make
        sudo make install
        sudo cp /etc/OpenCL/vendors/pocl.icd $HOME/.local/pocl/
    else
        echo "Using cached POCL directory."

        sudo mkdir -p /etc/OpenCL/vendors/
        sudo cp $HOME/.local/pocl/pocl.icd /etc/OpenCL/vendors/
    fi
fi


#----------------------------------------
# Install Khronos cl2.hpp (linux only)
cd $TRAVIS_BUILD_DIR

if [ $TRAVIS_OS_NAME == 'linux' ]; then
    # CMakeLists.txt will also try to find this
    # file, and download it iff not found
    wget https://github.com/KhronosGroup/OpenCL-CLHPP/releases/download/v2.0.10/cl2.hpp
    sudo cp cl2.hpp /usr/include/CL/
fi


#----------------------------------------
# Test OpenCL using Oblomov's clinfo
cd $TRAVIS_BUILD_DIR

git clone https://github.com/Oblomov/clinfo.git
cd clinfo
make
./clinfo
