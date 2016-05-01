**程序准备**

 1. Appium移动测试框架
 Ubuntu下Appium的安装、使用请见我发表在Testerhome社区的文章 [点我][1]
 2. 后台数据库为MongoDB
 3. 手机使用数据线连接电脑，并保持手机调试功能处于开启状态。

**程序运行**

 1. 启动Appium，`node --max_old_space_size=4096 appium`
 
 2. 打开**wechat_lxml.py**文件，填写自己QQ账号。获取朋友圈数据，执行`python wechat_lxml.py`
 3. 从获取到的朋友圈数据XML文件中抽取**好友昵称**、**分享文章标题**、**分享理由**、**点赞好友列表**及**评论列表**等字段，当然，还包括了**纯文本内容**。等第二步骤运行结束后，执行`python lxml_store.py`
 4. 统计获得好友赞票的人员比例和送出赞票的统计概况，执行`python vote_stat.py`

附：从MongoDB导出数据至wechat.csv文件里，执行：

    mongoexport -d wechatDB -c wechatcollection --type=csv -f content,reason_artile,artile_title -o wechat.csv

 



  [1]: https://testerhome.com/topics/4235