# GradingWithLLMs
## Installation
### 1. (Optional but useful) Add a ssh key to the Repository. 
You can find instruction how to do this here: https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/GitHub-SSH-Windows-Example
### 2. Clone the repository

### 3. Create the python environment
For Windows instruction see: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment
```bash
 python3 -m venv .venv
 source .venv/bin/activate
 #You can check if you are in the correct environment by typing: which python
 pip install -r requirements.txt
```
### 4. Create a .key file in the src/ directory
The .key file has to have the key in the first line, the url in the second line and the project name in the third line. You can use  the editor of your choice and just drag and drop it there
(Niklas sent us these in teams)
### 5. Start the application
```bash
cd src
python api_test.py
```
Congratulations you just used the gpt-4 API for the first time (Hooray!)

### 6. Play around
Now you can edit the api_test.py file or create your own one. Please use different branch if you do so you can name it like dev/yourNameofChoice
