# -*- coding: utf8 -*-

from __future__ import division
from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
import os
from os import environ
import pypyodbc
import math
import collections
import datetime as dt
import sys
import hashlib
import json
import sqlite3
from functools import wraps



def hash_user(user):
    return hashlib.md5(user.encode('utf-8')).hexdigest()


def dt_to_str(x):
    return '{}/{}/{} {}'.format(str(x)[8:10],str(x)[5:7],str(x)[:4],str(x)[11:16])

def str_to_dt(x):
    return dt.datetime.strptime(x,'%m/%d/%Y')


def List2Dict(list_):
    changed = []
    for i in list_:
        if i['status'] == 'Processing':
            changed.append({'case_ID':i['case_id'], 'ten_KH':i['ten_kh'], 'IDKH':i['idkh'], 'san_pham':i['san_pham'], 'ket_qua':i['ket_qua'], 'thoi_gian_tao_HS':i['ngay_tao'] + ' ' + i['thoi_gian_tao'], 'thoi_gian_tra_kq': '-', 'action':'''<button type="button" class="btn_bbh" name="detail" value="" id="view_detail"> <a href="el/'''+i['case_id']+'''"> <input type="checkbox" class="tgl tgl-flip" /> <label class="tgl-btn" data-tg-off="PROCESSING" data-tg-on="COMPLETE"></label> </a> </button>'''} ) 
        else:
            changed.append({'case_ID':i['case_id'], 'ten_KH':i['ten_kh'], 'IDKH':i['idkh'], 'san_pham':i['san_pham'], 'ket_qua':i['ket_qua'], 'thoi_gian_tao_HS':i['ngay_tao'] + ' ' + i['thoi_gian_tao'], 'thoi_gian_tra_kq':i['ngay_tra_ket_qua'] + ' ' + i['thoi_gian_tra_ket_qua'], 'action':'''<button type="button" class="btn_bbh" name="detail" value="" id="view_detail"> <a href="el/'''+i['case_id']+'''"> <input type="checkbox" class="tgl tgl-flip" checked="true" /> <label class="tgl-btn" data-tg-off="PROCESSING" data-tg-on="COMPLETE"></label> </a> </button>'''} ) 
    return changed

def round_int(x):
    return int(round(x))

def convert_int(x):
    if x:
        return int(x.replace(',',''))
    else:
        return 0

def change_list_order(x,i):
    if i == 3:
        x = [x[1], x[2], x[0]]
    elif i == 4:
        x = [x[2], x[1], x[3], x[0]]
    return x

def add_comma(x):
    if len(x) <= 3:
        result = x
    else:
        no_part = len(x)//3
        result = ''
        if no_part == 1:
            part_1 = x[-3:]
            result = part_1
            result = x[:-3] + ',' + result
        else:
            part_1 = x[-3:]
            result = part_1
            for r in xrange(1, no_part):
                part_n = x[- 3*(r + 1): - 3*r]
                result = part_n + ',' + result
            if len(x)%3 == 0:
                pass
            else:
                result = x[: - 3*(r + 1)] + ',' + result
    return result

def bo_dau_tieng_viet(x):
    dict_co_dau = {'a': [u'á', u'à', u'ả', u'ã', u'ạ', u'ă', u'ắ', u'ằ', u'ẳ', u'ẵ', u'ặ', u'â', u'ấ', u'ầ', u'ẩ', u'ẫ', u'ậ'], 'e': [u'é', u'è', u'ẻ', u'ẽ', u'ẹ', u'ê', u'ế', u'ề', u'ể', u'ễ', u'ệ'], 'i': [u'í', u'ì', u'ỉ', u'ĩ', u'ị'], 'o': [u'ó', u'ò', u'ỏ', u'õ', u'ọ', u'ô', u'ố', u'ồ', u'ổ', u'ỗ', u'ộ', u'ơ', u'ớ', u'ờ', u'ở', u'ỡ', u'ợ'], 'u': [u'ú', u'ù', u'ủ', u'ũ', u'ụ', u'ư', u'ứ', u'ừ', u'ử', u'ữ', u'ự'], 'y': [u'ý', u'ỳ', u'ỷ', u'ỹ', u'ỵ'], 'd': [u'đ']}

    for r in dict_co_dau.keys():
        for r1 in dict_co_dau[r]:
            x = x.replace(r1, r)
    return x

def find_ko_dau(x, y):
    list_co_dau = [u'á', u'à', u'ả', u'ã', u'ạ', u'ắ', u'ằ', u'ẳ', u'ẵ', u'ặ', u'ấ', u'ầ', u'ẩ', u'ẫ', u'ậ', u'é', u'è', u'ẻ', u'ẽ', u'ẹ', u'ế', u'ề', u'ể', u'ễ', u'ệ', u'í', u'ì', u'ỉ', u'ĩ', u'ị', u'ó', u'ò', u'ỏ', u'õ', u'ọ', u'ố', u'ồ', u'ổ', u'ỗ', u'ộ', u'ớ', u'ờ', u'ở', u'ỡ', u'ợ', u'ú', u'ù', u'ủ', u'ũ', u'ụ', u'ứ', u'ừ', u'ử', u'ữ', u'ự', u'ý', u'ỳ', u'ỷ', u'ỹ', u'ỵ', u'ă', u'â', u'ê', u'ô', u'ơ', u'ư', u'đ']
    if True in [r in list_co_dau for r in y.lower()]:
        result = x.find(y)
    else:
        result = bo_dau_tieng_viet(x).find(bo_dau_tieng_viet(y))
    return result

# ----------------- ISV -----------------
# Thổ cư
list_header = ['Case ID', u'Người yêu cầu', u'Đơn vị yêu cầu', u'Ngày gửi yêu cầu', u'Người khởi tạo', u'Thời gian khởi tạo']
