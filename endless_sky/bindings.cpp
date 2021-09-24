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
#include "endless-sky/source/Account.h"
#include "endless-sky/source/Angle.h"
#include "endless-sky/source/CaptureOdds.h"
#include "endless-sky/source/Color.h"
#include "endless-sky/source/ConditionSet.h"
#include "endless-sky/source/Conversation.h"
#include "endless-sky/source/CoreStartData.h"
#include "endless-sky/source/DataNode.h"
#include "endless-sky/source/DataFile.h"
#include "endless-sky/source/DataWriter.h"
#include "endless-sky/source/Date.h"
#include "endless-sky/source/GameData.h"
#include "endless-sky/source/Galaxy.h"
#include "endless-sky/source/Government.h"
#include "endless-sky/source/Outfit.h"
#include "endless-sky/source/Planet.h"
#include "endless-sky/source/PlayerInfo.h"
#include "endless-sky/source/Point.h"
#include "endless-sky/source/Random.h"
#include "endless-sky/source/SavedGame.h"
#include "endless-sky/source/Set.h"
#include "endless-sky/source/Ship.h"
#include "endless-sky/source/System.h"
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
        .def("Get", py::overload_cast<const std::string&>(&Class::Get, py::const_), py::return_value_policy::reference)
        .def("__getitem__", py::overload_cast<const std::string&>(&Class::Get, py::const_), py::return_value_policy::reference)
        .def("Get_mutable", py::overload_cast<const std::string&>(&Class::Get))
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

    // source/Account
    py::class_<Account>(m, "Account")
        .def(py::init<>())
        .def("Load", &Account::Load)
        .def("Save", &Account::Save)
        .def("Credits", &Account::Credits)
        .def("AddCredits", &Account::AddCredits)
        .def("PayExtra", &Account::PayExtra)

        .def("Step", &Account::Step)
        .def("SalariesOwed", &Account::SalariesOwed)
        .def("PaySalaries", &Account::PaySalaries)
        .def("MaintenanceDue", &Account::MaintenanceDue)
        .def("PayMaintenance", &Account::PayMaintenance)

        //.def("Mortgages", &Account::Mortgages)
        .def("AddMortgage", &Account::AddMortgage)
        .def("AddFine", &Account::AddFine)
        .def("Prequalify", &Account::Prequalify)
        .def("NetWorth", &Account::NetWorth)

        .def("CreditScore", &Account::CreditScore)
        .def("TotalDebt", &Account::TotalDebt);

    // source/AI

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

    // source/Armament
    // source/AsteroidField
    // source/Audio

    // source/CaptureOdds
    py::class_<CaptureOdds>(m, "CaptureOdds")
        .def(py::init<Ship&, Ship&>())
        .def("Odds", &CaptureOdds::Odds)
        .def("AttackerCasualties", &CaptureOdds::AttackerCasualties)
        .def("DefenderCasualties", &CaptureOdds::DefenderCasualties)
        .def("AttackerPower", &CaptureOdds::AttackerPower)
        .def("DefenderPower", &CaptureOdds::DefenderPower);

    // source/CargoHold

    // source/Color
    py::class_<Color>(m, "Color")
        .def(py::init<float,float>())
        .def(py::init<float,float,float,float>())
        .def("Load", &Color::Load)
        .def("Get", &Color::Get)
        .def("Opaque", &Color::Opaque)
        .def("Transparent", &Color::Transparent)
        .def("Additive", &Color::Additive)
        .def("Combine", &Color::Combine);

    // source/Command

    // source/ConditionSet
    py::class_<ConditionSet>(m, "ConditionSet");
    // missing many methods

    // source/Conversation
    py::class_<Conversation>(m, "Conversation");
    // missing many methods

    // source/CoreStartData
    py::class_<CoreStartData>(m, "CoreStartData");
    // missing many methods

    // source/DataFile
    py::class_<DataFile>(m, "DataFile")
        .def(py::init<>())
        .def(py::init<std::string&>())
        .def("Load", py::overload_cast<const std::string&>(&DataFile::Load))
        .def("__iter__", [](DataFile &f) {
            return py::make_iterator(f.begin(), f.end());
        }, py::keep_alive<0, 1>()); // TODO is this keep_alive policy right?
                                    // It means "keep this (the DataFile) alive for
                                    // at least as long as the return value (the iterator)

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

    // source/DataWriter
    py::class_<DataWriter>(m, "DataWriter")
        .def(py::init<std::string&>())
        .def("Write", [](DataWriter &w, const DataNode &node) {
            return w.Write(node);
        })
        .def("Write", [](DataWriter &w) {
            return w.Write();
        })

        .def("BeginChild", &DataWriter::BeginChild)
        .def("WriteComment", &DataWriter::WriteComment)
        .def("WriteToken", [](DataWriter &w, const double &a) {
            return w.WriteToken(a);
        })
        .def("WriteToken", [](DataWriter &w, const int &a) {
            return w.WriteToken(a);
        })
        .def("WriteToken", [](DataWriter &w, const std::string &a) {
            return w.WriteToken(a);
        });

    // source/Date
    py::class_<Date>(m, "Date")
        .def(py::init<>())
        .def(py::init<int,int,int>())
        .def("LongString", &Date::LongString)
        .def("inc", [](Date &d) { d++; })
        .def(py::self + int())
        .def(py::self - py::self)
        .def(py::self < py::self)
        .def(py::self <= py::self)
        .def(py::self > py::self)
        .def(py::self >= py::self)
        .def(py::self == py::self)
        .def(py::self != py::self)
        .def("DaysSinceEpoch", &Date::DaysSinceEpoch)
        .def("Day", &Date::Day)
        .def("Month", &Date::Month)
        .def("Year", &Date::Year);

    // source/Depreciation
    // source/Dialog

    // source/Dictionary
    py::class_<Dictionary>(m, "Dictionary")
        .def(py::init<>())
        .def("__iter__", [](Dictionary &d) {
            return py::make_iterator(d.begin(), d.end());
        }, py::keep_alive<0, 1>())
        .def("Get", py::overload_cast<const std::string&>(&Dictionary::Get, py::const_))
        .def("__getitem__", py::overload_cast<const std::string&>(&Dictionary::Get, py::const_));

    // source/Engine
    // source/Files
    // source/Fleet
    // source/Engine
    // source/Galaxy
    py::class_<Galaxy>(m, "Galaxy")
        .def(py::init<>())
        .def("Load", &Galaxy::Load)
        .def("Position", &Galaxy::Position);
        //.def("load", &Galaxy::GetSprite)

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
	.def_static("Ships", &GameData::Ships, py::return_value_policy::reference)
	.def_static("Governments", &GameData::Governments, py::return_value_policy::reference)
	.def_static("Outfits", &GameData::Outfits, py::return_value_policy::reference)
	.def_static("Planets", &GameData::Planets, py::return_value_policy::reference)
	.def_static("Systems", &GameData::Systems, py::return_value_policy::reference);

    // source/GameEvent
    // source/GameWindow

    // source/Government
    py::class_<Government, std::shared_ptr<Government>>(m, "Government")
        .def(py::init<>())
        .def("Load", &Government::Load)
        .def("GetName", &Government::GetName)
        .def("SetName", &Government::SetName)
        .def("GetTrueName", &Government::GetTrueName)
        .def("GetSwizzle", &Government::GetSwizzle)
        .def("GetColor", &Government::GetColor)

        .def("AttitudeToward", &Government::AttitudeToward)
        .def("InitialPlayerReputation", &Government::InitialPlayerReputation)
        .def("PenaltyFor", &Government::PenaltyFor)
        .def("GetBribeFraction", &Government::GetBribeFraction)
        .def("GetFineFraction", &Government::GetFineFraction)

        .def("CanEnforce", py::overload_cast<const System*>(&Government::CanEnforce, py::const_))
        .def("CanEnforce", py::overload_cast<const Planet*>(&Government::CanEnforce, py::const_))
        .def("DeathSentence", &Government::DeathSentence)

        .def("GetHail", &Government::GetHail)
        .def("Language", &Government::Language)
        .def("RaidFleet", &Government::RaidFleet)

        .def("IsEnemy", py::overload_cast<const Government*>(&Government::IsEnemy, py::const_))
        .def("IsEnemy", py::overload_cast<>(&Government::IsEnemy, py::const_ ))
        .def("IsPlayer", &Government::IsPlayer)
        .def("Offend", &Government::Offend)
        .def("Bribe", &Government::Bribe)
        .def("GetHail", &Government::GetHail)
        .def("Fine", &Government::Fine)
        .def("Reputation", &Government::Reputation)
        .def("SetReputation", &Government::SetReputation)
        .def("CrewAttack", &Government::CrewAttack)
        .def("CrewDefense", &Government::CrewDefense);

    // source/Hardpoint
    // source/Hazard
    // source/LocationFilter

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

    // source/Messages
    // source/Minable
    // source/Mission
    // source/MissionAction
    // source/Mortgage
    // source/News
    // source/NPC

    // source/Outfit
    py::class_<Outfit, std::shared_ptr<Outfit>>(m, "Outfit")
        .def(py::init<>())
        .def("Load", &Outfit::Load)
        .def("Name", &Outfit::Name)
        .def("Attributes", &Outfit::Attributes);

    // source/Person
    // source/Personality
    // source/Phrase
    py::class_<Phrase>(m, "Phrase")
        .def(py::init<>())
        .def("Load", &Phrase::Load)
        .def("IsEmpty", &Phrase::IsEmpty)
        .def("Name", &Phrase::Name)
        .def("Get", &Phrase::Get);

    // source/Planet
    py::class_<Planet, std::shared_ptr<Planet>>(m, "Planet")
        // TODO add a constructor that takes data?
        .def("Load", &Planet::Load)
        .def("IsValid", &Planet::IsValid)
        .def("Name", &Planet::Name)
        .def("SetName", &Planet::SetName)
        .def("TrueName", &Planet::TrueName)
        .def("Description", &Planet::Description)
//        .def("Landscape", &Planet::Landscape)
        .def("MusicName", &Planet::MusicName)
        .def("Attributes", &Planet::Attributes)
        .def("Noun", &Planet::Noun)

        .def("HasSpaceport", &Planet::HasSpaceport)
        .def("SpaceportDescription", &Planet::SpaceportDescription)
        .def("HasShipyard", &Planet::HasShipyard)
        .def("Shipyard", &Planet::Shipyard)
        .def("Outfitter", &Planet::Outfitter)

        .def("Government", &Planet::GetGovernment, py::return_value_policy::reference)
        .def("RequiredReputation", &Planet::RequiredReputation)
        .def("GetBribeFraction", &Planet::GetBribeFraction)
        .def("Security", &Planet::Security)
        .def("GetSystem", &Planet::GetSystem, py::return_value_policy::reference)
        .def("IsInSystem", [](Planet &p, const System *s) { return p.IsInSystem(s); } )
        .def("IsInSystemOrig", &Planet::IsInSystem)
        .def("SetSystem", &Planet::SetSystem)
        .def("RemoveSystem", &Planet::RemoveSystem)

        .def("IsWormhole", &Planet::IsWormhole)
        .def("WormholeSource", &Planet::WormholeSource)
        .def("WormholeDestination", &Planet::WormholeDestination)
        .def("WormholeSystems", &Planet::WormholeSystems)

        .def("IsAccessible", &Planet::IsAccessible)
        .def("IsUnrestricted", &Planet::IsUnrestricted)

        .def("HasFuelFor", &Planet::HasFuelFor)
        .def("CanLand", py::overload_cast<>(&Planet::CanLand, py::const_))
        .def("CanLand", py::overload_cast<const Ship&>(&Planet::CanLand, py::const_))
        .def("CanUseServices", &Planet::CanUseServices)
        .def("Bribe", &Planet::Bribe)

        .def("DemandTribute", &Planet::DemandTribute)
        .def("DeployDefense", &Planet::DeployDefense)
        .def("ResetDefense", &Planet::ResetDefense);

    // source/PlayerInfo
    py::class_<PlayerInfo, std::shared_ptr<PlayerInfo>>(m, "PlayerInfo")
        .def("Ships", &PlayerInfo::Ships)
        .def_static("CurrentPlayer", &PlayerInfo::CurrentPlayer);
    // lots of missing methods

    // source/Point
    py::class_<Point>(m, "Point")
        .def(py::init<double,double>())
        .def_property_readonly("X", py::overload_cast<>(&Point::X, py::const_))
        .def_property_readonly("Y", py::overload_cast<>(&Point::Y, py::const_))
        .def("Unit", &Point::Unit);

    // source/Politics
    // source/Preferences
    // source/Projectile
    // source/Radar

    // source/Random
    m.def("RandomSeed", &Random::Seed);
    m.def("RandomInt", py::overload_cast<>(&Random::Int));
    m.def("RandomInt", py::overload_cast<uint32_t>(&Random::Int));

    // source/Sale

    // source/Set
    std::string shipString = std::string("Ship");
    declare_set<Ship>(m, shipString);
    std::string governmentString = std::string("Government");
    declare_set<Government>(m, governmentString);
    std::string outfitString = std::string("Outfit");
    declare_set<Outfit>(m, outfitString);
    std::string planetString = std::string("Planet");
    declare_set<Planet>(m, planetString);
    std::string systemString = std::string("System");
    declare_set<System>(m, systemString);

    // source/SavedGame
    py::class_<SavedGame, std::shared_ptr<SavedGame>>(m, "SavedGame")
        .def(py::init<>())
        .def(py::init<const std::string&>())
        .def("Load", &SavedGame::Load)
        .def("Path", &SavedGame::Path)
        .def("IsLoaded", &SavedGame::IsLoaded)
        .def("Clear", &SavedGame::Clear)
        .def("Name", &SavedGame::Name)
        .def("Credits", &SavedGame::Credits)

        .def("GetSystem", &SavedGame::GetSystem)
        .def("GetPlanet", &SavedGame::GetPlanet)
        .def("GetPlayTime", &SavedGame::GetPlayTime)

//        .def("ShipSprite", &SavedGame::ShipSprite)
        .def("ShipName", &SavedGame::ShipName);

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
        .def("SetSystem", &Ship::SetSystem)
        .def("SetPlanet", &Ship::SetPlanet)
        .def("SetGovernment", &Ship::SetGovernment)
        .def("SetIsSpecial", &Ship::SetIsSpecial)
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
        .def("Board", &Ship::Board)
        .def("Scan", &Ship::Scan)
        .def("CargoScanFraction", &Ship::CargoScanFraction)
        .def("OutfitScanFraction", &Ship::OutfitScanFraction)

//        .def("Fire", &Ship::Fire)
//        .def("FireAntiMissile", &Ship::FireAntiMissile)

        .def("GetSystem", &Ship::GetSystem)
        .def("GetPlanet", &Ship::GetPlanet)

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
        .def("JumpFuel", &Ship::JumpFuel)
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

    // source/ShipEvent
    // source/ShipInfoDisplay
    // source/Sound
    // source/Sprite
    // source/StartConditions
    // source/StellarObject

    // source/System
    py::class_<System, std::shared_ptr<System>>(m, "System")
        .def("Load", &System::Load)
        .def("UpdateSystem", &System::UpdateSystem)

        .def("Link", &System::Link)
        .def("Unlink", &System::Unlink)

        .def("IsValid", &System::IsValid)
        .def("Name", &System::Name)
        .def("SetName", &System::SetName)
        .def("Position", &System::Position)
        .def("GetGovernment", &System::GetGovernment, py::return_value_policy::reference)
        .def("MusicName", &System::MusicName)

        .def("Attributes", &System::Attributes)

        .def("Links", &System::Links)
        .def("JumpNeighbors", &System::JumpNeighbors)
        .def("Hidden", &System::Hidden)
        .def("ExtraHyperArrivalDistance", &System::ExtraHyperArrivalDistance)
        .def("ExtraJumpArrivalDistance", &System::ExtraJumpArrivalDistance)
        .def("VisibleNeighbors", &System::VisibleNeighbors)

        .def("SetDate", &System::SetDate)
//        .def("Objects", &System::Objects)
        .def("FindStellar", &System::SetDate)
        .def("HabitableZone", &System::HabitableZone)
        .def("AsteroidBelt", &System::AsteroidBelt)
        .def("JumpRange", &System::JumpRange)
        .def("SolarPower", &System::SolarPower)
        .def("SolarWind", &System::SolarWind)
        .def("IsInhabited", &System::IsInhabited)
        .def("HasFuelFor", &System::HasFuelFor)
        .def("HasShipyard", &System::HasShipyard)
        .def("HasOutfitter", &System::HasOutfitter)

        .def("Asteroids", &System::Asteroids)
//        .def("Haze", &System::Haze)

        .def("Trade", &System::Trade)
        .def("HasTrade", &System::HasTrade)

        .def("StepEconomy", &System::StepEconomy)
        .def("SetSupply", &System::SetSupply)
        .def("Supply", &System::Supply)
        .def("Exports", &System::Exports)

//        .def("Fleets", &System::Fleets)
//        .def("Hazards", &System::Hazards)
        .def("Danger", &System::Danger);

    // source/Test
    // source/TestData
    // source/Trade
    // source/Sysasdftem
    // source/Weapon
    // source/Weather


#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
