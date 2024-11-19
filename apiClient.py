import os
from openai import OpenAI

# apiKey is ignored in gitignore. To try the script yourself you can put your ChatGPT API
# key in a apiKey.py script in the "API_Shared_Key" variable. Nothing else is needed.
from apiKey import API_Shared_Key

initPrompt = ("Return a random 3D-printable simple object and a max 15 word description of it, "
              "separated by a #. Keep the models with simple geometry "
              "that is easy for the AI to make; explain geometry and texture and "
              "not what the item is called. The name can not have any spaces. "
              "Ex: 'fidget_spinner#Red standard fidgetspinner with 3 arms'")

def get_prompt():
    client = OpenAI(
        api_key= API_Shared_Key,
    )
    apiHistory_file = open("API Logs.txt", "r")
    apiHistory = apiHistory_file.read()
    chatCompletion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": apiHistory + "\n Here is the prompt:\n" + initPrompt,
            }
        ],
    )
    apiHistory_file.close()
    return chatCompletion.choices[0].message.content