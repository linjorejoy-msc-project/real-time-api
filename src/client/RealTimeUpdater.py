import socket
import threading

# import pandas as pd

from common_functions import (
    check_to_run_cycle,
    drag_received,
    field_received,
    format_msg_with_header,
    fuel_flow_received,
    make_all_cycle_flags_default,
    motion_received,
    recv_msg,
    recv_topic_data,
    request_constants,
    send_config,
    send_topic_data,
    thrust_received,
)

# Logging
import logging
import os


class ClientVisualizationClass:
    def __init__(self) -> None:
        self.file_path = os.path.join(
            os.path.abspath(os.curdir), "src\\client_main\\LOGS"
        )

        self.FORMAT = "%(levelname)-10s %(asctime)s: %(message)s"
        logging.basicConfig(
            handlers=[
                logging.FileHandler(
                    filename="logs_visualization.log", encoding="utf-8", mode="w"
                )
            ],
            level=logging.DEBUG,
            format=self.FORMAT,
        )

        self.HEADERSIZE = 5
        self.CONFIG_DATA = {
            "id": "CLIENT_8",
            "name": "realtimeupdation",
            "subscribed_topics": ["field"],
            "published_topics": ["update_motion"],
            "constants_required": ["timestepSize"],
            "variables_subscribed": [],
        }

        self.server_socket: socket.socket = None  #

        self.CONSTANTS = {}

        self.cycle_flags = {
            "field": False,
        }
        self.topic_func_dict = {
            "field": field_received,
        }

        # to store data received
        self.data_dict = {}

        self.all_data_list = []

        # self.all_data = {}
        self.all_data_seperated_dict = {}
        # self.all_data_df = pd.DataFrame()
        self.convert_df_period = 5
        self.current_period_cycle = 0

    def run_one_cycle(self):
        # global data_dict
        # self.all_data[self.data_dict["currentTimestep"]] = self.data_dict.copy()

        for each_key in self.data_dict.keys():
            if each_key in self.all_data_seperated_dict.keys():
                self.all_data_seperated_dict[each_key].append(self.data_dict[each_key])
            else:
                self.all_data_seperated_dict[each_key] = [self.data_dict[each_key]]

        # self.all_data_list.append(self.data_dict.copy())
        # self.current_period_cycle += 1
        # if self.current_period_cycle == self.convert_df_period:
        #     self.all_data_df = pd.DataFrame.from_dict(self.all_data_list)
        #     self.current_period_cycle = 0
        # self.all_data_df = pd.concat(
        #     [
        #         self.all_data_df,
        #         pd.DataFrame(self.data_dict, index=[self.data_dict["currentTimestep"]]),
        #     ]
        # )
        # self.all_data_df = self.all_data_df.append(self.data_dict, ignore_index=True)
        logging.debug(
            f"Timestep: {self.data_dict['currentTimestep']:5}-{self.data_dict}"
        )
        # print(f"Timestep: {self.data_dict['currentTimestep']:5}-{self.data_dict}")

    def run_cycle(self):
        # global cycle_flags
        while True:
            if check_to_run_cycle(self.cycle_flags):
                make_all_cycle_flags_default(self.cycle_flags)
                self.run_one_cycle()

    def listen_analysis(self):
        # global data_dict
        # global cycle_flags
        logging.info(f"Started Listening for analysis")
        while True:
            topic, sent_time, recv_time, info = recv_topic_data(self.server_socket)
            if topic in self.cycle_flags.keys():
                self.cycle_flags[topic] = True
                self.topic_func_dict[topic](self.data_dict, sent_time, recv_time, info)
            else:
                logging.error(
                    f"{self.CONFIG_DATA['name']} is not subscribed to {topic}"
                )

    # Helper Functions

    def listening_function(self, server_socket):
        # global CONFIG_DATA
        # global CONSTANTS

        while True:
            try:
                msg = recv_msg(server_socket)
                if msg == "CONFIG":
                    send_config(server_socket, self.CONFIG_DATA)
                    self.CONSTANTS = request_constants(server_socket)
                elif msg == "START":
                    analysis_listening_thread = threading.Thread(
                        target=self.listen_analysis
                    )
                    analysis_listening_thread.start()
                    break
            except Exception as e:
                logging.error(f"listening_function error: {str(e)}")
                break
        self.run_cycle()

    def main(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.server_socket.connect(("192.168.1.2", 1234))
        self.server_socket.connect(("localhost", 1234))

        listening_thread = threading.Thread(
            target=self.listening_function, args=(self.server_socket,)
        )

        listening_thread.start()


if __name__ == "__main__":
    obj = ClientVisualizationClass()
    obj.main()
