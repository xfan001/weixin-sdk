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

**2. WxApi-微信基本接口**

**3. WxAuthApi-网页授权获取用户信息**

**4. WxJsApi-微信JS-API**


### weixin-sdk.pay包含类

**1. WxPay-微信支付**