import sys
import time
from datetime import datetime

import paho.mqtt.client as mqtt

from anova import AnovaCooker

def main(config):
    mqtt_client = mqtt.Client(client_id="anova2mqtt_"+datetime.now().strftime("%Y%m%d-%H%M%S"))
    mqtt_client.username_pw_set(username=config['mqtt']['username'], password=config['mqtt']['password'])
    mqtt_client.connect(config['mqtt']['host'])

    cooker = None
    cooker_state = None

    while True:
        end_time = time.time() + int(config['general']['interval'])

        if cooker is None:
            print("Creating cooker")
            try:
                cooker = AnovaCooker(config['cooker']['deviceid'])
                cooker.authenticate(config['cooker']['email'], config['cooker']['password'])
            except Exception as e:
                cooker = None
                print("Device not found")

        if cooker is not None:
            cooker_state = loop(config, cooker_state, cooker, mqtt_client)

        sleep_time = end_time - time.time()
        print(f"Sleeping {sleep_time}s")
        time.sleep(sleep_time)


def loop(config, cooker_state, cooker, mqtt_client):
    if cooker_state is not None:
        cooker_state_old = cooker_state.copy()
    else:
        cooker_state_old = None

    cooker_state = cooker_update(cooker)

    if cooker_state_old is None or not cooker_state['heater_temp'] == cooker_state_old['heater_temp']:
        res = mqtt_client.publish(config['mqtt']['basetopic'] + config['cooker']['deviceid'] + "/heater_temp", payload=str(cooker_state['heater_temp']), retain=True)
        print(f"Publishing new temp {cooker_state['heater_temp']}°C: {res}")
    elif cooker_state_old is not None:
        print(f"Temp did not change ({cooker_state['heater_temp']})")

    return cooker_state

def cooker_update(cooker: AnovaCooker):
    cooker.update_state()

    cooker_state = {
        'job_status': cooker.job_status,
        'job_time_remaining': cooker.job_time_remaining,
        'heater_duty_cycle': cooker.heater_duty_cycle,
        'motor_duty_cycle': cooker.motor_duty_cycle,
        'wifi_connected': cooker.wifi_connected,
        'wifi_ssid': cooker.wifi_ssid,
        'device_safe': cooker.device_safe,
        'water_leak': cooker.water_leak,
        'water_level_critical': cooker.water_level_critical,
        'water_level_low': cooker.water_level_low,
        'heater_temp': cooker.heater_temp,
        'triac_temp': cooker.triac_temp,
        'water_temp': cooker.water_temp,
    }

    return cooker_state


def shutdown(signum, frame):  # signum and frame are mandatory
    sys.exit(0)
