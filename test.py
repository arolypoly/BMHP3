from dxl.dxlchain import DxlChain

# Open the serial device
chain = DxlChain("/dev/ttyUSB0", rate=3000000)

# Load all the motors and obtain the list of IDs
motors = chain.get_motor_list()  # Discover all motors on the chain and return their IDs
print(motors)

# Move a bit
chain.goto(0, 500, speed=200)  # Motor ID 1 is sent to position 500 with high speed
chain.goto(0, 100)  # Motor ID 1 is sent to position 100 with last speed value

# Move and print current position of all motors while moving
chain.goto(0, 1000, speed=20, blocking=False)  # Motor ID 1 is sent to position 1000
while chain.is_moving():
    print(chain.get_position())

# Disable the motors
chain.disable()
