from consumer.api.api import ConsumerAPI
from headers import headers
from body import body
import json


class Consumer:
    def __init__(self, port, param):
        self.catalogs = []
        self.currentCatalog = None
        self.resources = []
        self.contract = None
        self.rule = None
        self.representation = None
        self.artifacts = []
        self.data = []
        self.agreement = None

        self.negotiatedAgreements = []
        self.index = 0

        self.consumerAPI = ConsumerAPI(port)
        self.params = param

    def getCatalogs(self):
        self.consumerAPI.post(self.consumerAPI.endPoint, headers=headers.json, params=self.params)
        self.catalogs = json.loads(self.consumerAPI.response.content)["ids:resourceCatalog"]

    def getCurrentCatalog(self, catalogs):
        for i in range(0, len(catalogs)):
            elementId = catalogs[i]['@id']
            self.params["elementId"] = elementId
            self.consumerAPI.post(self.consumerAPI.endPoint, headers=headers.json, params=self.params)
            if "ids:offeredResource" in json.loads(self.consumerAPI.response.content):
                self.currentCatalog = elementId
                break

    def getResources(self):
        self.consumerAPI.post(self.consumerAPI.endPoint, headers=headers.json, params=self.params)
        offeredResources = json.loads(self.consumerAPI.response.content)['ids:offeredResource']
        for i in range(0, len(offeredResources)):
            self.resources.append(offeredResources[i]['@id'])

    def getArtifacts(self):
        self.consumerAPI.post(self.consumerAPI.endPoint, headers=headers.json, params=self.params)
        offeredResources = json.loads(self.consumerAPI.response.content)['ids:offeredResource']
        for i in range(0, len(offeredResources)):
            offeredArtifacts = offeredResources[i]['ids:representation'][0]['ids:instance']
            for j in range(0, len(offeredArtifacts)):
                self.artifacts.append(offeredArtifacts[j]['@id'])
        self.params["artifactIds"] = self.artifacts
        self.params["resourceIds"] = self.resources
        self.params.pop("elementId")

    def negotiateContract(self):
        self.params["download"] = True
        payload = []
        for i in range(0, len(self.artifacts)):
            self.consumerAPI.postBody(self.consumerAPI.policy, headers.json, json.dumps(body.policy))
            artifactRequest = json.loads(self.consumerAPI.response.content)
            artifactRequest["ids:target"] = self.artifacts[i]
            payload.append(artifactRequest)
        self.consumerAPI.postBodyParams(self.consumerAPI.contract, headers.json, json.dumps(payload), self.params)
        self.agreement = self.consumerAPI.response.headers.get("Location").rsplit('/', 1)[-1]
        self.negotiatedAgreements.append(self.agreement)

    def getNegotiatedArtifacts(self):
        self.consumerAPI.get(self.consumerAPI.agreement + str(self.agreement) + "/artifacts", headers=headers.json)
        artifacts = json.loads(self.consumerAPI.response.content)['_embedded']['artifacts']
        for i in range(0, len(artifacts)):
            negotiatedArtifact = artifacts[i]['_links']['data']['href']
            self.consumerAPI.get(negotiatedArtifact + "/**", headers=headers.json)
            self.data.append(json.loads(self.consumerAPI.response.content))

    def getExistingNegotiatedArtifacts(self, negotiatedAgreement):
        self.consumerAPI.get(self.consumerAPI.agreement + str(negotiatedAgreement) + "/artifacts", headers=headers.json)
        artifacts = json.loads(self.consumerAPI.response.content)['_embedded']['artifacts']
        for i in range(0, len(artifacts)):
            negotiatedArtifact = artifacts[i]['_links']['data']['href']
            self.consumerAPI.get(negotiatedArtifact + "/**", headers=headers.json)
            self.data.append(json.loads(self.consumerAPI.response.content))
