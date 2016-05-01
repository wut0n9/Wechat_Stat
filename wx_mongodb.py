from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)


def save_wechat(doc):
        client = MongoClient()
        moments_doc = client.wechatDB.wechatcollection
        moments_doc.insert_one(doc)
        logging.info('< %s >Insertto document successfully' % doc)
        # save method