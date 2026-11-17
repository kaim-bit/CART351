import os
import secrets
import json
from pathlib import Path
# all import stuff that is needed
from flask import Flask, jsonify, render_template, request, redirect, url_for, session, send_from_directory

app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY") or secrets.token_hex(32) # needed for storage json thing? i had to look up what this does

data_thing = os.path.join(app.instance_path, "survey_saveJ.json")

# the default route
@app.route("/")
def index():
      return render_template("index.html")

@app.route("/first-gif") #image stuff
def first_gif():
    return send_from_directory(os.path.join(app.root_path, "images"), "first-0001.gif")
#image stuff

@app.route("/question-gif/<path:filename>")
def question_gif(filename):
    return send_from_directory(os.path.join(app.root_path, "images"), filename)

#all questions, and the route they will take to the next question aka 1-2 2-3 3-4, etc also gets the answers prepped for the handle question func
@app.route("/QuestionOne.html", methods=["GET", "POST"])
def QuestionOne():
    return handle_question("QuestionOne.html", "question_1_answer", "QuestionTwo")


@app.route("/QuestionTwo.html", methods=["GET", "POST"])
def QuestionTwo():
    return handle_question("QuestionTwo.html", "question_2_answer", "QuestionThree")


@app.route("/QuestionThree.html", methods=["GET", "POST"])
def QuestionThree():
    return handle_question("QuestionThree.html", "question_3_answer", "QuestionFour")


@app.route("/QuestionFour.html", methods=["GET", "POST"])
def QuestionFour():
    return handle_question("QuestionFour.html", "question_4_answer", "QuestionFive")


@app.route("/QuestionFive.html", methods=["GET", "POST"])
def QuestionFive():
    return handle_question("QuestionFive.html", "question_5_answer", "QuestionSix")


@app.route("/QuestionSix.html", methods=["GET", "POST"])
def QuestionSix():
    return handle_question("QuestionSix.html", "question_6_answer", "QuestionSeven")


@app.route("/QuestionSeven.html", methods=["GET", "POST"])
def QuestionSeven():
    return handle_question("QuestionSeven.html", "question_7_answer", "QuestionEight")


@app.route("/QuestionEight.html", methods=["GET", "POST"])
def QuestionEight():
    return handle_question("QuestionEight.html", "question_8_answer", "QuestionNine")


@app.route("/QuestionNine.html", methods=["GET", "POST"])
def QuestionNine():
    return handle_question("QuestionNine.html", "question_9_answer", "QuestionTen")


@app.route("/QuestionTen.html", methods=["GET", "POST"])
def QuestionTen():
    return handle_question("QuestionTen.html", "question_10_answer")

#handles questions as in the name basically shows a question and saves the answer then gives the next question
def handle_question(template_name, answer_key, next_question=None):
    if request.method == "POST":
        session[answer_key] = request.form.get("answer", "").strip() # gets the answer thing

        if next_question:
            return redirect(url_for(next_question)) #loop till no more questions left, if not then the game starts
        return redirect(url_for("game"))

    return render_template( #obv
        template_name,
        answer=session.get(answer_key, "")
    )

# had to look this up, basically the data thing is a file relating to survey responses, and both handles the answers with this 
def load_answers():

    # reads text from the file
    response_text = Path(data_thing).read_text(encoding="utf-8")

    # decode text to py and return
    return json.loads(response_text)


def save_answers(answers):

    # turns answer into json opp of the func above
    response_text = json.dumps(answers, ensure_ascii=False, indent=2)

    # json text to file
    Path(data_thing).write_text(response_text, encoding="utf-8")


#the game
@app.route("/game")
def game():
    #return the last item
    session.pop("game_results", None)

    answers = {
        "Question 1": session.get("question_1_answer", ""),
        "Question 2": session.get("question_2_answer", ""),
        "Question 3": session.get("question_3_answer", ""),
        "Question 4": session.get("question_4_answer", ""),
        "Question 5": session.get("question_5_answer", ""),
        "Question 6": session.get("question_6_answer", ""),
        "Question 7": session.get("question_7_answer", ""),
        "Question 8": session.get("question_8_answer", ""),
        "Question 9": session.get("question_9_answer", ""),
        "Question 10": session.get("question_10_answer", ""),
    }
    return render_template("game.html", answers=answers)


@app.route("/evil/secret", methods=["POST"])
# had to look some of this up to but i will comment it so its undestandable
def survey_save_thing():
    #read answers sent from brow
    request_data = request.get_json()
    answers = request_data["answers"]

    # saves to the json
    save_answers(answers)

    # tells brow the func did its job
    return jsonify(saved=True)


@app.route("/evil/secret/final")
def recieve_surv():
    # sees the answers in the json
    saved_answers = load_answers()

    # sends the answers back in json
    return jsonify(answers=saved_answers)


@app.route("/game/results", methods=["POST"])
def game_results():
    time_alive = request.form.get("time_alive", type = float)
    won = time_alive > 60
    if won:
        # gets rid of everything
        os.remove(data_thing) 

        # clear the browser sesh
        session.pop("question_1_answer", None)
        session.pop("question_2_answer", None)
        session.pop("question_3_answer", None)
        session.pop("question_4_answer", None)
        session.pop("question_5_answer", None)
        session.pop("question_6_answer", None)
        session.pop("question_7_answer", None)
        session.pop("question_8_answer", None)
        session.pop("question_9_answer", None)
        session.pop("question_10_answer", None)

# GAME STUFF
    session["game_results"] = {
        "won": won,
        "time_alive": int(time_alive),
        }
    return redirect(url_for("game_result_page"))


#results for game... duh
@app.route("/game/results")
def game_result_page():
    results = session.get("game_results")

    if results is None:
        return redirect(url_for("game"))
    return render_template("game_results.html", results=results)

app.run()