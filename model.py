from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Sequence, VARCHAR,NVARCHAR, DateTime, update
app = Flask(__name__,static_url_path='/static')



db = SQLAlchemy(app)

# USER
class User_SM(db.Model):
    __tablename__ = "sm_user"
    name = db.Column('name', String, nullable = False)
    cmnd = db.Column('cmnd', String, nullable = False)
    mail = db.Column('mail', String, nullable = False)
    sdt = db.Column('sdt', String, nullable = False)
    username = db.Column('username', String, primary_key = True, nullable = False)
    password = db.Column('password', String, nullable = False)
    passhash = db.Column('passhash', String, nullable = False)
    ngay_khoi_tao = db.Column('ngay_khoi_tao', String, nullable = False)
    phan_quyen = db.Column('phan_quyen', String, nullable = False)
    trang_thai = db.Column('trang_thai', String, nullable = False)
    def __init__(self, name, cmnd, mail, sdt, username, password, passhash, ngay_khoi_tao, phan_quyen, trang_thai):
        self.name = name
        self.cmnd = cmnd
        self.mail = mail
        self.sdt = sdt
        self.username = username
        self.password = password
        self.passhash = passhash
        self.ngay_khoi_tao = ngay_khoi_tao
        self.phan_quyen = phan_quyen
        self.trang_thai = trang_thai
    def __repr__(self):
        return str([self.name, self.cmnd, self.mail, self.sdt, self.username, self.password, self.passhash, self.ngay_khoi_tao, self.phan_quyen, self.trang_thai])
# KHUNG GIA UY BAN
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
    def __repr__(self):
        return str([self.thanh_pho, self.quan_huyen, self.tuyen_duong, self.doan_tu_den, self.VT1, self.VT2, self.VT3, self.VT4, self.VT5])


# DATA MB
class Data_MB(db.Model):
    __tablename__ = "Data_MB"
    Tinh_thanh = db.Column('Tinh_thanh', String, primary_key = True, nullable = False)
    Quan = db.Column('Quan', String, primary_key = True, nullable = False)
    Duong = db.Column('Duong', String, primary_key = True, nullable = False)
    Doan_duong = db.Column('Doan_duong', String, primary_key = True, nullable = False)
    Vi_tri = db.Column('Vi_tri', String, primary_key = True, nullable = False)
    Gia_UBND = db.Column('Gia_UBND', String, primary_key = True, nullable = False)
    Gia_thi_truong = db.Column('Gia_thi_truong', String, primary_key = True, nullable = False)
    Thong_tin_quy_hoach = db.Column('Thong_tin_quy_hoach', String, primary_key = True, nullable = False)
    Dia_chi = db.Column('Dia_chi', String, primary_key = True, nullable = False)
    Mien = db.Column('Mien', String, primary_key = True, nullable = False)

    def __init__(self, Tinh_thanh, Quan, Duong, Doan_duong, Vi_tri, Gia_UBND, Gia_thi_truong, Thong_tin_quy_hoach, Dia_chi, Mien):
        self.Tinh_thanh
        self.Quan
        self.Duong
        self.Doan_duong
        self.Vi_tri
        self.Gia_UBND
        self.Gia_thi_truong
        self.Thong_tin_quy_hoach
        self.Dia_chi
        self.Mien
    def __repr__(self):
        return str([self.Tinh_thanh, self.Quan, self.Duong, self.Doan_duong, self.Vi_tri, self.Gia_UBND, self.Gia_thi_truong, self.Thong_tin_quy_hoach, self.Dia_chi, self.Mien])


# DATA CHUNG CU
class Data_chung_cu(db.Model):
    __tablename__ = "data_chung_cu"
    ten_du_an = db.Column('ten_du_an', String, primary_key = True, nullable = False)
    ten_toa_duong_day_khu = db.Column('ten_toa_duong_day_khu', String, primary_key = True, nullable = False)
    ten_tang_loai_nha = db.Column('ten_tang_loai_nha', String, primary_key = True, nullable = False)
    ma_can = db.Column('ma_can', String, primary_key = True, nullable = False)
    dien_tich = db.Column('dien_tich', String, primary_key = True, nullable = False)
    loai_dien_tich = db.Column('loai_dien_tich', String, primary_key = True, nullable = False)
    don_gia = db.Column('don_gia', String, primary_key = True, nullable = False)
    def __init__(self, ten_du_an, ten_toa_duong_day_khu, ten_tang_loai_nha, ma_can, dien_tich, loai_dien_tich, don_gia):
        self.ten_du_an
        self.ten_toa_duong_day_khu
        self.ten_tang_loai_nha
        self.ma_can
        self.dien_tich
        self.loai_dien_tich
        self.don_gia
    def __repr__(self):
        return str([self.ten_du_an, self.ten_toa_duong_day_khu, self.ten_tang_loai_nha, self.ma_can, self.dien_tich, self.loai_dien_tich, self.don_gia])


# BDS BIET THU
class BDS_biet_thu(db.Model):
    __tablename__ = "bds_lien_ke_bt"
    ten_du_an = db.Column('ten_du_an', String, primary_key = True, nullable = False)
    ten_duong = db.Column('ten_duong', String, primary_key = True, nullable = False)
    ten_tang = db.Column('ten_tang', String, primary_key = True, nullable = False)
    ma_can = db.Column('ma_can', String, primary_key = True, nullable = False)
    dien_tich_dat = db.Column('dien_tich_dat', String, primary_key = True, nullable = False)
    dien_tich_san_xay_dung = db.Column('dien_tich_san_xay_dung', String, primary_key = True, nullable = False)
    tong_gia_tri_xay_tho = db.Column('tong_gia_tri_xay_tho', String, primary_key = True, nullable = False)
    tong_gia_tri_hoan_thien = db.Column('tong_gia_tri_hoan_thien', String, primary_key = True, nullable = False)
    don_gia_dat = db.Column('don_gia_dat', String, primary_key = True, nullable = False)
    don_gia_ctxd = db.Column('don_gia_ctxd', String, primary_key = True, nullable = False)
    def __init__(self, ten_du_an, ten_duong, ten_tang, ma_can, dien_tich_dat, dien_tich_san_xay_dung, tong_gia_tri_xay_tho, tong_gia_tri_hoan_thien, don_gia_dat, don_gia_ctxd):
        self.ten_du_an
        self.ten_duong
        self.ten_tang
        self.ma_can
        self.dien_tich_dat
        self.dien_tich_san_xay_dung
        self.tong_gia_tri_xay_tho
        self.tong_gia_tri_hoan_thien
        self.don_gia_dat
        self.don_gia_ctxd
    def __repr__(self):
        return str([self.ten_du_an, self.ten_duong, self.ten_tang, self.ma_can, self.dien_tich_dat, self.dien_tich_san_xay_dung, self.tong_gia_tri_xay_tho, self.tong_gia_tri_hoan_thien, self.don_gia_dat, self.don_gia_ctxd])


# YEU TO
class Yeu_to(db.Model):
    __tablename__ = "yeu_to"
    yeu_to = db.Column('yeu_to', String, primary_key = True, nullable = False)
    ti_le = db.Column('ti_le', String, primary_key = True, nullable = False)
    mien = db.Column('mien', String, primary_key = True, nullable = False)
    vi_tri = db.Column('vi_tri', String, primary_key = True, nullable = False)
    phan_loai = db.Column('phan_loai', String, primary_key = True, nullable = False)
    def __init__(self, yeu_to, ti_le, mien, vi_tri, phan_loai):
        self.yeu_to
        self.ti_le
        self.mien
        self.vi_tri
        self.phan_loai
    def __repr__(self):
        return str([self.yeu_to, self.ti_le, self.mien, self.vi_tri, self.phan_loai])

#
# MAT TIEN
class Mat_tien(db.Model):
    __tablename__ = "mat_tien"
    mat_tien = db.Column('mat_tien', String, primary_key = True, nullable = False)
    ti_le = db.Column('ti_le', String, primary_key = True, nullable = False)
    mien = db.Column('mien', String, primary_key = True, nullable = False)
    vi_tri = db.Column('vi_tri', String, primary_key = True, nullable = False)
    def __init__(self, mat_tien, ti_le, mien, vi_tri):
        self.mat_tien
        self.ti_le
        self.mien
        self.vi_tri
    def __repr__(self):
        return str([self.mat_tien, self.ti_le, self.mien, self.vi_tri])


# QUY MO
class Quy_mo(db.Model):
    __tablename__ = "quy_mo"
    quy_mo = db.Column('quy_mo', String, primary_key = True, nullable = False)
    ti_le = db.Column('ti_le', String, primary_key = True, nullable = False)
    mien = db.Column('mien', String, primary_key = True, nullable = False)
    vi_tri = db.Column('vi_tri', String, primary_key = True, nullable = False)
    def __init__(self, quy_mo, ti_le, mien, vi_tri):
        self.quy_mo
        self.ti_le
        self.mien
        self.vi_tri
    def __repr__(self):
        return str([self.quy_mo, self.ti_le, self.mien, self.vi_tri])


# HINH DANG
class Hinh_dang(db.Model):
    __tablename__ = "hinh_dang"
    hinh_dang = db.Column('hinh_dang', String, primary_key = True, nullable = False)
    ti_le = db.Column('ti_le', String, primary_key = True, nullable = False)
    mien = db.Column('mien', String, primary_key = True, nullable = False)
    vi_tri = db.Column('vi_tri', String, primary_key = True, nullable = False)
    def __init__(self, hinh_dang, ti_le, mien, vi_tri):
        self.hinh_dang
        self.ti_le
        self.mien
        self.vi_tri
    def __repr__(self):
        return str([self.hinh_dang, self.ti_le, self.mien, self.vi_tri])


# DO RONG NGO
class Do_rong_ngo(db.Model):
    __tablename__ = "do_rong_ngo"
    Tinh_thanh = db.Column('Tinh_thanh', String, primary_key = True, nullable = False)
    vi_tri = db.Column('vi_tri', String, primary_key = True, nullable = False)
    khoang_cach = db.Column('khoang_cach', String, primary_key = True, nullable = False)
    ti_le = db.Column('ti_le', String, primary_key = True, nullable = False)
    mien = db.Column('mien', String, primary_key = True, nullable = False)
    
    def __init__(self, Tinh_thanh, vi_tri, khoang_cach, ti_le, mien):
        self.Tinh_thanh
        self.vi_tri
        self.khoang_cach        
        self.ti_le
        self.mien
    def __repr__(self):
        return str([self.Tinh_thanh, self.vi_tri, self.khoang_cach , self.ti_le, self.mien])


# KHOANG CACH TRUC CHINH
class Khoang_cach_truc(db.Model):
    __tablename__ = "khoang_cach_den_truc_chinh"
    Tinh_thanh = db.Column('Tinh_thanh', String, primary_key = True, nullable = False)
    vi_tri = db.Column('vi_tri', String, primary_key = True, nullable = False)
    khoang_cach = db.Column('khoang_cach', String, primary_key = True, nullable = False)
    ti_le = db.Column('ti_le', String, primary_key = True, nullable = False)
    mien = db.Column('mien', String, primary_key = True, nullable = False)
    
    def __init__(self, Tinh_thanh, vi_tri, khoang_cach, ti_le, mien):
        self.Tinh_thanh
        self.vi_tri
        self.khoang_cach        
        self.ti_le
        self.mien
    def __repr__(self):
        return str([self.Tinh_thanh, self.vi_tri, self.khoang_cach , self.ti_le, self.mien])


#DAC DIEM VI TRI
class Dac_diem_VT(db.Model):
    __tablename__ = "dac_diem_vi_tri"
    thanh_pho = db.Column('thanh_pho', String, primary_key = True, nullable = False)
    vi_tri = db.Column('vi_tri', String, primary_key = True, nullable = False)
    dac_diem = db.Column('dac_diem', String, primary_key = True, nullable = False)
    def __init__(self, thanh_pho, vi_tri, dac_diem):
        self.thanh_pho
        self.vi_tri
        self.dac_diem
    def __repr__(self):
        return str([self.thanh_pho, self.vi_tri, self.dac_diem])
db.create_all()