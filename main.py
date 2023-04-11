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
        'tags': 'test-cloud-endpoints',
        'url': 'https://logs.private.us-south.logging.cloud.ibm.com/logs/ingest',
        'log_error_response': True,
        'env': 'development',
        'app': 'test-cloud-endpoints'
    }

    logger = LogDNAHandler(key, options)

    log.addHandler(logger)

    return log


def check_url(url):
    logger = setup_logger()
    response = requests.get(url)
    logger.info(f"Status code for base URL {url}: {response.status_code}")

def get_virtual_guests(apiEndpoint):
    logger = setup_logger()
    url = str(apiEndpoint + "/rest/v3/SoftLayer_Account/getVirtualGuests")
    headers = {"Authorization": f"Basic {username}:{api_key}"}
    response = requests.get(url, headers=headers)
    logger.info(f"Status code for authenticated call to {url}: {response.status_code}")

def main():
    logger = setup_logger()
    logger.info("Testing public classic endpoints")
    check_url(publicEndpoint)
    get_virtual_guests(publicEndpoint)
    logger.info("Testing private classic endpoints")
    check_url(privateEndpoint)
    get_virtual_guests(privateEndpoint)

if __name__ == '__main__':
    main()
