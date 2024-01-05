from flask import Flask, render_template, jsonify, request
import GPT

app = Flask(__name__)

# Initialize with a default response
response_text = "Your OpenAI API response here"

@app.route('/')
def index():
    return render_template('index.html', response_text=response_text)

@app.route('/get_response', methods=['GET'])
def get_response():
    return jsonify(response_text=GPT.response)

@app.route('/process_input', methods=['POST'])
def process_input():
    user_input = request.form['userInput']

    # Use the user input to generate a response (replace this with your OpenAI API call)
    # For demonstration purposes, let's just echo the user input.
    response_text = f"You asked: {user_input}"

    return jsonify(response_text=response_text)

if __name__ == '__main__':
    app.run(debug=True)


# from flask import Flask, render_template, request, jsonify
# import openai
# import GPT
#
# app = Flask(__name__)
#
# @app.route('/')
# def index():
#
#     return render_template('index.html')
#
# # Route to handle chat interactions
# @app.route('/chat', methods=['POST'])
# def chat():
#     user_input = request.form['user_input']
#     # GPT API usage for response eventually
#     response = GPT.response
#     return jsonify({'usr_in': user_input}, {'response': response})
#
# @app.route('/get_response', methods=['GET'])
# def get_response():
#     return jsonify(response_text=GPT.response)
#
# if __name__ == '__main__':
#     app.run(debug=True)
