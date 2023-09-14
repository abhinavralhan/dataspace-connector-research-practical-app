import json
import os
from os import path


class Utils:
    def __init__(self):
        cwd = os.getcwd() + "\\downloads"
        filePath = cwd + "\\aggregate.txt"
        self.filePath = filePath

    def writefile(self, jsonData):
        content = json.dumps(jsonData)
        f = open(self.filePath, "w")
        f.write(content)
        f.close()


