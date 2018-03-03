import time

import sys
from multiprocessing import Pool

import myo
import classify_myo
from myo_raw import Pose

from dxl.dxlchain import DxlChain

# Open the serial device
chain = DxlChain("/dev/ttyUSB0", rate=1000000)


def git_to(position, blocking=True):
    chain.set_position({n + 1: position for n in range(chain.motors.__len__() + 1)}, blocking=blocking)


# Load all the motors and obtain the list of IDs
motors = chain.get_motor_list(broadcast=True)  # Discover all motors on the chain and return their IDs
print("Discovering Dynamixels and dumping information...")
chain.dump()
git_to(1000)
git_to(0)
print(chain.get_reg(1, "present_load"))


def myo2dyna(pose):
    if pose.__str__().__eq__("Pose.FIST"):
        print(pose)
        git_to(0, False)
    elif pose.__str__().__eq__("Pose.REST"):
        print(pose)
        git_to(500, False)
    elif pose.__str__().__eq__("Pose.FINGERS_SPREAD"):
        print(pose)
        git_to(1000, False)
    elif pose.__str__().__eq__("THUMB_TO_PINKY"):
        print(pose)
        chain.set_position({1: 0, 6: 0}, False)
    else:
        print("Please gib funding to do gud wrist thank.")


def periodic(func, hz=1, **kwargs):
    starttime = time.time()
    while True:
        func(**kwargs)
        time.sleep(float(1 / hz) - ((time.time() - starttime) % float(1 / hz)))


m = myo.Myo(myo.NNClassifier(), sys.argv[1] if len(sys.argv) >= 2 else None)
hnd = classify_myo.EMGHandler(m)
m.add_emg_handler(hnd)
m.add_arm_handler(lambda arm, xdir: print('arm', arm, 'xdir', xdir))
m.add_pose_handler(lambda p: myo2dyna(p))
print("Myoband initialized.")
try:
    m.connect()
    while True:
        m.run()
except RuntimeError:
    print("Oof.")
except KeyboardInterrupt:
    print("Stopping...")
finally:
    m.disconnect()
    print("Have nice day.")
