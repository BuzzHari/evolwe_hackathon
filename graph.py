import json
from configparser import SectionProxy
from azure.identity import DeviceCodeCredential, ClientSecretCredential
from msgraph.core import GraphClient

class Graph:
    settings: SectionProxy
    device_code_credential: DeviceCodeCredential
    user_client: GraphClient
    client_credential: ClientSecretCredential
    app_client: GraphClient

    def __init__(self, config: SectionProxy):
        self.settings = config
        client_id = self.settings['clientId']
        tenant_id = self.settings['authTenant']
        graph_scopes = self.settings['graphUserScopes'].split(' ')

        self.device_code_credential = DeviceCodeCredential(client_id, tenant_id = tenant_id)
        self.user_client = GraphClient(credential=self.device_code_credential, scopes=graph_scopes)

    def get_user_token(self):
        graph_scopes = self.settings['graphUserScopes']
        access_token = self.device_code_credential.get_token(graph_scopes)
        return access_token.token

    def get_user(self):
        endpoint = '/me'
        # Only request specific properties
        select = 'displayName,mail,userPrincipalName'
        request_url = f'{endpoint}?$select={select}'

        user_response = self.user_client.get(request_url)
        return user_response.json()

    def get_any_user(self, user_mail): 
        endpoint = '/users/' + user_mail
        select = 'displayName,mail,userPrincipalName'
        request_url = f'{endpoint}?$select={select}'

        user_response = self.user_client.get(request_url)
        return user_response.json()

    def send_mail(self, subject: str, body: str, recipient: str):
        request_body = {
            'message': {
                'subject': subject,
                'body': {
                    'contentType': 'text',
                    'content': body
                },
                'toRecipients': [
                    {
                        'emailAddress': {
                            'address': recipient
                        }
                    }
                ]
            }
        }

        request_url = '/me/sendmail'

        self.user_client.post(request_url,
                              data=json.dumps(request_body),
                              headers={'Content-Type': 'application/json'})


    def get_free_time(self, attendee_name: str, attendee_email: str):
        request_body = {
            'attendees': [
                {
                    'type': 'required',
                    'emailAddress': {
                        'name': attendee_name,
                        'address': attendee_email 
                     }
                }
            ],
            'timeConstraint': {
                'activityDomain': 'work',
                'timeSlots': [
                    {
                        'start': {
                            'dateTime': '2022-12-02T09:00:00',
                            'timeZone': 'India Standard Time' 
                        },
                        'end': {
                            'dateTime': '2022-12-02T17:00:00',
                            'timeZone': 'India Standard Time'

                        }
                    }
                ]
            },
            'isOrgazizerOptional': 'false',
            'meetingDuration': 'PT1H',
            'returnSuggestionReasons': 'true',
        }   

        request_url = '/me/findMeetingTimes'
        preference = "outlook.timezone=\"India Standard Time\""
        response = self.user_client.post(request_url,
                             data=json.dumps(request_body),
                             headers={'Prefer': preference, 'Content-Type': 'application/json'})
        return response.json()
    
    def schedule_meeting(self, user, recipient, start_time, end_time):
        request_body = {
            "subject": user['displayName'] + " - " + recipient['displayName'] + " 1 - 1",
            "body": {
            "contentType": "HTML",
            "content": "Does this time work for you?"
            },
            "start": {
              "dateTime": start_time,
              "timeZone": "India Standard Time"
            },
            "end": {
              "dateTime": end_time,
              "timeZone": "India Standard Time"
            },
            "location":{
              "displayName":"Microsoft teams"
            },
            "attendees": [
            {
              "emailAddress": {
                "address": recipient['mail'],
                "name": recipient['displayName'] 
              },
              "type": "required"
            }
            ],
            "allowNewTimeProposals": "true",
            "isOnlineMeeting": "true",
            "onlineMeetingProvider": "teamsForBusiness"
        }


        request_url = '/me/events'
        preference = "outlook.timezone=\"India Standard Time\""
        response = self.user_client.post(request_url,
                             data=json.dumps(request_body),
                             headers={'Prefer': preference, 'Content-Type': 'application/json'})
        return response.json()
