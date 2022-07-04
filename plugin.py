#!/usr/bin/env python3
# Basic Python Plugin Example
#
# Author: GizMoCuz
#
"""
<plugin key="DomoticzFairlandModbus" name="Fairland Modbus" author="NijeboerFrank" version="0.1.0" wikilink="https://github.com/NijeboerFrank/DomoticzFairlandModbus/wiki">
    <description>
        <h2>Domoticz Fairland Modbus</h2><br/>
    </description>
    <params>
      <param field="Address" label="IP Address" />
      <param field="Port" label="Port Number" />
      <param field="Mode1" label="Pollrate" />
    </params>
</plugin>
"""
from typing import Callable

from pymodbus.client.common import ReadHoldingRegistersResponse, ReadInputRegistersResponse
import Domoticz
from pymodbus.client.sync import ModbusTcpClient

RUNNING_MODE_MAPPING = {
    0: "Smart",
    1: "Silent",
    2: "Super Silent",
    3: "Turbo",
}

OPTIONS = {
    "LevelNames": "Smart|Silent|Super Silent|Turbo",
    "LevelOffHidden": "true",
    "SelectorStyle": "1",
}


class FairlandModbusClient:

    def __init__(self, ip_address: str, port: int):
        self._client = ModbusTcpClient(host=ip_address, port=port)

    def get_outlet_temperature(self):
        Domoticz.Log("Getting Outlet Temp")
        return self.get_temp(4, self._client.read_input_registers)

    def get_inlet_temperature(self):
        Domoticz.Log("Getting Inlet Temp")
        return self.get_temp(3, self._client.read_input_registers)

    def get_ambient_temperature(self):
        Domoticz.Log("Getting Ambient Temp")
        return self.get_temp(5, self._client.read_input_registers)

    def get_heating_temperature(self):
        Domoticz.Log("Getting Heating Temp")
        return self.get_temp(3, self._client.read_holding_registers)

    def get_temp(self, address: int, function: Callable):
        response = function(address=address, count=1, unit=1)
        degree = ((response.registers[0] - 96) / 2) + 18
        return f"{degree}"

    def get_speed_percentage(self):
        Domoticz.Log("Getting Running Speed")
        response: ReadInputRegistersResponse = self._client.read_input_registers(address=0, count=1, unit=1)
        return f"{response.registers[0]}"

    def get_running_mode(self):
        Domoticz.Log("Getting running mode")
        response: ReadHoldingRegistersResponse = self._client.read_holding_registers(address=1, count=1, unit=1)
        return RUNNING_MODE_MAPPING.get(response.registers[0])


class BasePlugin:
    enabled = False

    def __init__(self):
        self._client = None
        return

    def onStart(self):
        Domoticz.Log("onStart called")

        try:
            pollrate = int(Parameters["Mode1"])
            Domoticz.Log(f"Setting pollrate to {pollrate}")
            Domoticz.Heartbeat(int(pollrate))
        except Exception as e:
            Domoticz.Log(f"Could not set pollrate because of exception '{e}'")

        self._client = FairlandModbusClient(ip_address=Parameters["Address"], port=Parameters["Port"])

        if len(Devices) == 0:
            Domoticz.Device(Name=f"Outlet Temperature", Unit=1, TypeName="Temperature", Used=1).Create()
            Domoticz.Device(Name=f"Inlet Temperature", Unit=2, TypeName="Temperature", Used=1).Create()
            Domoticz.Device(Name=f"Ambient Temperature", Unit=3, TypeName="Temperature", Used=1).Create()
            Domoticz.Device(Name=f"Heating Temperature", Unit=4, TypeName="Temperature", Used=1).Create()
            Domoticz.Device(Name=f"Running Speed", Unit=5, TypeName="Percentage", Used=1).Create()
            Domoticz.Device(Name=f"Running Mode", Unit=6, TypeName="Selector Switch", Options=OPTIONS, Image=7, Used=1).Create()

    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")

    def onMessage(self, Connection, Data):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

    def onHeartbeat(self):
        Domoticz.Log("onHeartbeat called")
        if len(Devices) == 0:
            Domoticz.Log("Could not update because devices list is 0")
            return

        if self._client is None:
            Domoticz.Log("Could not update values, because ModbusClient is not initialized")
            return

        Devices[1].Update(nValue=0, sValue=self._client.get_outlet_temperature())
        Devices[2].Update(nValue=0, sValue=self._client.get_inlet_temperature())
        Devices[3].Update(nValue=0, sValue=self._client.get_ambient_temperature())
        Devices[4].Update(nValue=0, sValue=self._client.get_heating_temperature())
        Devices[5].Update(nValue=0, sValue=self._client.get_speed_percentage())
        Devices[6].Update(nValue=0, sValue=self._client.get_running_mode())

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return
