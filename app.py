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
    """Renders the survey starting page and clears previous responses."""
    responses.clear()
    survey_title = survey.title
    survey_instructions = survey.instructions
    #could also just pass in servey and refer to it in html
    return render_template("survey_start.html", 
                            survey_title = survey_title, 
                            survey_instructions = survey_instructions)

@app.post("/begin")
def go_to_questions():
    """Goes to first survey question."""
    return redirect("/questions/0")

@app.get("/questions/<int:ques_num>")
def ask_questions(ques_num):
    """Displays survey question and choices."""
    survey_question= survey.questions[ques_num]
    question_choices= survey_question.choices
    return render_template("question.html", 
                            choices = question_choices,
                            question = survey_question)

@app.post("/answer")
def go_to_next_question():
    """Populates response list with survery answers. If all survey questions are answered, route to completion page."""
    responses.append(request.form["answer"])
    if len(responses)<len(survey.questions):
        return redirect(f"/questions/{len(responses)}")
    else:
        return redirect("/completion")

@app.get("/completion")
def render_thanks():
    """Renders completions page to thank the user for completing survey."""
    return render_template("completion.html")

