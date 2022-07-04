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
    </params>
</plugin>
"""
import Domoticz


class BasePlugin:
    enabled = False

    def __init__(self):
        return

    def onStart(self):
        Domoticz.Log("onStart called")

        if len(Devices) == 0:
            Domoticz.Device(Name=f"{Parameters['Name']} - Outlet Temperature", Unit=1, TypeName="Temperature", Used=1).Create()
            Domoticz.Device(Name=f"{Parameters['Name']} - Inlet Temperature", Unit=2, TypeName="Temperature", Used=1).Create()
            Domoticz.Device(Name=f"{Parameters['Name']} - Ambient Temperature", Unit=3, TypeName="Temperature", Used=1).Create()
            Domoticz.Device(Name=f"{Parameters['Name']} - Heating Temperature", Unit=4, TypeName="Temperature", Used=1).Create()

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

        Devices[1].Update(nValue=0, sValue="35.0")
        Devices[2].Update(nValue=0, sValue="40.0")
        Devices[3].Update(nValue=0, sValue="17.0")
        Devices[4].Update(nValue=0, sValue="19.0")

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
