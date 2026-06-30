from flask import Flask, render_template, request, redirect, session
from pdf_generator import create_pdf
from flask import send_file
import os

app = Flask(__name__)
app.secret_key = "trip_report"

@app.route("/", methods=["GET", "POST"])
def home():

    if "trips" not in session:
        session["trips"] = []

    if request.method == "POST":

        edit_index = request.form.get("edit_index")

        trip = {
            "date": request.form["date"],
            "work": request.form["work"],
            "amount": request.form["amount"]
        }

        trips = session["trips"]

        if edit_index != "":
            trips[int(edit_index)] = trip
        else:
            trips.append(trip)

        session["trips"] = trips

        return redirect("/")

    return render_template(
    "index.html",
    trips=session["trips"],
    edit_trip=None,
    edit_index=None
)

@app.route("/delete/<int:index>")
def delete(index):

    trips = session["trips"]

    if 0 <= index < len(trips):
        trips.pop(index)

    session["trips"] = trips

    return redirect("/")



@app.route("/edit/<int:index>")
def edit(index):

    trip = session["trips"][index]

    return render_template(
        "index.html",
        trips=session["trips"],
        edit_trip=trip,
        edit_index=index
    )

@app.route("/generate_pdf", methods=["POST"])
def generate_pdf():

    filename = request.form["filename"].strip()

    if not filename:
        filename = "Trip_Report"

    if not filename.lower().endswith(".pdf"):
        filename += ".pdf"

    create_pdf(filename, session["trips"])

    return send_file(
        filename,
        as_attachment=True,
        download_name=filename
    )

@app.route("/clear")
def clear():

    session["trips"] = []
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)