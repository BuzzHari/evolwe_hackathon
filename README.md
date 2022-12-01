# Evolwe Hackathon

## Introduction
This script implements part 2 of our solution where we monitor communication between mentor and mentee across channels like email and Teams and accordingly set up meetings or suggest reminders to have a conversation.
The script utilizes the Microsoft Graph APIs, to find the optimal time and for scheduling the meetings. 

Currently using the script a mentor/mentee can schedule meetings, they just input the frequency of calls required in a week and the script will auto schedule the meeting series based on their free time. 
The implementation of adding intelligence to automatically decide when a meeting could be required, is yet to be implemented since this requires monitoring communication on email/Teams.   


## Requirements
* python3
* pip 

## Installing Dependencies
* `python3 -m pip install azure-identity`
* `python3 -m pip install msgraph-core`

## Running the script

* `python3 main.py`.
* `follow on screen instructions`.

## Screenshots


![image](https://user-images.githubusercontent.com/35808993/204996871-3aa97191-88d8-49a7-8a76-801ad89e0fce.png)
![image](https://user-images.githubusercontent.com/35808993/204997048-3e510ab5-dc08-414f-b09b-7a239af73e0c.png)
