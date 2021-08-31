#include <pybind11/pybind11.h>
#include "endless-sky/source/Angle.h"
#include "endless-sky/source/Point.h"
#include "endless-sky/source/Random.h"

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

int add(int i, int j) {
    return i + j;
}

namespace py = pybind11;

PYBIND11_MODULE(endless_sky_bindings, m) {
    m.doc() = R"pbdoc(
        Endless Sky Bindings
        -----------------------
        .. currentmodule:: endless_sky_bindings
        .. autosummary::
           :toctree: _generate
           add
           subtract
    )pbdoc";

    m.def("add", &add, R"pbdoc(
        Add two numbers
        Some other explanation about the add function.
    )pbdoc");

    m.def("subtract", [](int i, int j) { return i - j; }, R"pbdoc(
        Subtract two numbers
        Some other explanation about the subtract function.
    )pbdoc");

    // source/Point
    py::class_<Point>(m, "Point")
            .def(py::init<double,double>())
            .def_readwrite("x", &Point::x)
            .def_readwrite("y", &Point::y)
            .def("Unit", &Point::Unit);

    m.def("RandomSeed", &Random::Seed);
    m.def("RandomInt", &Random::Int);

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
