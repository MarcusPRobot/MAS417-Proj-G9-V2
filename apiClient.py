import os
from openai import OpenAI

# apiKey is ignored in gitignore. To try the script yourself you can put your ChatGPT API
# key in a apiKey.py script in the "API_Shared_Key" variable. Nothing else is needed.
from apiKey import API_Shared_Key

initPrompt = ("Return a random 3D-printable marvel superhero with a max 10 word description of it, "
              "separated by a #. The name can not have any spaces. "
              "Ex: 'Superman#Superman from the newest movies'")

def get_prompt():
    client = OpenAI(
        api_key= API_Shared_Key,
    )
    apiHistory_file = open("API Logs.txt", "r")
    apiHistory = apiHistory_file.read()

    try:
        chatCompletion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": apiHistory + "\n Here is the prompt:\n" + initPrompt,
                }
            ],
        )
    except Exception as error:
        print("An error occurred: " + error)
        return

    apiHistory_file.close()
    return chatCompletion.choices[0].message.content