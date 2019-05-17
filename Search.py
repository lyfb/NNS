# coding=utf-8
import base64
import Db
import model
import ExtractFeature


RESULT_OK = 0
RESULT_ERROR = 1
MSG_OK = 'OK'


class Searcher(object):
    def __init__(self, config):
        self.__db = Db.Db.load(config['db'])
        self.__searcher = model.create(config['model'])
        self.__featureExtractor = ExtractFeature.FeatureExtractor(config['featureExtractor'])

    def __savePic(self, data, path, fileName):
        picData = data.split(",")[1]
        decodedPicData = base64.b64decode(picData)
        path = f'{path}/{fileName}'

        with open(path, 'wb') as f:
            f.write(decodedPicData)

    def search(self, data, pageNum, pageSize, num):
        path = 'data/tmp'   # 图片存放路径
        fileName = 'tmp.jpg'

        # 将图片保存到data/tmp下，图片名为tmp.jpg
        try:
            self.__savePic(data, path, fileName)
        except Exception as err:
            return RESULT_ERROR, "图片数据不正确", None

        # 提取图片的特征
        result, msg, _, features = self.__featureExtractor.extract(path, 0)

        if result != 0 or features.shape[0] != 1:
            return RESULT_ERROR, msg, None

        # 搜索
        indexes = self.__searcher.search(features[0], num)
        modelNum = indexes.shape[0]
        pageSizeOneModel = pageSize // modelNum
        if pageSizeOneModel * modelNum != pageSize:
            return RESULT_ERROR, f'当前model数目为:{modelNum},pageSize应该为它的整数倍', None, None
        indexes = indexes[:, pageNum * pageSizeOneModel:(pageNum + 1) * pageSizeOneModel]

        try:
            neighborPaths = []
            for index in indexes:
                neighborPaths.extend(self.__db.getPath(index))
        except Exception as err:
            return RESULT_ERROR, "查询出错", None

        return RESULT_OK, MSG_OK, neighborPaths

