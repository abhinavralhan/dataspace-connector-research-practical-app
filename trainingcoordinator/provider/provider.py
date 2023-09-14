from provider.api.api import ProviderAPI
from headers import headers
from body import body
from downloads import downloads
import json


class Provider:
    def __init__(self, port):
        self.catalog = None
        self.resource = None
        self.contract = None
        self.rule = None
        self.representation = None
        self.artifact = None
        self.data = None
        self.representation = None
        self.status = 400

        self.providerAPI = ProviderAPI(port=port)

    def addArtifact(self):
        self.providerAPI.post(self.providerAPI.artifactEndPoint, headers=headers.json, body=json.dumps(body.artifact))
        self.artifact = json.loads(self.providerAPI.response.content)["_links"]["self"]["href"]

    def addData(self, url, filePath):
        f = open(filePath, "rb")
        self.providerAPI.put(url, headers=headers.octet, body=f)
        f.close()
        self.status = 200

    def addCatalog(self):
        self.providerAPI.post(self.providerAPI.catalogEndPoint, headers=headers.json, body=json.dumps(body.catalog))
        self.catalog = json.loads(self.providerAPI.response.content)["_links"]["self"]["href"]

    def addResource(self):
        self.providerAPI.post(self.providerAPI.resourceEndPoint, headers=headers.json, body=json.dumps(body.resource))
        self.resource = json.loads(self.providerAPI.response.content)["_links"]["self"]["href"]

    def addRepresentation(self):
        self.providerAPI.post(self.providerAPI.representationEndPoint, headers=headers.json,
                              body=json.dumps(body.representation))
        self.representation = json.loads(self.providerAPI.response.content)["_links"]["self"]["href"]

    def addRule(self):
        self.providerAPI.post(self.providerAPI.ruleEndPoint, headers=headers.json, body=json.dumps(body.rule))
        self.rule = json.loads(self.providerAPI.response.content)["_links"]["self"]["href"]

    def addContract(self):
        self.providerAPI.post(self.providerAPI.contractEndPoint, headers=headers.json, body=json.dumps(body.contract))
        self.contract = json.loads(self.providerAPI.response.content)["_links"]["self"]["href"]

    def clearResources(self):
        params = {}
        self.providerAPI.get(self.providerAPI.catalogEndPoint, headers=headers.json)
        catalogs = json.loads(self.providerAPI.response.content)["_embedded"]["catalogs"]
        for i in range(0, len(catalogs)):
            catUrl = catalogs[i]["_links"]["self"]["href"]
            splits = catUrl.split("/")
            params["id"] = splits[-1]
            self.providerAPI.delete(self.providerAPI.catalogEndPoint + "/" + params["id"], headers=headers.json,
                                    params=params)

    def checkCatalog(self):
        self.providerAPI.get(self.providerAPI.catalogEndPoint, headers=headers.json)
        catalogs = json.loads(self.providerAPI.response.content)["_embedded"]["catalogs"]
        if len(catalogs) > 0:
            return True
        return False

    def getExistingArtifact(self):
        params = {}
        self.providerAPI.get(self.providerAPI.artifactEndPoint, headers=headers.json)
        artifacts = json.loads(self.providerAPI.response.content)["_embedded"]["artifacts"]
        catUrl = artifacts[0]["_links"]["self"]["href"]
        splits = catUrl.split("/")
        params["id"] = splits[-1]
        return self.providerAPI.catalogEndPoint + "/" + params["id"]

    def bind(self, parentUrl, childUrl):
        bindResource = [childUrl]
        self.providerAPI.post(parentUrl, headers=headers.json, body=json.dumps(bindResource))
        self.status = 200


def setResources(Path):
    return Path + "/offers"


def setRules(Path):
    return Path + "/rules"


def setContracts(Path):
    return Path + "/contracts"


def setArtifacts(Path):
    return Path + "/artifacts"


def setRepresentations(Path):
    return Path + "/representations"


def setDataLink(Path):
    return Path + "/data"
