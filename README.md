# weixin-sdk
微信公众平台python SDK

## 安装

    pip install weixin-sdk

## 基本使用(以tornado为例)

```python
    # -*- coding: utf-8 -*-
    import tornado.web, tornado.ioloop
    from weixin_sdk.public import WxBasic

    class WechatHandler(tornado.web.RequestHandler):

        def prepare(self):
            self.wechat = WxBasic(appid='YOUR APPID',
                                  appsecret='YOUR APPSECRET',
                                  token='YOUR TOKEN')

        def get(self):
            #首次接入验证,传入url上的query字符串键值对
            if self.wechat.check_signature(self.query_arguments):
                echo_str = self.get_query_argument('echostr', '')
                self.write(echo_str)
            else:
                self.write('wrong, request not from wechat!')

        def post(self):
            self.wechat.parse_data(self.request.body)
            message = self.wechat.message
            #收到消息后针对不同消息类型进行处理
            if message.msgType == 'text':
                content = message.content
                print u'收到文本消息:%s' % content
                self.write(self.wechat.pack_text(content))
                return
            elif message.msgType == 'image':
                pass
            elif message.msgType == 'event':
                pass

        @property
        def query_arguments(self):
            """获取url中的查询字符串dict"""
            query = {}
            for k in self.request.arguments.keys():
                query[k] = self.get_query_argument(k)
            return query

    if __name__ == '__main__':
        app = tornado.web.Application([
            (r"/?", WechatHandler),
        ], autoreload=True)
        app.listen(8888)
        print('server starting...')
        tornado.ioloop.IOLoop.instance().start()
```

## 接口

### weixin-sdk.public包含类

**1. WxBasic-基本消息解析及被动回复,包含签名校验和加解密**

初始化参数: appid, appsecret, token, aes_key=None(默认明文)

相关接口如下:

- check_signature 检查签名,传入url-query-string,必须包含signature,timestamp,nonce三个键
- parse_data 解析原始消息,传入request-body(原始xml字符串)
- message(property修饰) 返回消息字典(对象), 类型有:text,image,voice,video,shortvideo,location,news,event. 字典对象是由xml转换成的键值对,key为驼峰式,也可作为对象属性访问,如message.msgType
- pack_text 将待回复的文本消息打包成xml字符串,下同
- pack_image
- pack_voice
- pack_video
- pack_music
- pack_news
- pack_transfer_kf


**2. WxApi-微信基本接口**

staticmethod:

- request_access_token 网络请求获取access_token, 返回{'access_token':'', 'expires_in':3600}, 获取后需要全局缓存,并在有效期到后需要重新调用接口获取

初始化,传入参数access_token, 相关实例方法:

- request_jsapi_ticket 网络请求jsapi_ticket
- request_card_api_ticket 网络请求card_api_ticket(卡券需要)

客服消息接口:

- send_text 主动发送文本消息,下同
- send_image
- send_voice
- send_video
- send_music
- send_news
- send_mp_news
- send_template_msg
- add_kfaccount  客服账号操作,下同
- update_kfaccount
- del_kfaccount
- get_kf_list

素材管理API:

- get_material_count
- get_material_list
- download_tmp_material  获取临时素材(下载多媒体文件)
- get_material 获取永久素材

用户管理API:

- create_group
- get_groups
- get_group_by_openid
- rename_group
- move_user
- delete_group
- remark_user
- get_user_info 获取/批量获取用户信息
- get_user_list 获取用户列表dict

自定义菜单API:

- create_menu 创建自定义菜单/个性化菜单
- get_menu 获取自定义菜单/个性化菜单
- delete_menu 删除所有菜单
- delete_condition_menu 删除个性化菜单

其他功能API:

- get_wechat_ips 获取微信服务器ip地址
- url_long2short 长连接转短链接
- create_qrcode 创建临时二维码或永久二维码


**3. WxAuthApi-网页授权获取用户信息**

所有方法均为静态方法

- authorized_redirect_url 给定参数,生成授权url
- get_access_token 通过code换取网页授权acces_token
- refresh_access_token 刷新网页授权acces_token
- check_access_token 检验授权凭证（access_token）是否有效
- get_user_info 拉取用户信息, snsapi_base中不需此步骤


**4. WxJsApi-微信JS-API**

- sign 对页面进行签名 传参:appid, jsapi_ticket, page_url(不含#之后的部分), 返回:{'appid':'', 'timestamp':123456789, 'nonce_str':'', 'signature':''}


### weixin-sdk.pay包含类

**1. WxPay-微信支付**

构造参数: appid, mch_id(商户号), sign_key(商户签名密钥), cert=None(商户证书文件,涉及到资金回滚的接口需要)

相关接口:

- unified_order 微信统一下单api
- query_order 查询订单api
- close_order 关闭交易

其他功能接口:

- parse_notify_result 微信服务器通知支付结果时使用, 将request body的xml格式转为dict,签名错误时返回None
- pack_notify_response 将支付结果通知请求的响应结果打包成xml
- sign_for_jspay jssdk调起支付时需要的sign