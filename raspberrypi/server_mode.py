from flask import Flask, render_template, redirect, request
import json

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
    return render_template("map.html")

def main() -> None:
    app.run(host = "0.0.0.0", port=5000, debug=True)

if (__name__ == "__main__"):
    main()

