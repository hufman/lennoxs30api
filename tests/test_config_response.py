from lennoxs30api.s30api_async import (
    LENNOX_HVAC_COOL,
    LENNOX_HVAC_HEAT,
    LENNOX_HVAC_HEAT_COOL,
    LENNOX_HVAC_OFF,
    lennox_zone,
    s30api_async,
    lennox_system,
)
from lennoxs30api.lennox_home import lennox_home

import json
import os


def setup_load_configuration() -> s30api_async:
    script_dir = os.path.dirname(__file__) + "/messages/"
    file_path = os.path.join(script_dir, "login_response.json")
    with open(file_path) as f:
        data = json.load(f)

    api = s30api_async("myemail@email.com", "mypassword", None)
    api.process_login_response(data)

    file_path = os.path.join(script_dir, "config_response_system_01.json")
    with open(file_path) as f:
        data = json.load(f)
    api.processMessage(data)

    file_path = os.path.join(script_dir, "config_response_system_02.json")
    with open(file_path) as f:
        data = json.load(f)
    api.processMessage(data)
    return api


def test_process_configuration_message():
    api = setup_load_configuration()

    lsystem: lennox_system = api.getSystems()[0]
    assert lsystem.sysId == "0000000-0000-0000-0000-000000000001"
    assert lsystem.productType == "S30"
    assert lsystem.name == "Moetown North"
    assert lsystem.numberOfZones == 4
    assert lsystem.outdoorTemperature == 80
    assert lsystem.outdoorTemperatureC == 27
    assert lsystem.temperatureUnit == "F"
    assert lsystem.indoorUnitType == "furnace"
    assert lsystem.outdoorUnitType == "air conditioner"
    assert lsystem.diagPoweredHours == 40950
    assert lsystem.diagRuntime == 15605
    assert lsystem.diagVentilationRuntime == 0
    assert lsystem.diagLevel == 0
    assert lsystem.humidifierType == "none"
    assert lsystem.ventilationUnitType == "ventilator"
    assert lsystem.supports_ventilation() == True
    assert lsystem.ventilationControlMode == "timed"
    assert lsystem.feelsLikeMode == False
    assert lsystem.ventilatingUntilTime == ""
    assert lsystem.manualAwayMode == False == lsystem.get_manual_away_mode()

    zones = lsystem.getZoneList()
    assert len(zones) == 4

    zone_1: lennox_zone = zones[0]

    assert zone_1.name == "Zone 1"
    assert zone_1.id == 0
    assert zone_1.coolingOption == True
    assert zone_1.csp == 77 == zone_1.getCoolSP()
    assert zone_1.dehumidificationOption == True
    assert zone_1.desp == 50
    assert zone_1.emergencyHeatingOption == False
    assert zone_1.fanMode == "auto" == zone_1.getFanMode()
    assert zone_1.heatingOption == True
    assert zone_1.hsp == 64 == zone_1.getHeatSP()
    assert zone_1.hspC == 18
    assert zone_1.humOperation == "off"
    assert zone_1.humidificationOption == False
    assert zone_1.humidity == 28 == zone_1.getHumidity()
    assert zone_1.humidityMode == "dehumidify"
    assert zone_1.husp == 40
    assert zone_1.maxCsp == 99
    assert zone_1.maxCspC == 37
    assert zone_1.minCsp == 60
    assert zone_1.minCspC == 15.5
    assert zone_1.maxHsp == 90
    assert zone_1.maxHspC == 32
    assert zone_1.minHsp == 40
    assert zone_1.minHspC == 4.5
    assert zone_1.sp == 73
    assert zone_1.spC == 22.5

    assert zone_1.maxDehumSp == 60
    assert zone_1.scheduleId == 16 == zone_1.getManualModeScheduleId()
    assert zone_1.systemMode == LENNOX_HVAC_HEAT == zone_1.getSystemMode()
    assert zone_1.tempOperation == "off"
    assert zone_1.temperature == 79 == zone_1.getTemperature()
    assert zone_1.temperatureC == 26 == zone_1.getTemperatureC()
    assert zone_1._system.sysId == "0000000-0000-0000-0000-000000000001"

    assert zone_1.getTargetTemperatureF() == zone_1.hsp
    assert zone_1.getTargetTemperatureC() == zone_1.hspC
    lsystem.single_setpoint_mode = True
    assert zone_1.getTargetTemperatureF() == zone_1.sp
    assert zone_1.getTargetTemperatureC() == zone_1.spC
    lsystem.single_setpoint_mode = False

    zone_1.systemMode = LENNOX_HVAC_COOL
    assert zone_1.getTargetTemperatureF() == zone_1.csp
    assert zone_1.getTargetTemperatureC() == zone_1.cspC
    lsystem.single_setpoint_mode = True
    assert zone_1.getTargetTemperatureF() == zone_1.sp
    assert zone_1.getTargetTemperatureC() == zone_1.spC
    lsystem.single_setpoint_mode = False

    zone_1.systemMode = LENNOX_HVAC_OFF
    assert zone_1.getTargetTemperatureF() == None
    assert zone_1.getTargetTemperatureC() == None
    lsystem.single_setpoint_mode = True
    assert zone_1.getTargetTemperatureF() == None
    assert zone_1.getTargetTemperatureC() == None
    lsystem.single_setpoint_mode = False

    zone_1.systemMode = LENNOX_HVAC_HEAT_COOL
    assert zone_1.getTargetTemperatureF() == None
    assert zone_1.getTargetTemperatureC() == None
    lsystem.single_setpoint_mode = True
    assert zone_1.getTargetTemperatureF() == zone_1.sp
    assert zone_1.getTargetTemperatureC() == zone_1.spC
    lsystem.single_setpoint_mode = False

    zone_1.systemMode = LENNOX_HVAC_HEAT

    zone_2: lennox_zone = zones[1]

    assert zone_2.name == "Zone 2"
    assert zone_2.id == 1
    assert zone_2.coolingOption == True
    assert zone_2.csp == 78 == zone_2.getCoolSP()
    assert zone_2.dehumidificationOption == True
    assert zone_2.desp == 50
    assert zone_2.emergencyHeatingOption == False
    assert zone_2.fanMode == "auto" == zone_2.getFanMode()
    assert zone_2.heatingOption == True
    assert zone_2.hsp == 69
    assert zone_2.humOperation == "off"
    assert zone_2.humidificationOption == False
    assert zone_2.humidity == 28 == zone_2.getHumidity()
    assert zone_2.humidityMode == "dehumidify"
    assert zone_2.husp == 40
    assert zone_2.maxCsp == 99
    assert zone_2.maxDehumSp == 60
    assert zone_2.maxHsp == 90
    assert zone_2.maxHumSp == 45
    assert zone_2.minCsp == 60
    assert zone_2.minHsp == 40
    assert zone_2.scheduleId == 17 == zone_2.getManualModeScheduleId()
    assert zone_2.sp == 73
    assert zone_2.spC == 23
    assert zone_2.systemMode == "cool" == zone_2.getSystemMode()
    assert zone_2.tempOperation == "off"
    assert zone_2.temperature == 78 == zone_2.getTemperature()
    assert zone_2.temperatureC == 25.5 == zone_2.getTemperatureC()
    assert zone_2._system.sysId == "0000000-0000-0000-0000-000000000001"

    zone_3: lennox_zone = zones[2]

    assert zone_3.name == "Zone 3"
    assert zone_3.id == 2
    assert zone_3.coolingOption == True
    assert zone_3.csp == 71 == zone_3.getCoolSP()
    assert zone_3.dehumidificationOption == True
    assert zone_3.desp == 50
    assert zone_3.emergencyHeatingOption == False
    assert zone_3.fanMode == "auto" == zone_3.getFanMode()
    assert zone_3.heatingOption == True
    assert zone_3.hsp == 40 == zone_3.getHeatSP()
    assert zone_3.humOperation == "off"
    assert zone_3.humidificationOption == False
    assert zone_3.humidity == 28 == zone_3.getHumidity()
    assert zone_3.humidityMode == "dehumidify"
    assert zone_3.husp == 40
    assert zone_3.maxCsp == 99
    assert zone_3.maxDehumSp == 60
    assert zone_3.maxHsp == 90
    assert zone_3.maxHumSp == 45
    assert zone_3.minCsp == 60
    assert zone_3.minHsp == 40
    assert zone_3.scheduleId == 18 == zone_3.getManualModeScheduleId()
    assert zone_3.sp == 73
    assert zone_3.spC == 23
    assert zone_3.systemMode == "cool" == zone_3.getSystemMode()
    assert zone_3.tempOperation == "cooling"
    assert zone_3.temperature == 71 == zone_3.getTemperature()
    assert zone_3._system.sysId == "0000000-0000-0000-0000-000000000001"

    zone_4: lennox_zone = zones[3]
    assert zone_4.name == "Zone 4"
    assert zone_4.id == 3
    assert zone_4.coolingOption == True
    assert zone_4.csp == 72 == zone_4.getCoolSP()
    assert zone_4.dehumidificationOption == True
    assert zone_4.desp == 50
    assert zone_4.emergencyHeatingOption == False
    assert zone_4.fanMode == "auto" == zone_4.getFanMode()
    assert zone_4.heatingOption == True
    assert zone_4.hsp == 64 == zone_4.getHeatSP()
    assert zone_4.humOperation == "off"
    assert zone_4.humidificationOption == False
    assert zone_4.humidity == 28 == zone_4.getHumidity()
    assert zone_4.humidityMode == "dehumidify"
    assert zone_4.husp == 40
    assert zone_4.maxCsp == 99
    assert zone_4.maxDehumSp == 60
    assert zone_4.maxHsp == 90
    assert zone_4.maxHumSp == 45
    assert zone_4.minCsp == 60
    assert zone_4.minHsp == 40
    assert zone_4.scheduleId == 19 == zone_4.getManualModeScheduleId()
    assert zone_4.sp == 73
    assert zone_4.spC == 23
    assert zone_4.systemMode == "off" == zone_4.getSystemMode()
    assert zone_4.tempOperation == "off"
    assert zone_4.temperature == 76 == zone_4.getTemperature()
    assert zone_4._system.sysId == "0000000-0000-0000-0000-000000000001"

    lsystem: lennox_system = api.getSystems()[1]
    assert lsystem.sysId == "0000000-0000-0000-0000-000000000002"
    assert lsystem.productType == "S30"
    assert lsystem.name == "South Moetown"
    assert lsystem.numberOfZones == 1
    assert lsystem.outdoorTemperature == 97
    assert lsystem.outdoorTemperatureC == 36
    assert lsystem.temperatureUnit == "F"
    assert lsystem.indoorUnitType == "furnace"
    assert lsystem.outdoorUnitType == "air conditioner"
    assert lsystem.diagPoweredHours == 41071
    assert lsystem.diagRuntime == 5884
    assert lsystem.humidifierType == "none"
    assert lsystem.ventilationUnitType == "none"
    assert lsystem.manualAwayMode == True == lsystem.get_manual_away_mode()

    zone_5: lennox_zone = lsystem.getZoneList()[0]
    assert zone_5.name == "Zone 1"
    assert zone_5.id == 0
    assert zone_5.coolingOption == True
    assert zone_5.csp == 78 == zone_5.getCoolSP()
    assert zone_5.dehumidificationOption == True
    assert zone_5.desp == 50
    assert zone_5.emergencyHeatingOption == False
    assert zone_5.fanMode == "auto" == zone_5.getFanMode()
    assert zone_5.heatingOption == True
    assert zone_5.hsp == 68 == zone_5.getHeatSP()
    assert zone_5.humOperation == "off"
    assert zone_5.humidificationOption == False
    assert zone_5.humidity == 30 == zone_5.getHumidity()
    assert zone_5.humidityMode == "off"
    assert zone_5.husp == 40
    assert zone_5.maxCsp == 99
    assert zone_5.maxDehumSp == 60
    assert zone_5.maxHsp == 90
    assert zone_5.maxHumSp == 45
    assert zone_5.minCsp == 60
    assert zone_5.minHsp == 40
    assert zone_5.scheduleId == 16 == zone_5.getManualModeScheduleId()
    assert zone_5.sp == 73
    assert zone_5.spC == 22.5
    assert zone_5.systemMode == "off" == zone_5.getSystemMode()
    assert zone_5.tempOperation == "off"
    assert zone_5.temperature == 79 == zone_5.getTemperature()
    assert zone_5._system.sysId == "0000000-0000-0000-0000-000000000002"
