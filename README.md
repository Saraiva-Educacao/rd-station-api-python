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

Create file auth rdstation_client.json

Vide: https://developers.rdstation.com/en/overview

## Python code examples:
**Create a webhook subscription:**
```
from rd_station.rd_station_api import RdApi
from os import environ as env

client_id = rd_station_authentication['client_id']
client_secret = rd_station_authentication['client_secret']
refresh_token = rd_station_authentication['refresh_token']

webhook_url = "http://example-url.com"

# Create webhook
rd_api = RdApi(client_id, client_secret, refresh_token=refresh_token)
create_webhook_response = rd_api.create_webhook(webhook_url,
                                                event_type='CONVERTED',
                                                include_relations=["COMPANY", "CONTACT_FUNNEL"])
print(create_webhook_response.json())
```

**List all webhook subscriptions from your account:**
```
from rd_station.rd_station_api import RdApi
from os import environ as env

client_id = rd_station_authentication['client_id']
client_secret = rd_station_authentication['client_secret']
refresh_token = rd_station_authentication['refresh_token']

rd_api = RdApi(client_id, client_secret, refresh_token=refresh_token)
webhooks = rd_api.list_webhooks().json()['webhooks']
print(webhooks)
```