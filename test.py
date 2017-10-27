import dxlcore
from dxl.dxlchain import DxlChain

# Open the serial device
chain = DxlChain("/dev/ttyUSB0", rate=1000000)

# Load all the motors and obtain the list of IDs
motors = chain.get_motor_list(broadcast=True)  # Discover all motors on the chain and return their IDs
chain.dump()
chain.goto(0, 0, speed=100, blocking=True)
chain.goto(0, 4000, speed=0, blocking=True)
print(chain.get_reg(0, "present_load"))
chain.disable()
