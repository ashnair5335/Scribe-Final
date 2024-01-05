import openai

# optional; defaults to `os.environ['OPENAI_API_KEY']`
openai.api_key = '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'

usr_in = input("Ask Scribe: ")
print(usr_in)

completion = openai.chat.completions.create(
    model="gpt-4-1106-preview",
    messages=[
        {
            "role": "user",
            "content": usr_in,
        },
    ],
)
response = completion.choices[0].message.content