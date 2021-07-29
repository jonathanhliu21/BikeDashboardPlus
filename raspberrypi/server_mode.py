"""
MIT License

Copyright (c) 2021 jonyboi396825

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import json
import os
from copy import deepcopy

import pytz
from flask import Flask, jsonify, redirect, render_template, request

app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template("index.html")


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


@app.route("/cfg_saved")
def cfg_saved_page():
    return render_template("cfg_saved.html")


@app.route("/tzs")
def tzs_page():
    return render_template("tzs.html")

@app.route("/tzs/raw")
def tzs_raw_page():
    return jsonify(pytz.common_timezones)

@app.route("/map")
def map_page():
    # displays links to files of maps
    
    def _conv_filename(name):
        return ("Started tracking at: " + name[0:4]+"-"+name[5:7]+"-"+name[8:10]+" "+name[11:13]+":"+name[14:16]+":"+name[17:19])

    # get all track files
    filenames = next(os.walk("tracking"), (None, None, []))[2]
    filenames.sort()

    oldf = deepcopy(filenames)
    filenames = [_conv_filename(name) for name in filenames]
    filenames = [filenames, oldf]

    return render_template("map_main.html", filenames=filenames)

@app.route("/map/<f_name>")
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

    return render_template("map.html", tracking=track_str, unit=unit, valid=is_valid)

@app.route("/map/combine", methods=["GET", "POST"])
def combine_map_page():
    def _conv_filename(name):
        return ("Started tracking at: " + name[0:4]+"-"+name[5:7]+"-"+name[8:10]+" "+name[11:13]+":"+name[14:16]+":"+name[17:19])

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


def main() -> None:
    app.run(host="0.0.0.0", port=5000, debug=True)


if (__name__ == "__main__"):
    main()
