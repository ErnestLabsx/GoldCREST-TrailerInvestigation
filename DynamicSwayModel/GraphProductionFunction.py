import CalculationFunction as CF
import ControlledInputs as CI
import numpy as np
import matplotlib.pyplot as plt
import copy

def resultVsTime(config, yKey, investigatedVar, iVOptions):

    d = config[2]["hitchToCentre"] + config[2]["centreToAxle"]
    plt.figure()

    for i in range(len(iVOptions)):

        testConfig = copy.deepcopy(config)

        #Calculate the data
        if investigatedVar == "longitudinalSpeed":
            testConfig[3][investigatedVar] = iVOptions[i]
        elif investigatedVar == "yawMomentOfInertia":
            testConfig[2][investigatedVar] = iVOptions[i]
        elif investigatedVar == "centreToAxle":
            testConfig[2][investigatedVar] = iVOptions[i]
            testConfig[2]["hitchToCentre"] = d - iVOptions[i]
        elif investigatedVar == "timeStep":
            testConfig[4][investigatedVar] = iVOptions[i]

        results = CF.dynamicCalc(
            testConfig[0],
            testConfig[1],
            testConfig[2],
            testConfig[3],
            testConfig[4]
        )
        #Plot the data
        plotOneLine(yKey, results, getLegendLabel(iVOptions[i], investigatedVar))

    #Make grpah look nice and output
    yLabel, title = getWordyStuffResults(yKey, investigatedVar)
    plt.xlabel("Time (s)")
    plt.ylabel(yLabel)
    plt.grid(alpha=0.3)
    plt.title(title)
    plt.axvline(
        x=config[3]["steerDuration"],
        color="black",
        linestyle="--",
        linewidth=1,
        label="Steering input ends"
    )
    plt.legend(loc="upper right")
    # plt.legend(
    #     loc="center left",
    #     bbox_to_anchor=(1.02, 0.5),
    #     fontsize=8
    # )
    plt.tight_layout()
    plt.show()


def plotOneLine(yKey, results, legendLabel):
    x = results["time"]
    if yKey in [
        "steeringAngle",
        "vehicleYawRate",
        "trailerYawRate",
        "articulationAngle"
        ]:
        y = np.rad2deg(np.array(results[yKey]))
    else:
        y = np.array(results[yKey])
    plt.plot(x, y, label=legendLabel)
    print(f"max:{np.max(np.abs(y))}, Label:{yKey}")

def getWordyStuffResults(yKey, investigatedVar):
    axisLabel = {
        "steeringAngle": "Steering angle (°)",
        "vehicleLateralVelocity": "Vehicle lateral velocity (m/s)",
        "vehicleYawRate": "Vehicle yaw rate (°/s)",
        "trailerYawRate": "Trailer yaw rate (°/s)",
        "articulationAngle": "Articulation angle (°)"
    }
    y = {
        "steeringAngle": "Steering Angle",
        "vehicleLateralVelocity": "Vehicle Lateral Velocity",
        "vehicleYawRate": "Vehicle Yaw Rate",
        "trailerYawRate": "Trailer Yaw Rate",
        "articulationAngle": "Articulation Angle"
    }
    invest = {
        "longitudinalSpeed": "Longitudinal Speeds",
        "yawMomentOfInertia": "Trailer Yaw Moments of Inertia",
        "centreToAxle": "Trailer Centre of Mass Positions",
        "timeStep": "Time Steps"
    }
    return (axisLabel[yKey], 
                (f"{y[yKey]} against Time for Different"
                 "\n"
                f"{invest[investigatedVar]}"))

def getLegendLabel(iVOption, iVar):
    invest = {
            "longitudinalSpeed": ["Longitudinal Speed = ", "m/s"],
            "yawMomentOfInertia": ["Trailer Yaw Moments of Inertia = ","kgm^2"],
            "centreToAxle": ["Trailer Centre of Mass Positions = ","m"],
            "timeStep": ["Time Step = ", "s"],
        }
    if iVar == "yawMomentOfInertia":
        iVOption = f"{iVOption:.0f}"
    elif iVar == "timeStep":
        iVOption = f"{iVOption:.4f}"
    else:
        iVOption = f"{iVOption:.1f}"

    return f"{invest[iVar][0]}{iVOption} {invest[iVar][1]}"

def plotThreeResults(config, investigatedVar, iVOptions):
    yKeyOptions = ["articulationAngle", "vehicleYawRate", "trailerYawRate", "steeringAngle", "vehicleLateralVelocity"]
    for i in range(3):
        yKey = yKeyOptions[i]
        resultVsTime(config, yKey, investigatedVar, iVOptions)

def calculateDampingRatio(results, steerDuration, numberOfRatios=3):
    time = np.asarray(results["time"])
    beta = np.asarray(results["articulationAngle"])

    valid = (time >= steerDuration) & np.isfinite(beta)
    beta = beta[valid]

    if len(beta) < 3:
        return np.nan

    signs = np.sign(beta)
    for i in range(len(signs)-1):
        if signs[i+1] == 0:
            signs[i+1] = signs[i]
    ends = np.where(signs[:-1] != signs[1:])[0] + 1

    peaks = []
    for i in range(len(ends)-1):
        section = beta[ends[i]:ends[i+1]]

        if len(section) > 0:
            peaks.append(section[np.argmax(np.abs(section))])

    nOPR = numberOfRatios + 2 # Number Of Peaks Requried
    if len(peaks) < nOPR:
        return np.nan
    
    maxBetas  = peaks[:nOPR]

    differences = []
    for i in range(len(maxBetas)-1):
        differences.append(np.abs(maxBetas[i] - maxBetas[i+1]))

    differences = np.asarray(differences)
    if np.any(differences <= 0):
        return np.nan

    #Calculate the actual ratio

    n = np.log(differences[:-1] / differences[1:]) / np.pi

    ratios = np.sign(n) * np.sqrt(n**2 / (1 + n**2))

    return np.mean(ratios)

def plotSummaryGraph(config, investigatedVar, iVOptions):

    d = config[2]["hitchToCentre"] + config[2]["centreToAxle"]
    plt.figure()

    damping = []

    for i in range(len(iVOptions)):

        testConfig = copy.deepcopy(config)

        #Calculate the data
        if investigatedVar == "longitudinalSpeed":
            testConfig[3][investigatedVar] = iVOptions[i]
        elif investigatedVar == "yawMomentOfInertia":
            testConfig[2][investigatedVar] = iVOptions[i]
        elif investigatedVar == "centreToAxle":
            testConfig[2][investigatedVar] = iVOptions[i]
            testConfig[2]["hitchToCentre"] = d - iVOptions[i]

        results = CF.dynamicCalc(
            testConfig[0],
            testConfig[1],
            testConfig[2],
            testConfig[3],
            testConfig[4]
        )
        #get the dampening ratio
        damping.append(calculateDampingRatio(results, testConfig[3]["steerDuration"]))

    print(damping)
    #plot the graph
    plt.plot(iVOptions, damping, marker="o")
    
    #Make grpah look nice and output
    xLabel, title = getWordyStuffSum(investigatedVar)
    plt.xlabel(xLabel)
    plt.ylabel("Estimated Damping Ratio")
    plt.grid(alpha=0.3)
    plt.title(title)
    plt.axhline(
        y=0,
        color="black",
        linestyle="--",
        linewidth=1,
        label="Neutrally stable"
    )
    plt.legend()
    plt.tight_layout()
    plt.show()

def getWordyStuffSum(iVar):
    xAxis = {
            "longitudinalSpeed": "Longitudinal Speed (m/s)",
            "yawMomentOfInertia": "Trailer Yaw Moments of Inertia (kg m²)",
            "centreToAxle": "Centre of Mass Distance Ahead of Axle (m)",
        }
    invest = {
        "longitudinalSpeed": "Longitudinal Speeds",
        "yawMomentOfInertia": "Trailer Yaw Moments of Inertia",
        "centreToAxle": "Trailer Centre of Mass Positions",
    }
    return (xAxis[iVar], 
                (f"Estimated Damping ratio for Different {invest[iVar]}"))

initialConditions = CI.initialConditions2.copy()
vehicleCharacteristics = CI.vehicleCharacteristics2.copy()
trailerCharacteristics = CI.trailerCharacteristics2.copy()
controls = CI.controls2.copy()
settings = CI.settings2.copy()

config = [
    initialConditions,
    vehicleCharacteristics,
    trailerCharacteristics,
    controls,
    settings
]
#longitudinalSpeed, yawMomentOfInertia, centreToAxle, timeStep
# Ignore this now yKey = ["articulationAngle", "vehicleYawRate", "trailerYawRate", "steeringAngle", "vehicleLateralVelocity"]
investigatedVar = "timeStep"
iVOptions = np.array([0.0005])
plotThreeResults(config, investigatedVar, iVOptions)
#plotSummaryGraph(config, investigatedVar, iVOptions)