from dronekit import connect, VehicleMode
import time

# Connect to the vehicle
connection_string = '/dev/ttyAMA0'  # Adjust this based on your setup (e.g., /dev/serial0)
baud_rate = 57600

print("Connecting to vehicle on: %s" % connection_string)
vehicle = connect(connection_string, baud=baud_rate, wait_ready=True)

# Function to arm and take off
def arm_and_takeoff(target_altitude):
    print("Arming motors")
    
    while not vehicle.is_armable:
        print(" Waiting for vehicle to become armable...")
        time.sleep(1)

    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(target_altitude)

    # Wait until the vehicle reaches a safe altitude
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt >= target_altitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

# Arm and take off to 10 meters
arm_and_takeoff(10)

# Hover for 10 seconds
print("Hovering...")
time.sleep(10)

# Land the drone
print("Landing...")
vehicle.mode = VehicleMode("LAND")

# Close the connection
vehicle.close()
print("Completed")
