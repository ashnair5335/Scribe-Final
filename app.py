import subprocess

subprocess.run(["pip", "install", "openai", "flask", "flask_sqlalchemy", "flask_login"])

import openai 
from flask import Flask, render_template, jsonify, request, flash, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import json
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'student_login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    conversation = db.relationship('Conversation', back_populates='user', uselist=False)

class Teacher(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    messages = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = db.relationship('User', back_populates='conversation')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    return render_template("studentlogin.html", response_text=response_text)

@app.route("/login", methods=["GET", "POST"])
def student_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            print(f"[LOGIN] User {username} (ID: {user.id}) logged in.")
            
            # Load existing conversation
            conversation = Conversation.query.filter_by(user_id=user.id).first()
            if conversation:
                response_var.clear()
                response_var.extend(json.loads(conversation.messages))
                print(f"[LOAD] Loaded conversation for user {user.id}: {response_var}")
            else:
                print(f"[LOAD] No conversation found for user {user.id}.")
            
            return redirect(url_for('chat'))
        else:
            flash("Login Unsuccessful. Please check username and password", "danger")
    return render_template("studentlogin.html")

@app.route("/signup-student", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
        else:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash("Account created successfully!", "success")
            return redirect(url_for('student_login'))
    return render_template("studentsignup.html")

@app.route("/login-teacher", methods=["GET", "POST"])
def teacher_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        teacher = Teacher.query.filter_by(username=username).first()
        if teacher and check_password_hash(teacher.password, password):
            login_user(teacher)
            print(f"[LOGIN] Teacher {username} (ID: {teacher.id}) logged in.")
            return redirect(url_for('teacher_home'))
        else:
            flash("Login Unsuccessful. Please check username and password", "danger")
    return render_template("teacherlogin.html")

@app.route("/signup-teacher", methods=["GET", "POST"])
def signup_teacher():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
        else:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_teacher = Teacher(username=username, password=hashed_password)
            db.session.add(new_teacher)
            db.session.commit()
            flash("Account created successfully!", "success")
            return redirect(url_for('teacher_login'))
    return render_template("teachersignup.html")

@app.route("/chat")
@login_required
def chat():
    return render_template("chat.html")

@app.route("/dashboard")
@login_required
def teacher_home():
    # Fetch all users for display
    all_users = User.query.all()
    return render_template("teacherhome.html", all_users=all_users)

@app.route("/fetch_conversation/<int:user_id>")
@login_required
def fetch_conversation(user_id):
    conversation = Conversation.query.filter_by(user_id=user_id).first()
    if conversation:
        messages = json.loads(conversation.messages)
        return jsonify(messages=messages)
    return jsonify(messages=[])

@app.route("/process_input", methods=["POST"])
def process_input():
    user_input = request.form["promptTextArea"]
    return jsonify(response_text=make_response(user_input, response_var))

@app.route("/account")
@login_required
def account():
    return render_template("account.html")

response_var = []

@app.route("/logout")
@login_required
def logout():
    temp_response_var = response_var
    if temp_response_var:  # Save conversation if not empty
        messages_text = json.dumps(response_var)
        conversation = Conversation.query.filter_by(user_id=current_user.id).first()
        if conversation:
            # Update existing conversation
            conversation.messages = messages_text
            conversation.timestamp = datetime.utcnow()
            print(f"[UPDATE] Updated conversation for user {current_user.id}.")
        else:
            # Create new conversation
            conversation = Conversation(user_id=current_user.id, messages=messages_text)
            db.session.add(conversation)
            print(f"[CREATE] Created new conversation for user {current_user.id}.")
        db.session.commit()
        print(f"[SAVE] Conversation for user {current_user.id}: {response_var}")

        log_path = os.path.join(os.path.dirname(__file__), 'conversation_log.txt')
        with open(log_path, "w") as file:
            # Write some text to the file
            file.write(messages_text)

        return send_file(log_path, as_attachment=True)
        
    
    logout_user()
    response_var.clear()
    return redirect(url_for('student_login'))

main_instructions = "Your name is Scribe, a helpful teacher's assistant. You know that any information you provide has a chance of being wrong, so you ask the user to double-check with their teacher."
course_category = ("physics", "math", "history", "economics", "biology", "chemistry", "general academics and admissions")
custom_instructions = "Respond like a teacher. Be helpful, but aid the user's learning. You should facilitate the student's learning, but if asked for something like an example, respond with why you should not provide one. Aid the user through the process, but don't lead them directly to the answer. Only respond to questions that advance the user's knowledge academically."
course_specific_instructions = "Only respond to questions related to " + course_category[0] + ". Provide no information about questions on any other topics and tell them to focus on the current subject only. Whenever you are posed with a question about another subject, respond with the following phrase ONLY (do not do anything else): I'm sorry, but I can't help with that question as it is not in the realm of this subject."
conversational_instructions = "The following is the previous parts of our conversation. Use it to guide the rest of the conversation. For example, if I ask a question with no particular target, assume that I'm talking about the last topic."

response_var.clear()

def make_response(chat_input, previous_inputs):
    openai.api_key = "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"

    print(chat_input)

    completion = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": main_instructions},
            {"role": "system", "content": custom_instructions},
            {"role": "system", "content": course_specific_instructions},
            {"role": "system", "content": conversational_instructions + str(previous_inputs)},
            {"role": "user", "content": chat_input}
        ]
    )

    response_var.append(chat_input)
    response_var.append(completion.choices[0].message.content)

    return completion.choices[0].message.content

response_text = ""

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)