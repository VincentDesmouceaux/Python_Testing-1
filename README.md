# gudlift-registration

1. **Why**

   This is a proof of concept (POC) project to show a light-weight version of our competition booking platform. The aim is to keep things as light as possible, and use feedback from the users to iterate.

2. **Getting Started**

   This project uses the following technologies:

   - **Python v3.x+**
   - **[Flask](https://flask.palletsprojects.com/en/1.1.x/)**
     > Whereas Django does a lot of things for us out of the box, Flask allows us to add only what we need.

   - **[Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)**
     > This ensures you'll be able to install the correct packages without interfering with Python on your machine.  
     Before you begin, please ensure you have this installed globally.

3. **Installation**

   - After cloning, change into the directory and type:
     ```bash
     virtualenv .
     ```
     This will then set up a virtual python environment within that directory.

   - Next, type:
     ```bash
     source bin/activate
     ```
     You should see that your command prompt has changed to the name of the folder.  
     This means that you can install packages in here without affecting files outside.  
     To deactivate, type `deactivate`.

   - Rather than hunting around for the packages you need, you can install in one step:
     ```bash
     pip install -r requirements.txt
     ```
     This will install all the packages listed in the respective file.  
     If you install a package, make sure others know by updating the requirements.txt file.  
     An easy way to do this is:
     ```bash
     pip freeze > requirements.txt
     ```

   - Flask requires that you set an environmental variable to the python file.  
     However you do that, you'll want to set the file to be `server.py`.  
     Check [here](https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application) for more details.

   - You should now be ready to test the application.  
     In the directory, type either:
     ```bash
     flask run
     ```
     or
     ```bash
     python -m flask run
     ```
     The app should respond with an address you can open in your browser.

4. **Current Setup**

   The app is powered by [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm). This is to avoid having a DB until we actually need one.  
   The main ones are:
   - **competitions.json** - list of competitions
   - **clubs.json** - list of clubs with relevant information  
     (You can look here to see what email addresses the app will accept for login.)

5. **Testing**

   You are free to use whatever testing framework you like — the main thing is that you can show what tests you are using.

   We also like to show how well we're testing, so there's a module called [coverage](https://coverage.readthedocs.io/en/coverage-5.1/) you should add to your project.

6. **Commands**

   Below are the most common commands you might use in this project:

   - **Run Flask locally**:
    
     flask run
    
     or
     
     python -m flask run
     

   - **Run all unittests** (discovery mode, looks in `tests/` folder):
     
     python -m unittest discover -s tests
     

   - **Run tests with coverage**:
     
     coverage run -m unittest discover -s tests
     coverage report -m
     
     This will show a summary of code coverage for all tested files.

   - **Run Locust tests** for performance (assuming `locustfile.py` is in `tests/performance/`):
    
     locust -f tests/performance/locustfile.py --host=http://127.0.0.1:5000
    
     Then open `http://127.0.0.1:8089` in your browser, set the number of users (default 6), and start the test.

   - **Deactivate virtual environment**:
    
     deactivate
    


