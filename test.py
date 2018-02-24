import logging
import time

import keyboard
import sys

import myo
import classify_myo
from myo_raw import Pose

from dxl.dxlchain import DxlChain

# Open the serial device
chain = DxlChain("/dev/ttyUSB0", rate=1000000)

# Load all the motors and obtain the list of IDs
motors = chain.get_motor_list(broadcast=True)  # Discover all motors on the chain and return their IDs
print("Discovered Dynamixels and Information:")
chain.dump()
chain.goto(4, 0, speed=100, blocking=True)
chain.goto(4, 1000, speed=0, blocking=True)
print(chain.get_reg(4, "present_load"))


def myo2dyna(pose):
    if pose.__eq__(Pose.REST):
        chain.goto(4, 0, speed=100, blocking=False)
    elif pose.__eq__(Pose.FINGERS_SPREAD):
        chain.goto(4, 1000, speed=100, blocking=False)
    else:
        logging.error("Invalid pose.")


def periodic(func, **kwargs):
    starttime = time.time()
    while True:
        func(**kwargs)
        time.sleep(60.0 - ((time.time() - starttime) % 60.0))


m = myo.Myo(myo.NNClassifier(), sys.argv[1] if len(sys.argv) >= 2 else None)
hnd = classify_myo.EMGHandler(m)
m.add_emg_handler(hnd)
m.add_arm_handler(lambda arm, xdir: print('arm', arm, 'xdir', xdir))
m.add_pose_handler(lambda p: print('pose', p))
m.add_pose_handler(lambda p: myo2dyna(p))
try:
    m.connect()
    while True:
        periodic(m.run(1))
except RuntimeError:
    logging.error("Oof.")
except KeyboardInterrupt:
    logging.info("Stopping...")
finally:
    m.disconnect()
    logging.info("Have nice day.")

# n = 0
# while True:
#    if keyboard.is_pressed('a'):
#        chain.goto(2, n.__add__(1), speed=100, blocking=False)
#    elif keyboard.is_pressed('d'):
#        chain.goto(2, n.__sub__(1), speed=100, blocking=False)
#    elif keyboard.is_pressed('space'):
#        chain.disable()
#        break
#    else:
#        time.sleep(.001)
