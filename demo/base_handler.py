# -*- coding: utf-8 -*-

import tornado.web
from tornado.options import options

from weixin_sdk.public import WxApi


class BaseHandler(tornado.web.RequestHandler):

    @property
    def cache(self):
        return self.application.cache

    @property
    def wx_access_token(self):
        token = self.cache.get('wechat_access_token')
        if not token:
            dresults = WxApi.request_access_token(options.wx_appid, options.wx_appsecret)
            token = dresults.get('access_token')
            expires = int(dresults.get('expires_in'))
            self.cache.setex('wechat_access_token', expires, token)
        return token

    @property
    def wx_jsapi_ticket(self):
        token = self.cache.get('wechat_jsapi_ticket')
        if not token:
            dresults = WxApi(self.wx_access_token).request_jsapi_ticket()
            token = dresults.get('jsapi_ticket')
            expires = int(dresults.get('expires_in'))
            self.cache.setex('wechat_jsapi_ticket', expires, token)
        return token

    @property
    def wx_card_api_ticket(self):
        token = self.cache.get('wechat_card_api_ticket')
        if not token:
            dresults = WxApi(self.wx_access_token).request_card_api_ticket()
            token = dresults.get('card_api_ticket')
            expires = int(dresults.get('expires_in'))
            self.cache.setex('wechat_card_api_ticket', expires, token)
        return token


    def get_current_user(self):
        return self.get_secure_cookie('user7')
