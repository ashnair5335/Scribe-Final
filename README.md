# Scribe - an AI Tool for Education

Scribe is a ChatGPT-powered solution that allows students to use AI to aid their learning process without impacting their learning experience, creativity, or productivity negatively.

## Setup Instructions

To start, you need two modules: Flask and OpenAI.

Flask is the module that allows HTML, CSS, and JS files to be connected to and call functions from a Python file. Install using pip:

```bash
pip install flask
```

OpenAI is the module that allows calling the ChatGPT API. Install using pip:

```bash
pip install openai
```

Another aspect of the setup process is selecting the course focus for Scribe. This will eventually be done through a button on the UI, and then into an automated process that occurs when a student logs in with the teacher-provided key.

But for now, open ```app.py``` and find the following line:

```python
course_specific_instructions = "Only respond to questions related to " + course_category[2] + ". Provide no information about questions on any other topics and tell them to focus on the current subject only."
```

If you look a bit before, you will see the following line:

```python
course_category = ("physics", "math", "history", "economics", "biology", "chemistry")
```

Find the index of the topic you want to ask about and edit the index in ```course_category[2]``` to the new index.

Also, find the following line:

```python
    openai.api_key = "PLACEHOLDER_API_KEY"
```

Replace ```PLACEHOLDER_API_KEY``` with your personal paid-for key.

You should be all set to test Scribe!
