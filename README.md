# MS-DS_Project

This project is for visualizing the trajectory of the dataset on the map to help in the process of understanding the data and make some future prediction of what is missing to be introduced and extend the feautures or improve the existing features.

It takes the Longitude and Latitude of different users and the time and date on which these different Users were at that particular location and store them into a database that were created using sqlalchemy and communication to the web application using Flask.

All the trajectories are displayed on the map using leaflet.js and the web application is written in Java, python and Jinja2.

There is a facility to add new Users and new data points to the database and deletions of Users or data points from the database.

At the loading of the home page, you need to select which user to be visualized on the map either indivually or select to visualize all the users together.

You then have to click the start botton to start the visualization and then you can speed up the visualization and stop.
Once the visualization have started, in case a stop botton were not pressed, the visualization will run in infinite loops.
