# All inputs given in metres radians and seconds
import numpy as np

initialConditions1 = {
	"vehicleLateralVelocity": 0,
	"vehicleYawRate": 0,
	"trailerYawRate": 0,
    "articulationAngle": 0,
}
vehicleCharacteristics1 = {
	"mass": 1900,
	"yawMomentOfInertia": 1700,
	"centreToFrontAxle": 1.3, 		#a
    "centreToRearAxle": 1.5,		    #b
    "centreToHitch": 2.5, 			#d
    "frontCorneringStiffness": 70000,		
    "rearCorneringStiffness": 70000, 				
}
trailerCharacteristics1 = {
	"mass": 1100,
	"yawMomentOfInertia": 1500,
	"hitchToCentre": 3.7, 			    #e
    "centreToAxle": 0.3,			    #h
    "corneringStiffness": 50000,						
}
controls1 = {
	"longitudinalSpeed": 22,
	"maxSteeringAngle": 0.03,
	"steerDuration": 2,		
}
settings1 = {
	"timeStep": 0.0005,
	"totalTime": 10,			
}


#Sun et al exactly

initialConditions2 = {
	"vehicleLateralVelocity": 0,
	"vehicleYawRate": 0,
	"trailerYawRate": 0,
    "articulationAngle": 0,
}
vehicleCharacteristics2 = {
	"mass": 2200,
	"yawMomentOfInertia": 2000,
	"centreToFrontAxle": 1.5, 		#a
    "centreToRearAxle": 1.7,		    #b
    "centreToHitch": 2.9, 			#d
    "frontCorneringStiffness": 80000,		
    "rearCorneringStiffness": 80000, 				
}
trailerCharacteristics2 = {
	"mass": 2000,
	"yawMomentOfInertia": 3000,
	"hitchToCentre": 6, 			    #e
    "centreToAxle": 0,			    #h
    "corneringStiffness": 80000,						
}
controls2 = {
	"longitudinalSpeed": 80/3.6,
	"maxSteeringAngle": 0.03,
	"steerDuration": 2,		
}
settings2 = {
	"timeStep": 0.0005,
	"totalTime": 15,			
}
