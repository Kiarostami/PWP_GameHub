# PWP SPRING 2021
# GameHub
GameHub is an API to make interesting website for video games and who love video games!
# Group information
* Student 1. Sina Kiarostami, mohammad.kiarostami@oulu.fi
* Student 2. Sadaf Nazari, sadaf.3.nazari@student.oulu.fi
* Student 3. Vahid Mohsseni, vahid.mohsseni@oulu.fi
* Student 4. Danial Khoshkholgh, danial.3.khoshkholgh@student.oulu.fi

__Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint and instructions on how to setup and run the client__

# Initializing the database

### Description
Our database system and its entities and their relations has been explained in the wiki page. For this 
implementation we used `SQLite3`
However, in this section, we will introduce the simple commands to run the project and initialize the DB. 

We did not use the so-called ready to user database engines for three reasons. 

- First, we wanted to keep the project as simple as possible for our learning purpose. 
- Second, in the upcoming deadlines for the project we may have some complex sql queries. 
- And the third, this was the fastest way we know when we were designing the project.


### Run
Before runing the project please install the requirement of the project available in the `requirements.txt` file.

To init the database and populate it with some entities:

```shell
$ export FLASK_APP=API
$ export FLASK_ENV=development
$ flask init-db
```
The above command will run our database initializer using the already-defined schema which is available in the 
directory `databae/schema.sql`, and then to populate the DB with some pre-defined data, it will use the 
`database/data.sql` file. The instance file of the database, since we are using the sqlite is available in the 
`instance/db.sqlite` file.


To run the application on the port of 5000:

```shell
$ python3 app.py
```
