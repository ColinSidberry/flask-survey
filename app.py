from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []


@app.get("/")
def render_survey():
    survey_title = survey.title
    survey_instructions = survey.instructions
    return render_template("survey_start.html", 
                            survey_title = survey_title, 
                            survey_instructions = survey_instructions)

@app.post("/begin")
def go_to_questions():

    return redirect("/questions/0") # ToDo: 0 is a placeholder

