import adbutils
import unidecode

import re
import time
import requests
import json

import xml.etree.ElementTree as ET

adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
device = adb.device()

def get_ui():
    device.shell("uiautomator dump -x")
    device.sync.pull("/sdcard/window_dump.xml","tree.xml")
    mytree = ET.parse("./tree.xml")
    # print(mytree.getroot())
    trees = list(mytree.iter())
    return trees

def get_screen_size():
    screen_size = device.shell("wm size")
    screen = screen_size.split("x")
    for a in range(len(screen)):
        # print(screen[a])
        screen[a] = re.sub(r"\D", "", screen[a])
        # print(screen[a])
    display_width = int(screen[0])
    display_height = int(screen[1])
    return display_width, display_height

def find_element( obj, key, value, is_coord=True):
    for a in range(len(obj)):
        list_object = list(obj[a].attrib.values())
        for b in range(len(list_object)):
            if key in list_object[b]:
                # print(obj[a].attrib)
                if is_coord :
                    return obj[a].attrib["bounds"]
                else :
                    return obj[a].attrib[value]
    return False

def find_elements(obj, key, value, is_coord=True):
    result = []
    for a in range(len(obj)):
        list_object = list(obj[a].attrib.values())
        for b in range(len(list_object)):
            if key in list_object[b]:
                # print(obj[a].attrib)
                if is_coord :
                    result.append(obj[a].attrib["bounds"])
                else :
                    result.append(obj[a].attrib[value])
    return result

def tap(element_coord, tap_position=5):
    target_coordinates = re.split("\W",element_coord)
    stripped_coordinates = ' '.join(target_coordinates).split()
    if isinstance(stripped_coordinates, list) :
        x1, y1, x2, y2 = int(stripped_coordinates[0]), int(stripped_coordinates[1]), int(stripped_coordinates[2]), int(stripped_coordinates[3])
        if tap_position == 1 :
            target = [x1,y1]
        elif tap_position == 2 :
            target = [x1+(x2-x1/2),y1]
        elif tap_position == 3 :
            target = [x2,y1]
        elif tap_position == 4 :
            target = [x1,y1+(y2-y1)/2]
        elif tap_position == 5 :
            target = [x1+(x2-x1)/2,y1+(y2-y1)/2]
        elif tap_position == 6 :
            target = [x2,y1+(y2-y1)/2]
        elif tap_position == 7 :
            target = [x1,y2]
        elif tap_position == 8 :
            target = [x1+(x2-x1)/2,y2]
        elif tap_position == 9 :
            target = [x2,y2]
        # print(target)
        device.shell("input tap " + str(target[0]) + " " + str(target[1]))
    else :
        print("Element's coordinate is not valid.")

def close_keyboard():
    if "mInputShown=true" in device.shell("dumpsys input_method") :
        print("Keyboard shown up Closing")
        print(device.shell("input keyevent 111"))
    else :
        print("Keyboard hidden.")

def type(words, enter=False):
    words = unidecode.unidecode(words)
    print(device.shell('input text "' + str(words) +'"' ))
    if enter==True:
        device.shell('input keyevent "KEYCODE_ENTER"' )

def back():
    device.shell('input keyevent "KEYCODE_BACK"' )

def swipe(start_point, end_point, dur=500, multiply=1):
    # print(start_point)
    # print(end_point)
    # print(dur)
    for a in range(0,multiply):
        device.shell("input swipe " + str(start_point[0]) + " " + str(start_point[1]) + " " + str(end_point[0]) + " " + str(end_point[1]) + " " + str(dur))
