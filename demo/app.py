# -*- coding: utf-8 -*-
import redis
import tornado.web
import tornado.ioloop
from tornado.options import define, options

from wechat_handler import WechatHandler
from main_handler import MainHandler


define('wx_appid', default='')
define('wx_appsecret', default='')
define('wx_token', default='')
define('website', default='')
options.parse_command_line()


url_partern = [
    (r'/wechat/?', WechatHandler),
    (r'/?', MainHandler),
]

settings = {
    'autoreload' : True,
    'debug' : True,
    'cookie_secret':'fdsfaffsfsa',
}


if __name__ == '__main__':
    app = tornado.web.Application(url_partern, **settings)
    app.cache = redis.StrictRedis()
    app.listen(8888)
    print('server starting...')
    tornado.ioloop.IOLoop.instance().start()