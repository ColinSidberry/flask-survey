from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"

@app.get("/")
def render_survey():
    """Renders the survey starting page.
    """
    return render_template("survey_start.html",
                           survey=survey)


@app.post("/begin")
def go_to_questions():
    """
    Better:
    Sets up empty list of responses and redirects to the first question

    Original:
    Goes to first survey question. and populates the session object 
    at the key of "responses" to an empty list."""

    session[RESPONSES_KEY] = []
    return redirect("/questions/0")


@app.get("/questions/<int:ques_num>")
def ask_questions(ques_num):
    """Displays survey question and choices. If user tries to answer 
    survey questions out of order, redirect them to the correct survey question"""


    #note: have the guard first
    if len(session["responses"]) != ques_num:
        flash("Please answer the questions in order.")
        return redirect(f"/questions/{len(session['responses'])}")
    
    return render_template("question.html",
                               question=survey.questions[ques_num])


@app.post("/answer")
def go_to_next_question():
    """Populates response list with survery answers. 
    If all survey questions are answered, route to completion page."""

    responses = session["responses"]
    responses.append(request.form["answer"])
    session["responses"] = responses

    if len(responses) < len(survey.questions):
        return redirect(f"/questions/{len(responses)}")
    else:
        return redirect("/completion")


@app.get("/completion")
def render_thanks():
    """Renders completions page to thank the user for completing survey."""
    return render_template("completion.html")
