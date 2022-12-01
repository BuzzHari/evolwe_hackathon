#Evolwe Hackathon

#Introduction
This script implements part 2 of our solution where we monitor communication between mentor and mentee across channels like email and Teams and accordingly set up meetings or suggest reminders to have a conversation.
The script utilizes the Microsoft Graph APIs, to find the optimal time and for scheduling the meetings. 

Currently using the script a mentor/mentee can schedule meetings, they just input the frequency of calls required in a week and the script will auto schedule the meeting series based on their free time. 
The implementation of adding intelligence to automatically decide when a meeting could be required, is yet to be implemented since this requires monitoring communication on email/Teams.   


#Requirements
* python3
* pip 

#Installing Dependencies
* `python3 -m pip install azure-identity`
* `python3 -m pip install msgraph-core`


