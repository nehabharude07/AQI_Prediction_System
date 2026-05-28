id="u0a29n"
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secret123"

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        session["logged_in"] = True
        return redirect(url_for("predict"))

    return render_template("login.html")


@app.route("/predict", methods=["GET", "POST"])
def predict():

    if not session.get("logged_in"):
        return redirect(url_for("login"))

    if request.method == "POST":

        pm25 = float(request.form["pm25"])
        pm10 = float(request.form["pm10"])
        no2  = float(request.form["no2"])
        so2  = float(request.form["so2"])
        co   = float(request.form["co"])
        o3   = float(request.form["o3"])

        aqi = (pm25 + pm10 + no2 + so2 + co + o3) / 6

        return render_template(
            "result.html",
            aqi=round(aqi, 2)
        )

    return render_template("predict.html")


@app.route("/logout")
def logout():

    session.pop("logged_in", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run()

