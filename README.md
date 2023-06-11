 #  Running DIS-G 

## Initialisation 

First, make sure you have a newer version of Python installed. If you need to check your Python version, write Python --version.
Clone the repository files into your preferred folder. Install all dependencies - either directly in PyCharm or another Python 
IDE which supports packages, or open up your terminal, navigate to the folder where the ‘requirements.txt’ is, then write 
the following command from the project root directory: 

	pip install -r requirements.txt 

If you have Python3 installed, you will need to use pip3 to install the requirements, instead of pip.

In /src/db/ add a .env file containing the following: 

    SECRET_KEY=<secret_key> 
    DB_USERNAME=postgres || <postgres_user_name>
    DB_PASSWORD=<postgres_user_password>
    DB_NAME=DIS-G || <postgres_db_name>

Replace the secret key with your own secret key, along with the DB username and password. If your local filename is different 
from DIS-G, then make sure to replace this as well. 


# Using the website

We implemented basic "Add", "Update", and "Delete" functionality to the "Tags" page.
You can only modify or delete tags that are not referred to by other tables, as the name itself is their primary key.

The search page as options on the left side. You need to:
- Choose a line (only the F line works currently).
- Choose an origin station.
- Choose a destination.
  - Only the stations between your origin and destination (inclusive bounds) will be returned when searching for amenities.
  - "All" is a special destination, that searches the whole line
  - "None" is a special destination, that only checks your origin station
- Choose a sorting method.
- The 4 integer inputs are optional. NULL values are replaced with appropriate constants that catch everything.
- Select any tags you want to search on.
- Finally, hit search!


# The database in general		

The database comprises an overlook over amenities located along the S-train net. It helps the user select one or more amenities 
they wish to find. Different filters can be applied to the search, such as: A starting station (origin) and a destination, such that only amenities along their path will be displayed. 
The user can input certain search preferences, such as minimum/maximum walking distance. 


## Initializing the database

The file /src/__init__.py contains a function call to /src/db/util.reset() on line 17. This is a python function that runs the .sql files in /src/db/schema and then loads the .csv files in /src/db/data by building an INSERT statement.
This function call drops all tables (if there are any) and creates a fresh schema with fresh test data each time the program is started.
This function call can safely be removed, if one wishes to do so.


## How to interact with database 

Run the program using flask. Open up the local webserver that will be suggested. This will lead onto the website, which 
displays the database.

Only "Tags" support ADD, UPDATE and DELETE functionality right now.


# Known issues 

-	We have not implemented user functionality, which means that everyone has access to modify the database as they wish. There should have existed a two-tiered layer of users with an 
admin and moderators, where moderators would be able to make INSERT and UPDATE statements, however DELETE statements should 
only be at the discretion of the admin to ensure parts of the database will not be deleted by accident.

## Other

The uses the same general structure as the given example projects, and some parts are inspired from them, but everything is built from the ground up.
We designed the database schema and created the test data.

We only created data for the F line, but we designed our schema based on the fact that a single station can be a part of many lines.
As such, if you perform any search and select any line except "F", no results will be returned.

We used one trigger. The 'line' table contains the length of any given line, and the 'station_lines' table contains a stations position on a given line.
We created a constraint trigger, that ensures that a 'station_lines' position is a value that actually is within the line's length that it references.

If you look closely at the cat in the lower right corner, you will see that he/she is a train conductor.

We tried to add extra search types, such as a search option where all tags need to be matched with a station and one where the amount of tag hits were counted.
Our queries did somewhat work, when they were supplied with a specific destination station, not out "None" and "All" options.
They were commented out, as they were not finished.


# Licence 



All pictures included in this project are either created by ourselves, or part of the Creative Common project, which – as 
specified by https://kubku.dk/brug-biblioteket/studerende/ophavsret/brug-af-billeder/ are okay to use in projects. 

"Copenhagen location map" by Kopenhagen-norrebro.PNG H.Loper at Dutch Wikipedia derivative work: ויקיג'אנקי is licensed under 
CC BY-SA 3.0.