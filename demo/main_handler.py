# -*- coding: utf-8 -*-
from tornado.options import options
from base_handler import BaseHandler

from weixin_sdk.public import WxJsApi


class MainHandler(BaseHandler):

    def get(self):
        if not self.current_user:
            redirect_uri = self.reverse_url('wx_auth') + '?state=main'
            self.redirect(redirect_uri)
            return
        # self.write(str(self.current_user))
        sign_dict = WxJsApi.sign(options.wx_appid, self.wx_jsapi_ticket, options.website+self.request.path)
        print(sign_dict)
        print options.website+self.request.path
        self.render('main.html', sign=sign_dict, user=self.current_user)
