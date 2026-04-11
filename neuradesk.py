# step 1 install python 3.10 best for Gen AI projects, 3.11 2nd best,
#  higher versions may have compatibility issues with some libraries

# Step 2 create a virtual environment for your project -- py -3.10 -m venv venv

# Step 3 activate the virtual environment -- venv\Scripts\activate

# step 4 upgrade pip -- python.exe -m pip install --upgrade pip

# step 5 install git -- https://git-scm.com/downloads

# step 6 install ollama -- https://ollama.com/docs/installation
# ollama list -- to check if the installation was successful
#ollama pull llama3 -- to pull the llama3 model to your local machine
#ollama run llama3 -- to run the model and check if it's working properly
#ollama rm llama3 -- to remove the model from your local machine if you want to free up space


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


# freeze the dependencies in a requirements.txt file -pip freeze > requirements.txt

#Add this content:
'''
# Virtual environment
venv/

# Environment variables (secrets)
.env
'''
#git init -- to initialize a git repository in your project folder
#git add . -- to stage all the files for commit 
'''Run

  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"'''
#git commit -m "Initial commit" -- to commit the staged files with a message
#git remote add origin <https://github.com/tejaschechar/GPT_PRO_FREE> -- to link your local repository to a remote repository on GitHub
#git pull origin main -- to pull any changes from the remote repository before pushing your commits
#git push -u origin main -- to push your commits to the remote repository on GitHub
#git status -- to check the status of your repository and see which files are staged, unstaged, or untracked
#git log -- to view the commit history of your repository
#git branch -- to check which branch you are currently on
#git checkout -b <branch-name> -- to create and switch to a new branch for

#phase 1
# model router integrated
#Unified LLM interface
#Multi-model support (phi3, llama3)
#Auto + manual model selection
# Clean modular code
#multi model pipeline with draft, refine, critic steps
# Basic error handling with fallback

''' 
llm/
 ├── model_router.py
 ├── ollama_client.py
 └── prompt_builder.py
 |__ multi_model_pipeline.py

tests/
 └── test_llm.py '''


#Phase 2
#Internet search
#Math pipeline
#Multi-model routing
#Context-aware answers
#allucination reduction

'''
tools/
 ├── search.py
 ├── math_solver.py

services/
 ├── context_builder.py
'''


#PHASE 3 — MEMORY + PERSONALIZATION + SELF-LEARNING
'''
✅ Long-term memory (FAISS)
✅ Conversation memory
✅ User preferences tracking
✅ Context-aware personalization
✅ Self-improving responses

User Query
   ↓
Memory Retriever 🔥
   ↓
Search (if needed)
   ↓
Context Builder
   ↓
Multi-Model Pipeline
   ↓
Response
   ↓
Memory Storage (learn)
'''