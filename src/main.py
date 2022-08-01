from flask import *
import json, time
import csv
import pandas as pd

app = Flask(__name__)

# Data Import
real_data = pd.read_csv("src//data/incoming_data_actual.csv")
incoming_data_1 = pd.read_csv("src//data/incoming_data_actual.csv")
incoming_data_2 = pd.read_csv("src//data/incoming_data_actual.csv")


@app.route("/", methods=["GET"])
def home_page():
    data_set = {"Page": "Home", "Message": "Hi", "Timestamp": time.time()}
    json_dump = json.dumps(data_set)

    return json_dump


@app.route("/real/", methods=["GET"])
def real_data_get():
    user_query = str(request.args.get("timestep"))

    row_to_return = real_data.query(f"currentTimestep == {user_query}")

    row_to_return_dict = row_to_return.to_dict()

    data_set = {
        "Page": "Home",
        "Message": "Hi",
        "Timestamp": time.time(),
        "Data": row_to_return_dict,
    }
    json_dump = json.dumps(data_set)

    return json_dump


if __name__ == "__main__":
    app.run(port=7777)
