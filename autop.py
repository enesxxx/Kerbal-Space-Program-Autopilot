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
circularize = False

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
	stagefuel = rocket.resources_in_decouple_stage(rocket.control.current_stage - 1).amount("LiquidFuel")
	if rocket.situation == rocket.situation.pre_launch and isPre:
     	#turn SAS on
		rocket.control.sas = True
		#takeoff
		rocket.control.activate_next_stage()
		isAscending = True
		isPre = False
  
	elif isAscending:
		if firstStage:
			rocket.control.throttle = 1
			if apoapsis >= 10000 and apoapsis <= 80000 and thrust >= 0.1:
				pitchangle = 86.8007 -0.00103381 * apoapsis
				rocket.control.throttle = 1
				rocket.auto_pilot.engage()
				if rocket.flight().pitch >= 5:
					rocket.auto_pilot.target_pitch_and_heading(pitchangle, 90) #bu değişecek
				if apoapsis >= 80000:
					rocket.auto_pilot.disengage()
					rocket.control.sas = True
					try:
						rocket.control.sas_mode = rocket.control.sas_mode.retrograde
					except:
						print("SAS Mode: Prograde failed")
					break
					
         			#burda roket dönmeye başlıyo. autopilot on veya offken sas'i açık tutmak lazım
			if stagefuel < 15 and altitude > 200:
				rocket.control.throttle = 0
				time.sleep(2)
				print("first stage done")
				print("Stage fuel amount is:" + str(stagefuel))
				rocket.control.activate_next_stage()
				time.sleep(1)
				rocket.control.activate_next_stage()
				firstStage = False
				secondStage = True
				print("second stage started")
				

		if secondStage:
			print("2nd")
			timetoapoapsisfirst = rocket.orbit.time_to_apoapsis
			time.sleep(1)
			timetoapoapsissecond = rocket.orbit.time_to_apoapsis
			if apoapsis >= 80000 and periapsis <= 80000 and rocket.orbit.time_to_apoapsis > 25:
				rocket.control.throttle = 0
				time.sleep(5)
				rocket.control.sas = True
				rocket.auto_pilot.target_pitch_and_heading(0, 90)
				print("waiting for time to apoapsis")
				
			if apoapsis > 80000 and rocket.orbit.time_to_apoapsis <= 25 and periapsis < 80000:
				if timetoapoapsissecond < timetoapoapsisfirst and timetoapoapsisfirst <= 30:
					rocket.auto_pilot.target_pitch_and_heading(0, 90)
					rocket.control.throttle = 1
					print("apoapsise geldik atesledik")
				else:
					if timetoapoapsisfirst == 25:
						rocket.control.throttle = 0
						print("gaz kestik apoapsis artıyor")
						time.sleep(10)
			if periapsis > 80000:
				rocket.control.throttle = 0
				secondStage = False
				circularize = True
		if circularize:
			rocket.auto_pilot.target_pitch_and_heading(0, 90)
			desiredorbit = 250000
			if stagefuel != 0 and periapsis < desiredorbit + 100000 and apoapsis < desiredorbit + 100000:
				if periapsis < desiredorbit:
					if rocket.orbit.time_to_apoapsis < 10 and rocket.orbit.time_to_apoapsis >= 0:
						rocket.control.throttle = 1
						time.sleep(2.5)
					else:
						rocket.control.throttle = 0

				if apoapsis < desiredorbit:
					if rocket.orbit.time_to_periapsis < 5 and rocket.orbit.time_to_periapsis >= 0:
						rocket.control.throttle = 1
					else:
						rocket.control.throttle = 0
			else:
				print("out of fuel at current stage")
				circularize = False

			