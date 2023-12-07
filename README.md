# MySQL + Flask Boilerplate Project

This repo contains a boilerplate setup for spinning up 3 Docker containers: 
1. A MySQL 8 container for obvious reasons
1. A Python Flask container to implement a REST API
1. A Local AppSmith Server

## How to setup and start the containers
**Important** - you need Docker Desktop installed

1. Clone this repository.  
1. Create a file named `db_root_password.txt` in the `secrets/` folder and put inside of it the root password for MySQL. 
1. Create a file named `db_password.txt` in the `secrets/` folder and put inside of it the password you want to use for the a non-root user named webapp. 
1. In a terminal or command prompt, navigate to the folder with the `docker-compose.yml` file.  
1. Build the images with `docker compose build`
1. Start the containers with `docker compose up`.  To run in detached mode, run `docker compose up -d`. 

_______________________________________________

-----STUDY GROUP APP-----

-----DATABASE-----
Our database consists of several portions, including student users, moderators, study groups, message boards, and more.

Within the db folder of this project you will see the Mockaroo data we used to populate our database.

-----FLASK API-----
Our api consists of blueprints for Bookmarks, Message Boards, Resources, Reviews, Study Groups, and Users

Many of these calls use joins and subqueries in SQL to deliver meaningful data from the endpoint.
The exposed functionality is:
/s/StudyGroups ...
/rev/reviews ...
/b/bookmarks ...
/rsrc/resources ...
/u/Users ...
/m/MessageBoards ...


LINK TO VIDEO: https://drive.google.com/file/d/1XpQhNmwW534p7g4XiKiQb2UXHJc4scKL/view
