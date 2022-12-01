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

def get_free_time(graph: Graph):
    user_name = 'Victor, Ashish Christopher';
    user_email = 'ashish-christopher.victor@hpe.com'

    suggested_times = graph.get_free_time(user_name, user_email)

    print(suggested_times)
    #for timeSuggestion in suggested_times['meetingTimeSuggestions']: 
    #    print('Meeting Time slot: ', timeSuggestion['meetingTimeSlot']['start']['dateTime'], ' - ' , timeSuggestion['meetingTimeSlot']['end']['dateTime'], 'timezone:',
    #            timeSuggestion['meetingTimeSlot']['start']['timeZone'], '\n')
    return 1


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
            get_free_time(graph)
        else:
            print('Invalid choice!\n')

main()
