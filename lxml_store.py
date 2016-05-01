# coding=utf-8
from wx_mongodb import save_wechat
from lxml import etree
import re
pattern = re.compile(r'(,\{\{line2}},)')
pattern2 = re.compile(r',$')
with open('wechat.utf8.text', 'rt') as wx:  #
    last_page = []
    for w in wx:  # 1.49440693855
        doc = etree.fromstring(w)
        singal_person = doc.xpath('//android.widget.LinearLayout[contains(@resource-id, "com.tencent.mm:id/bwb")]/..')

        for sp in singal_person:
            wx_dict = {}
            # /@text获取到自身及子代的所有非空text值，不单单是其本身
            # 获取的仅为分享理由，排除了分享文章标题
            # 图文类，如果确实有文字而没有，那么一定转存在content-desc属性中了，此时content-desc即为正确值，如果本来就是没有文字的，content-desc即使有也不是正确的。
            if int(sp.get('index')) == 0:
                content_desc = sp.get('content-desc')
                nickname_index = content_desc.find(',')
                nickname, content = content_desc[:nickname_index], content_desc[nickname_index+1:]
                wx_dict['nickname'] = nickname
                if pattern.search(content):
                    content = pattern.sub('', content)
                if pattern2.search(content):
                    content = pattern2.sub('', content)
                wx_dict['content'] = content
            else:
                nickname = sp.xpath('android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.TextView[contains(@resource-id, "com.tencent.mm:id/cb")]/@text')
                if len(nickname) != 0:
                    wx_dict['nickname'] = nickname[0]

                personal_content_link_text = sp.xpath('android.widget.LinearLayout/android.widget.LinearLayout[contains(@resource-id, "com.tencent.mm:id/bwe")]')  # 显然这个还是从文档开头算起的
                if len(personal_content_link_text) != 0:
                    pc = personal_content_link_text[0]
                    wx_dict['reason_artile'] = pc.get('text')
                    # pass

            # link_content单单为分享文章标题，已排除了分享理由
            link_content = sp.xpath('android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[contains(@resource-id, "com.tencent.mm:id/bpq")]/@text')

            if len(link_content) != 0:
                wx_dict['artile_title'] = link_content[0]

            friends_voted = sp.xpath('android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[contains(@resource-id,"com.tencent.mm:id/bwz")]/@text')
            if len(friends_voted) != 0:
                # 去掉点赞人前的空格
                wx_dict['friends_voted'] = friends_voted[0][2:]  # "friends_voted" : " 张迎"

            # comment_list 好友评论一定是个列表。如果是多人评论必须使用循环语句
            #TODO 这个Xpath在获取好友评论的同时，也能够获取到文章标题，需要分离
            # 真正的评论列表的resource-id属性是为空的，假的（文章标题）的resource-id为com.tencent.mm:id/bpq
            # 上面那条规律还不太好处理，我们可以依据第三个LinearLayout类具有resource-id值为com.tencent.mm:id/bx1的特性分离
            comment_list = sp.xpath('android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[@resource-id="com.tencent.mm:id/bx1"]/android.widget.TextView/@text')

            if len(comment_list) != 0:
                for cl in comment_list:
                    wx_dict['comments'] = cl
            temp_list = []
            for lp in last_page:
                lp_content = lp.get('content', '')
                temp_list.append(lp_content)
                lp_reason_artile = lp.get('reason_artile', '')
                temp_list.append(lp_reason_artile)

            if 'content' in wx_dict:
                if wx_dict['content'] not in temp_list:
                    last_page.append(wx_dict)
                    save_wechat(wx_dict)

            if 'reason_artile' in wx_dict:
                if wx_dict['reason_artile'] not in temp_list:
                    last_page.append(wx_dict)
                    save_wechat(wx_dict)

            # 特例 content与reason_artile都不存在，即表现形式为单单分享了篇文章，没带任何理由。
            if 'reason_artile' not in wx_dict and 'content' not in wx_dict:
                save_wechat(wx_dict)

        if len(last_page) > 10:
            del last_page[0: len(last_page)/2]

        # db.wechatcollection.find({friends_voted: {$in:['WuT0n9']}}).count()
