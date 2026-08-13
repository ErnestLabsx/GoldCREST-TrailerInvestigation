import numpy as np

ogInitialConditions = {
    "vehicleHeading": np.deg2rad(0),
    "articulation": np.deg2rad(0)
}
testInitialConditions = {
    "vehicleHeading": np.deg2rad(0),
    "articulation": np.deg2rad(0)
}
stabInitialConditions = {
    "vehicleHeading": np.deg2rad(0),
    "articulation": np.deg2rad(1)
}
manInitialConditions = {
    "vehicleHeading": np.deg2rad(0),
    "articulation": np.deg2rad(0)
}
landRoverDimensions = {
    "wheelbase": 2.8,
    "hitchOffset": 1,
    "width": 1.8,
    "length": 4.6,
    "exposedHitch": 0.1,
    "wheelWidth": 0.24,
    "wheelLength": 0.8
}
ogTrailerDimensions = {
    "hitchToAxle": 3,  # For main test will change from 1.5 to 4
    "width": 1.5,
    "length": 3.6,
    "exposedDrawbarLength": 0.5,
    "wheelWidth": 0.2,
    "wheelLength": 0.4
}
testTrailerDimensions = {
    "hitchToAxle": 3,  # For main test will change from 1.5 to 4
    "width": 1.5,
    "length": 3.6,
    "exposedDrawbarLength": 0.5,
    "wheelWidth": 0.2,
    "wheelLength": 0.4
}
ogControls = {
    "speed": -3, # m/s
    "steeringAngle": np.deg2rad(0)
}
testControls = {
    "speed": -1, # m/s
    "steeringAngle": np.deg2rad(0)
}
stabControls = {
    "speed": -3, # m/s
    "steeringAngle": np.deg2rad(0)
}
manControls = {
    "speed": -3, # m/s
    "steeringAngle": np.deg2rad(10)
}
ogSettings = {
    "timeStep": 0.01,
    "totalTime": 10,
    "typeOfTest": "N" # Stability: "S", Manoeuvrability: "M", None: "N"
}
stabSettings = {
    "timeStep": 0.01,
    "totalTime": 60,
    "typeOfTest": "S" # Stability: "S", Manoeuvrability: "M", None: "N"
}
manSettings = {
    "timeStep": 0.01,
    "totalTime": 60,
    "typeOfTest": "M" # Stability: "S", Manoeuvrability: "M", None: "N"
}