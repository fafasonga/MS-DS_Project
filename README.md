
MS DS Project on Geolocation
============================

This project is for visualizing the trajectory of the dataset on the map to help in the process of understanding the data representation and visualization, to make some future prediction of missing features or to introduced and extend the functionalities of some pre-existing features or improve the existing features.

This application, takes the Longitude and Latitude of different users to be displayed on the map and the time and date these users were at that particular location and store them into a database that were created using sqlalchemy (Python library that facilitate the communication between the python program and database) and readed by the web application using Flask.

All the trajectories are displayed on the map using leaflet.js (Open-source JavaScript library used to create interactive maps).
The web application is written in JavaScript, Python and Jinja2.

There are options on the application to upload a new CSV file to the database and see all the elements stored in your database if they are as you wanted, and you can perform some action to the database like deleting the whole existing database or modify the database using the following features:
 - Adding new Users and new data points to the database.
 - Deletion the Users or data points from the database.

At the Home page. y
You need to select which user have to be visualized on the map either each user individually or selecting to visualize all the users together.

You then have to click the Start botton to start the visualization and then you can speed up the visualization and stop according to your preferences.
Once the visualization have started, as long as the stop botton were not pressed, the visualization will run in infinite number of loops.


# Getting started:

# Install the libraries.

Clone the Repository.

Open Terminal and go through the directories you cloned and run:

```
pip install -r requirements.txt

```
