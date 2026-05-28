from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)

# Secret Key
app.secret_key = os.environ.get("SECRET_KEY", "secret123")


# ---------------- LOGIN PAGE ----------------
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        # Demo Login
        session["logged_in"] = True

        return redirect(url_for("predict"))

    return render_template("login.html")


# ---------------- AQI PREDICTION ----------------
@app.route("/predict", methods=["GET", "POST"])
def predict():

    # Check Login
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    if request.method == "POST":

        try:
            pm25 = float(request.form["pm25"])
            pm10 = float(request.form["pm10"])
            no2  = float(request.form["no2"])
            so2  = float(request.form["so2"])
            co   = float(request.form["co"])
            o3   = float(request.form["o3"])

            # Simple AQI Formula
            aqi = (pm25 + pm10 + no2 + so2 + co + o3) / 6

            return render_template(
                "result.html",
                aqi=round(aqi, 2)
            )

        except Exception as e:
            return f"Error: {e}"

    return render_template("predict.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():

    session.pop("logged_in", None)

    return redirect(url_for("login"))


# ---------------- VERCEL ENTRYPOINT ----------------
app = app


# ---------------- RUN APP ----------------
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

