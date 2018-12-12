# Flask Recipe Book

A simple Flask application to showcase recipes.

With help from [The Flask Mega Tutorial](https://courses.miguelgrinberg.com/p/flask-mega-tutorial) and Flask Web Development, 2nd Edition by Miguel Grinberg.

Written for WEB 3200 course at Weber State.

## Running the Application Locally
After cloning the repository, you'll have to create a virtual environment and install the packages.
* In a command prompt, `cd` into the root of the repo.
* Create a virtual environment: `python -m venv venv`
* Activate the virtual environment: `venv\Scripts\activate`
* Install the dependencies: `pip install -r requirements.txt`
* Run the app: `flask run`
* Navigate to http://localhost:5000/ to view the app.

### Notes
There is currently no way to modify the database within the app, other than registering a new user. You can add/edit the database either using `flask shell` and adding entries manually, or using a program to browse the database directly (such as [DB Browser for SQLite](https://sqlitebrowser.org/)). This will hopefully be changed soon.