# care-backend
This repo is responsible for the backend aspect of care connect

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
