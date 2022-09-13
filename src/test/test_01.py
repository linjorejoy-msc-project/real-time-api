from math import floor
from flask import *
import json, time
import csv
import pandas as pd

app = Flask(__name__)

# Data Import

file_name = "data_altered_4.csv"

data_df = pd.read_csv(f"src/data/{file_name}", index_col=["currentTimestep"])
filtered_file = f"src/filtered_data/{file_name}"

data_cols = [
    "currentTime",
    "totalTimestepsRun",
    "versions",
    "currentMassFlowRate",
    "currentOxidiserMass",
    "currentFuelMass",
    "currentRocketTotalMass",
    "netThrust",
    "currentAcceleration",
    "currentVelocityDelta",
    "currentVelocity",
    "currentAltitudeDelta",
    "currentAltitude",
    "requiredThrustChange",
]


data_df[data_cols].query(f"currentTimestep == 1 or currentTimestep % 20 == 0").to_csv(
    filtered_file
)
