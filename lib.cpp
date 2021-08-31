#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include "endless-sky/source/Angle.h"
#include "endless-sky/source/DataNode.h"
#include "endless-sky/source/GameData.h"
#include "endless-sky/source/Point.h"
#include "endless-sky/source/Random.h"
#include "endless-sky/source/Set.h"
#include "endless-sky/source/Ship.h"
#include "endless-sky/tests/include/datanode-factory.h"

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


    // test/src/helpers/datanode-factory
    m.def("AsDataNode", &AsDataNode);

    // source/DataNode
    py::class_<DataNode>(m, "DataNode")
        .def(py::init<DataNode*>())
        .def("Size", &DataNode::Size)
        .def("Tokens", &DataNode::Token)
        .def("Token", &DataNode::Token)
        .def("Value", py::overload_cast<int>(&DataNode::Value, py::const_))
        .def("IsNumber", py::overload_cast<int>(&DataNode::IsNumber, py::const_))
        .def("HasChildren", &DataNode::HasChildren)
        .def("PrintTrace", &DataNode::PrintTrace)
        .def("__len__", [](const DataNode &n) { return n.Size(); })
        .def("__iter__", [](DataNode &n) {
            return py::make_iterator(n.begin(), n.end());
        }, py::keep_alive<0, 1>());

    // source/Angle
    py::class_<Angle>(m, "Angle")
        .def(py::init<>())
        .def(py::init<double>())
        .def(py::init<Point>())
        .def(py::self + py::self)
        .def(py::self += py::self)
        .def(py::self - py::self)
        .def(py::self -= py::self)
        .def(-py::self)
        .def("Unit", &Angle::Unit)
        .def("Degrees", &Angle::Degrees)
        .def("Rotate", &Angle::Rotate);

    // source/Point
    py::class_<Point>(m, "Point")
        .def(py::init<double,double>())
        .def_property_readonly("X", py::overload_cast<>(&Point::X, py::const_))
        .def_property_readonly("Y", py::overload_cast<>(&Point::Y, py::const_))
        .def("Unit", &Point::Unit);

    m.def("RandomSeed", &Random::Seed);
    m.def("RandomInt", py::overload_cast<>(&Random::Int));
    m.def("RandomInt", py::overload_cast<uint32_t>(&Random::Int));

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
