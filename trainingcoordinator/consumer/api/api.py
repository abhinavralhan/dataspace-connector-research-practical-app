import requests
from credentials import credentials
import warnings

warnings.filterwarnings("ignore", message="Unverified HTTPS request")
docker_host = "host.docker.internal"
localhost = "localhost"


class ConsumerAPI:

    def __init__(self, port):
        self.endPoint = "https://" + docker_host + ":" + str(port) + "/api/ids/description"
        self.policy = "https://" + docker_host + ":" + str(port) + "/api/examples/policy"
        self.contract = "https://" + docker_host + ":" + str(port) + "/api/ids/contract"
        self.agreement = "https://" + docker_host + ":" + str(port) + "/api/agreements/"
        self.response = None

    def post(self, url, headers, params):
        self.response = \
            requests.post(url, verify=False, headers=headers, params=params,
                          auth=(credentials.username, credentials.password))

    def get(self, url, headers):
        self.response = requests.get(url, verify=False, headers=headers,
                                     auth=(credentials.username, credentials.password))

    def postBodyParams(self, url, headers, body, params):
        self.response = \
            requests.post(url, verify=False, headers=headers, data=body, params=params,
                          auth=(credentials.username, credentials.password))

    def postBody(self, url, headers, body):
        self.response = \
            requests.post(url, verify=False, headers=headers, data=body,
                          auth=(credentials.username, credentials.password))
