import json
import requests
from tools.exceptions import AuthorizationError


class RdApi:

    def __init__(self, client_id, client_secret, refresh_token=None, code=None, callback_url=None):
        """RD Station API use OAuth authentication method.

        See: https://developers.rdstation.com/en/authentication

        Args:
            client_id (str): Get in RD Station App Store.
            client_secret (str): Get in RD Station App Store.
            refresh_token (str): Get from access token.
            code (str): Just needed if refresh_token is not passed. Get from callback URL.
            callback_url (str): Just needed if code is not passed.
            In an authentication flow, RD needs a "delivery address" to return the access code.
            This delivery address is the callback URL.

        Raises:
            AuthorizationError: when code or refresh_token is not valid.
        """

        self.base_url = 'https://api.rd.services'
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        if code:
            self.access_token = self._get_access_token(code)
        elif refresh_token:
            self.access_token = self._refresh_access_token()
        else:
            authorization_url = self._get_authorization_url(callback_url)
            print(authorization_url)

        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def _get_authorization_url(self, callback_url):
        return f'{self.base_url}/auth/dialog?client_id={self.client_id}&redirect_url={callback_url}'

    def _get_access_token(self, code):
        print('Getting access_token...')
        url = f'{self.base_url}/auth/token'
        req_data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code
        }
        response = requests.post(url, data=req_data)
        status_code = response.status_code
        if status_code == 200:
            json_token = response.json()
            self.refresh_token = json_token['refresh_token']
            print('Done!')
            return json_token['access_token']
        elif status_code == 401:
            raise AuthorizationError('ACCESS_DENIED: Wrong credentials provided.')

    def _refresh_access_token(self):
        print('Refreshing token...')
        url = f'{self.base_url}/auth/token'
        req_data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token
        }
        response = requests.post(url, data=req_data)
        status_code = response.status_code
        if status_code == 200:
            json_token = response.json()
            self.refresh_token = json_token['refresh_token']
            print('Done!')
            return json_token['access_token']
        elif status_code == 401:
            raise AuthorizationError('ACCESS_DENIED: Wrong credentials provided.')

    def create_webhook(self, webhook_url, event_type='CONVERTED', include_relations=[]):
        """ It creates a webhook subscription.
        See: https://developers.rdstation.com/pt-BR/reference/webhooks#methodPostDetails

        Args:
            webhook_url (str): The webhook destination URL. The URL to RD Station send the data.
            event_type (str): The valid options are: WEBHOOK.CONVERTED, WEBHOOK.MARKED_OPPORTUNITY.
            include_relations (list): The relations you would like to include in webhook payload.
            Only "COMPANY" and "CONTACT_FUNNEL" are supported.

        Returns:
            requests.models.Response
        """

        print('Creating webhook...')
        api_url = f'{self.base_url}/integrations/webhooks'

        req_data = {
            "entity_type": "CONTACT",
            "event_type": f"WEBHOOK.{event_type}",
            "event_identifiers": [],
            "url": webhook_url,
            "http_method": "POST",
            "include_relations": include_relations
        }
        response = requests.post(api_url, headers=self.headers, data=json.dumps(req_data))

        return response

    def list_webhooks(self):
        url = f'{self.base_url}/integrations/webhooks'
        response = requests.get(url, headers=self.headers)

        return response

    def delete_webhook(self, webhook_uuid):
        print(f'Deleting webhook {webhook_uuid}...')
        url = f'{self.base_url}/integrations/webhooks/{webhook_uuid}'
        response = requests.delete(url, headers=self.headers)

        return response

    def updated_webhooks(self, webhook_uuid, req_data):
        url = f'{self.base_url}/integrations/webhooks/{webhook_uuid}'
        response = requests.put(url, headers=self.headers, data=json.dumps(req_data))

        return response
