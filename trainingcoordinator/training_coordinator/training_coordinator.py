from consumer.consumer import Consumer
from provider.provider import Provider
from aggregation.aggregation import Aggregation
from provider import provider as providerUrl
import traceback
from downloads import downloads
import os
from os import path

'''params = [{"recipient": "https://edge-contributor-1:8080/api/ids/data"},
          {"recipient": "https://edge-contributor-2:8080/api/ids/data"},
          {"recipient": "https://edge-contributor-3:8080/api/ids/data"}]'''

params = [{"recipient": "http://host.docker.internal:8081/api/ids/data"},
          {"recipient": "http://host.docker.internal:8082/api/ids/data"},
          {"recipient": "http://host.docker.internal:8083/api/ids/data"}]

agreements = {}


def trainingCoordinator(port):
    global agreements
    edgeData = []
    aggregation = Aggregation()
    provider = Provider(port)
    for param in params:
        consumer = Consumer(port, param)
        try:
            consumer.getCatalogs()
            consumer.getCurrentCatalog(consumer.catalogs)
            consumer.getResources()
            consumer.getArtifacts()
            if consumer.resources[0] in agreements.keys():
                consumer.getExistingNegotiatedArtifacts(agreements[consumer.resources[0]])
            else:
                consumer.negotiateContract()
                consumer.getNegotiatedArtifacts()
                agreements[consumer.resources[0]] = consumer.agreement
            edgeData.append(consumer.data[0])
            print(consumer.data)
        except:
            print("trainingCoordinator Consumer failed")

    aggregation.aggregateData(edgeData)
    aggregation.writeData(aggregation.aggregateContent)

    print(aggregation.aggregateContent)

    try:
        if provider.checkCatalog():
            artifact_url = provider.getExistingArtifact()
            provider.addData(providerUrl.setDataLink(artifact_url), aggregation.filePath)
            os.remove(aggregation.filePath)
        else:
            provider.clearResources()
            provider.addCatalog()
            provider.addResource()
            provider.bind(providerUrl.setResources(provider.catalog), provider.resource)

            provider.addContract()
            provider.addRule()
            provider.bind(providerUrl.setRules(provider.contract), provider.rule)
            provider.bind(providerUrl.setContracts(provider.resource), provider.contract)

            provider.addRepresentation()
            provider.addArtifact()
            provider.bind(providerUrl.setArtifacts(provider.representation), provider.artifact)
            provider.bind(providerUrl.setRepresentations(provider.resource), provider.representation)

            provider.addData(providerUrl.setDataLink(provider.artifact), aggregation.filePath)
            os.remove(aggregation.filePath)

    except:
        traceback.print_exc()
        print("trainingCoordinator Provider failed")
