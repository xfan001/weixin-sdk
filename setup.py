# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import weixin_sdk


setup(
    name='weixin-sdk',
    version=weixin_sdk.__version__,
    description=u'wechat python sdk',
    keywords="weixin wx wechat sdk",
    author='xfan001',
    author_email='lifan121@gmail.com',
    install_requires = ['requests>=2.9','pycrypto==2.6.1'],
    packages=find_packages(exclude=['demo']),
    url='https://github.com/xfan001/weixin-sdk'
)
