import krpc
import time
import math
from timeit import default_timer as timer

connection = krpc.connect()
rocket = connection.space_center.active_vessel
print(rocket.name)
isPre = False
isAscending = False
isCruising = False
isDescending = False
isLanding = False
firstStage = False
secondStage = False
thirdStage = False
circularize = True

ref_frame = connection.space_center.ReferenceFrame.create_hybrid(
	position=rocket.orbit.body.reference_frame,
	rotation=rocket.surface_reference_frame)



while isPre or isAscending or isCruising or isDescending or isLanding or circularize:
	altitude = rocket.flight().surface_altitude
	verticalspeed = rocket.flight(ref_frame).vertical_speed
	thrust = rocket.thrust
	apoapsis = rocket.orbit.apoapsis_altitude
	periapsis = rocket.orbit.periapsis_altitude
	pitch = rocket.flight(ref_frame).pitch
	stagefuel = rocket.resources_in_decouple_stage(rocket.control.current_stage - 1).amount("LiquidFuel")
	if circularize:
		rocket.auto_pilot.engage()
		rocket.auto_pilot.target_pitch_and_heading(0, 90)
		desiredorbit = 500000
		if stagefuel != 0 and periapsis < desiredorbit or apoapsis < desiredorbit:
			if periapsis < desiredorbit:
				rocket.auto_pilot.engage()
				rocket.auto_pilot.target_pitch_and_heading(0, 90)
				if rocket.orbit.time_to_apoapsis < 10 and rocket.orbit.time_to_apoapsis >= 0:
					rocket.control.throttle = 0.5
				else:
					rocket.control.throttle = 0

			if apoapsis < desiredorbit:
				rocket.auto_pilot.engage()
				rocket.auto_pilot.target_pitch_and_heading(0, 90)
				if rocket.orbit.time_to_periapsis < 10 and rocket.orbit.time_to_periapsis >= 0:
					rocket.control.throttle = 0.5
				else:
					rocket.control.throttle = 0
			
		else:
			rocket.auto_pilot.disengage()
			if stagefuel <= 0:
				print("out of fuel at current stage")
			else:
				print("orbit done")
			circularize = False

			