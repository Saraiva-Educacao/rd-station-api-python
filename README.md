# rd-station-api-python

Python for access RD Station API.

[RD Developers Official Documentation](https://developers.rdstation.com/en/overview)

## Development Environment setup

To create the development environment it's recommended to use conda. 
You can download and install it from the links bellow:

https://docs.conda.io/en/latest/miniconda.html
https://www.anaconda.com/distribution/

Run the following commands to get the environment ready

```
conda create -n ENVIRONMENT_NAME python=3.7
conda activate ENVIRONMENT_NAME
pip install -r requirements.txt
``` 

# Usage

### Configuration

Before getting youre credentials, you need to create file auth rd_station_authentication.json:

For details on what `client_id`, `client_secret` and `refresh_token` are, 
check the [developers portal](https://developers.rdstation.com/en/authentication).

```json
{
  "client_id": "049bf777-bbbb-0000-9e09-7ebe2972b8b0",
  "client_secret": "952e14d9dbad9c28d2247da9a19645d8",
  "refresh_token": "refresh_token"
}
```

```python
import json
from rd_station.rd_station_api import RdApi


with open('rd_station_authentication.json') as json_file:
    rd_station_authentication = json.load(json_file)

client_id = rd_station_authentication['client_id']
client_secret = rd_station_authentication['client_secret']
refresh_token = rd_station_authentication['refresh_token']

rd_api = RdApi(client_id, client_secret, refresh_token=refresh_token)
```
### Contacts

#### Getting a Contact by UUID
Returns data about a specific Contact

```python
rd_api = RdApi(client_id, client_secret, refresh_token=refresh_token)
rd_api.get_contact_by_uuid('lead_uuid')
```

#### Getting a Contact by Email

Returns data about a specific Contact

```python
rd_api = RdApi(client_id, client_secret, refresh_token=refresh_token)
rd_api.get_contact_by_email('email')
```

### Webhooks

#### Create a webhook subscription
```python
webhook_url = "http://example-url.com"
rd_api = RdApi(client_id, client_secret, refresh_token=refresh_token)
create_webhook_response = rd_api.create_webhook(
    webhook_url,
    event_type='CONVERTED',
    include_relations=["COMPANY", "CONTACT_FUNNEL"]
)
print(create_webhook_response.json())
```

#### List all webhooks
```python
rd_api = RdApi(client_id, client_secret, refresh_token=refresh_token)
webhooks = rd_api.list_webhooks().json()['webhooks']
print(webhooks)
```