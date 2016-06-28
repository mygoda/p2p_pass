# -*- coding: utf-8 -*-
# __author__ = xutao

from __future__ import division, unicode_literals, print_function
import imghdr

from qiniu import put_data, Auth, put_file
import requests
from config import config

q = Auth(config.get('qiniu', 'QINIU_ACCESS_KEY'), config.get('qiniu', 'QINIU_SECRET_KEY'))
q_token = q.upload_token(bucket=config.get('qiniu', 'QINIU_BUCKET_NAME'), expires=31536000)

def detect_image_type(content):
    return imghdr.what("", h=content)


__author__ = 'bohan'

def upload_img_by_url(url, filename):
    r = requests.get(url=url, stream=True)
    return upload_img(stream=r.content, filename=filename)


def upload_img(stream, filename):
    put_data(up_token=q_token, key=filename, data=stream)
    return 'http://7xkvl2.com1.z0.glb.clouddn.com/%s' % filename

