import numpy as np
import ControlledInputs as CI

def dynamicCalc(initialConditions, 
                vehicleCharacteristics, 
                trailerCharacteristics, 
                controls, 
                settings):

    Vv = initialConditions["vehicleLateralVelocity"]
    rv = initialConditions["vehicleYawRate"]
    rt = initialConditions["trailerYawRate"]
    articulation = initialConditions["articulationAngle"]

    mv = vehicleCharacteristics["mass"]
    Iv = vehicleCharacteristics["yawMomentOfInertia"]
    a = vehicleCharacteristics["centreToFrontAxle"]
    b = vehicleCharacteristics["centreToRearAxle"]
    d = vehicleCharacteristics["centreToHitch"]
    c1 = vehicleCharacteristics["frontCorneringStiffness"]	
    c2 = vehicleCharacteristics["rearCorneringStiffness"]				
    
    mt = trailerCharacteristics["mass"]
    It = trailerCharacteristics["yawMomentOfInertia"]
    e = trailerCharacteristics["hitchToCentre"]
    h = trailerCharacteristics["centreToAxle"]
    c3 = trailerCharacteristics["corneringStiffness"]					

    u = controls["longitudinalSpeed"]
    maxAlpha = controls["maxSteeringAngle"]
    steerDuration = controls["steerDuration"]			
    
    timeStep = settings["timeStep"]     #Should divide nicely into total time
    totalTime = settings["totalTime"]
    numberOfSteps = int(np.floor(totalTime/timeStep))	

    #Created Arrays for outputs
    results = {
        "time": np.arange(numberOfSteps) * timeStep,
        "steeringAngle": np.zeros(numberOfSteps),
        "vehicleLateralVelocity": np.zeros(numberOfSteps),
        "vehicleYawRate": np.zeros(numberOfSteps),
        "trailerYawRate": np.zeros(numberOfSteps),
        "articulationAngle": np.zeros(numberOfSteps),
    }
    #Assigned Initial Values, including steering
    steerOn = (results["time"] <= steerDuration)
    results["steeringAngle"][steerOn] = maxAlpha * np.sin(
        2 * np.pi * results["time"][steerOn] / steerDuration)

    results["vehicleLateralVelocity"][0] = Vv
    results["vehicleYawRate"][0] = rv
    results["trailerYawRate"][0] = rt
    results["articulationAngle"][0] = articulation

    #Began first loop
    for i in range(numberOfSteps-1):
        cIndex = i  # Current Index
        nIndex = i + 1# Next Index

        # Fetch current Iteration Values
        Vv = results["vehicleLateralVelocity"][cIndex]
        rv = results["vehicleYawRate"][cIndex]
        rt = results["trailerYawRate"][cIndex]
        articulation = results["articulationAngle"][cIndex]
        steer = results["steeringAngle"][cIndex]

        #Calculate intermediate values in order
        Vt = (Vv + d*rv + e*rt +u*articulation)

        gamma1 = (steer + ((Vv -a*rv) / u))
        gamma2 = ((Vv + b*rv) / u)
        gamma3 = ((Vt + h*rt) / u)

        f1 = -c1 * gamma1
        f2 = -c2 * gamma2
        f3 = -c3 * gamma3

        coefficientMatrix = np.array([
            [mv, 0, 0, 1],
            [0, Iv, 0, d],
            [mt, mt*d, mt*e, -1],
            [0, 0, It, e]
        ], dtype=float)

        rightHandSide = np.array([
            f1 + f2 + mv*u*rv,
            -a*f1 + b*f2,
            f3 + mt*u*rv,
            h*f3
        ], dtype=float)

        solution = np.linalg.solve(coefficientMatrix, rightHandSide)
        VDotv = solution[0]
        rDotv = solution[1]
        rDott = solution[2]
        y = solution[3]

        articulationDot = rt - rv

        # Now update the fundamental variables using Eulers Method
        results["vehicleLateralVelocity"][nIndex] = Vv + VDotv * timeStep

        results["vehicleYawRate"][nIndex] = rv + rDotv * timeStep

        results["trailerYawRate"][nIndex] = rt + rDott * timeStep

        results["articulationAngle"][nIndex] = articulation + articulationDot * timeStep

    return results

initialConditions = CI.initialConditions1
vehicleCharacteristics = CI.vehicleCharacteristics1
trailerCharacteristics = CI.trailerCharacteristics1
controls = CI.controls1
settings = CI.settings1


results = dynamicCalc(initialConditions, vehicleCharacteristics, trailerCharacteristics, controls, settings)
