import os
import logging
import requests
from logdna import LogDNAHandler


username = 'apikey'
api_key = os.environ.get('IBMCLOUD_API_KEY')
privateEndpoint = "https://api.service.softlayer.com"
publicEndpoint = "https://api.softlayer.com"

def setup_logger():
    key = os.environ.get('LOGDNA_INGESTION_KEY')
    log = logging.getLogger('logdna')
    log.setLevel(logging.INFO)

    options = {
        'index_meta': True,
        'tags': 'testing-ce-private-endpoints',
        'url': 'https://logs.private.us-south.logging.cloud.ibm.com/logs/ingest',
        'log_error_response': True
    }

    logger = LogDNAHandler(key, options)

    log.addHandler(logger)

    return log


def check_url(url):
    logger = setup_logger()
    response = requests.get(url)
    logger.info(f"Status code for {url}: {response.status_code}")

def get_virtual_guests(apiEndpoint):
    logger = setup_logger()
    url = str(apiEndpoint + "/rest/v3/SoftLayer_Account/getVirtualGuests")
    headers = {"Authorization": f"Basic {username}:{api_key}"}
    response = requests.get(url, headers=headers)
    logger.info(f"Status code for {url}: {response.status_code}")

def main():
    logger = setup_logger()
    check_url(publicEndpoint)
    check_url(privateEndpoint)
    get_virtual_guests(publicEndpoint)
    get_virtual_guests(privateEndpoint)

if __name__ == '__main__':
    main()
