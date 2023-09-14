import json
import pandas as pd

from headers import headers
from utils.utils import Utils
from ports import ports

utils = Utils()


class Aggregation:
    def __init__(self):
        self.aggregateContent = {}
        self.readContent = []
        self.writeContent = None
        self.filePath = None

    '''def readData(self, data_urls):
        for i in range(0, len(data_urls)):
            consumerAPI.get(data_urls[i], headers=headers.json)
            self.readContent.append(json.loads(consumerAPI.response.content))'''

    def aggregateData(self, content):
        params = {}
        keys = getKeys(content[0])
        for key in keys:
            values = []
            for i in range(0, len(content)):
                values.append(content[i][key])
            params[key] = values
        df = pd.DataFrame(data=params)
        mean = df.mean()

        for key in keys:
            self.aggregateContent[key] = mean[key]

    def writeData(self, content):
        utils.writefile(content)
        self.writeContent = content
        self.filePath = utils.filePath


def getKeys(content):
    keys = []
    for key in content.keys():
        keys.append(key)
    return keys
