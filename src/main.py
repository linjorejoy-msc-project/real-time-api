from math import floor
from flask import *
import json, time
import csv
import pandas as pd

app = Flask(__name__)

# Data Import
filenames = [
    "src//data/incoming_data_actual.csv",
    "src//data/incoming_data_altered_1.csv",
    "src//data/incoming_data_altered_2.csv",
    "src//data/incoming_data_altered_3.csv",
    "src//data/incoming_data_altered_3_1.csv",
    "src/data/data_altered_4.csv",
    "src/filtered_data/data_altered_4.csv",
]

data_df = pd.read_csv(filenames[6])

data_cols = [
    "currentTimestep",
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


@app.route("/data/", methods=["GET"])
def data_get():
    # Get parameter 'timestart' which will indicate
    # the start time of the simulation
    time_start_query = int(str(request.args.get("timestart")))

    # Comparing with current device time and finding tme elapsed
    current_time = time.time()
    time_elapsed = current_time - time_start_query

    # Querying into the dataset to get the latest data
    row_to_return = data_df[data_cols].query(
        f"currentTimestep <= {floor(time_elapsed)}"
    )

    # Formatting the queried data to appropriate format
    row_to_return_dict = row_to_return.iloc[-1:].to_dict(orient="index")
    row_to_return_dict = row_to_return_dict[[key for key in row_to_return_dict][-1]]

    # Converting it into a JSON format for API response
    data_set = {
        "timestamp": time.time(),
        "data": row_to_return_dict,
    }
    json_dump = json.dumps(data_set)

    return json_dump


if __name__ == "__main__":
    app.run(port=7777, host="192.168.1.2")
