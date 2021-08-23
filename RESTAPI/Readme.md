## Requirements
Create a virtual environment and then install the package
requirements.

The package requirements of the project are defined in 
_requirements.txt_.

You can install them using _"pip install -r requirements.txt"_

## Database
The database used in the project is _sqlite3_.

## Installation
A dump of database is created using 
_python manage.py dumpdata > dumpdatabase.json_ and
is stored in dumpdatabase.json .

This database can be loaded using
 _python manage.py loaddata > dumpdatabase.json_
 
 Now the project can be started by running the 
 following commands:
 
 _python manage.py makemigrations_
 
 _python manage.py migrate_
 
 _python manage.py runserver_
 
 ## Documentation
 
 All the APIs are mentioned using _Swagger Docs_.
 
 The list of all APIs can be accessed on the main page of 
 the project, i.e., if you run the server on port 8000, then
 the access link will be _http://127.0.0.1:8000/_.