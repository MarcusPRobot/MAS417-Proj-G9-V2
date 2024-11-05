import os
from openai import OpenAI
from apiKey import API_Shared_Key

# Load environment variables from .env file

# Set up the OpenAI API key
def get_prompt():
    client = OpenAI(
        api_key= API_Shared_Key,
    )

    # Create a chat completion
    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": "Return a random 3D-printable object and a max 10 word description of it, separated by a #. The name can not have any spaces. Ex: 'glassBottle#A blue baby bottle made from glass'",
            }
        ],
    )
    return chat_completion.choices[0].message.content