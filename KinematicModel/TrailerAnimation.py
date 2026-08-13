import numpy as np
import matplotlib.pyplot as plt
from CalculationFunction import runCalculation
from matplotlib.animation import FuncAnimation
import ConfigurationSettings as CS

def produceCoords(fixedInputs, calcInputs):
    # Unchanging Dimensions or Values
    vWidth = fixedInputs[0]["width"]
    vLength = fixedInputs[0]["length"]
    vExposedHitch = fixedInputs[0]["exposedHitch"]
    vHitchOffset = fixedInputs[0]["hitchOffset"]
    vWheelbase = fixedInputs[0]["wheelbase"]
    vWheelWidth = fixedInputs[0]["wheelWidth"]
    vWheelLength = fixedInputs[0]["wheelLength"]

    tWidth = fixedInputs[1]["width"]
    tLength = fixedInputs[1]["length"]
    tExposedDrawbar = fixedInputs[1]["exposedDrawbarLength"]
    tHitchToAxle = fixedInputs[1]["hitchToAxle"]
    tWheelWidth = fixedInputs[1]["wheelWidth"]
    tWheelLength = fixedInputs[1]["wheelLength"]

    steeringAngle = fixedInputs[2]["steeringAngle"]

    # Angles and Coordinates that change with time
    vHeading = calcInputs["vehicleHeading"]
    tHeading = calcInputs["trailerHeading"]
    xRearAxle = calcInputs["xRearAxle"]
    yRearAxle = calcInputs["yRearAxle"]
    xHitch = calcInputs["xHitch"]
    yHitch = calcInputs["yHitch"]
    xTrailerAxle = calcInputs["xTrailerAxle"]
    yTrailerAxle = calcInputs["yTrailerAxle"]

    #All coordinate rectangles will be stored starting clockwise from 12 o'clock
    outputs = {
        "vehicleCorners": [], # A list with 4 coord list per frame
        "rearVehicle": [], # A list with 1 coord list per frame
        "vehicleFrontWheelsCoords":[], # A list with 2 lists each with 4 coord list per frame
        "vehicleRearWheelsCoords":[],

        "hitchCoords": [], # A list with one coord list per frame
        
        "trailerCorners": [], # A list with 4 coord list per frame
        "frontTrailer": [], # A list with 1 coord list per frame
        "trailerWheelsCoords":[], # A list with 2 lists each with four coord list per frame
    }

    for i in range(len(vHeading)):
        outputs["hitchCoords"].append([xHitch[i], yHitch[i]])

        #Produce Coords for Rectangle of car and trailer and 
        #then lines for the hitch and points it joins the trailer and car

        #Calculting the front and rear of trailer and rear of the car
        #Front of Trailer
        xFT = xHitch[i] + tExposedDrawbar * np.sin(tHeading[i])
        yFT = yHitch[i] - tExposedDrawbar * np.cos(tHeading[i])
        outputs["frontTrailer"].append([xFT, yFT])

        xRT = xFT + tLength * np.sin(tHeading[i])
        yRT = yFT - tLength * np.cos(tHeading[i])

        xRV = xHitch[i] - vExposedHitch * np.sin(vHeading[i])
        yRV = yHitch[i] + vExposedHitch * np.cos(vHeading[i])
        outputs["rearVehicle"].append([xRV, yRV])

        # Add Corner of vehicle and trailer to the outputs using function
        outputs["vehicleCorners"].append(recCoordsRear(xRV, yRV, vWidth, vLength, vHeading[i]))
        outputs["trailerCorners"].append(recCoordsRear(xRT, yRT, tWidth, tLength, tHeading[i]))

        # Front Axle on Vehicle
        xFA = xRearAxle[i] - vWheelbase * np.sin(vHeading[i])
        yFA = yRearAxle[i] + vWheelbase * np.cos(vHeading[i])

        outputs["vehicleFrontWheelsCoords"].append(findWheelPair(xFA, yFA, vWheelWidth, vWheelLength, vHeading[i], vWidth, steerAngle=steeringAngle))
        outputs["vehicleRearWheelsCoords"].append(findWheelPair(xRearAxle[i], yRearAxle[i], vWheelWidth, vWheelLength, vHeading[i], vWidth))
        outputs["trailerWheelsCoords"].append(findWheelPair(xTrailerAxle[i], yTrailerAxle[i], tWheelWidth, tWheelLength, tHeading[i], tWidth))

    return outputs

def recCoordsRear(x, y, w, l, angle):
    xBL = x - w * np.cos(angle) / 2
    yBL = y - w * np.sin(angle) / 2
    backLeft = [xBL, yBL]
    xBR = x + w * np.cos(angle) / 2
    yBR = y + w * np.sin(angle) / 2
    backRight = [xBR, yBR]

    xFL = xBL - l * np.sin(angle)
    yFL = yBL + l * np.cos(angle)
    frontLeft = [xFL, yFL]
    xFR = xBR - l * np.sin(angle)
    yFR = yBR + l * np.cos(angle)
    frontRight = [xFR, yFR]
    #Clockwise from 12 o clock when heading angle is 0
    return [frontRight, backRight, backLeft, frontLeft]

def findRightWheel(x, y, wheelWidth, wheelLength, angle, axleWidth, steerAngle=0):
    xCA = x + axleWidth * np.cos(angle) / 2
    yCA = y + axleWidth * np.sin(angle) / 2

    angle = angle + steerAngle

    xRA = xCA + wheelLength * np.sin(angle) / 2
    yRA = yCA - wheelLength * np.cos(angle) / 2

    return recCoordsRear(xRA, yRA, wheelWidth, wheelLength, angle)

def findLeftWheel(x, y, wheelWidth, wheelLength, angle, axleWidth, steerAngle=0):
    xCA = x - axleWidth * np.cos(angle) / 2
    yCA = y - axleWidth * np.sin(angle) / 2

    angle = angle + steerAngle
    
    xRA = xCA + wheelLength * np.sin(angle) / 2
    yRA = yCA - wheelLength * np.cos(angle) / 2

    return recCoordsRear(xRA, yRA, wheelWidth, wheelLength, angle)

def findWheelPair(x, y, wheelWidth, wheelLength, angle, axleWidth, steerAngle=0):
    return ([findRightWheel(x, y, wheelWidth, wheelLength, angle, axleWidth, steerAngle),
            findLeftWheel(x, y, wheelWidth, wheelLength, angle, axleWidth, steerAngle)])

def drawRectangle(ax, corners, **style):
    newcorners = corners[:]
    newcorners.append(corners[0])
    x =[]
    y = []

    for i in range(len(newcorners)):
        x.append(newcorners[i][0])
        y.append(newcorners[i][1])

    ax.plot(x, y, **style)
    
def drawLine(ax, point1, point2, **style):
        
        ax.plot([point1[0], point2[0]],
                [point1[1], point2[1]], 
                **style)


def drawFrame(ax, outputs, frame, **style):
    #Vehicle
    drawRectangle(ax,
                  outputs["vehicleCorners"][frame],
                  **style)
    #Trailer
    drawRectangle(ax,
                      outputs["trailerCorners"][frame],
                      **style)
    #Wheels
    wheelPairs = ["vehicleFrontWheelsCoords", "vehicleRearWheelsCoords", "trailerWheelsCoords"]
    for i in range(len(wheelPairs)):
        for j in range(2):
            drawRectangle(ax,
                        outputs[wheelPairs[i]][frame][j],
                        **style)
    #Hitch and DrawBar
    drawLine(ax, outputs["hitchCoords"][frame], outputs["rearVehicle"][frame], **style)
    drawLine(ax, outputs["hitchCoords"][frame], outputs["frontTrailer"][frame], **style)


def produceAnimation(fixedInputs, results, framestep=5, interval=40):
    outputs = produceCoords(fixedInputs, results)

    fig, ax = plt.subplots()

    useFrames = range(0, len(outputs["vehicleCorners"]), framestep)

    paused = False
    def togglePause(event):
        nonlocal paused
        if event.key in [" ", "space"]:
            if paused:
                animation.resume()
            else:
                animation.pause()
            paused = not paused

    def animate(frame):
        ax.clear()

        drawFrame(ax, outputs, frame, color="black", linewidth=1.5, alpha=0.9)

        ax.set_xlim(-25, 25)
        ax.set_ylim(-25, 25)
        ax.set_aspect("equal", adjustable="box")
        ax.grid(alpha=0.3)

        ax.set_xlabel("x coordinate (m)")
        ax.set_ylabel("y coordinate (m)")
        ax.set_title(f"Time = {results['time'][frame]:.2f} s")

    animation = FuncAnimation(
        fig, animate, frames=useFrames, interval=interval, repeat=False
    )

    fig.canvas.mpl_connect("key_press_event", togglePause)

    plt.show()

    return animation

    

    # #All coordinate rectangles will be stored starting clockwise from 12 o'clock
    # outputs = {
    #     "vehicleCorners": [], # A list with 4 coord list per frame
    #     "rearVehicle": [], # A list with 1 coord list per frame
    #     "vehicleFrontWheelsCoords":[], # A list with 2 lists each with 4 coord list per frame
    #     "vehicleRearWheelsCoords":[],

    #     "hitchCoords": [], # A list with one coord list per frame
        
    #     "trailerCorners": [], # A list with 4 coord list per frame
    #     "frontTrailer": [], # A list with 1 coord list per frame
    #     "trailerWheelsCoords":[], # A list with 2 lists each with four coord list per frame
    # }





#Default Conditions
initialConditions   = CS.testInitialConditions.copy()
vehicleDimensions   = CS.landRoverDimensions.copy()
trailerDimensions   = CS.testTrailerDimensions.copy()
controls            = CS.testControls.copy()
settings            = CS.stabSettings.copy()

results, finalInfo = runCalculation(
    initialConditions,
    vehicleDimensions,
    trailerDimensions,
    settings,
    controls
)

fixedInputs = [
    vehicleDimensions,
    trailerDimensions,
    controls,
]

ani = produceAnimation(fixedInputs, results)