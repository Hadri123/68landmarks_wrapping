#include <Python.h>
#include <Windows.h>
#include <cmath>
#include <stdlib.h>
#include <ctime>

double doNothing(double a) {
    a += 1.0;
    a -= 1.0;
    return a;
}

PyObject* get_point_impl(PyObject*, PyObject* o) {
    double x = PyFloat_AsDouble(o);
    x = doNothing(x);
    return PyFloat_FromDouble(x);
}

PyObject* get_point2_impl(PyObject*, PyObject* o) {
    double x = PyFloat_AsDouble(o);
    return PyFloat_FromDouble(10*x);
}

// Creating the Python callable object
static PyMethodDef getpoints_methods[] = {
    // The first property is the name exposed to Python
    // The second is the C++ function with the implementation
    // METH_O means it takes a single PyObject argument
    { "c_get_point", (PyCFunction)get_point_impl, METH_O, nullptr },
    { "c_get_point2", (PyCFunction)get_point2_impl, METH_O, nullptr },

    // Terminate the array with an object containing nulls.
    { nullptr, nullptr, 0, nullptr }
};

// Creating Python Module
static PyModuleDef getpoints_module = {
    PyModuleDef_HEAD_INIT,
    "getpoints",                // Module name to use with Python import statements
    "Get 68 points shape in C++",   // Module description
    0,
    getpoints_methods           // Structure that defines the methods of the module
};

// Making the shared object importable
PyMODINIT_FUNC PyInit_getpoints() {
    return PyModule_Create(&getpoints_module);
}
