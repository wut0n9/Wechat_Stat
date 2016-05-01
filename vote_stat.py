# coding: utf8
import pymongo
from bson import SON, Code
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import re


client = MongoClient()
moments_doc = client.wechatDB.wechatcollection

# build indexfriends_voted_1
if 'friends_voted_1' in list(moments_doc.index_information()):
    pass
else:
    moments_doc.create_index([('friends_voted', pymongo.ASCENDING)], unique=False)

def sendmostvote():


        result = moments_doc.find({'friends_voted': {'$regex': 'WuT0n9'}})
        print '#---------------------------------------#'
        print '共送出赞的个数为：', result.count()
        for i, r in enumerate(result):
            print '#----------第 %s 位------------#' % (i + 1)
            print '赞送给了：', r.get('nickname')
            print '所赞文章标题:', r.get('artile_title', u'未知')
            print '所赞消息:', r.get('content', u'未知')
            print '同赞的人：', r.get('friends_voted')
        # http://www.tuicool.com/articles/i6n6Vv
        # http://api.mongodb.org/python/current/api/pymongo/collection.html?highlight=group#pymongo.collection.Collection.group
        reducer = Code("""
                    function(obj, pre){
                        pre.count++;
                    }
        """)
        conditionsql = {'friends_voted': {'$regex': 'WuT0n9'}}
        result_grouped = moments_doc.group(key={'nickname': 1}, condition=conditionsql, initial={'count': 0}, reduce=reducer)

        """
        [{u'count': 3.0, u'nickname': u'\u946b\u60c5'}, {u'count': 1.0, u'nickname': u'WuT0n9'}, {u'count': 3.0, u'nickname': u'\u5929\u732b'}, {u'count': 1.0, u'nickname': u'impyer'}, {u'count': 2.0, u'nickname': u'\u5f20\u8fce'}, {u'count': 1.0, u'nickname': u'\u8b5a\u6797\u6ce2'}, {u'count': 3.0, u'nickname': u'\u77e5\u9053\u521b\u5b87-Fooying'}, {u'count': 4.0, u'nickname': u'\u9ebb\u9f99\u6cc9'}, {u'count': 1.0, u'nickname': u'\u738b\u5a9b'}, {u'count': 3.0, u'nickname': u'\u4f59\u5f26'}, {u'count': 1.0, u'nickname': u'\u5415\u66fc\u4e3d'}, {u'count': 1.0, u'nickname': u'\u8d75\u9633'}, {u'count': 3.0, u'nickname': u'\u5e05\u54e5'}, {u'count': 1.0, u'nickname': u'\u6c6a\u653f\u8f89'}, {u'count': 2.0, u'nickname': u'\u5b9d\u6e90'}, {u'count': 2.0, u'nickname': u'\u53d1\u6167'}, {u'count': 1.0, u'nickname': u'\u9648\u8499\u8499'}, {u'count': 1.0, u'nickname': u'\u9a6c\u709c\u97ec'}, {u'count': 1.0, u'nickname': u'\u5468\u5fd7\u7f8e'}, {u'count': 2.0, u'nickname': u'\u738b\u838e\u838e'}, {u'count': 1.0, u'nickname': u'\u674e\u5a1c'}, {u'count': 1.0, u'nickname': u'\u5218\u745e\u6668'}, {u'count': 1.0, u'nickname': u'\u90a2\u6cfd\u548c'}]
        """

        def getkey(item):

            return item.get('count')
        result_sorted = sorted(result_grouped, key=getkey, reverse=True)
        print '<送出赞数： 接收者>'
        for rs in result_sorted:
            nn = rs.get('nickname')
            print '%*s:%3s' % (7, rs.get('count'), nn)
        print '共计送出 %s 个赞' % sum([r.get('count') for r in result_sorted])
        print '-------结束对送出赞的统计-------------'

# sendmostvote()


def getmostvote():

    result = moments_doc.find({'nickname': {'$regex': 'WuT0n9'}})
    print '-------进入对获取的赞的处理----------'
    print '近72天朋友圈共发出 %s 条信息' % result.count()
    voting_friends_list = []
    for r in result:
        vfl = r.get('friends_voted')
        voting_friends_list.append(vfl)
    result_delete = [x for x in voting_friends_list if x is not None]
    pattern = re.compile(r'^ ')
    temp_list = []
    for a in ','.join(result_delete).split(','):
        temp_list.append(pattern.sub('', a))
    voting_friends = {}
    for rd in temp_list:
        if rd not in voting_friends:
            voting_friends[rd] = 1
        else:
            voting_friends[rd] += 1
    print '<获得赞数 ： 来自>'
    new_voting_friends = sorted(voting_friends.items(), key=lambda v: v[1], reverse=False)
    # list(reversed(new_voting_friends))
    for k in new_voting_friends[::-1]:
        print '%*s:%3s' % (7, k[1], k[0])

    print '共计获得 %s 个赞' % sum(nvf[1] for nvf in new_voting_friends)


if __name__ == '__main__':
    print '------------------得到最多赞的统计----------------\n'
    getmostvote()
    print '------------------送出最多赞的统计----------------\n'
    sendmostvote()