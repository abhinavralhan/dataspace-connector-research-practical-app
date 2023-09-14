resource = {
    "title": "TrainingCoordinator Provider",
    "description": "data provider for training Coordinator",
    "keywords": ["TrainingCoordinator", "Provider"],
    "paymentModality": "fixedPrice",
    "publisher": "https://openweathermap.org/",
    "language": "EN",
    "license": "http://opendatacommons.org/licenses/odbl/1.0/",
    "sovereign": "https://openweathermap.org/",
    "endpointDocumentation": "https://example.com"
}

catalog = {
    "title": "TrainingCoordinator Catalog",
    "description": "This catalog is used in the TrainingCoordinator Provider"
}

contract = {
    "title": "TrainingCoordinator contract",
    "description": "This contract is used in the TrainingCoordinator Provider",
    "start": "2022-11-28T14:22:01.223Z",
    "end": "2024-11-28T17:22:01.223Z"
}

rule = {
  "value": "{\"@context\":{\"ids\":\"https://w3id.org/idsa/core/\",\"idsc\":\"https://w3id.org/idsa/code/\"},"
           "\"@type\":\"ids:Permission\",\"@id\":\"https://w3id.org/idsa/autogen/permission/2faf053e-63fe-4d47-9140"
           "-d9502639b692\",\"ids:title\":[{\"@value\":\"SimpleAccessRule\","
           "\"@type\":\"http://www.w3.org/2001/XMLSchema#string\"}],\"ids:description\":[{"
           "\"@value\":\"Thisisasimpleaccessrule\",\"@type\":\"http://www.w3.org/2001/XMLSchema#string\"}],"
           "\"ids:action\":[{\"@id\":\"https://w3id.org/idsa/code/USE\"}]} "
  }

artifact = {
    "title": "TrainingCoordinator artifact",
    "description": "This artifact is used in the TrainingCoordinator Provider",
    "value": "TrainingCoordinator",
    "basicAuth": {
        "key": "admin",
        "value": "password"
    },
    "apiKey": {
        "key": "string",
        "value": "string"
    },
    "automatedDownload": True
}

representation = {
    "title": "TrainingCoordinator representation",
    "description": "This representation is used in the TrainingCoordinator Provider",
    "mediaType": "string",
    "language": "en",
    "standard": "string"
}

policy = {
    "title": "Access Rule",
    "description": "Provide Access",
    "type": "PROVIDE_ACCESS"
}
