import os
from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(
    __name__,
    static_folder="static",  # Set the static folder explicitly
    template_folder="templates",  # Set the templates folder explicitly
)
app.secret_key = 'your_secret_key_here'  # Added secret key for session management

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
        race_ethnicity = request.form.get("ethnicity")
        parental_level_of_education = request.form.get("parental_level_of_education")
        lunch = request.form.get("lunch")
        test_preparation_course = request.form.get("test_preparation_course")
        reading_score = float(request.form.get("reading_score"))
        writing_score = float(request.form.get("writing_score"))

        data = CustomData(
            gender=gender,
            race_ethnicity=race_ethnicity,
            parental_level_of_education=parental_level_of_education,
            lunch=lunch,
            test_preparation_course=test_preparation_course,
            reading_score=reading_score,
            writing_score=writing_score,
        )
        pred_df = data.get_data_as_data_frame()
        print(pred_df)

        predict_pipeline = PredictPipeline()
        results = f"{predict_pipeline.predict(pred_df)[0]:.2f}"
        print("After Prediction")

        return render_template(
            "Predictor.html",
            results=results,
            gender=gender,
            race_ethnicity=race_ethnicity,
            parental_level_of_education=parental_level_of_education,
            lunch=lunch,
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
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)