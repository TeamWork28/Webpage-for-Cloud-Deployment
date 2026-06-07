import os
import logging
from flask import Flask, request, render_template, redirect, url_for, session

# Import pipeline classes
from src.pipeline.predict_pipeline import PredictPipeline, CustomData

# Configure logging
logging.basicConfig(
    filename='/var/log/flask-app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates",
)
app.secret_key = 'your_secret_key_here'

@app.route("/", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "admin" and password == "admin123":
            session['logged_in'] = True
            logger.info(f"Successful login - username: {username}")
            return redirect(url_for("home_page"))
        else:
            logger.warning(f"Failed login attempt - username: {username}")
            return render_template("login.html", error="Invalid username or password")
    return render_template("login.html")

@app.route("/homepage", methods=["GET"])
def home_page():
    logger.info("Homepage accessed")
    return render_template("homepage.html")

@app.route("/marks", methods=["GET"])
def marks_page():
    logger.info("Marks page accessed")
    return render_template("marks.html")

@app.route("/studentData", methods=["GET"])
def student_data_page():
    logger.info("Student data page accessed")
    return render_template("studentData.html")

@app.route("/marksComparison", methods=["GET"])
def compare_page():
    logger.info("Marks comparison page accessed")
    return render_template("compare.html")

@app.route("/predictor", methods=["GET", "POST"])
def predict_datapoint():
    if request.method == "POST":
        gender = request.form.get("gender")
        original_ethnicity = request.form.get("ethnicity")
        if original_ethnicity == "CSE":
            race_ethnicity = "group A"
        elif original_ethnicity == "ECE":
            race_ethnicity = "group B"
        else:
            race_ethnicity = original_ethnicity

        parental_level_of_education = request.form.get("parental_level_of_education")
        lunch = request.form.get("course_type")
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
        predict_pipeline = PredictPipeline()
        results = f"{predict_pipeline.predict(pred_df)[0]:.2f}"
        logger.info(f"Prediction made - gender: {gender}, ethnicity: {original_ethnicity}, result: {results}")

        return render_template(
            "Predictor.html",
            results=results,
            gender=gender,
            race_ethnicity=original_ethnicity,
            course_type=lunch,
            test_preparation_course=test_preparation_course,
            reading_score=reading_score,
            writing_score=writing_score,
        )
    return render_template("Predictor.html")

@app.route("/logout", methods=["GET"])
def logout():
    session.pop("logged_in", None)
    logger.info("User logged out")
    return redirect(url_for('login_page'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)