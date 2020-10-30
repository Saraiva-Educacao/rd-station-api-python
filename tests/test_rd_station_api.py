import requests
from tools.exceptions import AuthorizationError
from rd_station.rd_station_api import RdApi
from unittest import mock, TestCase

client_id = "client_id"
client_secret = "client_secret"
refresh_token = "refresh_token"


def mock_requests(*args, **kwargs):
    class MockResponse:
        def __init__(self, status_code, json_content=None):
            self.status_code = status_code
            self.json_content = json_content

        def json(self):
            return self.json_content

    _base_url = 'https://api.rd.services'

    if args[0] == f"{_base_url}/auth/token":
        refresh_token_response = {
            "access_token": "access_token",
            "expires_in": 86400,
            "refresh_token": "refresh_token"
        }
        return MockResponse(200, refresh_token_response)

    elif args[0] in [
        f'{_base_url}/platform/contacts/c2f3d2b3-7250-4d27-97f4-eef38be32f7f',
        f'{_base_url}/platform/contacts/email:contact@example.com',
    ]:
        contact_info_response = {
            "name": "RD Station Developer",
            "email": "contact@example.com",
            "uuid": "c2f3d2b3-7250-4d27-97f4-eef38be32f7f",
            "job_title": "Developer",
            "bio": "This documentation explains the RD Station API.",
            "website": "https://developers.rdstation.com/",
            "linkedin": "rd_station",
            "personal_phone": "+55 48 3037-3600",
            "city": "Florianópolis",
            "state": "SC",
            "country": "Brasil",
            "tags": ["developer", "rdstation", "api"],
            "extra_emails": ["contact2@example.com"],
            "cf_custom_field_2": "custom field value2",
            "legal_bases": [
                {
                    "category": "data_processing",
                    "type": "pre_existent_contract",
                    "status": "granted"
                },
                {
                    "category": "communications",
                    "type": "consent",
                    "status": "granted"
                }
            ]
        }
        return MockResponse(200, contact_info_response)

    elif args[0] == f"{_base_url}/platform/contacts/lead_uuid/events?event_type=CONVERSION&order=created_at:desc":
        contact_events_response = [
            {
                "event_type": "CONVERSION",
                "event_family": "CDP",
                "event_identifier": "newsletter",
                "event_timestamp": "2019-10-09T10:12:57.050-03:00",
                "payload": {
                    "conversion_identifier": "newsletter",
                    "name": "Lead Name",
                    "email": "contact_new@rdstation.com"
                }
            },
            {
                "event_type": "CONVERSION",
                "event_family": "CDP",
                "event_identifier": "contact-form",
                "event_timestamp": "2019-12-10T06:12:57.050-03:00",
                "payload": {
                    "conversion_identifier": "contact-form",
                    "email": "contact_new@rdstation.com",
                    "company_name": "Company Name",
                    "mobile_phone": "+55 00 00000-0000",
                    "cf_my_custom_field": "my custom field"
                }
            }
        ]
        return MockResponse(200, contact_events_response)

    elif args[0] == f"{_base_url}/platform/contacts/lead_uuid/funnels/default":
        funnels_response = {
            "lifecycle_stage": "Client",
            "opportunity": True,
            "contact_owner_email": "email@example.org",
            "fit": 60,
            "interest": 100
        }
        return MockResponse(200, funnels_response)

    elif args[0] == f"{_base_url}/integrations/webhooks":
        if kwargs.get('data'):
            create_webhook_response = {
                'uuid': 'deba1cba-d81c-4a57-8cfd-2aa1aa13b483',
                'event_type': 'WEBHOOK.CONVERTED',
                'entity_type': 'CONTACT',
                'url': 'http://example-url.com',
                'http_method': 'POST',
                'include_relations': ['COMPANY', 'CONTACT_FUNNEL'],
                'event_identifiers': []}
            return MockResponse(201, create_webhook_response)

        else:
            list_webhooks_response = {
                "webhooks": [
                    {
                        "uuid": "5408c5a3-4711-4f2e-8d0b-13407a3e30f3",
                        "event_type": "WEBHOOK.CONVERTED",
                        "event_identifiers": ["newsletter"],
                        "entity_type": "CONTACT",
                        "url": "http://my-url.com",
                        "http_method": "POST",
                        "include_relations": []
                    },
                    {
                        "uuid": "642d985c-487c-4c53-b9de-2c1223841cae",
                        "event_type": "WEBHOOK.MARKED_OPPORTUNITY",
                        "event_identifiers": [],
                        "entity_type": "CONTACT",
                        "url": "http://my-url.com",
                        "http_method": "POST",
                        "include_relations": ["COMPANY", "CONTACT_FUNNEL"]
                    }
                ]
            }
            return MockResponse(200, list_webhooks_response)

    elif args[0] == f"{_base_url}/integrations/webhooks/webhook_uuid":
        if kwargs.get('data'):
            update_webhooks_response = {
                "uuid": "webhook_uuid",
                "event_type": "WEBHOOK.CONVERTED",
                "entity_type": "CONTACT",
                "url": "http://my-url.com",
                "http_method": "POST",
            }
            return MockResponse(201, update_webhooks_response)
        else:
            return MockResponse(204)

    return MockResponse(404)


class TestRdApi(TestCase):

    @mock.patch('rd_station.rd_station_api.RdApi._refresh_access_token')
    def setUp(self, mock__refresh_access_token):
        self.rd_api = RdApi(client_id, client_secret, refresh_token)

    def test_if_authorization_error_is_raised_when_using_wrong_credentials(self):
        with self.assertRaises(AuthorizationError):
            RdApi(client_id, client_secret, refresh_token)

    @mock.patch.object(requests, 'post', side_effect=mock_requests)
    def test__refresh_access_token(self, mock_requests):
        access_token = self.rd_api._refresh_access_token()
        assert isinstance(access_token, str)
        mock_requests.assert_called_once()

    @mock.patch.object(requests, 'get', side_effect=mock_requests)
    def test_get_contact_by_uuid(self, mock_requests):
        uuid = 'c2f3d2b3-7250-4d27-97f4-eef38be32f7f'
        contact_info = self.rd_api.get_contact_by_uuid(uuid).json()
        assert isinstance(contact_info, dict)
        assert isinstance(contact_info['name'], str)
        mock_requests.assert_called_once()

    @mock.patch.object(requests, 'get', side_effect=mock_requests)
    def test_get_contact_by_email(self, mock_requests):
        email = 'contact@example.com'
        contact_info = self.rd_api.get_contact_by_email(email).json()
        assert isinstance(contact_info, dict)
        assert isinstance(contact_info['name'], str)
        mock_requests.assert_called_once()

    @mock.patch.object(requests, 'get', side_effect=mock_requests)
    def test_get_contact_events(self, mock_requests):
        contact_events = self.rd_api.get_contact_events('lead_uuid').json()
        assert isinstance(contact_events, list)
        assert isinstance(contact_events[1]['payload'], dict)
        mock_requests.assert_called_once()

    @mock.patch.object(requests, 'get', side_effect=mock_requests)
    def test_get_contact_funnels(self, mock_requests):
        contact_funnels = self.rd_api.get_contact_funnels('lead_uuid').json()
        assert isinstance(contact_funnels, dict)
        assert isinstance(contact_funnels['opportunity'], bool)
        assert isinstance(contact_funnels['contact_owner_email'], str)
        assert isinstance(contact_funnels['fit'], int)
        assert isinstance(contact_funnels['interest'], int)
        mock_requests.assert_called_once()

    @mock.patch.object(requests, 'post', side_effect=mock_requests)
    def test_create_webhook(self, mock_requests):
        webhook_url = 'http://my-url.com'
        webhook_response = self.rd_api.create_webhook(webhook_url)
        webhook = webhook_response.json()
        self.assertEqual(webhook_response.status_code, 201)
        assert isinstance(webhook, dict)
        assert isinstance(webhook['event_identifiers'], list)
        assert isinstance(webhook['include_relations'], list)
        mock_requests.assert_called_once()

    @mock.patch.object(requests, 'get', side_effect=mock_requests)
    def test_list_webhooks(self, mock_requests):
        webhooks = self.rd_api.list_webhooks().json()
        assert isinstance(webhooks, dict)
        assert isinstance(webhooks['webhooks'], list)
        mock_requests.assert_called_once()

    @mock.patch.object(requests, 'delete', side_effect=mock_requests)
    def test_delete_webhook(self, mock_requests):
        delete_webhook_response = self.rd_api.delete_webhook('webhook_uuid')
        self.assertEqual(delete_webhook_response.status_code, 204)
        mock_requests.assert_called_once()

    @mock.patch.object(requests, 'put', side_effect=mock_requests)
    def test_updated_webhooks(self, mock_requests):
        req_data = {
            "entity_type": "CONTACT",
            "event_type": "WEBHOOK.CONVERTED",
            "url": "http://my-url.com",
            "http_method": "POST",
        }
        update_webhook_response = self.rd_api.updated_webhooks('webhook_uuid', req_data)
        updated_webhook = update_webhook_response.json()
        self.assertEqual(update_webhook_response.status_code, 201)
        assert isinstance(updated_webhook, dict)
        self.assertEqual(updated_webhook['uuid'], 'webhook_uuid')
        mock_requests.assert_called_once()
