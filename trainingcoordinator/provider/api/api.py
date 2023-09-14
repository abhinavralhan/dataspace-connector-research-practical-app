import requests
from credentials import credentials
import warnings

warnings.filterwarnings("ignore", message="Unverified HTTPS request")
docker_host = "host.docker.internal"
localhost = "localhost"


class ProviderAPI:

    def __init__(self, port):
        self.artifactEndPoint = "https://" + docker_host + ":" + str(port) + "/api/artifacts"
        self.catalogEndPoint = "https://" + docker_host + ":" + str(port) + "/api/catalogs"
        self.resourceEndPoint = "https://" + docker_host + ":" + str(port) + "/api/offers"
        self.representationEndPoint = "https://" + docker_host + ":" + str(port) + "/api/representations"
        self.contractEndPoint = "https://" + docker_host + ":" + str(port) + "/api/contracts"
        self.ruleEndPoint = "https://" + docker_host + ":" + str(port) + "/api/rules"
        self.response = None

    def post(self, url, headers, body):
        self.response = \
            requests.post(url, verify=False, headers=headers, data=body,
                          auth=(credentials.username, credentials.password))

    def put(self, url, headers, body):
        self.response = \
            requests.put(url, verify=False, headers=headers, data=body,
                         auth=(credentials.username, credentials.password))

    def get(self, url, headers):
        self.response = requests.get(url, verify=False, headers=headers,
                                     auth=(credentials.username, credentials.password))

    def delete(self, url, headers, params):
        self.response = requests.delete(url, verify=False, headers=headers, params=params,
                                        auth=(credentials.username, credentials.password))
