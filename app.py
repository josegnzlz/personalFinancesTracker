from flask import Flask, render_template, jsonify, url_for, request, redirect
import pandas as pd
import csv
from main import CSV

app = Flask(__name__)

# Si quiero ponerla en produccion lo puedo hacer en render.com
# Start command tiene que ser: gunicorn app:app (porque app=Flask(__name__))

CSV_FILE = "finance_data.csv"

# Reading finance_data.csv
data = pd.read_csv("finance_data.csv")

# Converting data to a dictionary
data_dict = data.to_dict(orient="records")

@app.route("/")
def home():
    return render_template("home.html", data_entries=data_dict)

@app.route("/newentry")
def newentry():
    return render_template("newentry.html")

@app.route("/submit", methods=["POST"])
def submit():
    if request.method == 'POST':
        date = request.form['date']
        amount = request.form['amount']
        category = request.form['category']
        description = request.form['description']

        CSV.add_entry(date, amount, category, description)

        return redirect('/')

@app.route("/api/financialdata")
def list_data():
    return jsonify(data_dict)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)