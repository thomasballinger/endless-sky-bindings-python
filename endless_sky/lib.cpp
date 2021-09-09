#define GL_SILENCE_DEPRECATION

#include <pybind11/pybind11.h>
#include <pybind11/operators.h>

// this has implications! see https://pybind11.readthedocs.io/en/stable/advanced/cast/stl.html?highlight=vector#automatic-conversion
// default for the rest of the STL types
#include <pybind11/stl.h>
// some specific "opaque" types for which e.g. .append() actually updates both sides
//#include <pybind11/stl_bind.h>

int maine(int argc, char *argv[]);

#include <SDL2/SDL.h>
#include "endless-sky/source/Angle.h"
#include "endless-sky/source/DataNode.h"
#include "endless-sky/source/DataFile.h"
#include "endless-sky/source/GameData.h"
#include "endless-sky/source/Outfit.h"
#include "endless-sky/source/PlayerInfo.h"
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

template<typename T>
void declare_set(py::module &m, std::string &typestr) {
    using Class = Set<T>;
    std::string pyclass_name = std::string("SetOf") + typestr + std::string("s");
    py::class_<Class>(m, pyclass_name.c_str())
        .def(py::init<>())
        .def("size", &Class::size)
        .def("__len__", [](const Class &s) { return s.size(); })
        .def("__iter__", [](Class &s) {
            return py::make_iterator(s.begin(), s.end());
        }, py::keep_alive<0, 1>())
        .def("Find", &Class::Find, py::return_value_policy::reference)
        .def("__getitem__", &Class::Find, py::return_value_policy::reference)
        .def("Has", &Class::Has);
}

PYBIND11_MODULE(bindings, m) {
    m.doc() = R"pbdoc(
        Endless Sky Bindings
        -----------------------
        .. currentmodule:: endless_sky.bindings
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

    m.def("saves_directory", []() {
        // memory leak because we dont' SDL_free() this str
        return SDL_GetPrefPath("endless-sky", "saves");
    });
    m.def("plugins_directory", []() {
        // memory leak because we dont' SDL_free() this str
        return SDL_GetPrefPath("endless-sky", "plugins");
    });

    // test/src/helpers/datanode-factory
    m.def("AsDataNode", &AsDataNode);

    // source/Angle
    py::class_<Angle>(m, "Angle")
        .def(py::init<>())
        .def(py::init<double>())
        .def(py::self + py::self)
        .def(py::self += py::self)
        .def(py::self - py::self)
        .def(-py::self)
        .def("Unit", &Angle::Unit)
        .def("Degrees", &Angle::Degrees)
        .def("Rotate", &Angle::Rotate);
    // TODO why does -= (removed) give a warning?

    // source/DataFile
    py::class_<DataFile>(m, "DataFile")
        .def(py::init<>())
        .def(py::init<std::string&>())
        .def("Load", py::overload_cast<const std::string&>(&DataFile::Load))
        .def("__iter__", [](DataFile &f) {
            return py::make_iterator(f.begin(), f.end());
        }, py::keep_alive<0, 1>()); // TODO is this keep_alive policy right?

    // source/DataNode
    py::class_<DataNode>(m, "DataNode")
        .def(py::init<DataNode*>())
        .def("Size", &DataNode::Size)
        .def("Tokens", &DataNode::Tokens)
        .def("Token", &DataNode::Token)
        .def("Value", py::overload_cast<int>(&DataNode::Value, py::const_))
        .def("IsNumber", py::overload_cast<int>(&DataNode::IsNumber, py::const_))
        .def("HasChildren", &DataNode::HasChildren)
        .def("PrintTrace", &DataNode::PrintTrace)
        .def("__len__", [](const DataNode &n) { return n.Size(); })
        .def("__iter__", [](DataNode &n) {
            return py::make_iterator(n.begin(), n.end());
        }, py::keep_alive<0, 1>());

    // source/Dictionary
    py::class_<Dictionary>(m, "Dictionary")
        .def(py::init<>())
        .def("__iter__", [](Dictionary &d) {
            return py::make_iterator(d.begin(), d.end());
        }, py::keep_alive<0, 1>())
        .def("Get", py::overload_cast<const std::string&>(&Dictionary::Get, py::const_))
        .def("__getitem__", py::overload_cast<const std::string&>(&Dictionary::Get, py::const_));

    // source/GameData
    py::class_<GameData>(m, "GameData")
        .def_static("BeginLoad", [](std::vector<std::string> argVec) {
            // pybind11 doesn't do double pointers, so convert
            std::vector<char *> cstrs;
            cstrs.reserve(argVec.size() + 1);
            for (auto &s : argVec) {
                cstrs.push_back(const_cast<char *>(s.c_str()));
            }
            cstrs.push_back(NULL);
            return GameData::BeginLoad(cstrs.data());
        })
	.def_static("CheckReferences", &GameData::CheckReferences)
	.def_static("Ships", &GameData::Ships);

    // source/Outfit
    py::class_<Outfit>(m, "Outfit")
        .def(py::init<>())
        .def("Load", &Outfit::Load)
        .def("Name", &Outfit::Name)
        .def("Attributes", &Outfit::Attributes);

    // source/PlayerInfo
    py::class_<PlayerInfo>(m, "PlayerInfo")
        .def("Ships", &PlayerInfo::Ships)
        .def_static("CurrentPlayer", &PlayerInfo::CurrentPlayer);

    // source/Point
    py::class_<Point>(m, "Point")
        .def(py::init<double,double>())
        .def_property_readonly("X", py::overload_cast<>(&Point::X, py::const_))
        .def_property_readonly("Y", py::overload_cast<>(&Point::Y, py::const_))
        .def("Unit", &Point::Unit);

    m.def("RandomSeed", &Random::Seed);
    m.def("RandomInt", py::overload_cast<>(&Random::Int));
    m.def("RandomInt", py::overload_cast<uint32_t>(&Random::Int));

    // source/Set
    std::string a = std::string("Ship");
    declare_set<Ship>(m, a);

    // source/Ship
    py::class_<Ship, std::shared_ptr<Ship>>(m, "Ship")
        .def(py::init<>())
        .def(py::init<Ship const &>())
        .def(py::init<const DataNode&>())

        .def("Load", &Ship::Load)
        .def("FinishLoading", &Ship::FinishLoading)
        .def("IsValid", &Ship::IsValid)
//        .def("Save", &Ship::Save)

        .def("UUID", &Ship::UUID)
        .def("SetUUID", &Ship::SetUUID)

        .def("Name", &Ship::Name)

        .def("SetModelName", &Ship::ModelName)
        .def("ModelName", &Ship::ModelName)
        .def("PluralModelName", &Ship::ModelName)
        .def("VariantName", &Ship::VariantName)
        .def("Noun", &Ship::Noun)
        .def("Description", &Ship::Description)
//        .def("Thumbnail", &Ship::Thumbnail)
        .def("Cost", &Ship::Cost)
        .def("ChassisCost", &Ship::ChassisCost)

        .def("FlightCheck", &Ship::FlightCheck)

        .def("SetPosition", &Ship::SetPosition)
        .def("Place", &Ship::Place)
        .def("SetName", &Ship::SetName)
//        .def("SetSystem", &Ship::SetSystem)
//        .def("SetPlanet", &Ship::SetPlanet)
//        .def("SetGovernment", &Ship::SetGovernment)
//        .def("SetIsSpecial", &Ship::SetIsSpecial)
        .def("IsSpecial", &Ship::IsSpecial)

        .def("SetIsYours", &Ship::SetIsYours)
        .def("IsYours", &Ship::IsYours)
        .def("SetIsParked", &Ship::SetIsParked)
        .def("IsParked", &Ship::IsParked)
        .def("SetDeployOrder", &Ship::SetDeployOrder)
        .def("HasDeployOrder", &Ship::HasDeployOrder)

//        .def("Personality", &Ship::Personality)
//        .def("SetPersonality", &Ship::SetPersonality)
//        .def("SetHail", &Ship::SetPersonality)
//        .def("GetHail", &Ship::GetHail)

//        .def("SetCommands", &Ship::SetCommands)
//        .def("Command", &Ship::Command)
//        .def("Move", &Ship::Move)
//        .def("DoGeneration", &Ship::DoGeneration)
//        .def("Launch", &Ship::Launch)
//        .def("Board", &Ship::Board)
//        .def("Scan", &Ship::Scan)
//        .def("CargoScanFraction", &Ship::CargoScanFraction)
//        .def("OutfitScanFraction", &Ship::OutfitScanFraction)

//        .def("Fire", &Ship::Fire)
//        .def("FireAntiMissile", &Ship::FireAntiMissile)

//        .def("GetSystem", &Ship::GetSystem)
//        .def("GetPlanet", &Ship::GetPlanet)

	.def("IsCapturable", &Ship::IsCapturable)
	.def("IsTargetable", &Ship::IsTargetable)
	.def("IsOverheated", &Ship::IsOverheated)
	.def("IsDisabled", &Ship::IsDisabled)
	.def("IsBoarding", &Ship::IsBoarding)
	.def("IsLanding", &Ship::IsLanding)
	.def("CanLand", &Ship::CanLand)
	.def("CannotAct", &Ship::CannotAct)
	.def("Cloaking", &Ship::Cloaking)
	.def("IsEnteringHyperspace", &Ship::IsEnteringHyperspace)
	.def("IsHyperspacing", &Ship::IsHyperspacing)
	.def("IsUsingJumpDrive", &Ship::IsUsingJumpDrive)
	.def("IsReadyToJump", &Ship::IsReadyToJump)
	.def("CustomSwizzle", &Ship::CustomSwizzle)

	.def("IsThrusting", &Ship::IsThrusting)
	.def("IsReversing", &Ship::IsReversing)
	.def("IsSteering", &Ship::IsSteering)
	.def("SteeringDirection", &Ship::SteeringDirection)
//	.def("EnginePoints", &Ship::EnginePoints)
//	.def("ReverseEnginePoints", &Ship::ReverseEnginePoints)
//	.def("SteeringEnginePoints", &Ship::SteeringEnginePoints)

        .def("Disable", &Ship::Disable)
        .def("Destroy", &Ship::Destroy)
        .def("SelfDestruct", &Ship::SelfDestruct)
        .def("Restore", &Ship::Restore)
        .def("IsDestroyed", &Ship::IsDestroyed)
        .def("Recharge", &Ship::Recharge)
        .def("CanRefuel", &Ship::CanRefuel)
        .def("TransferFuel", &Ship::TransferFuel)
//        .def("WasCaptured", &Ship::WasCaptured)

        .def("Shields", &Ship::Shields)
        .def("Hull", &Ship::Hull)
        .def("Fuel", &Ship::Fuel)
        .def("Energy", &Ship::Energy)
        .def("Heat", &Ship::Heat)
        .def("Health", &Ship::Health)
        .def("DisabledHull", &Ship::DisabledHull)
        .def("JumpsRemaining", &Ship::JumpsRemaining)
//        .def("JumpFuel", &Ship::JumpFuel)
        .def("JumpRange", &Ship::JumpRange)
        .def("HyperdriveFuel", &Ship::HyperdriveFuel)
        .def("JumpDriveFuel", &Ship::JumpDriveFuel)
        .def("JumpFuelMissing", &Ship::JumpFuelMissing)
        .def("IdleHeat", &Ship::IdleHeat)
        .def("HeatDissipation", &Ship::HeatDissipation)
        .def("MaximumHeat", &Ship::MaximumHeat)
        .def("CoolingEfficiency", &Ship::CoolingEfficiency)

        .def("Crew", &Ship::Crew)
        .def("RequiredCrew", &Ship::RequiredCrew)
        .def("AddCrew", &Ship::AddCrew)
        .def("CanBeFlagship", &Ship::CanBeFlagship)

        .def("Mass", &Ship::Mass)
        .def("TurnRate", &Ship::TurnRate)
        .def("Acceleration", &Ship::Acceleration)
        .def("MaxVelocity", &Ship::MaxVelocity)
        .def("MaxReverseVelocity", &Ship::MaxReverseVelocity)

        // there are about 40 more to fill in

        .def("Attributes", &Ship::Attributes)
        .def("BaseAttributes", &Ship::BaseAttributes)
        .def("Recharge", &Ship::Recharge);


        // Custom helpers could go here (in lowercase)


    // source/main
    m.def("main", [](std::vector<std::string> argVec) {
        // pybind11 doesn't do double pointers, so convert
        std::vector<char *> cstrs;
        cstrs.reserve(argVec.size() + 1);
        for (auto &s : argVec) {
            cstrs.push_back(const_cast<char *>(s.c_str()));
        }
        cstrs.push_back(NULL);
        return maine(argVec.size(), cstrs.data());
    });

    m.def("main_no_GIL", [](std::vector<std::string> argVec) {
        // pybind11 doesn't do double pointers, so convert
        std::vector<char *> cstrs;
        cstrs.reserve(argVec.size() + 1);
        for (auto &s : argVec) {
            cstrs.push_back(const_cast<char *>(s.c_str()));
        }
        cstrs.push_back(NULL);
        py::gil_scoped_release release;
        auto ret = maine(argVec.size(), cstrs.data());
        py::gil_scoped_acquire acquire;
        return ret;
    });

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
