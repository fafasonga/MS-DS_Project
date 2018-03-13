
MS DS Project on Geolocation
============================

This project is for visualizing the trajectory of the dataset on the map to help in the process of understanding the data representation and visualization, to make some future prediction of missing features or to introduced and extend the functionalities of some pre-existing features or improve the existing features.

This application, takes the Longitude and Latitude of different people to be displayed on the map and the time and date these people were at that particular location and store them into a database that were created using sqlalchemy (Python library that facilitate the communication between the python program and database) and open a session to exchange the information between the server and the web application using Flask.

All the trajectories are displayed on the map using leaflet.js ( Open-source JavaScript library used to create interactive maps ).
The web application is written in JavaScript, Python with Jinja2 ( template engine for Python ).

There are options on the application to upload a new CSV file to the database and see all the elements stored in your database if they were stored as you wanted, if there are some feature data that are not the way you want, there are features to perform some action to the database like deleting the whole existing database or modify the database using the following features:
 - Adding new Users to database.
 - Adding new Data set to the database.
 - Deleting Users from the database.
 - Deleting data points from the database.

At the loading of the Home page.

You need to select which user have to be visualized on the map either each data point individually or selecting to visualize all the data points together.

You then have to click the Start botton to start the visualization and then you can speed up the visualization and stop according to your preferences and you can increase the number of markers that can be shown on the map from one marker.
Once the visualization have started, as long as the stop botton were not pressed, the visualization will run in infinite number of loops.

You can also see the path taken by the person with the two markers shown, where one marker is the start point of the person and the second marker is the end point of that person and then path goes from start point to the end point.
You can as well see all the path taken by the person from a botton click.


# Getting started:

# Install the libraries.

Clone this Repository.

Open Terminal and go through the directories you just cloned and run:

```
pip install -r requirements.txt

```
