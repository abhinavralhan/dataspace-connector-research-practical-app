import socket
from consumer.consumer import Consumer
from aggregation.aggregation import Aggregation
from provider.provider import Provider
import json
from ports import ports
from provider import provider as providerUrl
import os
import random
import traceback

HOST = '127.0.0.1'
PORT = 65432

files = ["a1"]
param = {"recipient": "https://training-coordinator:8080/api/ids/data"}


def writeFilepath(jsonData, Path):
    content = json.dumps(jsonData)
    f = open(Path, "w")
    f.write(content)
    f.close()


def randomGeneration():
    option1, option2, option3 = random.sample(range(1, 20), 3)
    content = {"d": option1, "q": option2, "n": option3}
    return content


def edgeNodeProvider(port):
    provider = Provider(port)

    try:
        provider.clearResources()
        provider.addCatalog()
        provider.addResource()
        provider.bind(providerUrl.setResources(provider.catalog), provider.resource)

        provider.addContract()
        provider.addRule()
        provider.bind(providerUrl.setRules(provider.contract), provider.rule)
        provider.bind(providerUrl.setContracts(provider.resource), provider.contract)

        provider.addRepresentation()
        provider.bind(providerUrl.setRepresentations(provider.resource), provider.representation)
        cwd = os.getcwd() + "\\downloads\\"
        for path in files:
            filePath = cwd + path + ".txt"
            provider.addArtifact()
            provider.bind(providerUrl.setArtifacts(provider.representation), provider.artifact)

            hyperParams = randomGeneration()
            writeFilepath(hyperParams, filePath)
            provider.addData(providerUrl.setDataLink(provider.artifact), filePath)
            print(hyperParams)
            os.remove(filePath)
    except:
        traceback.print_exc()
        print("edgeNode Provider failed for port :", port)


def edgeNodeConsumer(port):
    try:
        consumer = Consumer(port, param)

        consumer.getCatalogs()
        consumer.getCurrentCatalog(consumer.catalogs)
        consumer.getResources()
        consumer.getArtifacts()
        consumer.negotiateContract()
        consumer.getNegotiatedArtifacts()

        print(consumer.data)
    except:
        traceback.print_exc()
        print("edgeNode Consumer failed for port :", port)
