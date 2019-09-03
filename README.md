# HouseRules
[Visit the site](houserulez.net)

## Overview
	House Rules is a webapp that allows users to share the rules of their house with their friends.

## Local Hosting/Running Instructions
	1) Clone the main branch repository to your computer
	'''git clone https://github.com/jacobvsargent/HouseRules.git'''
	
	2) Download the Google Cloud SQL Proxy [here](https://cloud.google.com/sql/docs/mysql/connect-admin-proxy#install) (Step 2 shows how)
	
	3) Open a terminal window and navigate to the location fo the proxy exe file
	
	4) Go to the settings.py file in the project, down to the database settings and change the port number there to the number of the open tcp port you would like to connect to the cloud sql service with
	
	5) Run the following command 
	'''cloud_sql_proxy.exe -instances "house-rules-249409:us-east4:house-rules-db=tcp:$PORT_NUMBER"'''
	replacing $PORT_NUMBER with the same port chosen above
	
	6) Open another terminal window and navigate to the base project directory
	
	7) Run the following command to activate a local environment
	'''envs/Scripts/activate'''
	and a (env) should appear in front of the location in the terminal
	
	8) In the same terminal, run the command
	'''python manage.py runserver'''
	
	9) Open localhost:8000 to see the site's homepage

## Authors
	Jacob Sargent, Charlie Gallentine, Nicholas Deas

## Copyright
	Copyright 2019 by Bet On It, LLC. All Rights Reserved
