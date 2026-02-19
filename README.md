# Instructions

## Installation

* Make sure you have your git ssh set up, if you have ever cloned anything from git it probably is
* run `git clone git@github.com:jackmcau/quantum_hackathon.git` in a directory you want to work out of
* `cd quantum_hackathon`
* Open in your preferred IDE (VSCode)
* run `python -m venv venv` or `python3 -m venv venv`
* For Mac and Linux, run `source venv/bin/activate`
* For Windows, run `venv\Scripts\activate`
* `pip install .`
* `deactivate` to leave the virtual environment or just close the terminal

## Usage
* Make sure that you are in the virtual environment for this repository
* Re-running `pip install .` is never a bad idea, dependencies could be added
* run `git pull` if a change has been made to the repository
* If you are in a new terminal: 
    * For Mac and Linux, run `source venv/bin/activate`
    * For Windows, run `venv\Scripts\activate`
    * There should be a ((venv)) at the beginning of the line in your terminal
* I have implemented the first test from problem set 1 in test.py, so make sure you get no errors from `python test.py` and let me know if you need any help or something isn't working!
* I recommend making your own folder with your first name like I will have to do all of your work in, just so we don't overwrite others work
    * This will also help with merge conflicts
* Whenever you make changes that you want to share with the team, run
    * `git add *`
    * `git commit -m "{include a message describing your changes}"`
    * `git push`
* Please do not push files that are in the .gitignore





* also, on mac at least if `source venv/bin/activate` doesnt work I first did `python3 -m venv venv` and then that command it worked (changed (base) to (venv)). I am not sure if thisll work for everyone or what the point it but it created a venv folder w stuff in it and im pretty sure thats meant to be local not in the repo