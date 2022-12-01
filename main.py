import configparser
from graph import Graph

def greet_user(graph: Graph):
    user = graph.get_user()
    print('Hello,', user['displayName'])
    # For Work/school accounts, email is in mail property
    # Personal accounts, email is in userPrincipalName
    print('Email:', user['mail'] or user['userPrincipalName'], '\n')

def display_access_token(graph: Graph):
    token = graph.get_user_token()
    print('User token:', token, '\n')
    return 1
	
def send_mail(graph: Graph):
    # Send mail to the signed-in user
    # Get the user for their email address
    user = graph.get_user()
    user_email = user['mail'] or user['userPrincipalName']

    graph.send_mail('Testing Microsoft Graph', 'Hello world!', user_email)
    print('Mail sent.\n')

def get_free_time(graph: Graph, recipient_details):

    suggested_times = graph.get_free_time(recipient_details['displayName'], recipient_details['mail'])

    meeting_times = []
    for timeSuggestion in suggested_times['meetingTimeSuggestions']: 
        meeting_times.append({"start": timeSuggestion['meetingTimeSlot']['start']['dateTime'], "end": timeSuggestion['meetingTimeSlot']['end']['dateTime']})
    print(meeting_times)

    return meeting_times 

def schedule_meeting(graph: Graph):
    recipient_email = input("Enter email address of person you want to schedule meeting with: ")
    recipient_name = input("Enter name of person you want to schedule meeting with: ")
    recipient_details = {"displayName": recipient_name, "mail": recipient_email} 
    print(recipient_details)
    user_details = graph.get_user()

    meeting_times = get_free_time(graph, recipient_details)
    res = graph.schedule_meeting(user_details, recipient_details, meeting_times[0]['start'], meeting_times[0]['end'])
    print("Scheduled", res)

def main():
    print('Python Graph Tutorial\n')

    # Load settings
    config = configparser.ConfigParser()
    config.read(['config.cfg', 'config.dev.cfg'])
    azure_settings = config['azure']

    graph: Graph = Graph(azure_settings)

    greet_user(graph)

    choice = -1

    while choice != 0:
        print('Please choose one of the following options:')
        print('0. Exit')
        print('1. Display access token')
        print('2. Send mail')
        print('3. Find meeting times')
        print('4. Schedule 1-1 meeting')
        
        try:
            choice = int(input())
        except ValueError:
            choice = -1

        if choice == 0:
            print('Goodbye...')
        elif choice == 1:
            display_access_token(graph)
        elif choice == 2:
            send_mail(graph)
        elif choice == 3:
            recipient_email = "hari.om@hpe.com"  # Just for testing. 
            recipient_details = graph.get_any_user(recipient_email)
            print(recipient_details)
            get_free_time(graph, recipient_details)
        elif choice == 4:
            schedule_meeting(graph)
        else:
            print('Invalid choice!\n')

main()
