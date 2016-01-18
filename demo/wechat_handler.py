# -*- coding: utf-8 -*-

from pprint import pprint as pp

import tornado.web
import tornado.gen
from tornado.options import options
from base_handler import BaseHandler

from weixin_sdk.public import WxBasic, WxApi, WxMenuApi,WxAuthApi


def _menu_dict():
    return {
        'button': [
            {
                'type': 'view',
                'name': u'测试菜单',
                'url':  '/'
            },
            {
                'type': 'view',
                'name': u'测试',
                'url': 'http://www.qq.com/'
            }
        ]
    }


class WechatHandler(BaseHandler):

    def prepare(self):
        self.appid = options.wx_appid
        self.appsecret = options.wx_appsecret
        self.token = options.wx_token

        self.wechat = WxBasic(appid=self.appid,
                              appsecret=self.appsecret,
                              token=self.token)

    def get(self):
        if self.wechat.check_signature(self.query_arguments):
            echo_str = self.get_query_argument('echostr', '')
            self.write(echo_str)
        else:
            self.write('wrong, request not from wechat!')

    def post(self):
        if not self.wechat.check_signature(self.query_arguments):
            return self.write('signature error!')
        self.wechat.parse_data(self.request.body, query=self.query_arguments)
        message = self.wechat.message
        if message.msgType != 'event' and self._check_repeat(message.msgId):
            return self.write('')

        pp(message)
        if message.msgType == 'text':
            if message.content == u'菜单':
                results = WxMenuApi(self.wx_access_token).create_menu(_menu_dict())
                self.write(self.wechat.pack_text(results.get('errmsg', '')))
                return

        reply = self.wechat.pack_text('hi')
        self.write(reply)

    @property
    def query_arguments(self):
        query = {}
        for k in self.request.arguments.keys():
            query[k] = self.get_query_argument(k)
        return query


    def _check_repeat(self, msg_id):
        old_msg_id = self.cache.get("wechat_message_id")
        if old_msg_id and old_msg_id == msg_id:
            return True
        self.cache.set('wechat_message_id', msg_id)
        return False


class WechatOAuth2Handler(BaseHandler):
    def get(self):
        if self.get_query_argument('code', None):
            code = self.get_query_argument('code')
            state = self.get_query_argument('state', '')
            self.fetch_token(code, state)
        else:
            redirect_url = WxAuthApi.authorized_redirect_url(redirect_uri=options.website + self.reverse_url('wx_auth'),
                                                             appid=options.wx_appid,
                                                             scope='snsapi_base',
                                                             state=self.get_query_argument('state', 'main'))
            self.redirect(redirect_url)

    def fetch_token(self, code, state):
        resutls = WxAuthApi.get_access_token(
                appid=options.wx_appid,
                appsecret=options.wx_appsecret,
                code=self.get_query_argument('code')
        )
        openid = resutls.get('openid', '')
        self.set_secure_cookie('user7', openid)
        if state == 'main':
            self.redirect('/', permanent=True)
        else:
            pass
