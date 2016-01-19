# -*- coding: utf-8 -*-
import functools
import tornado.web
from tornado.options import options

from weixin_sdk.public import WxApi, WxAuthApi


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


def wx_authenticated(method):
    """
    微信web认证装饰器,需实现get_wx_user和set_wx_user方法
    :return:
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.get_wx_user():
            if self.request.method in ("GET", "HEAD"):
                if self.get_query_argument('code', None):
                    code = self.get_query_argument('code')
                    resutls = WxAuthApi.get_access_token(
                            appid=options.wx_appid,
                            appsecret=options.wx_appsecret,
                            code=code
                    )
                    openid = resutls.get('openid', '')
                    if not openid:
                        raise tornado.web.HTTPError(401)
                    self.set_wx_user(openid)
                else:
                    url = options.website + self.request.uri
                    authorize_url = WxAuthApi.authorized_redirect_url(redirect_uri=url,
                                                                      appid=options.wx_appid,
                                                                      scope='snsapi_base',
                                                                      state='STATE')
                    self.redirect(authorize_url)
                    return
            else:
                raise tornado.web.HTTPError(403)
        return method(self, *args, **kwargs)
    return wrapper