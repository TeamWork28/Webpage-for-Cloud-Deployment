import os
from flask import Flask, request, render_template, redirect, url_for, session
import numpy as np
import pandas as pd

app = Flask(
    __name__,
    static_folder="static",  # Set the static folder explicitly
    template_folder="templates",  # Set the templates folder explicitly
)
app.secret_key = os.environ.get('SECRET_KEY', 'default-secret-key')

class CustomData:
    def __init__(self, gender, branch, parental_level_of_education, test_preparation_course, reading_score, writing_score):
        self.gender = gender
        self.branch = branch
        self.parental_level_of_education = parental_level_of_education
        self.test_preparation_course = test_preparation_course
        self.reading_score = reading_score
        self.writing_score = writing_score

    def get_data_as_dataframe(self):
        data = {
            "gender": [self.gender],
            "branch": [self.branch],
            "parental_level_of_education": [self.parental_level_of_education],
            "test_preparation_course": [self.test_preparation_course],
            "reading_score": [self.reading_score],
            "writing_score": [self.writing_score]
        }
        return pd.DataFrame(data)

class PredictPipeline:
    def predict(self, data_frame):
        # Mock prediction logic: Average of reading and writing scores divided by 2
        reading_score = data_frame["reading_score"].values[0]
        writing_score = data_frame["writing_score"].values[0]
        predicted_score = (reading_score + writing_score) / 2
        return [predicted_score]

# Health check endpoint
@app.route("/health", methods=["GET"])
def health_check():
    return "Health Check OK", 200

# Default route for login
@app.route("/", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Default credentials
        if username == "admin" and password == "admin123":
            session['logged_in'] = True  # Set session
            return redirect(url_for("home_page"))  # Redirect to the homepage
        else:
            return render_template(
                "login.html", error="Invalid username or password"
            )  # Show error on login page

    return render_template("login.html")

@app.route("/homepage", methods=["GET"])
def home_page():
    return render_template("homepage.html")

@app.route("/marks", methods=["GET"])
def marks_page():
    return render_template("marks.html")

@app.route("/studentData", methods=["GET"])
def student_data_page():
    return render_template("studentData.html")

@app.route("/marksComparison", methods=["GET"])
def compare_page():
    return render_template("compare.html")

@app.route("/predictor", methods=["GET", "POST"])
def predict_datapoint():
    if request.method == "POST":
        gender = request.form.get("gender")
        branch = request.form.get("branch")  # Changed form field name from "ethnicity" to "branch"
        parental_level_of_education = request.form.get("parental_level_of_education")
        test_preparation_course = request.form.get("test_preparation_course")
        reading_score = float(request.form.get("reading_score"))
        writing_score = float(request.form.get("writing_score"))

        data = CustomData(
            gender=gender,
            branch=branch,  # Updated keyword from race_ethnicity to branch
            parental_level_of_education=parental_level_of_education,
            test_preparation_course=test_preparation_course,
            reading_score=reading_score,
            writing_score=writing_score,
        )
        pred_df = data.get_data_as_dataframe()
        print(pred_df)

        predict_pipeline = PredictPipeline()
        results = f"{predict_pipeline.predict(pred_df)[0]:.2f}"
        print("After Prediction")

        return render_template(
            "Predictor.html",
            results=results,
            gender=gender,
            branch=branch,  # Passing branch instead of race_ethnicity
            parental_level_of_education=parental_level_of_education,
            test_preparation_course=test_preparation_course,
            reading_score=reading_score,
            writing_score=writing_score,
        )
    return render_template("Predictor.html")

@app.route("/logout", methods=["GET"])
def logout():
    session.pop("logged_in", None)  # Clear session
    return redirect(url_for('login_page'))  # Redirect to login page

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)