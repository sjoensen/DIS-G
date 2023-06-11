#  Running DIS-G 

## Initialisation 

First, make sure you have a newer version of Python installed. If you need to check your Python version, write Python --version. 
If you have Python3 installed, you will need to use pip3 in the code down below. 
Clone the repository files into your preferred folder. Install all dependencies - either directly in PyCharm or another Python 
IDE which supports packages, or open up your terminal, navigating to the folder where the ‘requirements.txt’ is, then writing 
the following in the terminal: 

	pip install -r requirements.txt 

In schema add an .env file containing the following: 

    SECRET_KEY=<secret_key> 
    DB_USERNAME=postgres || <postgres_user_name>
    DB_PASSWORD=<postgres_user_password>
    DB_NAME=DIS-G || <postgres_db_name>

Replace the secret key with your own secret key, along with the DB username and password. If your local filename is different 
from DIS-G, then make sure to replace this as well. 


# The database in general		

The database comprises an overlook over amenities located along the S-train net. It helps the user select an/multiple amenities 
they wish to find, along with where they are travelling from/to, to ensure their desired amenities will be along the road. 
The user can input certain preferences, like a minimum/maximum walking distance. 


## How to interact with database 

Run the program using flask. Open up the local webserver that will be suggested. This will lead onto the website, which 
displays the database. 


# Known issues 

-	All users have access to modify the database as they wish. There should have existed a two-tiered layer of users with an 
admin and moderators, where moderators would be able to make INSERT and UPDATE statements, however DELETE statements should 
only be at the discretion of the admin to ensure parts of the database will not be deleted by accident. 

## Other

# Licence 



All pictures included in this project are either created by ourselves, or part of the Creative Common project, which – as 
specified by https://kubku.dk/brug-biblioteket/studerende/ophavsret/brug-af-billeder/ are okay to use in projects. 

"Copenhagen location map" by Kopenhagen-norrebro.PNG H.Loper at Dutch Wikipedia derivative work: ויקיג'אנקי is licensed under 
CC BY-SA 3.0.