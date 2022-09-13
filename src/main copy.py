from math import floor
from flask import *
import json, time
import csv
import pandas as pd

app = Flask(__name__)

# Data Import
real_data = pd.read_csv(
    "src//data/incoming_data_actual.csv", index_col="currentTimestep"
)
incoming_data_1 = pd.read_csv("src//data/incoming_data_altered_1.csv")
incoming_data_2 = pd.read_csv("src//data/incoming_data_altered_2.csv")
incoming_data_3 = pd.read_csv("src//data/incoming_data_altered_3.csv")
incoming_data_3_1 = pd.read_csv("src//data/incoming_data_altered_3.1.csv")


@app.route("/", methods=["GET"])
def home_page():
    data_set = {}
    json_dump = json.dumps(data_set)

    return json_dump


@app.route("/real/", methods=["GET"])
def real_data_get():
    # timestep_query = str(request.args.get("timestep"))
    time_start_query = int(str(request.args.get("timestart")))

    current_time = time.time()

    time_elapsed = current_time - time_start_query

    row_to_return = real_data.query(f"currentTimestep == {floor(time_elapsed)}")
    # time_start = real_data.query(f"startfrom == {time_start_query}")

    row_to_return_dict = row_to_return.to_dict(orient="index")

    data_set = {
        "timestamp": time.time(),
        "data": row_to_return_dict,
    }
    json_dump = json.dumps(data_set)

    return json_dump


@app.route("/altered1/", methods=["GET"])
def altered1_data_get():
    # timestep_query = str(request.args.get("timestep"))
    time_start_query = int(str(request.args.get("timestart")))

    current_time = time.time()

    time_elapsed = current_time - time_start_query

    row_to_return = incoming_data_1.query(f"currentTimestep == {floor(time_elapsed)}")
    # time_start = real_data.query(f"startfrom == {time_start_query}")

    row_to_return_dict = row_to_return.to_dict(orient="index")

    data_set = {
        "timestamp": time.time(),
        "data": row_to_return_dict,
    }
    json_dump = json.dumps(data_set)

    return json_dump


@app.route("/altered2/", methods=["GET"])
def altered2_data_get():
    # timestep_query = str(request.args.get("timestep"))
    time_start_query = int(str(request.args.get("timestart")))

    current_time = time.time()

    time_elapsed = current_time - time_start_query

    row_to_return = incoming_data_2.query(f"currentTimestep == {floor(time_elapsed)}")
    # time_start = real_data.query(f"startfrom == {time_start_query}")

    row_to_return_dict = row_to_return.to_dict(orient="index")

    data_set = {
        "timestamp": time.time(),
        "data": row_to_return_dict,
    }
    json_dump = json.dumps(data_set)

    return json_dump


@app.route("/altered3/", methods=["GET"])
def altered3_data_get():
    # timestep_query = str(request.args.get("timestep"))
    time_start_query = int(str(request.args.get("timestart")))

    current_time = time.time()

    time_elapsed = current_time - time_start_query

    row_to_return = incoming_data_3.query(f"currentTimestep == {floor(time_elapsed)}")
    # time_start = real_data.query(f"startfrom == {time_start_query}")

    row_to_return_dict = row_to_return.to_dict(orient="index")

    data_set = {
        "timestamp": time.time(),
        "data": row_to_return_dict,
    }
    json_dump = json.dumps(data_set)

    return json_dump


@app.route("/altered4/", methods=["GET"])
def altered4_data_get():
    # timestep_query = str(request.args.get("timestep"))
    time_start_query = int(str(request.args.get("timestart")))

    current_time = time.time()

    time_elapsed = current_time - time_start_query

    row_to_return = incoming_data_3_1.query(f"currentTimestep <= {floor(time_elapsed)}")
    # time_start = real_data.query(f"startfrom == {time_start_query}")

    row_to_return_dict = row_to_return.iloc[-1:].to_dict(orient="index")
    row_to_return_dict = row_to_return_dict[[key for key in row_to_return_dict][-1]]

    data_set = {
        "timestamp": time.time(),
        "data": row_to_return_dict,
    }
    json_dump = json.dumps(data_set)

    return json_dump


if __name__ == "__main__":
    app.run(port=7777)
