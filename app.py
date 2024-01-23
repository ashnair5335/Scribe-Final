from flask import Flask, render_template, jsonify, request
import openai
# import markdown2
# from bs4 import BeautifulSoup

app = Flask(__name__)

custom_instructions = "Respond like a teacher. Be helpful, but aid the user's learning. You should facilitate the student's learning, but if asked for something like an example, respond with why you should not provide one. Aid the user through the process, but don't lead them directly to the answer."

def make_response(chat_input):
    openai.api_key = "API_PLACEHOLDER_KEY"

    print(chat_input)

    completion = openai.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": custom_instructions},
            {"role": "user", "content": chat_input}
        ]
    )
    return completion.choices[0].message.content

response_text = ""

# final_text = BeautifulSoup(markdown2.markdown(response_text), 'html.parser')
# for bold_tag in final_text.find_all('strong'):
#     bold_tag['style'] = 'font-weight: bold;'

@app.route("/")
def index():
    return render_template("index.html", response_text=response_text)


@app.route("/process_input", methods=["POST"])
def process_input():
    user_input = request.form["promptTextArea"]

    # return response based on user_input

    return jsonify(response_text=make_response(user_input))


if __name__ == "__main__":
    app.run(debug=True)
