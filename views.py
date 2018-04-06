# -*- coding: utf8 -*-
import os
import pypyodbc
import sqlalchemy
import urllib

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine, inspect, or_, update


import datetime as dt
from config import Config
from model import Khung_gia_uy_ban, Data_MB, Data_chung_cu, BDS_biet_thu, Yeu_to, Mat_tien, Quy_mo, Hinh_dang, Do_rong_ngo, Khoang_cach_truc, Dac_diem_VT, User_SM, app, db

app.secret_key = os.urandom(24)

app.permanent_session_lifetime = dt.timedelta(minutes=900)
app.config.from_object(Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


from Setting import *

app.secret_key = os.urandom(24)
app.permanent_session_lifetime = dt.timedelta(minutes=900)


# #
# # select *
# result = [r[0] for r in db.session.query(Khung_gia_uy_ban.quan_huyen).filter_by(thanh_pho = u'Hải Phòng').distinct().all()]
# # xx =     db.session.query(Khung_gia_uy_ban.quan_huyen).filter_by(thanh_pho = u'Hải Phòng').first()

# for r in xx:

#
# update
#
# update(Khung_gia_uy_ban).where(Khung_gia_uy_ban.thanh_pho == "Hải Phòng").values(quan_huyen = 'Hồng Bàng')

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
    
    mien = db.session.query(Data_MB.Mien).filter_by(Tinh_thanh = tinh_thanh).distinct().all()[0][0]

    if mien == 'MB':
        yeu_to_loi_the = [r[0] for r in db.session.query(Yeu_to.yeu_to).filter_by(mien = mien, phan_loai = 'LT').distinct().order_by(Yeu_to.yeu_to.asc()).all()]

        yeu_to_bat_loi = [r[0] for r in db.session.query(Yeu_to.yeu_to).filter_by(mien = mien, phan_loai = 'BL').distinct().order_by(Yeu_to.yeu_to.asc()).all()]

    elif mien in ('MN', 'MN1'):
        yeu_to_loi_the = [r[0] for r in db.session.query(Yeu_to.yeu_to).filter_by(mien = mien, vi_tri = vi_tri, phan_loai = 'LT').distinct().order_by(Yeu_to.yeu_to.asc()).all()]
        
        yeu_to_bat_loi = [r[0] for r in db.session.query(Yeu_to.yeu_to).filter_by(mien = mien, vi_tri = vi_tri, phan_loai = 'BL').distinct().order_by(Yeu_to.yeu_to.asc()).all()]

    result = [r[0] for r in db.session.query(Dac_diem_VT.dac_diem).filter_by(thanh_pho = tinh_thanh, vi_tri = vi_tri).distinct().order_by(Dac_diem_VT.dac_diem.asc()).all()]

    return jsonify({'result' : result, 'loi_the' : yeu_to_loi_the, 'bat_loi' : yeu_to_bat_loi})


# -------------- BDS BIET THU --------------
@app.route('/ajax_get_option_ten_duong_biet_thu',methods=['GET', 'POST'])
def ajax_get_option_ten_duong_biet_thu():
    ten_du_an = request.args['ten_du_an']
    result = [r[0] for r in db.session.query(BDS_biet_thu.ten_duong).filter_by(ten_du_an = ten_du_an).distinct().order_by(BDS_biet_thu.ten_duong.asc()).all()]

    return jsonify({'result':result})


@app.route('/ajax_get_option_tang_biet_thu',methods=['GET', 'POST'])
def ajax_get_option_tang_biet_thu():
    ten_du_an = request.args['ten_du_an']
    ten_duong = request.args['ten_duong']

    result = [r[0] for r in db.session.query(BDS_biet_thu.ten_tang).filter_by(ten_du_an = ten_du_an, ten_duong = ten_duong).distinct().order_by(BDS_biet_thu.ten_tang.asc()).all()]

    return jsonify({'result':result})


@app.route('/ajax_get_option_ma_biet_thu',methods=['GET', 'POST'])
def ajax_get_option_ma_biet_thu():
    ten_du_an = request.args['ten_du_an']
    ten_duong = request.args['ten_duong']
    ten_tang = request.args['ten_tang']

    result = [r[0] for r in db.session.query(BDS_biet_thu.ma_can).filter_by(ten_du_an = ten_du_an, ten_duong = ten_duong, ten_tang = ten_tang).distinct().order_by(BDS_biet_thu.ma_can.asc()).all()]

    return jsonify({'result':result})


@app.route('/ajax_get_option_gia_biet_thu',methods=['GET', 'POST'])
def ajax_get_option_gia_biet_thu():
    ten_du_an = request.args['ten_du_an']
    ten_duong = request.args['ten_duong']
    ten_tang = request.args['ten_tang']
    ma_can = request.args['ma_can']

    result = db.session.query(BDS_biet_thu.dien_tich_dat, BDS_biet_thu.dien_tich_san_xay_dung, BDS_biet_thu.tong_gia_tri_xay_tho, BDS_biet_thu.tong_gia_tri_hoan_thien, BDS_biet_thu.don_gia_dat, BDS_biet_thu.don_gia_ctxd).filter_by(ten_du_an = ten_du_an, ten_duong = ten_duong, ten_tang = ten_tang, ma_can = ma_can).distinct().all()[0]

    return jsonify({'result':result})

# -------------- BDS CAN HO ----------------
@app.route('/ajax_get_option_du_an_can_ho',methods=['GET', 'POST'])
def ajax_get_option_du_an_can_ho():
    ten_du_an = request.args['ten_du_an']
    result = [r[0] for r in db.session.query(Data_chung_cu.ten_toa_duong_day_khu).filter_by(ten_du_an = ten_du_an).distinct().order_by(Data_chung_cu.ten_toa_duong_day_khu.asc()).all()]

    return jsonify({'result':result})


@app.route('/ajax_get_option_tang_can_ho',methods=['GET', 'POST'])
def ajax_get_option_tang_can_ho():
    ten_du_an = request.args['ten_du_an']
    ten_toa_nha = request.args['ten_toa_nha']


    list_1 = [r[0] for r in db.session.query(Data_chung_cu.ten_tang_loai_nha).filter_by(ten_du_an = ten_du_an, ten_toa_duong_day_khu = ten_toa_nha).distinct().order_by(Data_chung_cu.ten_tang_loai_nha.asc()).all()]

    result = sorted([r if 'A' not in r and 'B' not in r and ',' not in r and r != '' else 0 if r == '' else r for r in list_1], key=lambda x: int(str(x).split("A")[0].split("B")[0].split(",")[0]))
    return jsonify({'result':result})


@app.route('/ajax_get_option_ma_can_ho',methods=['GET', 'POST'])
def ajax_get_option_ma_can_ho():
    ten_du_an = request.args['ten_du_an']
    ten_toa_nha = request.args['ten_toa_nha']
    so_tang = request.args['so_tang']

    result = [r[0] for r in db.session.query(Data_chung_cu.ma_can).filter_by(ten_du_an = ten_du_an, ten_toa_duong_day_khu = ten_toa_nha, ten_tang_loai_nha = so_tang).distinct().order_by(Data_chung_cu.ma_can.asc()).all()]

    return jsonify({'result':result})


@app.route('/ajax_get_option_gia_can_ho',methods=['GET', 'POST'])
def ajax_get_option_gia_can_ho():
    ten_du_an = request.args['ten_du_an']
    ten_toa_nha = request.args['ten_toa_nha']
    so_tang = request.args['so_tang']
    ma_can = request.args['ma_can']

    result = db.session.query(Data_chung_cu.dien_tich, Data_chung_cu.loai_dien_tich ,Data_chung_cu.don_gia).filter_by(ten_du_an = ten_du_an, ten_toa_duong_day_khu = ten_toa_nha, ten_tang_loai_nha = so_tang, ma_can = ma_can).distinct().order_by(Data_chung_cu.ma_can.asc()).all()[0]

    return jsonify({'result':result})


# ---------------GET OPTION UY BAN-------------
@app.route('/ajax_get_option_quan_huyen_uy_ban',methods=['GET', 'POST'])
def ajax_get_option_quan_huyen_uy_ban():
    tinh_thanh = request.args['tinh_thanh']
    result = [r[0] for r in db.session.query(Khung_gia_uy_ban.quan_huyen).filter_by(thanh_pho = tinh_thanh).distinct().order_by(Khung_gia_uy_ban.quan_huyen.asc()).all()]

    return jsonify({'result' : result})


@app.route('/ajax_get_option_duong_pho_uy_ban',methods=['GET', 'POST'])
def ajax_get_option_duong_pho_uy_ban():
    tinh_thanh = request.args['tinh_thanh']
    quan_huyen = request.args['quan_huyen']
    result = [r[0] for r in db.session.query(Khung_gia_uy_ban.tuyen_duong).filter_by(thanh_pho = tinh_thanh, quan_huyen = quan_huyen).distinct().order_by(Khung_gia_uy_ban.tuyen_duong.asc()).all()]

    return jsonify({'result':result})


@app.route('/ajax_get_option_tuyen_duong_uy_ban',methods=['GET', 'POST'])
def ajax_get_option_tuyen_duong_uy_ban():
    tinh_thanh = request.args['tinh_thanh']
    quan_huyen = request.args['quan_huyen']
    ten_duong = request.args['ten_duong']
    result = [r[0] for r in db.session.query(Khung_gia_uy_ban.doan_tu_den).filter_by(thanh_pho = tinh_thanh, quan_huyen = quan_huyen, tuyen_duong = ten_duong).distinct().order_by(Khung_gia_uy_ban.doan_tu_den.asc()).all()]

    value = db.session.query(Khung_gia_uy_ban.VT1, Khung_gia_uy_ban.VT2, Khung_gia_uy_ban.VT3, Khung_gia_uy_ban.VT4, Khung_gia_uy_ban.VT5).filter_by(thanh_pho = tinh_thanh, quan_huyen = quan_huyen, tuyen_duong = ten_duong).distinct().all()[0]
    return jsonify({'result' : result, 'value' : value})


@app.route('/ajax_get_option_vi_tri_bds_uy_ban',methods=['GET', 'POST'])
def ajax_get_option_vi_tri_bds_uy_ban():
    tinh_thanh = request.args['tinh_thanh']
    quan_huyen = request.args['quan_huyen']
    ten_duong = request.args['ten_duong']
    tuyen_duong = request.args['tuyen_duong']

    result = db.session.query(Khung_gia_uy_ban.VT1, Khung_gia_uy_ban.VT2, Khung_gia_uy_ban.VT3, Khung_gia_uy_ban.VT4, Khung_gia_uy_ban.VT5).filter_by(thanh_pho = tinh_thanh, quan_huyen = quan_huyen, tuyen_duong = ten_duong, doan_tu_den = tuyen_duong).distinct().all()[0]

    return jsonify({'result':result})


# -------------- BDS NHA THO CU ------------
@app.route('/ajax_get_option_quan_huyen',methods=['GET', 'POST'])
def ajax_get_option_quan_huyen():
    tinh_thanh = request.args['tinh_thanh']
    result = [r[0] for r in db.session.query(Data_MB.Quan).filter_by(Tinh_thanh = tinh_thanh).distinct().order_by(Data_MB.Quan.asc()).all()]

    mien = [r[0] for r in db.session.query(Data_MB.Mien).filter_by(Tinh_thanh = tinh_thanh).distinct().order_by(Data_MB.Mien.asc()).all()]
    return jsonify({'result' : result, 'mien' : mien})


@app.route('/ajax_get_option_duong_pho',methods=['GET', 'POST'])
def ajax_get_option_duong_pho():
    tinh_thanh = request.args['tinh_thanh']
    quan_huyen = request.args['quan_huyen']

    result = [r[0] for r in db.session.query(Data_MB.Duong).filter_by(Tinh_thanh = tinh_thanh, Quan = quan_huyen).distinct().order_by(Data_MB.Duong.asc()).all()]

    return jsonify({'result':result})


@app.route('/ajax_get_option_tuyen_duong',methods=['GET', 'POST'])
def ajax_get_option_tuyen_duong():
    tinh_thanh = request.args['tinh_thanh']
    quan_huyen = request.args['quan_huyen']
    ten_duong = request.args['ten_duong']

    result = [r[0] for r in db.session.query(Data_MB.Doan_duong).filter_by(Tinh_thanh = tinh_thanh, Quan = quan_huyen, Duong = ten_duong).distinct().order_by(Data_MB.Doan_duong.asc()).all()]

    return jsonify({'result':result})


@app.route('/ajax_get_option_vi_tri_bds',methods=['GET', 'POST'])
def ajax_get_option_vi_tri_bds():
    tinh_thanh = request.args['tinh_thanh']
    quan_huyen = request.args['quan_huyen']
    ten_duong = request.args['ten_duong']
    tuyen_duong = request.args['tuyen_duong']

    result = [r[0] for r in db.session.query(Data_MB.Vi_tri).filter_by(Tinh_thanh = tinh_thanh, Quan = quan_huyen, Duong = ten_duong, Doan_duong = tuyen_duong ) .distinct().order_by(Data_MB.Vi_tri.asc()).all()]

    return jsonify({'result':result})


@app.route('/ajax_get_gia_uy_ban', methods=['GET', 'POST'])
def ajax_get_gia_uy_ban():
    tinh_thanh = request.args['tinh_thanh']
    quan_huyen = request.args['quan_huyen']
    ten_duong = request.args['ten_duong']
    tuyen_duong = request.args['tuyen_duong']
    vi_tri_bds = request.args['vi_tri_bds']
    
    result = db.session.query(Data_MB.Thong_tin_quy_hoach, Data_MB.Gia_thi_truong).filter_by(Tinh_thanh = tinh_thanh,Quan = quan_huyen, Duong = ten_duong, Doan_duong = tuyen_duong, Vi_tri = vi_tri_bds).distinct().order_by(Data_MB.Doan_duong.asc()).all()[0]

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
        quy_mo_data = db.session.query(Quy_mo).filter_by(mien = mien).all()
    elif mien in ('MN', 'MN1'):
        quy_mo_data = db.session.query(Quy_mo).filter_by(mien = mien, vi_tri = vi_tri).all()


    for r in range(len(quy_mo_data)):
        data_0 = float(quy_mo_data[r].quy_mo)
        data_1 = quy_mo_data[r].ti_le
        data_2 = quy_mo_data[r+1].ti_le
        data_3 = float(quy_mo_data[r+1].quy_mo)
        data_4 = float(quy_mo_data[-1].quy_mo)
        data_5 = quy_mo_data[-1].ti_le

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
        mat_tien_data = db.session.query(Mat_tien).filter_by(mien = mien).all()

    elif mien in ('MN', 'MN1'):
        mat_tien_data = db.session.query(Mat_tien).filter_by(mien = mien, vi_tri = vi_tri).all()


    for r in range(len(mat_tien_data)):
        if x < mat_tien_data[r].mat_tien:
            return mat_tien_data[r].ti_le
        elif x == mat_tien_data[r].mat_tien:
            return mat_tien_data[r].ti_le
        elif mat_tien_data[r].mat_tien < x < mat_tien_data[r+1].mat_tien:
            y = mat_tien_data[r+1].ti_le - ((mat_tien_data[r+1].mat_tien - x)*(mat_tien_data[r+1].ti_le - mat_tien_data[r].ti_le)/(mat_tien_data[r+1].mat_tien - mat_tien_data[r].mat_tien)) 
            return y
        elif x > mat_tien_data[-1].mat_tien:
            return mat_tien_data[-1].ti_le


#DO RONG NGO
def do_rong_ngo(a, b, x, mien):
    x = float(x)
    if x == 0 or x == '':
        return 0
    do_rong_ngo_data = db.session.query(Do_rong_ngo).filter_by(Tinh_thanh = a, vi_tri = b).all()

    if not do_rong_ngo_data and mien == 'MB':
        do_rong_ngo_data = db.session.query(Do_rong_ngo).filter_by(Tinh_thanh = u'Hà Nội', vi_tri = b).all()

    elif not do_rong_ngo_data and mien == 'MN':
        do_rong_ngo_data = db.session.query(Do_rong_ngo).filter_by(Tinh_thanh = u'Hồ Chí Minh', vi_tri = b).all()
    for r in range(len(do_rong_ngo_data)):
        if x < do_rong_ngo_data[r].khoang_cach:
            return do_rong_ngo_data[r].ti_le
        elif x == do_rong_ngo_data[r].khoang_cach:
            return do_rong_ngo_data[r].ti_le
        elif do_rong_ngo_data[r].khoang_cach < x < do_rong_ngo_data[r+1].khoang_cach:
            y = do_rong_ngo_data[r+1].ti_le - ((do_rong_ngo_data[r+1].khoang_cach - x)*(do_rong_ngo_data[r+1].ti_le - do_rong_ngo_data[r].ti_le)/(do_rong_ngo_data[r+1].khoang_cach - do_rong_ngo_data[r].khoang_cach)) 
            return y
        elif x > do_rong_ngo_data[-1].khoang_cach:
            return do_rong_ngo_data[-1].ti_le
  

#KC TRUC CHINH  
def khoang_cach_den_truc_chinh(a, b, x, mien):
    x = float(x)
    if x == 0 or x == '':
        return 0
    khoang_cach_den_truc_chinh_data = db.session.query(Khoang_cach_truc).filter_by(Tinh_thanh = a, vi_tri = b).all()
    if not khoang_cach_den_truc_chinh_data and mien == 'MB':
        khoang_cach_den_truc_chinh_data = db.session.query(Khoang_cach_truc).filter_by(Tinh_thanh = u'Hà Nội', vi_tri = b).all()
    elif not khoang_cach_den_truc_chinh_data and mien == 'MN':
        khoang_cach_den_truc_chinh_data = db.session.query(Khoang_cach_truc).filter_by(Tinh_thanh = u'Hồ Chí Minh', vi_tri = b).all()
    for r in range(len(khoang_cach_den_truc_chinh_data)):
        if x < khoang_cach_den_truc_chinh_data[r].khoang_cach:
            return khoang_cach_den_truc_chinh_data[r].ti_le
        elif x == khoang_cach_den_truc_chinh_data[r].khoang_cach:
            return khoang_cach_den_truc_chinh_data[r].ti_le
        elif khoang_cach_den_truc_chinh_data[r].khoang_cach < x < khoang_cach_den_truc_chinh_data[r+1].khoang_cach:
            y = khoang_cach_den_truc_chinh_data[r+1].ti_le - ((khoang_cach_den_truc_chinh_data[r+1].khoang_cach - x)*(khoang_cach_den_truc_chinh_data[r+1].ti_le - khoang_cach_den_truc_chinh_data[r].ti_le)/(khoang_cach_den_truc_chinh_data[r+1].khoang_cach - khoang_cach_den_truc_chinh_data[r].khoang_cach)) 
            return y
        elif x > khoang_cach_den_truc_chinh_data[-1].khoang_cach:
            return khoang_cach_den_truc_chinh_data[-1].ti_le


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
    gia_tri_du_lieu = db.session.query(Data_MB.Gia_thi_truong, Data_MB.Mien).filter_by(Tinh_thanh = tinh_thanh, Quan = quan_huyen, Duong = ten_duong, Doan_duong = tuyen_duong, Vi_tri = vi_tri_bds).all()


    gia_thi_truong = int(gia_tri_du_lieu[0][0].split(".")[0])
    mien = gia_tri_du_lieu[0][1]
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
            he_so_hinh_dang = float(db.session.query(Hinh_dang).filter_by(hinh_dang = hinh_dang, mien = mien)[0][1])

        elif mien in ('MN', 'MN1'):
            vi_tri = vi_tri_bds
            he_so_hinh_dang = float(db.session.query(Hinh_dang).filter_by(hinh_dang = hinh_dang, mien = mien, vi_tri = vi_tri_bds)[0][1])         

    except:
        he_so_hinh_dang = 0
    

    # TINH GIA DIEU CHINH
    gia_tri_dieu_chinh_dien_tich = he_so_dieu_chinh(gia_thi_truong, he_so_dien_tich)
    gia_tri_dieu_chinh_mat_tien = he_so_dieu_chinh(gia_thi_truong, he_so_mat_tien)
    gia_tri_dieu_chinh_hinh_dang = he_so_dieu_chinh(gia_thi_truong, he_so_hinh_dang)
    if list_yeu_to != [u'']:
        gia_tri_dieu_chinh_yeu_to = sum([he_so_dieu_chinh(gia_thi_truong, db.session.query(Yeu_to.ti_le).filter_by(yeu_to = r, mien = mien, vi_tri = vi_tri).all()[0].ti_le) for r in list_yeu_to])
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
        check_user = db.session.query(User_SM.phan_quyen, User_SM.name).filter_by(username = user, passhash = hash_user(pwd)).distinct().all()[0]

        if check_user:
            session['username'] = user
            session['role'] = check_user.phan_quyen
            session['name'] = check_user.name
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
# @login_required
# @admin_required
def check_gia():
    list_tinh_thanh = [r[0] for r in db.session.query(Data_MB.Tinh_thanh).distinct().order_by(Data_MB.Tinh_thanh.asc()).all()]
    list_tinh_thanh_uy_ban = [r[0] for r in db.session.query(Khung_gia_uy_ban.thanh_pho).distinct().order_by(Khung_gia_uy_ban.thanh_pho.asc()).all()]

    list_can_ho = [r[0] for r in db.session.query(Data_chung_cu.ten_du_an).distinct().order_by(Data_chung_cu.ten_du_an.asc()).all()]

    list_biet_thu = [r[0] for r in db.session.query(BDS_biet_thu.ten_du_an).distinct().order_by(BDS_biet_thu.ten_du_an.asc()).all()]

    list_hinh_dang_bds = [r[0] for r in db.session.query(Hinh_dang.hinh_dang).distinct().order_by(Hinh_dang.hinh_dang.asc()).all()]

    return render_template(
        "tool_calculate_template/check_gia.html",
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
    list_user = db.session.query(User_SM.name, User_SM.cmnd, User_SM.mail, User_SM.sdt, User_SM.username, User_SM.ngay_khoi_tao, User_SM.phan_quyen, User_SM.trang_thai).all()
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

        new_user = User_SM(name, cmnd, email, sdt, username, password, hash_user(password), str(dt.datetime.now()), role, status)


        db.session.add(new_user)
        db.session.commit()

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

    
if __name__ == '__main__':
    app.debug = True
    HOST = environ.get('server_host', 'localhost')
    # HOST = environ.get('server_host', '192.168.0.117')

##    NAME = environ.get('server_name','phu.co.tcb.vn:8888')
    # HOST = environ.get('server_host', 'localhost')
    try:
        # PORT = int(environ.get('8080', '8888'))
        PORT = int(environ.get('server_port', '8800'))
    except ValueError:
        PORT = 8800
    app.run(HOST, PORT, threaded = True)



