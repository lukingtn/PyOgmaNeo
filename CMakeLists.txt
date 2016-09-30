# ----------------------------------------------------------------------------
#  PyOgmaNeo
#  Copyright(c) 2016 Ogma Intelligent Systems Corp. All rights reserved.
#
#  This copy of PyOgmaNeo is licensed to you under the terms described
#  in the PYOGMANEO_LICENSE.md file included in this distribution.
# ----------------------------------------------------------------------------

# CMake version 3.1+ is required to enable C++14 features cleanly
cmake_minimum_required(VERSION 3.1)

project(PyOgmaNeo)
set(CMAKE_VERBOSE_MAKEFILE OFF)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/CMake/")

set(OGMANEO_PATH "${CMAKE_BINARY_DIR}/3rdparty")
include_directories("${OGMANEO_PATH}/include")
link_directories("${OGMANEO_PATH}/lib")


############################################################################
# Find OgmaNeo include and libs

find_package(OgmaNeo)

if(OGMANEO_FOUND)
    message(STATUS "Found existing OgmaNeo in ${OGMANEO_INCLUDE_DIRS}")
else()
    message(STATUS "-- OgmaNeo will be downloaded and built from source")

    if(WIN32)
        set(OGMANEO_SHARED_LIBS False)
    else()
        set(OGMANEO_SHARED_LIBS True)
    endif()

    include(ExternalProject)
    ExternalProject_Add(OgmaNeo
        PREFIX OgmaNeo
        GIT_REPOSITORY "https://github.com/ogmacorp/OgmaNeo.git"
        CMAKE_ARGS
            "-DBUILD_SHARED_LIBS=${OGMANEO_SHARED_LIBS}"
            "-DCMAKE_INSTALL_PREFIX=${OGMANEO_PATH}"
    )
    set(OGMANEO_INCLUDE_DIRS "${OGMANEO_PATH}/include")

    if(WIN32)
        set(OGMANEO_LIBRARY "${OGMANEO_PATH}/lib/${CMAKE_STATIC_LIBRARY_PREFIX}OgmaNeo${CMAKE_STATIC_LIBRARY_SUFFIX}")
    else()
        set(OGMANEO_LIBRARY "${OGMANEO_PATH}/lib/${CMAKE_SHARED_LIBRARY_PREFIX}OgmaNeo${CMAKE_SHARED_LIBRARY_SUFFIX}")
    endif()
endif()

include_directories(${OGMANEO_INCLUDE_DIRS})


############################################################################
# Find OpenCL package

#find_package(OPENCL REQUIRED)
find_path(OpenCL_INCLUDE_DIRS
    NAMES OpenCL/cl.h CL/cl.h
    HINTS /usr/local/include/ $ENV{AMDAPPSDKROOT}/include/
)
find_library(OpenCL_LIBRARIES
    NAMES OpenCL
    HINTS /usr/local/lib/ $ENV{AMDAPPSDKROOT}/lib/x86_64/
    PATH_SUFFIXES ${PLATFORM}${BITNESS} ${BITNESS_SUFFIX}
)

if(OpenCL_INCLUDE_DIRS STREQUAL "" OR OpenCL_LIBRARIES STREQUAL "")
    message(FATAL_ERROR "Could not locate OpenCL include & libs")
else()
    message(STATUS "Found existing OpenCL in ${OpenCL_INCLUDE_DIRS}")
endif()

include_directories(${OpenCL_INCLUDE_DIRS})


############################################################################
# Find SWIG and setup building the Python bindings to OgmaNeo library

find_package(SWIG REQUIRED)
include(${SWIG_USE_FILE})

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
endif()

############################################################################
# Find Python package

# Are we dealing with Anaconda?
set(CONDA_COMMAND conda info --root)
execute_process(
    COMMAND ${CONDA_COMMAND}
    RESULT_VARIABLE _CONDA_RESULT
    OUTPUT_VARIABLE _CONDA_OUTPUT
    OUTPUT_STRIP_TRAILING_WHITESPACE
    ERROR_STRIP_TRAILING_WHITESPACE
)
if(${_CONDA_RESULT} STREQUAL "0")
    string(TOLOWER ${_CONDA_OUTPUT} _CONDA_OUTPUT)
    string(REPLACE "\\" "/" _CONDA_OUTPUT ${_CONDA_OUTPUT})
    string(REGEX MATCH "anaconda" ANACONDA_PYTHON_FOUND "${_CONDA_OUTPUT}")
endif()

if(ANACONDA_PYTHON_FOUND)
    set(ANACONDA_PYTHON_DIR ${_CONDA_OUTPUT})
    message("Found anaconda in ${ANACONDA_PYTHON_DIR}")

    set(_PYTHON_COMMAND python --version)
    execute_process(
        COMMAND ${_PYTHON_COMMAND}
        ERROR_VARIABLE _PYTHON_ERROR
        OUTPUT_STRIP_TRAILING_WHITESPACE
        ERROR_STRIP_TRAILING_WHITESPACE
    )
    string(REGEX MATCH "Python ([0-9]+)[.]([0-9]+)[.]([0-9]+)" _PYTHON_VERSION_FOUND "${_PYTHON_ERROR}")
    set(_PYTHON_VERSION_MAJOR ${CMAKE_MATCH_1})
    set(_PYTHON_VERSION_MINOR ${CMAKE_MATCH_2})
    set(_PYTHON_VERSION_PATCH ${CMAKE_MATCH_3})

    if(WIN32)
        set(ANACONDA_PYTHON_VERSION ${_PYTHON_VERSION_MAJOR}${_PYTHON_VERSION_MINOR})
        set(_PYTHON_LIB "libs/python${ANACONDA_PYTHON_VERSION}${CMAKE_STATIC_LIBRARY_SUFFIX}")
    else()
        set(ANACONDA_PYTHON_VERSION ${_PYTHON_VERSION_MAJOR}.${_PYTHON_VERSION_MINOR})
        if(${_PYTHON_VERSION_MAJOR} MATCHES 2)
            set(_PYTHON_EXTENSION "")
        else()
            set(_PYTHON_EXTENSION "m")
        endif()
        set(_PYTHON_ID "python${ANACONDA_PYTHON_VERSION}${_PYTHON_EXTENSION}")
        set(_PYTHON_LIB "lib/${CMAKE_SHARED_LIBRARY_PREFIX}python${ANACONDA_PYTHON_VERSION}${_PYTHON_EXTENSION}${CMAKE_SHARED_LIBRARY_SUFFIX}")
    endif()

    if(NOT DEFINED ENV{CONDA_DEFAULT_ENV})
        set(PYTHON_INCLUDE_DIR "${ANACONDA_PYTHON_DIR}/include/${_PYTHON_ID}" CACHE INTERNAL "")
        set(PYTHON_LIBRARY "${ANACONDA_PYTHON_DIR}/${_PYTHON_LIB}" CACHE INTERNAL "")
    else()
        set(_CONDA_DEFAULT_ENV $ENV{CONDA_DEFAULT_ENV})
        string(REPLACE "\\" "/" _CONDA_DEFAULT_ENV ${_CONDA_DEFAULT_ENV})
        set(PYTHON_INCLUDE_DIR "${ANACONDA_PYTHON_DIR}/envs/${_CONDA_DEFAULT_ENV}/include/${_PYTHON_ID}" CACHE INTERNAL "")
        set(PYTHON_LIBRARY "${ANACONDA_PYTHON_DIR}/envs/${_CONDA_DEFAULT_ENV}/${_PYTHON_LIB}" CACHE INTERNAL "")
    endif()

    message("PYTHON_INCLUDE_DIR = ${PYTHON_INCLUDE_DIR}")
    message("PYTHON_LIBRARY = ${PYTHON_LIBRARY}")

    set(PYTHON_INCLUDE_DIRS "${PYTHON_INCLUDE_DIR}")
    set(PYTHON_LIBRARIES "${PYTHON_LIBRARY}")
    set(FOUND_PYTHONLIBS TRUE)
else()
    find_package(PythonLibs)
endif()

include_directories(${PYTHON_INCLUDE_DIR})


############################################################################
# Setup SWIG bindings

set(CMAKE_SWIG_OUTDIR "${CMAKE_BINARY_DIR}")
set(CMAKE_SWIG_FLAGS "-I\"${PYTHON_INCLUDE_DIR}\" -I\"${OpenCL_INCLUDE_DIRS}\" -I\"${OGMANEO_INCLUDE_DIRS}\"")

set_source_files_properties(ogmaneo.i PROPERTIES CPLUSPLUS ON)

swig_add_module(ogmaneo python ogmaneo.i)
swig_link_libraries(ogmaneo ${PYTHON_LIBRARIES} ${OpenCL_LIBRARIES} ${OGMANEO_LIBRARY})

if(NOT OGMANEO_FOUND)
    set_property(TARGET _ogmaneo PROPERTY DEPENDS OgmaNeo)
    set(SWIG_MODULE_ogmaneo_EXTRA_DEPS OgmaNeo)
endif()

set(CMAKE_INSTALL_PREFIX ${CMAKE_SWIG_OUTDIR})
install(TARGETS _ogmaneo DESTINATION ${CMAKE_SWIG_OUTDIR})
install(FILES ${CMAKE_BINARY_DIR}/ogmaneo.py DESTINATION ${CMAKE_SWIG_OUTDIR})
