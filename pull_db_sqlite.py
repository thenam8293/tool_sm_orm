# -*- coding: utf8 -*-

import pypyodbc
import sqlite3

def sql_tool_sm(query,var=''):
    connection = pypyodbc.connect('Driver={SQL Server};Server=10.62.24.161\SQLEXPRESS;Database=tool_SM;uid=aos;pwd=aos159753')
    cursor = connection.cursor()
    cursor.execute(query,var)
    if query.lower().startswith('select') and not query.lower().startswith('select * into'):
        x = cursor.fetchall()
        cursor.close()
        return x
    else:
        cursor.commit()
        cursor.close()

###
def sqlite(query,var=''):
    connection = sqlite3.connect(r'C:\Users\hp43\Desktop\sm_tool.db')
    cursor = connection.cursor()
    # connection.text_factory = str
    cursor.execute(query,var)
    if query.lower()[:6] == 'select':
        x = cursor.fetchall()
        connection.close()
        return x
    elif query.lower()[:6] == 'create':
        connection.close()
    else:
        connection.commit()
        connection.close()
bds_biet_thu_field = ['ten_du_an', 'ten_duong', 'ten_tang', 'ma_can', 'dien_tich_dat', 'dien_tich_san_xay_dung', 'tong_gia_tri_xay_tho', 'tong_gia_tri_hoan_thien', 'don_gia_dat', 'don_gia_ctxd']

chung_cu_field = ['ten_du_an', 'ten_toa_duong_day_khu', 'ten_tang_loai_nha', 'ma_can', 'dien_tich', 'loai_dien_tich', 'don_gia']

dac_diem_vi_tri = 3
data_mb = 10
rong_ngo_truc_chinh_yeu_to = 5
hinh_dang_quy_mo_mat_tien = 4
gia_uy_ban = 9
# for r in sql_tool_sm("SELECT * from bds_lien_ke_bt"):
# 	sqlite("INSERT INTO bds_lien_ke_bt VALUES({})".format(",".join(["?"]*len(bds_biet_thu_field))), r)

# for r in sql_tool_sm("SELECT * from data_chung_cu"):
# 	sqlite("INSERT INTO data_chung_cu VALUES({})".format(",".join(["?"]*len(chung_cu_field))), r)

# for r in sql_tool_sm("SELECT * from dac_diem_vi_tri"):
# 	sqlite("INSERT INTO dac_diem_vi_tri VALUES({})".format(",".join(["?"]*dac_diem_vi_tri)), r)

# for r in sql_tool_sm("SELECT * from khoang_cach_den_truc_chinh"):
# 	sqlite("INSERT INTO khoang_cach_den_truc_chinh VALUES({})".format(",".join(["?"]*rong_ngo_truc_chinh_yeu_to)), r)

# for r in sql_tool_sm("SELECT * from yeu_to"):
# 	sqlite("INSERT INTO yeu_to VALUES({})".format(",".join(["?"]*rong_ngo_truc_chinh_yeu_to)), r)

# for r in sql_tool_sm("SELECT * from do_rong_ngo"):
# 	sqlite("INSERT INTO do_rong_ngo VALUES({})".format(",".join(["?"]*rong_ngo_truc_chinh_yeu_to)), r)
for r in sql_tool_sm("SELECT * from quy_mo"):
	sqlite("INSERT INTO quy_mo VALUES({})".format(",".join(["?"]*hinh_dang_quy_mo_mat_tien)), r)
for r in sql_tool_sm("SELECT * from hinh_dang"):
	sqlite("INSERT INTO hinh_dang VALUES({})".format(",".join(["?"]*hinh_dang_quy_mo_mat_tien)), r)
for r in sql_tool_sm("SELECT * from mat_tien"):
	sqlite("INSERT INTO mat_tien VALUES({})".format(",".join(["?"]*hinh_dang_quy_mo_mat_tien)), r)
for r in sql_tool_sm("SELECT * from khung_gia_uy_ban"):
	sqlite("INSERT INTO khung_gia_uy_ban VALUES({})".format(",".join(["?"]*gia_uy_ban)), r)
# for r in sql_tool_sm("SELECT * from data_mb"):
# 	sqlite("INSERT INTO data_mb VALUES({})".format(",".join(["?"]*data_mb)), r)