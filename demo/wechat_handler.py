# -*- coding: utf-8 -*-

from pprint import pprint as pp

import tornado.web
from tornado.options import options
from base_handler import BaseHandler

from weixin_sdk.public import WxBasic, WxApi, WxMenuApi, WxMsgApi, WxUserApi


def _menu_dict():
    return {
        'button': [
            {
                'type': 'view',
                'name': u'测试菜单',
                'url':  options.website+'/'
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

        self.test(message)

        reply = self.wechat.pack_text('hi')
        self.write(reply)

    def test(self, message):
        self.wx_api = WxApi(self.wx_access_token)
        self.wxuser_api = WxUserApi(self.wx_access_token)
        self.wx_msg_api = WxMsgApi(self.wx_access_token)

        self.wx_msg_api.send_text(message.fromUserName, u'测试客服消息')
        print self.wxuser_api.get_groups()
        print self.wx_api.get_wechat_ips()


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


