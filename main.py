import csv
import json
import os
from typing import List, Dict
import matplotlib.pyplot as plt

def menu():
    print("\n" + "="*50)
    print("      QUẢN LÝ SẢN PHẨM VÀ TỒN KHO")
    print("="*50)
    print("1. Hiển thị danh sách sản phẩm")
    print("2. Thêm mới sản phẩm")
    print("3. Cập nhật thông tin sản phẩm")
    print("4. Xóa sản phẩm")
    print("5. Tìm kiếm sản phẩm")
    print("6. Sắp xếp danh sách sản phẩm")
    print("7. Thống kê kho hàng")
    print("8. Vẽ biểu đồ thống kê kho hàng")
    print("9. Lưu vào file CSV")
    print("10. Thoát")
    print("="*50)

def doc_du_lieu() -> List[Dict]:
    danh_sach = []
    if os.path.exists("data.csv"):
        try:
            with open("data.csv", "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row["gia_ban"] = float(row["gia_ban"])
                    row["so_luong"] = int(row["so_luong"])
                    row["gia_tri_ton"] = float(row["gia_tri_ton"])
                    danh_sach.append(row)
            print(f"Đã tải {len(danh_sach)} sản phẩm từ data.csv")
        except Exception as e:
            print(f"Lỗi khi đọc file CSV: {e}")
    elif os.path.exists("data.json"):
        try:
            with open("data.json", "r", encoding="utf-8") as f:
                danh_sach = json.load(f)
            print(f"Đã tải {len(danh_sach)} sản phẩm từ data.json")
        except Exception as e:
            print(f"Lỗi JSON: {e}")
    else:
        print("Không tìm thấy file dữ liệu. Bắt đầu với danh sách trống.")
    
    return danh_sach

def ghi_du_lieu(danh_sach: List[Dict]):
    if not danh_sach:
        print("Danh sách trống, không có gì để lưu.")
        return
    
    try:
        with open("data.csv", "w", encoding="utf-8", newline="") as f:
            fieldnames = ["masp", "ten_sp", "gia_ban", "so_luong", "gia_tri_ton", "trang_thai"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(danh_sach)
        print(f"Đã lưu {len(danh_sach)} sản phẩm vào data.csv")
    except Exception as e:
        print(f"Lỗi khi ghi file CSV: {e}")

def hien_thi_danh_sach(danh_sach: List[Dict]):
    if not danh_sach:
        print("\nDanh sách sản phẩm trống")
        return
    
    print("\n" + "="*120)
    print(f"{'Mã SP':<10} {'Tên sản phẩm':<30} {'Giá bán':>15} {'Số lượng':>12} {'Giá trị tồn':>18} {'Trạng thái':<15}")
    print("="*120)
    
    for sp in danh_sach:
        print(f"{sp['masp']:<10} {sp['ten_sp']:<30} {sp['gia_ban']:>15,.0f} {sp['so_luong']:>12} {sp['gia_tri_ton']:>18,.0f} {sp['trang_thai']:<15}")
    
    print("="*120)
    print(f"Tổng số sản phẩm: {len(danh_sach)}")
    print("="*120)

def them_san_pham(danh_sach: List[Dict]):
    print("\n" + "="*50)
    print("THÊM MỚI SẢN PHẨM")
    print("="*50)
    
    while True:
        ma_sp = input("Nhập mã sản phẩm: ").strip()
        if not ma_sp:
            print("Mã sản phẩm không được để trống")
            continue
        if any(sp["masp"] == ma_sp for sp in danh_sach):
            print(f"Mã sản phẩm '{ma_sp}' đã tồn tại! Vui lòng nhập mã khác.")
            continue
        break
    
    while True:
        ten_sp = input("Nhập tên sản phẩm: ").strip()
        if ten_sp:
            break
        print("Tên sản phẩm không được để trống")
    
    while True:
        try:
            gia_ban = float(input("Nhập giá bán: "))
            if gia_ban > 0:
                break
            print("Giá bán phải lớn hơn 0!")
        except ValueError:
            print("Vui lòng nhập số hợp lệ")
    
    while True:
        try:
            so_luong = int(input("Nhập số lượng: "))
            if so_luong > 0:
                break
            print("Số lượng phải lớn hơn 0!")
        except ValueError:
            print("Vui lòng nhập số nguyên hợp lệ")
    
    gia_tri_ton = gia_ban * so_luong
    
    if so_luong <= 5:
        trang_thai = "Cần nhập"
    elif so_luong > 50:
        trang_thai = "Khó bán"
    else:
        trang_thai = "Bình thường"
    
    san_pham_moi = {
        "masp": ma_sp,
        "ten_sp": ten_sp,
        "gia_ban": gia_ban,
        "so_luong": so_luong,
        "gia_tri_ton": gia_tri_ton,
        "trang_thai": trang_thai
    }
    
    danh_sach.append(san_pham_moi)
    print(f"\nĐã thêm sản phẩm '{ten_sp}' (Mã: {ma_sp}) thành công")
    print(f"  - Giá trị tồn: {gia_tri_ton:,.0f} VNĐ")
    print(f"  - Trạng thái: {trang_thai}")

def cap_nhat_san_pham(danh_sach: List[Dict]):
    if not danh_sach:
        print("\nDanh sách sản phẩm trống")
        return
    
    print("\n" + "="*50)
    print("CẬP NHẬT THÔNG TIN SẢN PHẨM")
    print("="*50)
    
    ma_sp = input("Nhập mã sản phẩm cần cập nhật: ").strip()
    
    san_pham = None
    for sp in danh_sach:
        if sp["masp"] == ma_sp:
            san_pham = sp
            break
    
    if not san_pham:
        print(f"Không tìm thấy sản phẩm với mã '{ma_sp}'")
        return
    
    print(f"\nThông tin hiện tại của sản phẩm '{san_pham['ten_sp']}' (Mã: {ma_sp}):")
    print(f"  - Giá bán: {san_pham['gia_ban']:,.0f} VNĐ")
    print(f"  - Số lượng: {san_pham['so_luong']}")
    print(f"  - Giá trị tồn: {san_pham['gia_tri_ton']:,.0f} VNĐ")
    print(f"  - Trạng thái: {san_pham['trang_thai']}")
    
    print("\n--- Cập nhật Giá bán ---")
    gia_ban_input = input(f"Giá bán mới (Enter để giữ nguyên [{san_pham['gia_ban']:,.0f}]): ").strip()
    if gia_ban_input:
        try:
            gia_ban = float(gia_ban_input)
            if gia_ban > 0:
                san_pham["gia_ban"] = gia_ban
            else:
                print("Giá bán phải lớn hơn 0. Giữ nguyên giá cũ.")
        except ValueError:
            print("Giá trị không hợp lệ. Giữ nguyên giá cũ.")
    
    print("\n--- Cập nhật Số lượng ---")
    so_luong_input = input(f"Số lượng mới (Enter để giữ nguyên [{san_pham['so_luong']}]): ").strip()
    if so_luong_input:
        try:
            so_luong = int(so_luong_input)
            if so_luong > 0:
                san_pham["so_luong"] = so_luong
            else:
                print("Số lượng phải lớn hơn 0. Giữ nguyên số lượng cũ.")
        except ValueError:
            print("Giá trị không hợp lệ. Giữ nguyên số lượng cũ.")
    
    san_pham["gia_tri_ton"] = san_pham["gia_ban"] * san_pham["so_luong"]
    
    if san_pham["so_luong"] <= 5:
        san_pham["trang_thai"] = "Cần nhập"
    elif san_pham["so_luong"] > 50:
        san_pham["trang_thai"] = "Khó bán"
    else:
        san_pham["trang_thai"] = "Bình thường"
    
    print(f"\nĐã cập nhật thành công")
    print(f"\nThông tin mới:")
    print(f"  - Giá bán: {san_pham['gia_ban']:,.0f} VNĐ")
    print(f"  - Số lượng: {san_pham['so_luong']}")
    print(f"  - Giá trị tồn: {san_pham['gia_tri_ton']:,.0f} VNĐ")
    print(f"  - Trạng thái: {san_pham['trang_thai']}")

def xoa_san_pham(danh_sach: List[Dict]):
    if not danh_sach:
        print("\nDanh sách sản phẩm trống")
        return
    
    print("\n" + "="*50)
    print("XÓA SẢN PHẨM")
    print("="*50)
    
    ma_sp = input("Nhập mã sản phẩm cần xóa: ").strip()
    
    san_pham = None
    index = -1
    for i, sp in enumerate(danh_sach):
        if sp["masp"] == ma_sp:
            san_pham = sp
            index = i
            break
    
    if not san_pham:
        print(f"Không tìm thấy sản phẩm với mã '{ma_sp}'")
        return
    
    print(f"\nThông tin sản phẩm cần xóa:")
    print(f"  - Mã SP: {san_pham['masp']}")
    print(f"  - Tên: {san_pham['ten_sp']}")
    print(f"  - Giá bán: {san_pham['gia_ban']:,.0f} VNĐ")
    print(f"  - Số lượng: {san_pham['so_luong']}")
    print(f"  - Giá trị tồn: {san_pham['gia_tri_ton']:,.0f} VNĐ")
    print(f"  - Trạng thái: {san_pham['trang_thai']}")
    
    xac_nhan = input("\nBạn có chắc muốn xóa? (yes/no): ").strip().lower()
    if xac_nhan in ["yes", "y", "có", "co"]:
        danh_sach.pop(index)
        print(f"\nĐã xóa sản phẩm '{san_pham['ten_sp']}' (Mã: {ma_sp}) thành công")
    else:
        print("\nĐã hủy thao tác xóa.")

def tim_kiem_san_pham(danh_sach: List[Dict]):
    if not danh_sach:
        print("\nDanh sách sản phẩm trống")
        return
    
    print("\n" + "="*50)
    print("TÌM KIẾM SẢN PHẨM")
    print("="*50)
    print("1. Tìm theo mã SP")
    print("2. Tìm theo tên (gần đúng)")
    
    lua_chon = input("\nChọn cách tìm kiếm (1/2): ").strip()
    
    ket_qua = []
    
    if lua_chon == "1":
        ma_sp = input("Nhập mã SP cần tìm: ").strip()
        ket_qua = [sp for sp in danh_sach if sp["masp"].lower() == ma_sp.lower()]
    elif lua_chon == "2":
        ten = input("Nhập tên cần tìm: ").strip().lower()
        ket_qua = [sp for sp in danh_sach if ten in sp["ten_sp"].lower()]
    else:
        print("Lựa chọn không hợp lệ")
        return
    
    if ket_qua:
        print(f"\nTìm thấy {len(ket_qua)} sản phẩm:")
        print("="*120)
        print(f"{'Mã SP':<10} {'Tên sản phẩm':<30} {'Giá bán':>15} {'Số lượng':>12} {'Giá trị tồn':>18} {'Trạng thái':<15}")
        print("="*120)
        for sp in ket_qua:
            print(f"{sp['masp']:<10} {sp['ten_sp']:<30} {sp['gia_ban']:>15,.0f} {sp['so_luong']:>12} {sp['gia_tri_ton']:>18,.0f} {sp['trang_thai']:<15}")
        print("="*120)
    else:
        print("\nKhông tìm thấy sản phẩm nào")

def sap_xep_danh_sach(danh_sach: List[Dict]):
    if not danh_sach:
        print("\nDanh sách sản phẩm trống")
        return
    
    print("\n" + "="*50)
    print("SẮP XẾP DANH SÁCH SẢN PHẨM")
    print("="*50)
    print("1. Sắp xếp theo Giá bán tăng dần")
    print("2. Sắp xếp theo Giá trị tồn giảm dần")
    
    lua_chon = input("\nChọn cách sắp xếp (1/2): ").strip()
    
    if lua_chon == "1":
        danh_sach.sort(key=lambda x: x["gia_ban"], reverse=False)
        print("\nĐã sắp xếp theo Giá bán tăng dần.")
    elif lua_chon == "2":
        danh_sach.sort(key=lambda x: x["gia_tri_ton"], reverse=True)
        print("\nĐã sắp xếp theo Giá trị tồn giảm dần.")
    else:
        print("\nLựa chọn không hợp lệ")
        return
    
    hien_thi_danh_sach(danh_sach)

def thong_ke_kho_hang(danh_sach: List[Dict]):
    if not danh_sach:
        print("\nDanh sách sản phẩm trống")
        return
    
    print("\n" + "="*60)
    print("THỐNG KÊ KHO HÀNG")
    print("="*60)
    
    thong_ke = {
        "Cần nhập": 0,
        "Bình thường": 0,
        "Khó bán": 0
    }
    
    for sp in danh_sach:
        trang_thai = sp["trang_thai"]
        if trang_thai in thong_ke:
            thong_ke[trang_thai] += 1
    
    print(f"{'Trạng thái':<20} {'Số lượng SP':<15} {'Tỷ lệ (%)':<15}")
    print("="*60)
    
    tong_so = len(danh_sach)
    for trang_thai, so_luong in thong_ke.items():
        ty_le = (so_luong / tong_so * 100) if tong_so > 0 else 0
        print(f"{trang_thai:<20} {so_luong:<15} {ty_le:>14.2f}%")
    
    print("="*60)
    print(f"{'Tổng số sản phẩm:':<35} {tong_so}")
    print("="*60)
    
    return thong_ke

def ve_bieu_do_thong_ke(danh_sach: List[Dict]):
    if not danh_sach:
        print("\nDanh sách sản phẩm trống")
        return
    
    print("\n" + "="*50)
    print("VẼ BIỂU ĐỒ THỐNG KÊ KHO HÀNG")
    print("="*50)
    
    thong_ke = {
        "Cần nhập": 0,
        "Bình thường": 0,
        "Khó bán": 0
    }
    
    for sp in danh_sach:
        trang_thai = sp["trang_thai"]
        if trang_thai in thong_ke:
            thong_ke[trang_thai] += 1
    
    labels = []
    values = []
    for trang_thai, so_luong in thong_ke.items():
        if so_luong > 0:
            labels.append(trang_thai)
            values.append(so_luong)
    
    if not values:
        print("Không có dữ liệu để vẽ biểu đồ!")
        return
    
    plt.figure(figsize=(10, 8))
    colors = ['#ff6b6b', '#4ecdc4', '#ffe66d']
    explode = [0.05] * len(values)
    
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, 
            colors=colors[:len(values)], explode=explode, shadow=True)
    plt.title('THỐNG KÊ TRẠNG THÁI KHO HÀNG', fontsize=18, fontweight='bold', pad=20)
    plt.axis('equal')
    
    print("Đang hiển thị biểu đồ...")
    plt.show()
    print("Đã đóng biểu đồ.")

def luu_vao_file_csv(danh_sach: List[Dict]):
    ghi_du_lieu(danh_sach)

def main():
    print("="*50)
    print("CHƯƠNG TRÌNH QUẢN LÝ SẢN PHẨM VÀ TỒN KHO")
    print("="*50)
    
    danh_sach_san_pham = doc_du_lieu()
    
    while True:
        menu()
        choice = input("\nChọn chức năng (1-10): ").strip()
        
        if choice == "1":
            hien_thi_danh_sach(danh_sach_san_pham)
        elif choice == "2":
            them_san_pham(danh_sach_san_pham)
        elif choice == "3":
            cap_nhat_san_pham(danh_sach_san_pham)
        elif choice == "4":
            xoa_san_pham(danh_sach_san_pham)
        elif choice == "5":
            tim_kiem_san_pham(danh_sach_san_pham)
        elif choice == "6":
            sap_xep_danh_sach(danh_sach_san_pham)
        elif choice == "7":
            thong_ke_kho_hang(danh_sach_san_pham)
        elif choice == "8":
            ve_bieu_do_thong_ke(danh_sach_san_pham)
        elif choice == "9":
            luu_vao_file_csv(danh_sach_san_pham)
        elif choice == "10":
            print("\n" + "="*50)
            print("Đang lưu dữ liệu trước khi thoát...")
            ghi_du_lieu(danh_sach_san_pham)
            print("="*50)
            print("Cảm ơn bạn đã sử dụng chương trình!")
            print("Tạm biệt!")
            print("="*50)
            break
        else:
            print("\nLựa chọn không hợp lệ! Vui lòng chọn từ 1 đến 10.")
        
        input("\nNhấn Enter để tiếp tục...")

if __name__ == "__main__":
    main()
