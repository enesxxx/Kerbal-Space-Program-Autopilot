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

ref_frame = connection.space_center.ReferenceFrame.create_hybrid(
	position=rocket.orbit.body.reference_frame,
	rotation=rocket.surface_reference_frame)
totalheight= 21.6	
seaaltitude = rocket.flight().mean_altitude
groundaltitude = rocket.flight().surface_altitude
print(seaaltitude)
print(groundaltitude)
heighttocenter = 9.8
bottomaltitude = groundaltitude - heighttocenter
print(bottomaltitude)