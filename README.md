# care-backend
This repo is responsible for the backend aspect of care connect
### Code commented
- incase you see a line of comment with more than two # that is an error that should not be taken to production

# Running the flask app
## setting up
- Run envivonment (environment used is pipenv)
- Run shell - (pipenv shell)
- Install all  dependancies -(pipenv install) 
- point the run to run.py (export FLASK_APP=run.p)
- Run app (flask run)
- Incase of errors run the run.py file install all dependancies in requirements.txt ( pip install (the dependancy name))

## setting up database 
- run flask db init(create intances folder)
- run flask db migrate -m "your meesage"
- run flask db upgrade 
- this will be done only once on set up

# folder structure
## server
contains the 2 folder and models which has the tables and Views which has the endpoints 
## Models
contains all the database models
## Views
- has the init.py file that has the blueprint with all endpoints be (be very carefull when editing this file i.e the apiendpoints)
- Has files with all the endpoints using flask restfull
## Other files 
- app.py 
containst all the essential elements that require the program to run (coution when editing)
- config.py
Has all the default configurations for the app
- run.py
runs the program
## git ignore
Has the intances and migratons set not to be psuhed to the repo
## pipfile and pipfile.lock
Have installed  things inside
