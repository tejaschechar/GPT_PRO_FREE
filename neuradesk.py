# step 1 install python 3.10 best for Gen AI projects, 3.11 2nd best,
#  higher versions may have compatibility issues with some libraries

# Step 2 create a virtual environment for your project -- py -3.10 -m venv venv

# Step 3 activate the virtual environment -- venv\Scripts\activate

# step 4 upgrade pip -- python.exe -m pip install --upgrade pip

# step 5 install git -- https://git-scm.com/downloads

# step 6 install ollama -- https://ollama.com/docs/installation

#install the required libraries for the project

# mkdir app   -- create a folder named app in the project directory
#ni app/main.py -- create a file named main.py in the app folder
'''
mkdir app
ni app/main.py
mkdir llm
ni llm/ollama.py
mkdir config
ni config/config.py
'''


#Create .env file:
'''n .env

Add:
MODEL_NAME=llama3
ENV=dev

🔥 Load env in Python

from dotenv import load_dotenv
import os
load_dotenv()
model = os.getenv("MODEL_NAME")

💡 Why this matters:
Later you can:
    switch models easily
    add API keys
    deploy safely    '''
