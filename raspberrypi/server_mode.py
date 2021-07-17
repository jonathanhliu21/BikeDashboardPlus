from copy import deepcopy
import json
import os

from flask import Flask, redirect, render_template, request

app = Flask(__name__)


@app.route("/")
def home_page() -> None:
    return render_template("index.html")


@app.route("/cfg", methods=["GET", "POST"])
def cfg_page() -> None:
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
def cfg_saved_page() -> None:
    return render_template("cfg_saved.html")


@app.route("/tzs")
def tzs_page() -> None:
    return render_template("tzs.html")


@app.route("/map")
def map_page() -> None:
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
    f = open(os.path.join("tracking", f_name), 'r')
    track_str = f.read()
    f.close()

    f = open("raspberrypi/cfg.json", 'r')
    unit = json.load(f)["UNT"]

    return render_template("map.html", tracking=track_str, unit=unit)

# @app.route("/static/<img>", methods=["GET"])
# def get_img(img):
#     pass


def main() -> None:
    app.run(host="0.0.0.0", port=5000, debug=True)


if (__name__ == "__main__"):
    main()
