# -*- coding: utf-8 -*-
from tornado.options import options
from base_handler import BaseHandler, wx_authenticated

from weixin_sdk.public import WxJsApi


class MainHandler(BaseHandler):

    def prepare(self):
        self.wx_user = None

    @wx_authenticated
    def get(self, *args, **kwargs):
        openid = self.get_wx_user()
        self.write(u'你的openid是:%s' % openid)


    def get_wx_user(self):
        if self.wx_user:
            return self.wx_user
        return self.get_secure_cookie('wx_user')

    def set_wx_user(self, openid):
        self.wx_user = openid
        self.set_secure_cookie('wx_user', openid)
