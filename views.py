# -*- coding: utf8 -*-
import os
import pypyodbc
import sqlalchemy
import urllib
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Sequence, VARCHAR,NVARCHAR, DateTime, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine, inspect, or_, update
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import datetime as dt
from config import Config


app = Flask(__name__,static_url_path='/static')
app.config.from_object(Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = os.urandom(24)
app.permanent_session_lifetime = dt.timedelta(minutes=900)

db = SQLAlchemy(app)




from Setting import *

app.secret_key = os.urandom(24)
app.permanent_session_lifetime = dt.timedelta(minutes=900)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:   
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['role'] == 'Admin':   
            return f(*args, **kwargs)
        else:
            return redirect(url_for('home'))
    return wrap


@app.route('/ajax_get_dac_diem_vi_tri',methods=['GET', 'POST'])
def ajax_get_dac_diem_vi_tri():
    tinh_thanh = request.args['tinh_thanh']
    vi_tri = request.args['vi_tri']
    mien = sql_tool_sm("""SELECT distinct Mien 
                          from Data_MB 
                          where Tinh_thanh = ?""", [tinh_thanh])[0][0]
    if mien == 'MB':
        yeu_to_loi_the = [r[0] for r in sql_tool_sm("""SELECT yeu_to from yeu_to where mien = ? and phan_loai = 'LT'""", [mien])]
        yeu_to_bat_loi = [r[0] for r in sql_tool_sm("""SELECT yeu_to from yeu_to where mien = ? and phan_loai = 'BL'""", [mien])]
    elif mien in ('MN', 'MN1'):
        yeu_to_loi_the = [r[0] for r in sql_tool_sm("""SELECT yeu_to from yeu_to where mien = ? and vi_tri = ? and phan_loai = 'LT'""", [mien, vi_tri])]
        yeu_to_bat_loi = [r[0] for r in sql_tool_sm("""SELECT yeu_to from yeu_to where mien = ? and vi_tri = ? and phan_loai = 'BL'""", [mien, vi_tri])]
    result = [r[0] for r in sql_tool_sm("""SELECT dac_diem 
                                           from dac_diem_vi_tri 
                                           where thanh_pho = ?
                                           and vi_tri = ?""",
                                           [tinh_thanh, vi_tri])]
    return jsonify({'result' : result, 'loi_the' : yeu_to_loi_the, 'bat_loi' : yeu_to_bat_loi})


# -------------- BDS BIET THU --------------
@app.route('/ajax_get_option_ten_duong_biet_thu',methods=['GET', 'POST'])
def ajax_get_option_ten_duong_biet_thu():
    ten_du_an = request.args['ten_du_an']
    result = [r[0] for r in sql_tool_sm("""SELECT distinct ten_duong 
                                           from bds_lien_ke_bt 
                                           where ten_du_an = ? order by 1""",
                                           [ten_du_an])]
    return jsonify({'result':result})


@app.route('/ajax_get_option_tang_biet_thu',methods=['GET', 'POST'])
def ajax_get_option_tang_biet_thu():
    ten_du_an = request.args['ten_du_an']
    ten_duong = request.args['ten_duong']

    result = [r[0] for r in sql_tool_sm("""SELECT distinct ten_tang 
                                           from bds_lien_ke_bt 
                                           where ten_du_an = ? 
                                           and ten_duong = ?  order by 1""",
                                           [ten_du_an, ten_duong])]
    return jsonify({'result':result})


@app.route('/ajax_get_option_ma_biet_thu',methods=['GET', 'POST'])
def ajax_get_option_ma_biet_thu():
    ten_du_an = request.args['ten_du_an']
    ten_duong = request.args['ten_duong']
    ten_tang = request.args['ten_tang']

    result = [r[0] for r in sql_tool_sm("""SELECT distinct ma_can 
                                           from bds_lien_ke_bt 
                                           where ten_du_an = ? 
                                           and ten_duong = ? 
                                           and ten_tang = ?  order by 1""",
                                           [ten_du_an, ten_duong, ten_tang])]
    return jsonify({'result':result})


@app.route('/ajax_get_option_gia_biet_thu',methods=['GET', 'POST'])
def ajax_get_option_gia_biet_thu():
    ten_du_an = request.args['ten_du_an']
    ten_duong = request.args['ten_duong']
    ten_tang = request.args['ten_tang']
    ma_can = request.args['ma_can']

    result = sql_tool_sm("""SELECT dien_tich_dat, dien_tich_san_xay_dung, tong_gia_tri_xay_tho, tong_gia_tri_hoan_thien, don_gia_dat, don_gia_ctxd
                            from bds_lien_ke_bt 
                            where ten_du_an = ? 
                            and ten_duong = ? 
                            and ten_tang = ? 
                            and ma_can = ?  order by 1""",
                            [ten_du_an, ten_duong, ten_tang, ma_can])
    return jsonify({'result':result})

# -------------- BDS CAN HO ----------------
@app.route('/ajax_get_option_du_an_can_ho',methods=['GET', 'POST'])
def ajax_get_option_du_an_can_ho():
    ten_du_an = request.args['ten_du_an']
    result = [r[0] for r in sql_tool_sm("""SELECT distinct ten_toa_duong_day_khu 
                                           from data_chung_cu 
                                           where ten_du_an = ?  order by 1""",
                                           [ten_du_an])]
    return jsonify({'result':result})


@app.route('/ajax_get_option_tang_can_ho',methods=['GET', 'POST'])
def ajax_get_option_tang_can_ho():
    ten_du_an = request.args['ten_du_an']
    ten_toa_nha = request.args['ten_toa_nha']

    list_1 = [r[0] for r in sql_tool_sm("""SELECT distinct ten_tang_loai_nha 
                                           from data_chung_cu 
                                           where ten_du_an = ? 
                                           and ten_toa_duong_day_khu = ?  order by 1""",
                                           [ten_du_an, ten_toa_nha])]
    result = sorted([r if 'A' not in r and 'B' not in r and ',' not in r and r != '' else 0 if r == '' else r for r in list_1], key=lambda x: int(str(x).split("A")[0].split("B")[0].split(",")[0]))
    return jsonify({'result':result})


@app.route('/ajax_get_option_ma_can_ho',methods=['GET', 'POST'])
def ajax_get_option_ma_can_ho():
    ten_du_an = request.args['ten_du_an']
    ten_toa_nha = request.args['ten_toa_nha']
    so_tang = request.args['so_tang']

    result = [r[0] for r in sql_tool_sm("""SELECT distinct ma_can 
                                           from data_chung_cu 
                                           where ten_du_an = ? 
                                           and ten_toa_duong_day_khu = ? 
                                           and ten_tang_loai_nha = ? order by 1""",
                                           [ten_du_an, ten_toa_nha, so_tang])]
    return jsonify({'result':result})


@app.route('/ajax_get_option_gia_can_ho',methods=['GET', 'POST'])
def ajax_get_option_gia_can_ho():
    ten_du_an = request.args['ten_du_an']
    ten_toa_nha = request.args['ten_toa_nha']
    so_tang = request.args['so_tang']
    ma_can = request.args['ma_can']

    result = sql_tool_sm("""SELECT dien_tich, loai_dien_tich, don_gia 
                            from data_chung_cu 
                            where ten_du_an = ? 
                            and ten_toa_duong_day_khu = ? 
                            and ten_tang_loai_nha = ? 
                            and ma_can = ?""",
                            [ten_du_an, ten_toa_nha, so_tang, ma_can])
    return jsonify({'result':result})

# ---------------GET OPTION UY BAN-------------
@app.route('/ajax_get_option_quan_huyen_uy_ban',methods=['GET', 'POST'])
def ajax_get_option_quan_huyen_uy_ban():
    tinh_thanh = request.args['tinh_thanh']
    result = [r[0] for r in sql_tool_sm("""SELECT distinct quan_huyen 
                                           from khung_gia_uy_ban 
                                           where thanh_pho = ? order by quan_huyen""",
                                           [tinh_thanh])]

    return jsonify({'result' : result})


@app.route('/ajax_get_option_duong_pho_uy_ban',methods=['GET', 'POST'])
def ajax_get_option_duong_pho_uy_ban():
    tinh_thanh = request.args['tinh_thanh']
    quan_huyen = request.args['quan_huyen']
    result = [r[0] for r in sql_tool_sm("""SELECT distinct tuyen_duong 
                                           from khung_gia_uy_ban 
                                           where thanh_pho = ? 
                                           and quan_huyen = ? order by tuyen_duong""",
                                           [tinh_thanh,quan_huyen])]
    return jsonify({'result':result})


@app.route('/ajax_get_option_tuyen_duong_uy_ban',methods=['GET', 'POST'])
def ajax_get_option_tuyen_duong_uy_ban():
    tinh_thanh = request.args['tinh_thanh']
    quan_huyen = request.args['quan_huyen']
    ten_duong = request.args['ten_duong']
    result = [r[0] for r in sql_tool_sm("""SELECT distinct doan_tu_den 
                                           from khung_gia_uy_ban 
                                           where thanh_pho = ? 
                                           and quan_huyen = ? 
                                           and tuyen_duong = ? order by doan_tu_den""",
                                           [tinh_thanh,quan_huyen,ten_duong])]
    
    value = sql_tool_sm("""SELECT distinct VT1, VT2, VT3, VT4, VT5 
                                           from khung_gia_uy_ban 
                                           where thanh_pho = ? 
                                           and quan_huyen = ? 
                                           and tuyen_duong = ? """,
                                           [tinh_thanh, quan_huyen, ten_duong])

    return jsonify({'result' : result, 'value' : value})


@app.route('/ajax_get_option_vi_tri_bds_uy_ban',methods=['GET', 'POST'])
def ajax_get_option_vi_tri_bds_uy_ban():
    tinh_thanh = request.args['tinh_thanh']
    quan_huyen = request.args['quan_huyen']
    ten_duong = request.args['ten_duong']
    tuyen_duong = request.args['tuyen_duong']

    result = sql_tool_sm("""SELECT distinct VT1, VT2, VT3, VT4, VT5 
                                           from khung_gia_uy_ban 
                                           where thanh_pho = ? 
                                           and quan_huyen = ? 
                                           and tuyen_duong = ? 
                                           and doan_tu_den = ?""",
                                           [tinh_thanh, quan_huyen, ten_duong, tuyen_duong])

    return jsonify({'result':result})


# -------------- BDS NHA THO CU ------------
@app.route('/ajax_get_option_quan_huyen',methods=['GET', 'POST'])
def ajax_get_option_quan_huyen():
    tinh_thanh = request.args['tinh_thanh']
    result = [r[0] for r in sql_tool_sm("""SELECT distinct Quan 
                                           from Data_MB 
                                           where Tinh_thanh = ? order by Quan""",
                                           [tinh_thanh])]
    mien = [r[0] for r in sql_tool_sm("""SELECT distinct Mien 
                                         from Data_MB 
                                         where Tinh_thanh = ?""",
                                         [tinh_thanh])]
    return jsonify({'result' : result, 'mien' : mien})


@app.route('/ajax_get_option_duong_pho',methods=['GET', 'POST'])
def ajax_get_option_duong_pho():
    tinh_thanh = request.args['tinh_thanh']
    quan_huyen = request.args['quan_huyen']
    result = [r[0] for r in sql_tool_sm("""SELECT distinct Duong 
                                           from Data_MB 
                                           where Tinh_thanh = ? 
                                           and Quan = ? order by Duong""",
                                           [tinh_thanh,quan_huyen])]
    return jsonify({'result':result})


@app.route('/ajax_get_option_tuyen_duong',methods=['GET', 'POST'])
def ajax_get_option_tuyen_duong():
    tinh_thanh = request.args['tinh_thanh']
    quan_huyen = request.args['quan_huyen']
    ten_duong = request.args['ten_duong']

    result = [r[0] for r in sql_tool_sm("""SELECT distinct Doan_duong 
                                           from Data_MB 
                                           where Tinh_thanh = ? 
                                           and Quan = ? 
                                           and Duong = ? order by Doan_duong""",
                                           [tinh_thanh,quan_huyen,ten_duong])]
    return jsonify({'result':result})


@app.route('/ajax_get_option_vi_tri_bds',methods=['GET', 'POST'])
def ajax_get_option_vi_tri_bds():
    tinh_thanh = request.args['tinh_thanh']
    quan_huyen = request.args['quan_huyen']
    ten_duong = request.args['ten_duong']
    tuyen_duong = request.args['tuyen_duong']

    result = [r[0] for r in sql_tool_sm("""SELECT distinct Vi_tri 
                                           from Data_MB 
                                           where Tinh_thanh = ? 
                                           and Quan = ? 
                                           and Duong = ? 
                                           and Doan_duong = ? order by Vi_tri""",
                                           [tinh_thanh, quan_huyen, ten_duong, tuyen_duong])]
    return jsonify({'result':result})


@app.route('/ajax_get_gia_uy_ban', methods=['GET', 'POST'])
def ajax_get_gia_uy_ban():
    tinh_thanh = request.args['tinh_thanh']
    quan_huyen = request.args['quan_huyen']
    ten_duong = request.args['ten_duong']
    tuyen_duong = request.args['tuyen_duong']
    vi_tri_bds = request.args['vi_tri_bds']
    
    result = sql_tool_sm("""SELECT Thong_tin_quy_hoach, Gia_thi_truong
                            from Data_MB 
                            where Tinh_thanh = ? 
                            and Quan = ? 
                            and Duong = ? 
                            and Doan_duong = ? 
                            and Vi_tri = ?""",
                            [tinh_thanh, quan_huyen, ten_duong, tuyen_duong, vi_tri_bds])
    return jsonify({'result' : result})


# GET RESULT
def he_so_dieu_chinh(value,percent):
    if percent == 0:
        return 0
    else:
        return float(value)*(1-float(percent))/float(percent)


# TINH HE SO DIEN TICH
def quy_mo(x, mien, vi_tri):
    if x == 0 or x == '':
        return 0
    if mien == 'MB':
        quy_mo_data = sql_tool_sm("SELECT * FROM quy_mo where mien = ?",[mien])
    elif mien in ('MN', 'MN1'):
        quy_mo_data = sql_tool_sm("SELECT * FROM quy_mo where mien = ? and vi_tri = ?",[mien, vi_tri])
    for r in range(len(quy_mo_data)):
        data_0 = float(quy_mo_data[r][0])
        data_1 = quy_mo_data[r][1]
        data_2 = quy_mo_data[r+1][1]
        data_3 = float(quy_mo_data[r+1][0])
        data_4 = float(quy_mo_data[-1][0])
        data_5 = quy_mo_data[-1][1]

        if x < data_0:
            return data_1
        elif x == data_0:
            return data_1
        elif data_0 < x < data_3:
            y = data_2 - (data_3 - x)*(data_2 - data_1)/(data_3 - data_0)
            return y
        elif x > data_4:
            return data_5
        

# HE SO MAT TIEN
def mat_tien(x, mien, vi_tri):
    if x == 0 or x == '':
        return 0
    if mien == 'MB':
        mat_tien_data = sql_tool_sm("SELECT * FROM mat_tien where mien = ?",[mien])
    elif mien in ('MN', 'MN1'):
        mat_tien_data = sql_tool_sm("SELECT * FROM mat_tien where mien = ? and vi_tri = ?",[mien, vi_tri])

    for r in range(len(mat_tien_data)):
        if x < mat_tien_data[r][0]:
            return mat_tien_data[r][1]
        elif x == mat_tien_data[r][0]:
            return mat_tien_data[r][1]
        elif mat_tien_data[r][0] < x < mat_tien_data[r+1][0]:
            y = mat_tien_data[r+1][1] - ((mat_tien_data[r+1][0] - x)*(mat_tien_data[r+1][1] - mat_tien_data[r][1])/(mat_tien_data[r+1][0] - mat_tien_data[r][0])) 
            return y
        elif x > mat_tien_data[-1][0]:
            return mat_tien_data[-1][1]


#DO RONG NGO
def do_rong_ngo(a, b, x, mien):
    x = float(x)
    if x == 0 or x == '':
        return 0
    do_rong_ngo_data = sql_tool_sm("SELECT * FROM do_rong_ngo WHERE Tinh_thanh = ? and Vi_tri = ?",(a,b))
    if not do_rong_ngo_data and mien == 'MB':
        do_rong_ngo_data = sql_tool_sm("SELECT * FROM do_rong_ngo WHERE Tinh_thanh = ? and Vi_tri = ?",(u'Hà Nội',b))
    elif not do_rong_ngo_data and mien == 'MN':
        do_rong_ngo_data = sql_tool_sm("SELECT * FROM do_rong_ngo WHERE Tinh_thanh = ? and Vi_tri = ?",(u'Hồ Chí Minh',b))
    # print do_rong_ngo_data
    for r in range(len(do_rong_ngo_data)):
        if x < do_rong_ngo_data[r][2]:
            return do_rong_ngo_data[r][3]
        elif x == do_rong_ngo_data[r][2]:
            return do_rong_ngo_data[r][3]
        elif do_rong_ngo_data[r][2] < x < do_rong_ngo_data[r+1][2]:
            y = do_rong_ngo_data[r+1][3] - ((do_rong_ngo_data[r+1][2] - x)*(do_rong_ngo_data[r+1][3] - do_rong_ngo_data[r][3])/(do_rong_ngo_data[r+1][2] - do_rong_ngo_data[r][2])) 
            return y
        elif x > do_rong_ngo_data[-1][2]:
            return do_rong_ngo_data[-1][3]
  

#KC TRUC CHINH  
def khoang_cach_den_truc_chinh(a, b, x, mien):
    x = float(x)
    if x == 0 or x == '':
        return 0
    khoang_cach_den_truc_chinh_data = sql_tool_sm("SELECT * FROM khoang_cach_den_truc_chinh WHERE Tinh_thanh = ? and Vi_tri = ?",(a, b))
    if not khoang_cach_den_truc_chinh_data and mien == 'MB':
        khoang_cach_den_truc_chinh_data = sql_tool_sm("SELECT * FROM khoang_cach_den_truc_chinh WHERE Tinh_thanh = ? and Vi_tri = ?",(u'Hà Nội', b))
    elif not khoang_cach_den_truc_chinh_data and mien == 'MN':
        khoang_cach_den_truc_chinh_data = sql_tool_sm("SELECT * FROM khoang_cach_den_truc_chinh WHERE Tinh_thanh = ? and Vi_tri = ?",(u'Hồ Chí Minh', b))
    for r in range(len(khoang_cach_den_truc_chinh_data)):
        if x < khoang_cach_den_truc_chinh_data[r][2]:
            return khoang_cach_den_truc_chinh_data[r][3]
        elif x == khoang_cach_den_truc_chinh_data[r][2]:
            return khoang_cach_den_truc_chinh_data[r][3]
        elif khoang_cach_den_truc_chinh_data[r][2] < x < khoang_cach_den_truc_chinh_data[r+1][2]:
            y = khoang_cach_den_truc_chinh_data[r+1][3] - ((khoang_cach_den_truc_chinh_data[r+1][2] - x)*(khoang_cach_den_truc_chinh_data[r+1][3] - khoang_cach_den_truc_chinh_data[r][3])/(khoang_cach_den_truc_chinh_data[r+1][2] - khoang_cach_den_truc_chinh_data[r][2])) 
            return y
        elif x > khoang_cach_den_truc_chinh_data[-1][2]:
            return khoang_cach_den_truc_chinh_data[-1][3]


@app.route('/ajax_get_result', methods=['GET', 'POST'])
def ajax_get_result():
    # GET DATA
    tinh_thanh = request.args['tinh_thanh_thi_truong']
    quan_huyen = request.args['quan_huyen_thi_truong']
    ten_duong = request.args['ten_duong_thi_truong']
    tuyen_duong = request.args['tuyen_duong_thi_truong']
    vi_tri_bds = request.args['vi_tri_bds_thi_truong']

    try:
        do_rong_ngo_thi_truong = float(request.args['do_rong_ngo_thi_truong'])
    except:
        do_rong_ngo_thi_truong = 0
    try:
        kcach_truc_chinh_thi_truong = float(request.args['kcach_truc_chinh_thi_truong'])
    except:
        kcach_truc_chinh_thi_truong = 0
    try:
        dien_tich_dat_thi_truong = float(request.args['dien_tich_dat_thi_truong'])
    except:
        dien_tich_dat_thi_truong = 0
    try:
        do_rong_mat_tien_thi_truong = float(request.args['do_rong_mat_tien_thi_truong'])
    except:
        do_rong_mat_tien_thi_truong = 0
    hinh_dang = request.args['hinh_dang']
    list_yeu_to = request.args['data_yeu_to'].split("|")

    # TINH HE SO
    gia_tri_du_lieu = sql_tool_sm("""SELECT Gia_thi_truong, Mien
                            from Data_MB 
                            where Tinh_thanh = ? 
                            and Quan = ? 
                            and Duong = ? 
                            and Doan_duong = ? 
                            and Vi_tri = ?""",
                            [tinh_thanh, quan_huyen, ten_duong, tuyen_duong, vi_tri_bds])
    gia_thi_truong = int(gia_tri_du_lieu[0][0].split(".")[0])
    mien = gia_tri_du_lieu[0][1]
    # print do_rong_ngo(tinh_thanh,vi_tri_bds,7,mien)
    he_so_dien_tich = quy_mo(dien_tich_dat_thi_truong, mien, vi_tri_bds)
    he_so_mat_tien = mat_tien(do_rong_mat_tien_thi_truong, mien, vi_tri_bds)
    if vi_tri_bds in [u'Vị trí 2', u'Vị trí 3', u'Vị trí 4']:
        he_so_rong_ngo = do_rong_ngo(tinh_thanh, vi_tri_bds, do_rong_ngo_thi_truong, mien)
        he_so_kc_truc_chinh = khoang_cach_den_truc_chinh(tinh_thanh, vi_tri_bds, kcach_truc_chinh_thi_truong, mien)
    else:
        he_so_rong_ngo = 0
        he_so_kc_truc_chinh = 0
    try:
        if mien == 'MB':
            vi_tri = u'Vị trí 0'
            he_so_hinh_dang = float(sql_tool_sm("""SELECT * FROM hinh_dang 
                                        where hinh_dang = ? 
                                        and mien = ?""",[hinh_dang, mien])[0][1])
        elif mien in ('MN', 'MN1'):
            vi_tri = vi_tri_bds            
            he_so_hinh_dang = float(sql_tool_sm("""SELECT * FROM hinh_dang 
                                        where hinh_dang = ? 
                                        and mien = ?
                                        and vi_tri = ?""",[hinh_dang, mien, vi_tri_bds])[0][1])
    except:
        he_so_hinh_dang = 0
    

    # TINH GIA DIEU CHINH
    gia_tri_dieu_chinh_dien_tich = he_so_dieu_chinh(gia_thi_truong, he_so_dien_tich)
    gia_tri_dieu_chinh_mat_tien = he_so_dieu_chinh(gia_thi_truong, he_so_mat_tien)
    gia_tri_dieu_chinh_hinh_dang = he_so_dieu_chinh(gia_thi_truong, he_so_hinh_dang)
    if list_yeu_to != [u'']:
        gia_tri_dieu_chinh_yeu_to = sum([he_so_dieu_chinh(gia_thi_truong ,sql_tool_sm("select ti_le from yeu_to where yeu_to = ? and mien = ? and vi_tri = ?",[r, mien, vi_tri])[0][0]) for r in list_yeu_to])
    else:
        gia_tri_dieu_chinh_yeu_to = 0
    gia_dieu_chinh_rong_ngo = he_so_dieu_chinh(gia_thi_truong, he_so_rong_ngo)
    gia_dieu_kc_truc_chinh = he_so_dieu_chinh(gia_thi_truong, he_so_kc_truc_chinh)

    # SUM GIA
    gia_dieu_chinh = round(sum([gia_tri_dieu_chinh_dien_tich,
                        gia_tri_dieu_chinh_mat_tien,
                        gia_tri_dieu_chinh_hinh_dang,
                        gia_dieu_chinh_rong_ngo,
                        gia_dieu_kc_truc_chinh,
                        gia_tri_dieu_chinh_yeu_to]) + gia_thi_truong)
    # TRA KET QUA

    result = [gia_thi_truong, gia_dieu_chinh,
            he_so_rong_ngo, gia_dieu_chinh_rong_ngo,
            he_so_kc_truc_chinh, gia_dieu_kc_truc_chinh,
            gia_tri_dieu_chinh_hinh_dang, gia_tri_dieu_chinh_yeu_to]
    return jsonify({'result':result, 'list_yeu_to': list_yeu_to})


#---------------- PAGE ------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
# ----------------ADMIN -----------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get("usn")
        pwd = request.form.get("pd")
        check_user = sql_tool_sm("SELECT phan_quyen, name from sm_user where username = ? and passhash = ?",[user, hash_user(pwd)])
        if check_user:
            session['username'] = user
            session['role'] = check_user[0][0]
            session['name'] = check_user[0][1]
            session['logged_in'] = True
            return redirect(url_for("check_gia"))
        else:
            return redirect(url_for("login"))
    return render_template('login.html')
    


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


# ----------------ADMIN -----------------
@app.route('/ad_cnb_min',methods=['GET', 'POST'])
@login_required
@admin_required
def ad_cnb_min():
    return render_template(
        "trang-chu/admin.html",
        
    )


@app.route('/check_gia',methods=['GET', 'POST'])
@login_required
# @admin_required
def check_gia():
    list_tinh_thanh = [r[0] for r in sql_tool_sm("""SELECT distinct Tinh_thanh 
                                                    from Data_MB order by 1""")]
    list_tinh_thanh_uy_ban = [r[0] for r in sql_tool_sm("""SELECT distinct thanh_pho 
                                                    from khung_gia_uy_ban order by 1""")]
    list_can_ho = [r[0] for r in sql_tool_sm("""SELECT distinct ten_du_an 
                                                from data_chung_cu order by 1""")]
    list_biet_thu = [r[0] for r in sql_tool_sm("""SELECT distinct ten_du_an 
                                                  from bds_lien_ke_bt order by 1""")]
    list_hinh_dang_bds = [r[0] for r in sql_tool_sm("""SELECT distinct hinh_dang from hinh_dang""")]
    return render_template(
        "tool_calculate_template/check_gia.html",
        list_tinh_thanh = list_tinh_thanh,
        list_biet_thu = list_biet_thu,
        list_can_ho = list_can_ho,
        list_hinh_dang_bds = list_hinh_dang_bds,
        list_tinh_thanh_uy_ban = list_tinh_thanh_uy_ban,
        
    )


# ----------------- HOME -----------------
@app.route('/home',methods=['GET', 'POST'])
@login_required
def home():
    list_tinh_thanh = [r[0] for r in sql_tool_sm("""SELECT distinct Tinh_thanh 
                                                    from Data_MB order by 1""")]
    list_tinh_thanh_uy_ban = [r[0] for r in sql_tool_sm("""SELECT distinct thanh_pho 
                                                    from khung_gia_uy_ban order by 1""")]
    list_can_ho = [r[0] for r in sql_tool_sm("""SELECT distinct ten_du_an 
                                                from data_chung_cu order by 1""")]
    list_biet_thu = [r[0] for r in sql_tool_sm("""SELECT distinct ten_du_an 
                                                  from bds_lien_ke_bt order by 1""")]
    list_hinh_dang_bds = [r[0] for r in sql_tool_sm("""SELECT distinct hinh_dang from hinh_dang""")]
    return render_template(
        "trang-chu/home.html",
        list_tinh_thanh = list_tinh_thanh,
        list_biet_thu = list_biet_thu,
        list_can_ho = list_can_ho,
        list_hinh_dang_bds = list_hinh_dang_bds,
        list_tinh_thanh_uy_ban = list_tinh_thanh_uy_ban,
    )


@app.route('/tin_tuc/danh_muc_tin_tuc',methods=['GET', 'POST'])
@login_required
@admin_required
def form_tin_tuc():
    return render_template(
        "trang-chu/tin_tuc/danh_muc_tin_tuc.html",
        
    )

#
@app.route('/user/profile',methods=['GET', 'POST'])
@login_required
def profile():
    
    return render_template(
        "user/profile.html"
        
    )


@app.route('/user/quan_ly_user',methods=['GET', 'POST'])
@login_required
@admin_required
def quan_ly_user():
    quan_ly_user_field = ['name', 'cmnd', 'mail', 'sdt', 'username', 'ngay_khoi_tao', 'phan_quyen', 'trang_thai']
    list_user = sql_tool_sm("SELECT {} from sm_user".format(",".join(quan_ly_user_field)))
    return render_template(
        "user/quan_ly_user.html", list_user = list_user
        
    )


@app.route('/user/tao_moi_user',methods=['GET', 'POST'])
@login_required
@admin_required
def tao_moi_user():
    user_field = ['name', 'cmnd', 'mail', 'sdt', 'username', 'password', 'passhash', 'ngay_khoi_tao', 'phan_quyen', 'trang_thai']
    if request.method == 'POST':
        name = request.form.get("name")
        cmnd = request.form.get("cmnd")
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")
        status = request.form.get("status")
        sdt = request.form.get("sdt")


        sql_tool_sm("INSERT INTO sm_user VALUES({})".format(",".join(["?"]*len(user_field))), [name, cmnd, email, sdt, username, password, hash_user(password), str(dt.datetime.now()), role, status])

    return render_template(
        "user/tao_moi_user.html",
        
    )

from flask import request
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['GET','POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

    
# if __name__ == '__main__':
#     app.debug = True
#     HOST = environ.get('server_host', 'localhost')
#     # HOST = environ.get('server_host', '192.168.0.117')

# ##    NAME = environ.get('server_name','phu.co.tcb.vn:8888')
#     # HOST = environ.get('server_host', 'localhost')
#     try:
#         # PORT = int(environ.get('8080', '8888'))
#         PORT = int(environ.get('server_port', '8799'))
#     except ValueError:
#         PORT = 8899
#     app.run(HOST, PORT, threaded = True)


class Khung_gia_uy_ban(db.Model):
  __tablename__ = "Khung_gia_uy_ban"
  thanh_pho = db.Column('thanh_pho', String, primary_key = True, nullable = False)
  quan_huyen = db.Column('quan_huyen', String, primary_key = True, nullable = False)
  tuyen_duong = db.Column('tuyen_duong', String, primary_key = True, nullable = False)
  doan_tu_den = db.Column('doan_tu_den', String, primary_key = True, nullable = False)
  VT1 = db.Column('VT1', String, primary_key = True, nullable = False)
  VT2 = db.Column('VT2', String, primary_key = True, nullable = False)
  VT3 = db.Column('VT3', String, primary_key = True, nullable = False)
  VT4 = db.Column('VT4', String, primary_key = True, nullable = False)
  VT5 = db.Column('VT5', String, primary_key = True, nullable = False)
  def __init__(self, thanh_pho,quan_huyen,tuyen_duong,doan_tu_den,VT1,VT2,VT3,VT4,VT5):
    self.thanh_pho
    self.quan_huyen
    self.tuyen_duong
    self.doan_tu_den
    self.VT1
    self.VT2
    self.VT3
    self.VT4
    self.VT5
db.create_all()
#
# select *
#
# print(Khung_gia_uy_ban.query.filter_by(thanh_pho = 'Hải Phòng', quan_huyen = 'Hồng Bàng').all())
# print(db.session.query(Khung_gia_uy_ban.VT1, Khung_gia_uy_ban.VT2, Khung_gia_uy_ban.VT3, Khung_gia_uy_ban.VT4, Khung_gia_uy_ban.VT5).all())
#
# insert
#
a1 = update(Khung_gia_uy_ban).where(Khung_gia_uy_ban.thanh_pho == "Hải Phòng").values(quan_huyen = 'Hồng Bàng')