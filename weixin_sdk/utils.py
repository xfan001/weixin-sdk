# -*- coding: utf-8 -*-

import time
import string
import random
import json
import hashlib
import urlparse
import urllib
import requests
from xml.etree import ElementTree

class HttpUtil:

    def __init__(self):
        pass

    @staticmethod
    def get(url, params=None):
        response = requests.get(url, params)
        return json.loads(response.content)

    @staticmethod
    def post(url, params, ctype='json', **kwargs):
        """post请求,传入dict,返回dict,内部处理json或xml"""
        if ctype == 'json':
            data = json.dumps(params, ensure_ascii=False)
            data = data.encode('utf8')
            response = requests.post(url, data, **kwargs)
            return json.loads(response.content)
        elif ctype == 'xml':
            data = Util.encode_data(params)
            data = Util.dict_to_xml(data)
            response = requests.post(url, data, **kwargs)
            return Util.xml_to_dict(response.content)
        else:
            data = params
            response = requests.post(url, data, **kwargs)
            return response.json()

    @staticmethod
    def url_update_query(url, **kwargs):
        url_parts = list(urlparse.urlparse(url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(**kwargs)
        url_parts[4] = urllib.urlencode(query)
        final_url = urlparse.urlunparse(url_parts)
        return final_url


class Util:

    @staticmethod
    def xml_to_dict(xml_data):
        """xml -> dict"""
        xml_data = Util.encode_data(xml_data)
        data = {}
        for child in ElementTree.fromstring(xml_data):
            data[child.tag] = child.text
        return data

    @staticmethod
    def dict_to_xml(dict_data):
        xml_str = '<xml>'
        for key, value in dict_data.items():
            xml_str += '<%s><![CDATA[%s]]></%s>' % (key, value, key)
        xml_str += '</xml>'
        return xml_str

    @staticmethod
    def timestamp():
        return int(time.time())

    @staticmethod
    def generate_nonce(length=6):
        """生成随机字符串"""
        return ''.join([random.choice(string.digits + string.ascii_letters) for i in range(length)])

    @staticmethod
    def get_local_ip():
        """获取本机ip地址"""
        import socket
        return socket.gethostbyname(socket.gethostname())

    @staticmethod
    def camel_to_underline(camel_format):
        """驼峰命名格式转下划线命名格式"""
        underline_format=''
        if isinstance(camel_format, str):
            for _s_ in camel_format:
                underline_format += _s_ if _s_.islower() else '_'+_s_.lower()
        return underline_format.strip('_')

    @staticmethod
    def underline_to_camel(underline_format):
        """
        下划线命名格式驼峰命名格式
       """
        camel_format = ''
        if isinstance(underline_format, str):
            for _s_ in underline_format.split('_'):
                camel_format += _s_.capitalize()
        return camel_format

    @staticmethod
    def cap_lower(origin_str):
        """首字母小写"""
        if origin_str:
            return origin_str[0].lower() + origin_str[1:]
        return origin_str

    @staticmethod
    def md5(origin_str):
        return hashlib.md5(origin_str).hexdigest()

    @staticmethod
    def sha1(origin_str):
        return hashlib.sha1(origin_str).hexdigest()

    @staticmethod
    def encode_data(data):
        """对dict, list, unicode-str对象编码为utf-8格式"""
        if not data:
            return data

        if isinstance(data, basestring) and isinstance(data, unicode):
            result = data.encode('utf-8')

        elif isinstance(data, dict):
            result = {}
            for k,v in data.items():
                k = Util.encode_data(k)
                v = Util.encode_data(v)
                result.update({k:v})
            return result

        elif isinstance(data, list):
            result = []
            for item in data:
                result.append(Util.encode_data(item))
            return result

        else:
            result = data
        return result


class ObjectDict(dict):
    """
    Makes a dictionary behave like an object, with attribute-style access.
    """
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value


class WxError(Exception):
    pass


if __name__ == '__main__':
    pass