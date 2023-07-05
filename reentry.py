import krpc
import time
import math
from timeit import default_timer as timer

connection = krpc.connect()
rocket = connection.space_center.active_vessel
print(rocket.name)
isPre = True
isAscending = False
isCruising = False
isDescending = False
isLanding = False
firstStage = True
secondStage = False
thirdStage = False
isReentry = False

ref_frame = connection.space_center.ReferenceFrame.create_hybrid(
	position=rocket.orbit.body.reference_frame,
	rotation=rocket.surface_reference_frame)



while isPre or isAscending or isCruising or isDescending or isLanding:
	altitude = rocket.flight().surface_altitude
	verticalspeed = rocket.flight(ref_frame).vertical_speed
	thrust = rocket.thrust
	apoapsis = rocket.orbit.apoapsis_altitude
	periapsis = rocket.orbit.periapsis_altitude
	pitch = rocket.flight(ref_frame).pitch

	if isReentry:
		time.sleep(2)
		rocket.control.throttle = 0.5
		rocket.auto_pilot.target_pitch_and_heading(0, -90)
		if periapsis < 0 and isReentry:
			rocket.control.throttle = 0
			isReentry = False
			isAscending = False
			isCruising = True
				
			

				

  
	elif isCruising:				
		if verticalspeed <= 0:
			print("descending")
			time.sleep(1)
			rocket.control.activate_next_stage() #decouple lander
			try:
				rocket.control.sas = True
				rocket.control.sas_mode == rocket.control.sas_mode.retrograde
			except:
				print("SAS Mode Error")
			isDescending = True
			isCruising = False

	elif isDescending:
		if altitude <= 1700:
			print("Parachute deployed")
			rocket.control.activate_next_stage() #deploy chute
			isLanding = True
			isDescending = False
 									
	elif isLanding:
		bottomaltitude = altitude - 9.8 #current version of rocket's center of mass is 9.8m above the gorund
		if altitude < 500:
			time.sleep(1)
			print(int(bottomaltitude))
			estimatedlandingtime = bottomaltitude / abs(verticalspeed)
			if verticalspeed < 5:
				print("Estimated touchdown is: " +str(int(estimatedlandingtime)) + " seconds later")
				startTime = timer()
		if altitude < 20 and rocket.situation == rocket.situation.landed or rocket.situation == rocket.situation.splashed:
			endTime = timer()
			exacttouchdown = str(endTime-startTime)
			print("Exact touchdown was " + exacttouchdown + "seconds later")
			print("landed")
			isLanding = False
			time.sleep(2)
			print(rocket.position(ref_frame))
			print(altitude)
			print(bottomaltitude)

