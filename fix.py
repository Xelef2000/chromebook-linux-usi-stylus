#!/usr/bin/env python3

import argparse
import configparser
import sys
import pyudev
from pathlib import Path



def parse_hw_id(stylus_id : str) -> str:
    res = stylus_id.split(" ")[1]
    res = res.lower()
    
    return "i2c:" + res


def path_exists(path_str: str) -> bool:
    return Path(path_str).exists()

def terminate(meassage : str) -> None:
    print(meassage, file=sys.stderr)
    exit(1)


def render_tablet_file(stylus_id : str) -> str:
    
    file = """[Device]
Name={}
ModelName=
DeviceMatch={}
Class=ISDV4
Width=11
Height=7
IntegratedIn=Display;System
#Styli=isdv4-aes
Styli=@generic-no-eraser

[Features]
Stylus=true
Touch=false""".format(stylus_id, parse_hw_id(stylus_id))
    return file


def render_quirk(device:str) -> str:
    file = """[Google Chromebook {} Stylus Digitizer]
MatchUdevType=tablet
MatchDeviceTree=*{}*
MatchBus=i2c
ModelChromebook=1
AttrPressureRange=1100:1000""".format(device.title(), device)
    return file



def get_board() -> str:
    # x86: Get the board name from dmi
    if path_exists("/sys/devices/virtual/dmi/id/"): 
        with open("/sys/devices/virtual/dmi/id/product_name", "r") as dmi:
            device_board = dmi.read()
    # arm: Get board name from CrOS HWID
    if path_exists("/sys/firmware/devicetree/base/"):
        with open("/sys/firmware/devicetree/base/firmware/chromeos/hardware-id", "r") as hwid:
            device_board = hwid.read().split(" ")[0].split("-")[0]

    return device_board.lower().strip()


def starts_with_safe(input : str, selection : str) -> bool:
    if not isinstance(input, str):
        return False
    else:
        return input.startswith(selection)


def get_stylus() -> str:
    context = pyudev.Context()
    for device in context.list_devices(subsystem="input"):
        if starts_with_safe(device.device_node,"/dev/input/event") and device.get("ID_INPUT_TABLET", 0):
            name = device.get("NAME", None)
            if name is None:
                name = next((p.get("NAME") for p in device.ancestors if p.get("NAME")),None,)
            
            if name is not None:
                return name.replace("\"","")


    terminate("No Stylus found")







def main():
    print(render_tablet_file(get_stylus()))
    print(render_quirk(get_board()))



if __name__ == "__main__":
    main()