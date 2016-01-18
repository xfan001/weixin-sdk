# -*- coding: utf-8 -*-

# from .utils import HttpUtil, Util
#
#
# class WxPay(object):
#
#     """
#     微信支付相关接口
#     """
#
#     BASE_URL = 'https://api.mch.weixin.qq.com/'
#
#     def __init__(self, appid, mch_id, sign_key):
#         """
#         初始化支付对象
#         :param appid: 公众号appid
#         :param mch_id: 商户id
#         :param sign_key: 商户签名密钥
#         """
#         self._appid = appid
#         self._mchid = mch_id
#         self._sign_key = sign_key
#
#     def place_order(self, trade_type, out_trade_no, body, total_fee, notify_url, **kwargs):
#         """
#         微信统一下单api(文档http://pay.weixin.qq.com/wiki/doc/api/index.php?chapter=9_1)
#         :param trade_type: 交易类型('JSAPI', 'APP', 'NATIVE')
#         :param out_trade_no: 商户订单号,32个字符内
#         :param body: 商品或支付简单描述
#         :param total_fee: 金额(分),默认RMB,需要其他货币类型在kwargs内指定
#         :param notify_url: 支付结果通知地址
#         :return: 返回tuple(code, result), 统一下单结果
#         """
#         kwargs.update(trade_type=trade_type,
#                       out_trade_no=out_trade_no,
#                       body=body,
#                       total_fee=total_fee,
#                       notify_url=notify_url)
#         kwargs.update(appid=self._appid, mch_id=self._mchid)
#         kwargs.update(nonce_str=Util.generate_nonce(20))
#
#         if trade_type == 'NATIVE':
#             kwargs.update(spbill_create_ip=Util.get_local_ip())
#             assert kwargs.get('product_id'), 'Native pay must have product_id'
#         if trade_type == 'JSAPI':
#             kwargs.update(device_info='WEB')
#             assert kwargs.get('openid'), 'JSAPI pay must have openid parameter'
#             assert kwargs.get('spbill_create_ip'), 'ip shold be client(browser) ip when JSAPI'
#         #sign
#         kwargs.update(sign=None)
#         kwargs.update(sign=self._generate_sign(**kwargs))
#
#         return self._post('/pay/unifiedorder', kwargs)
#
#     def query_order(self, transaction_id=None, out_trade_no=None):
#         """
#         查询订单api, 文档(http://pay.weixin.qq.com/wiki/doc/api/index.php?chapter=9_2)
#         :param transaction_id: 微信订单号, 优先
#         :param out_trade_no: 商户内部订单号
#         :return 返回tuple(code, result)
#         """
#         assert transaction_id or out_trade_no, 'transaction_id and out_trade_no must have one'
#         kwargs = {'appid':self._appid, 'mch_id':self._mchid}
#         kwargs.update(nonce_str=Util.generate_nonce(20))
#         if transaction_id:
#             kwargs.update(transaction_id=transaction_id)
#         if out_trade_no:
#             kwargs.update(out_trade_no=out_trade_no)
#
#         sign = self._generate_sign(**kwargs)
#         kwargs.update(sign=sign)
#
#         return self._post('/pay/orderquery', kwargs)
#
#     def close_order(self, out_trade_no):
#         """
#         关闭交易
#         :param out_trade_no: 商户订单号
#         :return: 返回tuple(code, result)
#         """
#         kwargs = {'appid':self._appid, 'mch_id':self._mchid}
#         kwargs.update(out_trade_no=out_trade_no)
#         kwargs.update(nonce_str=Util.generate_nonce(20))
#
#         sign = self._generate_sign(**kwargs)
#         kwargs.update(sign=sign)
#
#         return self._post('/pay/closeorder', kwargs)
#
#     def refund(self):
#         """
#         退款,请求需要双向证书
#         """
#         pass
#
#     def query_refund(self):
#         """
#         查询退款
#         """
#         pass
#
#
#     def _generate_sign(self, **kwargs):
#         """
#         签名算法,返回得到的签名字符串
#         """
#         valid_keys = [k for k in kwargs if kwargs[k] and k != 'sign']
#         valid_keys.sort()
#         kv_str = ''
#         for k in valid_keys:
#             kv_str += '%s=%s&' % (k, kwargs[k])
#         kv_str += '%s=%s' % ('key', self._sign_key)
#         kv_str = Util.encode_data(kv_str)
#         sign = Util.md5(kv_str).upper()
#         return sign
#
#     def _post(self, url, ddata):
#         """
#         :return: (ret_code, dict_data/err_msg)
#         """
#         if self.BASE_URL not in url:
#             url = self.BASE_URL + url
#         xml_data = HttpUtil.post(url, ddata, type='xml')
#         results = Util.xml_to_dict(xml_data)
#         if results.get('return_code', '') == 'SUCCESS':
#             assert results.get('sign') == self._generate_sign(**results), 'sign error, not from wechat pay server'
#             if results.get('result_code','') == 'SUCCESS':
#                 return 0, results
#             else:return 1, results.get('err_code_des', '')
#         else:
#             return 1,results.get('return_msg', '')