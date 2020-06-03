from flask import Flask, render_template , render_template_string, jsonify
import plotly
import plotly.graph_objs as go
import json
import numpy as np
import requests
from time import sleep
import datetime
import pandas as pd
import plotly.express as px


app = Flask(__name__)

host_URL = "http://flaskosa.herokuapp.com/cmd/"
logs = []
global_dataFrame = pd.DataFrame(columns=["X","Y","count"])
index = 1

def add_logs(log):
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    logs.append(time + log)

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route("/plot")
def plot_graph():
    return get_trace_data()

@app.route("/logs")
def get_logs():
    print(logs)
    return jsonify(logs)

@app.route("/singleTrace")
def set_single_trace():
    #SINGLE:OK
    try_until_proper_resp(host_URL + "SINGLE" , "SINGLE")
    return get_trace_data()

@app.route("/start")
def start_osa():
    return try_until_proper_resp(host_URL + "START", "START")

@app.route("/stop")
def stop_osa():
    try_until_proper_resp(host_URL + "STOP", "STOP")
    return get_trace_data()

def try_until_proper_resp(url,type):
    add_logs(url)
    req_response = None
    try:
        if type == "json":
            req_response = requests.get(url)
            req_response = req_response.json()
            add_logs("SUCCESS")
            return req_response
        else:
            req_response = requests.get(url)
            req_response = str(req_response.content,"utf-8")
            if "READY" in req_response:
                add_logs(req_response)
                return req_response
            else:
                add_logs("ERROR")
                try_until_proper_resp(url, type)
    except Exception as e:
        sleep(1)
        print(e)
        add_logs("ERROR")
        try_until_proper_resp(url,type)

@app.route("/api/cmd", defaults={'query': None})
@app.route("/api/cmd/", defaults={'query': None})
@app.route("/api/cmd/<path:query>")
def run_query(query):
    url = host_URL + (query if query else "")
    print(url)
    add_logs(url)
    req_response = requests.get(url)
    if query == "TRACE":
        try:
            req_response = req_response.json()
            add_logs("SUCCESS")
        except Exception as e:
            return {},503
    else:
        req_response = str(req_response.content,"utf-8")
        if "READY" not in req_response:
            if "ERROR" not in req_response:
                req_response="ERROR: Unavailable"
            add_logs(req_response)
            return json.dumps(req_response), 503
        add_logs(req_response)
    return req_response



def get_trace_data():
    static_data = {}
    try:
        trace_response = try_until_proper_resp(host_URL + "TRACE","json")
    except Exception as e:
        system_state = requests.get(host_URL + "/STATE")
        static_data["Y"] = []
        static_data["X"] = []
        return construct_graph(static_data)

    static_data["Y"] = trace_response["ydata"]
    x_data = trace_response["xdata"]
    x_np_array = np.array(x_data)
    x_np_array = 1000000000 * x_np_array
    static_data["X"] = x_np_array
    local_dataFrame = pd.DataFrame(data=static_data)
    global index
    print("index")
    print(index)
    global global_dataFrame
    if index == 1:
        local_dataFrame["trials"] = index
        global_dataFrame = local_dataFrame
    else:
        if index <= 3:
            local_dataFrame["trials"] = index
            global_dataFrame = global_dataFrame.append(local_dataFrame)
        else:
            index = 1
            local_dataFrame["trials"] = index
            global_dataFrame = local_dataFrame
    index = index + 1
    print(local_dataFrame)
    print(global_dataFrame)
    return construct_graph(global_dataFrame)


def construct_graph(data):
    # fig = go.Figure(data=go.Scatter(x=data["X"], y=data["Y"]))
    fig = px.line(data, x="X", y="Y", color="trials")
    fig.update_layout(title="OSA", xaxis_title="Wavelength in nm",yaxis_title="Signal in dBm")
    return plotly.offline.plot(fig, output_type='div', include_plotlyjs=True)

if __name__ == '__main__':
    app.run(debug=True)
