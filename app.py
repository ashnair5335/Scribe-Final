from flask import Flask, render_template, jsonify, request
import openai

app = Flask(__name__)

main_instructions = "Your name is Scribe, a helpful teacher's assistant. You know that any information you provide has a chance of being wrong, so you " \
                    "ask the user to double-check with their teacher."

course_category = ("physics", "math", "history", "economics", "biology", "chemistry", "general academics and admissions")

custom_instructions = "Respond like a teacher. Be helpful, but aid the user's learning. You should facilitate the student's learning, but if asked for " \
                      "something like an example, respond with why you should not provide one. Aid the user through the process, but don't lead them " \
                      "directly to the answer. Only respond to questions that are advance the user's knowledge academically."

course_specific_instructions = "Only respond to questions related to " + course_category[2] + ". Provide no information about questions on any other " \
                               "topics and tell them to focus on the current subject only."

def make_response(chat_input):
    openai.api_key = "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"

    print(chat_input)

    completion = openai.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": main_instructions},
            {"role": "system", "content": custom_instructions},
            {"role": "system", "content": course_specific_instructions},
            {"role": "user", "content": chat_input}
        ]
    )
    return completion.choices[0].message.content

response_text = ""

@app.route("/home")
def index():
    return render_template("index.html", response_text=response_text)
@app.route("/login")
def student_login():
    return render_template("studentlogin.html")
@app.route("/login-teacher")
def teacher_login():
    return render_template("teacherlogin.html")
@app.route("/chat")
def chat():
    return render_template("chat.html")
@app.route("/dashboard")
def teacher_home():
    return render_template("teacherhome.html")


@app.route("/process_input", methods=["POST"])
def process_input():
    user_input = request.form["promptTextArea"]
    return jsonify(response_text=make_response(user_input))


if __name__ == "__main__":
    app.run(debug=True)
