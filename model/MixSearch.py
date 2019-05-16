# coding=utf-8
import model
import numpy as np


class Searcher(object):
    def __init__(self, searchers):
        self.__searchers = searchers

    @staticmethod
    def build(config):
        modelsConfig = config['models']
        searchers = [model.create(modelConfig) for modelConfig in modelsConfig]

        return Searcher(searchers)

    def search(self, query, k):
        return np.vstack([searcher.search(query, k) for searcher in self.__searchers])


if __name__ == '__main__':
    config = {
        'models': [{'name': 'PQ',
                    'config': {
                        'encoder': {
                            "type": "train",
                            "config": {
                                "datasetPath": "../data/dataset.npy",
                                "numOfSegments": 31,
                                "numOfClasses": 16,
                                "centroidsPath": "../data/centroids.npy"
                            }
                            # 'type': 'load',
                            # "config": {
                            #     'centroidsPath': '../data/centroids8x4.npy'
                            # }
                        },
                        'data': {
                            "type": "train",
                            "dataPath": "../data/dataset.npy",
                            "qdbPath": "../data/qDataset.npy"
                            # 'type': 'load',
                            # 'dataPath': 'data/qDataset.npy'
                        }
                    }},
                   {'name': 'BruteForce',
                    'config': {
                        'data': {
                            "path": "../data/dataset.npy"
                        }
                    }}
        ]
    }

    mixSearcher = Searcher.build(config)
    result = mixSearcher.search(np.random.rand(1, 62), 200)
    print(result)

