#!/bin/env python3

# As you can see, Python isn't my main language

import os
import time
import requests
import sounddevice as sd
import numpy as np
from dotenv import load_dotenv
from nanoleafapi import Nanoleaf 

load_dotenv()

API_KEY = os.getenv("API_KEY")
NANOLEAF_IP = os.getenv("NANOLEAF_IP")
NANOLEAF_IP_PORTLESS = os.getenv("NANOLEAF_IP_PORTLESS")
SENSIBILITY = int(os.getenv("SENSIBILITY"))
MIN_RED = int(os.getenv("MIN_RED"))
MIN_GREEN = int(os.getenv("MIN_GREEN"))
MIN_BLUE = int(os.getenv("MIN_BLUE"))
MAX_RED = int(os.getenv("MAX_RED"))
MAX_GREEN = int(os.getenv("MAX_GREEN"))
MAX_BLUE = int(os.getenv("MAX_BLUE"))

# I need to take Python courses I have no idea what I'm doing
g_volume = 0

def GET(path):
    return requests.get("http://" + NANOLEAF_IP + '/api/v1/' + API_KEY + path)

def PUT(path, data):
    return requests.put("http://" + NANOLEAF_IP + '/api/v1/' + API_KEY + path, data)


def print_sound(indata, frames, time, status):
    volume_norm = np.linalg.norm(indata)*10
    print(str(volume_norm) + "|" * int(volume_norm))

def update_sound(indata, frames, time, status):
    global g_volume
    g_volume = np.linalg.norm(indata)*10 * SENSIBILITY

def poll_sound_beta():
    with sd.InputStream(callback=print_sound):
        sd.sleep(10000)

def associate_panel_id_to_intensity(volume, cluster_info):
    num_panels = cluster_info["panelLayout"]["layout"]["numPanels"]
    per_panel_ceiling = 100 / num_panels
    max_panel_intensity = 100
    min_panel_intensity = 0
    panel_intensities = []

    for panel in cluster_info["panelLayout"]["layout"]["positionData"]:
        dic = {
            "id": panel["panelId"],
            "intensity": 0
        }

        if volume > 0:
            if volume > per_panel_ceiling:
                dic["intensity"] = max_panel_intensity
            else:
                dic["intensity"] = max_panel_intensity * volume / per_panel_ceiling
            
            volume -= per_panel_ceiling # should be <= 0 after this
        
        else:
            dic["intensity"] = min_panel_intensity

        panel_intensities.append(dic)
    
    return panel_intensities

def intensities_to_payload(intensities):
    num_panels = len(intensities)

    payload =  {
        "command": "display",
        "animType": "static",
        "animData": str(num_panels),
        "loop": False
    }

    for i, intensity in enumerate(intensities):
        num_frames = "1"

        panel_id = intensity["id"]
        panel_intensity_percent = intensity["intensity"] / 100

        panel_start_percent = i / num_panels
        panel_within_percent = panel_intensity_percent / num_panels
        panel_percent = panel_start_percent + panel_within_percent

        panel_red = (panel_percent * MAX_RED + (1 - panel_percent) * MIN_RED)
        panel_green = (panel_percent * MAX_GREEN + (1 - panel_percent) * MIN_GREEN)
        panel_blue = (panel_percent * MAX_BLUE + (1 - panel_percent) * MIN_BLUE)

        # Adjust brightness
        panel_red *= panel_intensity_percent
        panel_green *= panel_intensity_percent
        panel_blue *= panel_intensity_percent

        # R = int(255 * intensity["intensity"] / 100)
        # G = int(255 * intensity["intensity"] / 100)
        # B = int(255 * intensity["intensity"] / 100)
        R = int(panel_red)
        G = int(panel_green)
        B = int(panel_blue)
        W = 0
        T = 1
        payload["animData"] += " {} {} {} {} {} {} {}".format(panel_id, num_frames, R, G, B, W, T)

    return payload

def main():
    cluster_info = GET("").json()
    nl = Nanoleaf(NANOLEAF_IP_PORTLESS, API_KEY)
    
    with sd.InputStream(callback=update_sound):
        while True:
            time.sleep(0.2)
            
            intensities = associate_panel_id_to_intensity(g_volume, cluster_info)
            payload = intensities_to_payload(intensities)
            print("Volume: ", g_volume)
            # print("Payload", payload["animData"])
            nl.write_effect(payload)

    # https://pypi.org/project/nanoleafapi/
    #nl.set_color((0, 0, 255))

main()