import numpy as np
import matplotlib.pyplot as plt
from CalculationFunction import runCalculation
import ConfigurationSettings as CS

def drawGraph(xKey, yKey, results, legendLabel="Unknown"):
    x = results[xKey]
    y = np.rad2deg(np.array(results[yKey]))
    plt.plot(x, y, label=legendLabel)
    print(f"Label:{legendLabel}, RoC{y[0:5]} ")

def drawGraphs(resultsList, xLabel, yLabel, 
                        xKey, yKey, title, legendKeys):
    plt.figure()
    for i in range(len(resultsList)):
        drawGraph(xKey, yKey, resultsList[i][0], legendLabel=legendKeys[i])
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.title(title)
    plt.show()

def produceData(investigatedVar, iVOptions, allInputs):
    allResults = []
    for i in range(len(allInputs)):
        if investigatedVar in allInputs[i]:
            iVDict = i
    for j in range(len(iVOptions)):
        allInputs[iVDict][investigatedVar] = iVOptions[j]
        result, finalInfo = runCalculation(
            allInputs[0],
            allInputs[1],
            allInputs[2],
            allInputs[3],
            allInputs[4]
        )
        allResults.append([result, finalInfo])
    return allResults

def oVOWithInvestigation(investigatedVar, iVOptions, allInputs,
                xLabel, yLabel, xKey, yKey, title, legendKeys):
    allResults = produceData(investigatedVar, iVOptions, allInputs)
    drawGraphs(allResults, xLabel, yLabel, xKey, yKey, title, legendKeys)
    for i in range(len(allResults)):
        print(f"{iVOptions[i]} stopped after "
              f"{allResults[i][1]["finalDistance"]:.3f} m "
              f"due to {allResults[i][1]["endReason"]}.")
    return allResults

def oVOWithInvestigationValidation(investigatedVar, iVOptions, allInputs,
                xLabel, yLabel, xKey, yKey, title, legendKeys):
    problems=[]
    inputs = []
    outputs = []

    for listy in allInputs:
        for key in listy:
            inputs.append(key)
    if investigatedVar not in inputs:
            problems.append("Investigated variable is not in inputs")
    dummyResults, info = runCalculation(
                allInputs[0],
                allInputs[1],
                allInputs[2],
                allInputs[3],
                allInputs[4])
    for output in dummyResults:
        outputs.append(output)
    if yKey not in outputs:
        problems.append("Y axis variable is not in outputs")
    if xKey not in outputs:
            problems.append("X axis variable is not in outputs")
    if len(problems) != 0:
        print("There are problems with your inputs listed below")
        for line in problems:
            print(line)
    else:
        allResults = oVOWithInvestigation(investigatedVar, iVOptions, allInputs,
                xLabel, yLabel, xKey, yKey, title, legendKeys)
        return allResults

def getTestDistances(hitchToAxleOptions, allResults, testEndReason):
    distances = []

    for i in range(len(allResults)):
        if allResults[i][1]["endReason"] == testEndReason:
            distances.append(allResults[i][1]["finalDistance"])
        else:
            distances.append(np.nan)
            print(f"D = {hitchToAxleOptions[i]}m did not finish test")
            print(f"it ended due to {allResults[i][1]["endReason"]}")
    return distances

def compareTestGraphs(hitchToAxleOptions, stabResults, manResults):
    stabDistances = getTestDistances(hitchToAxleOptions, stabResults, "jackknife")
    manDistances = getTestDistances(hitchToAxleOptions, manResults, "heading")

    plt.figure(figsize=(8, 5))

    plt.plot(
        hitchToAxleOptions, stabDistances,
        marker="o",
        label="Distance to jackknife"
    )

    plt.plot(
        hitchToAxleOptions, manDistances,
        marker="s",
        label="Distance to 30° heading change"
    )

    plt.xlabel("Hitch-to-Axle Distance, D (m)")
    plt.ylabel("Distance Travelled (m)")
    plt.title(
        "Effect of Hitch-to-Axle Distance on "
        "Stability and Manoeuvrability"
    )
    plt.xticks(hitchToAxleOptions)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()

    return stabDistances, manDistances

initialConditions   = CS.testInitialConditions.copy()
vehicleDimensions   = CS.landRoverDimensions.copy()
trailerDimensions   = CS.ogTrailerDimensions.copy()
controls            = CS.testControls.copy()
settings            = CS.ogSettings.copy()

allInputs = [initialConditions, vehicleDimensions, trailerDimensions, settings, controls]

# Investigated Variable Inputs
investigatedVar = "steeringAngle"
iVOptions = np.deg2rad(np.linspace(50, -50, 7))
# Graph Appearance Inputs
xLabel = "Time (s)"
yLabel = " Vehicle Heading Angle ROC (°)"
xKey = "time"
yKey = "vehicleHeadingRoC"
title = "Vehicle Heading vs Time for Different Time Steps"
legendKeys = []
for i in range(len(iVOptions)):
    legendKeys.append(f"Time Step = {iVOptions[i]:.3f}s")

manResults = oVOWithInvestigationValidation(investigatedVar, iVOptions, allInputs,
                xLabel, yLabel, xKey, yKey, title, legendKeys)

# #Now Change for stability
# initialConditions   = CS.stabInitialConditions.copy()
# controls            = CS.stabControls.copy()
# settings            = CS.stabSettings.copy()
# allInputs = [initialConditions, vehicleDimensions, trailerDimensions, settings, controls]

# # Investigated Variable Inputs
# investigatedVar = "hitchToAxle"
# iVOptions = np.linspace(1.5, 4, 6)

# # Graph Appearance Inputs
# xLabel = "Distance Travelled (m)"
# yLabel = "Articulation Angle (°)"
# xKey = "totalDistance"
# yKey = "articulationAngle"
# title = "Articulation Angle vs Distance for Different Hitch-to-Axle Distances"
# legendKeys = []
# for i in range(len(iVOptions)):
#     legendKeys.append(f"D = {iVOptions[i]:.1f} m")
# stabResults = oVOWithInvestigationValidation(investigatedVar, iVOptions, allInputs,
#                 xLabel, yLabel, xKey, yKey, title, legendKeys)

# compareTestGraphs(np.linspace(1.5, 4, 6), stabResults, manResults)
# Input List:               Output List:
# vehicleHeading,           time
# articulation,             totalDistance
# wheelbase,                xRearAxle
# hitchOffset,              yRearAxle
# hitchToAxle,              vehicleHeading
# timeStep,totalTime,       xHitch
# typeOfTest,               yHitch
# speed,                    xTrailerAxle
# steeringAngle             yTrailerAxle
#                           trailerHeading
#                           articulationAngle
#                           vehicleHeadingRoC
#                           articulationRoC
