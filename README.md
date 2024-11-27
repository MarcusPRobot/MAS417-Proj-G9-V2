# AI-Based idea to model generation tool | MAS417-Proj-G9-V2
## Introduction
This github repository includes a Python 3.12 project, that uses two APIs to get random 3D-Model ideas from OpenAI's ChatGPT, and to use the given model idea to create a 3D-model using Meshy.AI.

Using this project requires that the user aquires his own API keys for both OpenAIs API platform and for Meshy.AI.

## Project information
MAS-417 project made and developed by Marcus Wold and Ole-Morten Nyheim.

This is the seccond repository, which is why it is called V2. V1 did only have one commit so it will not be linked here.

## Project setup
Install Python 3.12

The project does not need any other software to work, all it needs is a few Python packages which can be installed using:

`pip install <package>`

Example:

`pip install openai`

Every missing package will be listed in CMD when trying to run the project, and it is reccomended to download the packages whilst Pythons virtual environment is activated. The virtual environment can be activated whilst inside the root of the directory by going into CMD and using:

`.venv\Scripts\Activate.ps1`

The final step is to create a new python script within the environment called "apiKey.py", and writing these two lines of code into the "apiKey.py" script:

`API_Shared_Key = "Replace with API key from OpenAI Platform" #OpenAI`

`Meshy_APIKey = "Replace with API key from Meshy.AI" #Meshy.ai`

Make sure the actual API keys are replacing the instructions in the provided lines of code. When completed, the code should be ready to go.




