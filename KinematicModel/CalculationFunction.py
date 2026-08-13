import numpy as np
import ConfigurationSettings as CS

# The program will use metres, seconds and radians for all calculations
# However degrees may be used and converted into radians for ease of reading

def runCalculation(initialConditions, vehicleDimensions, trailerDimensions, settings, controls):

    # Bring in all initial variables and define locally for easy access
    initialVehicleHeading = initialConditions["vehicleHeading"]
    initialArticulation = initialConditions["articulation"]
    initialTrailerHeading = initialVehicleHeading + initialArticulation

    wheelbase = vehicleDimensions["wheelbase"]
    hitchOffset = vehicleDimensions["hitchOffset"]
    hitchToAxle = trailerDimensions["hitchToAxle"]

    speed = controls["speed"] # Signed
    steeringAngle = controls["steeringAngle"]

    typeOfTest = settings["typeOfTest"]
    timeStep = settings["timeStep"]
    totalTime = settings["totalTime"]
    totalSteps = int(np.floor(totalTime / timeStep))

    # Initialise the eventual final result dictionary
    ongoingResults = {
        "time": np.zeros(totalSteps+1),
        "totalDistance": np.zeros(totalSteps+1),

        "xRearAxle": np.zeros(totalSteps+1),
        "yRearAxle": np.zeros(totalSteps+1),
        "vehicleHeading": np.zeros(totalSteps+1),

        "xHitch": np.zeros(totalSteps+1),
        "yHitch": np.zeros(totalSteps+1),

        "xTrailerAxle": np.zeros(totalSteps+1),
        "yTrailerAxle": np.zeros(totalSteps+1),
        "trailerHeading": np.zeros(totalSteps+1),
        "articulationAngle": np.zeros(totalSteps+1),

        "vehicleHeadingRoC": np.zeros(totalSteps+1),  # RoC = Rate of Change
        "articulationRoC": np.zeros(totalSteps+1)
    }

    # Assigning conditions to index 0 which represents time 0
    ongoingResults["vehicleHeading"][0] = initialVehicleHeading
    ongoingResults["trailerHeading"][0] = initialTrailerHeading
    ongoingResults["articulationAngle"][0] = initialArticulation

    ongoingResults["xHitch"][0], ongoingResults["yHitch"][0] = calcHitchPos(
        ongoingResults["xRearAxle"][0], 
        ongoingResults["yRearAxle"][0], 
        ongoingResults["vehicleHeading"][0],
        hitchOffset)
    ongoingResults["xTrailerAxle"][0], ongoingResults["yTrailerAxle"][0] = calcTrailerAxlePos(
        ongoingResults["xHitch"][0], 
        ongoingResults["yHitch"][0], 
        ongoingResults["trailerHeading"][0],
        hitchToAxle)

    ongoingResults["vehicleHeadingRoC"][0] = calcVehicleRoC(
        speed, wheelbase, steeringAngle)
    ongoingResults["articulationRoC"][0] = calcArticulationRoC(
            speed, wheelbase, steeringAngle, hitchToAxle, 
            ongoingResults["articulationAngle"][0], hitchOffset)

    # Define varibales related to reasons to terminate function
    jackKnifed = False
    if np.abs(ongoingResults["articulationAngle"][0]) >= np.deg2rad(90):
        jackKnifed = True

    stepsFilled = 1 # This minus 1 is going to be the index that is being altered at a moment in time

    sTest = False
    mTest = False
    if typeOfTest == "S":
        sTest = True
    elif typeOfTest == "M":
        mTest = True
    
    while (jackKnifed == False
        and stepsFilled <= totalSteps
        and (not(mTest) or abs(ongoingResults["trailerHeading"][stepsFilled-1] - initialTrailerHeading) < np.deg2rad(30))
        # Stability Test stops at jack knife so doesnt require a seperate stop condition
        ):
        pIndex = stepsFilled - 1 # Previous Index
        cIndex = stepsFilled # Current Index

        # Update All Values
        ongoingResults["time"][cIndex] = cIndex * timeStep
        ongoingResults["totalDistance"][cIndex] = cIndex * timeStep * np.abs(speed)

        (ongoingResults["xRearAxle"][cIndex], 
        ongoingResults["yRearAxle"][cIndex]) = calcRearAxlePos(
            ongoingResults["xRearAxle"][pIndex], ongoingResults["yRearAxle"][pIndex],
            speed, ongoingResults["vehicleHeading"][pIndex], timeStep)
        
        ongoingResults["vehicleHeading"][cIndex] = ongoingResults["vehicleHeading"][pIndex] + timeStep * ongoingResults["vehicleHeadingRoC"][pIndex]
        ongoingResults["articulationAngle"][cIndex] = ongoingResults["articulationAngle"][pIndex] + timeStep * ongoingResults["articulationRoC"][pIndex]
        ongoingResults["trailerHeading"][cIndex] = ongoingResults["vehicleHeading"][cIndex] + ongoingResults["articulationAngle"][cIndex]
        
        (ongoingResults["xHitch"][cIndex], 
        ongoingResults["yHitch"][cIndex]) = calcHitchPos(
            ongoingResults["xRearAxle"][cIndex], ongoingResults["yRearAxle"][cIndex],
            ongoingResults["vehicleHeading"][cIndex], hitchOffset)

        (ongoingResults["xTrailerAxle"][cIndex], 
        ongoingResults["yTrailerAxle"][cIndex]) = calcTrailerAxlePos(
            ongoingResults["xHitch"][cIndex], ongoingResults["yHitch"][cIndex],
            ongoingResults["trailerHeading"][cIndex], hitchToAxle)

        ongoingResults["vehicleHeadingRoC"][cIndex] = calcVehicleRoC(
                speed, wheelbase, steeringAngle)
        ongoingResults["articulationRoC"][cIndex] = calcArticulationRoC(
                speed, wheelbase, steeringAngle, hitchToAxle, 
                ongoingResults["articulationAngle"][cIndex], hitchOffset)

        if abs(ongoingResults["articulationAngle"][cIndex]) >= np.deg2rad(90):
            jackKnifed = True

        stepsFilled += 1

    # Loop has finished and all information is recorded
    # Now remove empty list sections is code terminated early
    # And prepare the extra information

    if stepsFilled <= totalSteps:
        for entry in ongoingResults:
            ongoingResults[entry] = ongoingResults[entry][:stepsFilled]

    # Find reason for ending
    if jackKnifed:
        endreason = "jackknife"
    elif mTest and abs(ongoingResults["trailerHeading"][stepsFilled-1] - initialTrailerHeading) >= np.deg2rad(30):
        endreason = "heading"
    else:
        endreason = "time"

    finalInfo = {
        "finalTime": ongoingResults["time"][-1],
        "finalDistance": ongoingResults["totalDistance"][-1],
        "headingDifference": np.abs(ongoingResults["trailerHeading"][-1]-initialTrailerHeading),
        "maximumArticulation": np.max(np.abs(ongoingResults["articulationAngle"])),
        "jackKnifed": jackKnifed,
        "endReason": endreason,
    }

    return (ongoingResults, finalInfo)


def calcHitchPos(xRA, yRA, vehicleHeading, hitchOffset):
    xH = xRA + np.sin(vehicleHeading) * hitchOffset
    yH = yRA - np.cos(vehicleHeading) * hitchOffset
    return xH, yH

def calcTrailerAxlePos(xH, yH, trailerHeading, hitchToAxle):
    xT = xH + np.sin(trailerHeading) * hitchToAxle
    yT = yH - np.cos(trailerHeading) * hitchToAxle
    return xT, yT

def calcRearAxlePos(xRA, yRA, v, vehicleHeading, timeStep):
    nXRA = xRA - np.sin(vehicleHeading) * v * timeStep
    nYRA = yRA + np.cos(vehicleHeading) * v * timeStep
    return nXRA, nYRA

def calcVehicleRoC(v, L, steeringAngle):
    return (np.tan(steeringAngle) * v / L)

def calcArticulationRoC(v, L, steeringAngle, D, articulationAngle, O):
    return (- np.sin(articulationAngle) * v / D 
            - np.tan(steeringAngle) * v * (1 + np.cos(articulationAngle) * O / D) / L)


if __name__ == "__main__":
    initialConditions   = CS.ogInitialConditions.copy()
    vehicleDimensions   = CS.landRoverDimensions.copy()
    trailerDimensions   = CS.ogTrailerDimensions.copy()
    controls            = CS.ogControls.copy()
    settings            = CS.ogSettings.copy()

    results, finalInfo = runCalculation(
        initialConditions,
        vehicleDimensions,
        trailerDimensions,
        settings,
        controls
    )

    print(finalInfo)






