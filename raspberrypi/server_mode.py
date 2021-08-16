# MIT License

# Copyright (c) 2021 jonyboi396825

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import datetime
import json
import os
from copy import deepcopy

import pytz
import requests
from flask import Flask, jsonify, redirect, render_template, request

need_update = False
cur_version_f = open("VERSION", 'r')
cur_version = cur_version_f.read().strip()
cur_version_f.close()

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home_page():
    global need_update, cur_version

    return render_template("index.html", need_update=need_update, success=True, v=cur_version)


@app.route("/cfg", methods=["GET", "POST"])
def cfg_page():
    if (request.method == 'POST'):
        a = request.form.to_dict()
        f = open("raspberrypi/cfg.json", 'w')

        for key in a:
            try:
                a[key] = int(a[key])
            except ValueError:
                pass

        json.dump(a, f)
        f.close()

        return redirect("/cfg_saved")
    else:
        return render_template("cfg.html")


@app.route("/cfg_saved", methods=["GET"])
def cfg_saved_page():
    return render_template("cfg_saved.html")

@app.route("/cfg/raw", methods=["GET"])
def cfg_raw_page():
    cfgs = {}

    # read from cfg.json and put in cfgs
    with open("raspberrypi/cfg.json", 'r') as f:
        cfgs = json.load(f)

    return jsonify(cfgs)

@app.route("/tzs", methods=["GET"])
def tzs_page():
    return render_template("tzs.html")

@app.route("/tzs/raw", methods=["GET"])
def tzs_raw_page():
    # api for all timezones
    return jsonify(pytz.common_timezones)

@app.route("/map", methods=["GET"])
def map_page():
    # displays links to files of maps

    def _conv_filename(name):
        if (name.strip().upper() == "ERROR"):
            return "Error file, delete me!"
        else:
            _dt = datetime.datetime.strptime(name, "%Y-%m-%d_%H:%M:%S_track_path")
            s = datetime.datetime.strftime(_dt, "Started tracking at: %Y-%m-%d %H:%M:%S")
            return s

    # get all track files
    filenames = next(os.walk("tracking"), (None, None, []))[2]
    filenames.sort()

    oldf = deepcopy(filenames)
    filenames = [_conv_filename(name) for name in filenames]
    filenames = [filenames, oldf]

    return render_template("map_main.html", filenames=filenames)

@app.route("/map/<f_name>", methods=["GET"])
def map_file_page(f_name) -> None:
    # displays maps themselves

    # get track files and contents
    filenames = next(os.walk("tracking"), (None, None, []))[2]
    if (f_name not in filenames):
        return ("Track file not found", 400)

    f = open(os.path.join("tracking", f_name), 'r')
    track_str = f.read()
    f.close()

    # see if track file is valid
    track_arr = track_str.rstrip().split('\n')
    while (len(track_arr) > 0 and (track_arr[-1] == "PAUSED" or track_arr[-1] == "")):
        track_arr.pop()

    is_valid = len(track_arr) > 0

    # get cfg units
    f = open("raspberrypi/cfg.json", 'r')
    unit = json.load(f)["UNT"]
    f.close()

    return render_template("map.html", tracking=track_str, unit=unit, valid=is_valid)

@app.route("/map/combine", methods=["GET", "POST"])
def combine_map_page():
    def _conv_filename(name):
        if (name.strip().upper() == "ERROR"):
            return "Error file, delete me!"
        else:
            _dt = datetime.datetime.strptime(name, "%Y-%m-%d_%H:%M:%S_track_path")
            s = datetime.datetime.strftime(_dt, "Started tracking at: %Y-%m-%d %H:%M:%S")
            return s

    # get all track files
    filenames = next(os.walk("tracking"), (None, None, []))[2]
    filenames.sort()

    oldf = deepcopy(filenames)
    filenames = [_conv_filename(name) for name in filenames]
    filenames = [filenames, oldf]

    if (request.method == "GET"):
        return render_template("combine.html", filenames=filenames)
    else:
        files = json.loads(request.data.decode("utf-8"))["files"]

        s_total = ""
        f_name_final = oldf[int(files[0])]
        print(f_name_final)
        for i in files:
            ind = int(i)
            f_name = os.path.join("tracking", oldf[ind])

            if (str(i) != files[-1]):
                with open(f_name, 'a') as f:
                    f.write("PAUSED\n")

            with open(f_name, 'r') as f:
                s_total += f.read()

            os.remove(f_name)

        with open(os.path.join("tracking", f_name_final), 'w') as f:
            f.write(s_total)

        return ("Successfully combined", 200)

@app.route("/map/delete/<f_name>", methods=["POST"])
def delete_map_endpt(f_name):
    # delete file

    filenames = next(os.walk("tracking"), (None, None, []))[2]
    if (f_name not in filenames):
        return ("File not found", 400)

    os.remove(os.path.join("tracking", f_name))
    return ("Successfully removed", 200)


def check_for_update() -> None:
    global need_update, cur_version

    response = requests.get("https://raw.githubusercontent.com/jonyboi396825/BikeDashboardPlus/master/VERSION")
    need_update = not (response.text.strip() == cur_version)


def main() -> None:
    check_for_update()
    app.run(host="0.0.0.0", port=7123, debug=True)


if (__name__ == "__main__"):
    main()
