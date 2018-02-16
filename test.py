import time

import keyboard

from dxl.dxlchain import DxlChain

# Open the serial device
chain = DxlChain("/dev/ttyUSB0", rate=1000000)

# Load all the motors and obtain the list of IDs
motors = chain.get_motor_list(broadcast=True)  # Discover all motors on the chain and return their IDs
chain.dump()
chain.goto(2, 0, speed=100, blocking=True)
chain.goto(2, 1000, speed=0, blocking=True)
print(chain.get_reg(2, "present_load"))


def periodic(func, **kwargs):
    starttime = time.time()
    while True:
        func(**kwargs)
        time.sleep(60.0 - ((time.time() - starttime) % 60.0))


n = 0
while True:
    if keyboard.is_pressed('a'):
        chain.goto(2, n.__add__(1), speed=100, blocking=False)
    elif keyboard.is_pressed('d'):
        chain.goto(2, n.__sub__(1), speed=100, blocking=False)
    elif keyboard.is_pressed('space'):
        chain.disable()
        break
    else:
        time.sleep(.001)
