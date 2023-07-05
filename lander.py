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
cutoff = False
suicide = False

ref_frame = connection.space_center.ReferenceFrame.create_hybrid(
	position=rocket.orbit.body.reference_frame,
	rotation=rocket.surface_reference_frame)



while isPre or isAscending or isCruising or isDescending or isLanding or isReentry:
	altitude = rocket.flight().surface_altitude
	verticalspeed = rocket.flight(ref_frame).vertical_speed
	thrust = rocket.thrust
	apoapsis = rocket.orbit.apoapsis_altitude
	periapsis = rocket.orbit.periapsis_altitude
	pitch = rocket.flight(ref_frame).pitch
	if rocket.situation == rocket.situation.pre_launch and isPre:
     	#turn SAS on
		rocket.control.sas = True
		#takeoff
		rocket.control.activate_next_stage()
		isAscending = True
		isPre = False
  
	elif isAscending:
		if apoapsis < 3000 and isAscending:
			rocket.control.throttle = 1
			rocket.control.gear = False
		elif apoapsis >= 3000:
			rocket.control.throttle = 0
			isDescending = True
			isAscending = False
   
	elif isDescending:
		if firstStage:
			if verticalspeed <= -2:
				rocket.control.sas_mode = rocket.control.sas_mode.retrograde
				rocket.control.rcs = True
			if apoapsis >= 3000 and cutoff == False:
				rocket.control.throttle = 0
				rocket.control.brakes = True
				suicide = True
				cutoff = True
		if suicide:
			if verticalspeed < -30 and altitude < 1500 and altitude >= 900:
				rocket.control.throttle = 1
			elif verticalspeed <= -20 and verticalspeed >= -30 and altitude < 600:
				rocket.control.throttle = 0.7
			elif verticalspeed <= -10 and verticalspeed > -20 and altitude < 400:
				rocket.control.throttle = 0.5
				rocket.control.gear = True
			elif verticalspeed <= -5 and verticalspeed > -10 and altitude >= 50 and altitude < 100:
				rocket.control.throttle = 0.25
			elif verticalspeed >= -3:
				rocket.control.throttle = 0

							
					#burda roket dönmeye başlıyo. autopilot on veya offken sas'i açık tutmak lazım
			trynfailorbital_height = 21.6
			bottomaltitude = altitude - 9.8 #current version of rocket's center of mass is 2.81m above the gorund
			if altitude < 500 and verticalspeed < 0:
				time.sleep(1)
				print(int(bottomaltitude))
				estimatedlandingtime = bottomaltitude / abs(verticalspeed)
				if verticalspeed > -10:
					print("Estimated touchdown is: " +str(int(estimatedlandingtime)) + " seconds later")
					startTime = timer()
			if rocket.situation == rocket.situation.landed or rocket.situation == rocket.situation.splashed:
				suicide = False
				endTime = timer()
				exacttouchdown = str(endTime-startTime)
				print("Exact touchdown was " + exacttouchdown + "seconds later")
				print("landed")
				isLanding = False
				time.sleep(2)
				print(rocket.position(ref_frame))
				print(altitude)
				print(bottomaltitude)