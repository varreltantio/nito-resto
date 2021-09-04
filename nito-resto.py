import json
import getpass
import os
from prettytable import PrettyTable
from datetime import datetime as dt

data_account = {}


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def main():
    clear_screen()
    print("\n======== Selamat Datang di NITO RESTO ========")
    print("[1] Login")
    print("[2] Daftar Meja")
    print("[3] Exit")

    select_menu = input("\nPilih Menu> ")

    if select_menu == "1":
        isLogged(data_account)
    elif select_menu == "2":
        role = "admin"
        lihat_akun(role)
    elif select_menu == "3":
        exit()
    else:
        input("Menu yang anda pilih salah, tekan enter untuk kembali")
        main()


def isLogged(data_account):
    loggedIn = login(data_account)

    if loggedIn == True:
        role = data_account["role"]
        if role == "user":
            is_file = os.path.exists("transactions.json")
            nama = input("Nama: ")
            if is_file:
                with open("transactions.json", mode="r") as file:
                    transactions = json.load(file)
                isCheck = True
                for transaction in transactions:
                    if nama == transaction["nama"]:
                        isCheck = False
                        break

                if isCheck == True:
                    data_account["nama"] = nama
                    user_menu()
                else:
                    print("Nama telah digunakan")
                    isLogged(data_account)
            else:
                data_account["nama"] = nama
                user_menu()
        elif role == "admin":
            admin_menu()
    else:
        print("username atau password salah")
        isLogged(data_account)


def login(data_account):
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    with open("accounts.json", mode="r") as file:
        accounts = json.load(file)

    for account in accounts:
        if username == account['username'] and password == account['password']:
            data_account["username"] = account['username']
            data_account["role"] = account['role']
            return True

    return False


def back_to_menu():
    input("\nTekan enter untuk kembali ke menu...")

    if data_account["role"] == "admin":
        admin_menu()
    elif data_account["role"] == "user":
        user_menu()


def admin_menu():
    clear_screen()
    # menampilkan tampilan menu
    print("\n======== ADMIN NITO RESTO ========")
    print("[1] Daftar Menu")
    print("[2] Daftar Akun")
    print("[3] Daftar Transaksi")
    print("[4] Logout")

    select_menu = input("\nPilih Menu> ")

    if select_menu == "1":
        daftar_menu()
    elif select_menu == "2":
        daftar_akun()
    elif select_menu == "3":
        daftar_transaksi()
    elif select_menu == "4":
        main()
    else:
        print("Menu yang anda pilih salah")
        back_to_menu()


def daftar_menu():
    clear_screen()
    print("\n======== Daftar Menu ========")
    print("[1] Lihat Menu")
    print("[2] Tambah Menu")
    print("[3] Edit Menu")
    print("[4] Hapus Menu")
    print("[5] Kembali")

    select_menu = input("\nPilih Menu> ")

    if select_menu == "1":
        lihat_menu()
    elif select_menu == "2":
        tambah_menu()
    elif select_menu == "3":
        edit_menu()
    elif select_menu == "4":
        hapus_menu()
    elif select_menu == "5":
        admin_menu()
    else:
        print("Menu yang anda pilih salah")
        back_to_menu()


def lihat_menu():
    try:
        clear_screen()
        with open("menu.json", mode="r") as file:
            menu = json.load(file)
        draw_table(menu)

        back_to_menu()
    except FileNotFoundError:
        print("Tambah menu terlebih dahulu")
        back_to_menu()


def tambah_menu():
    clear_screen()
    is_file = os.path.exists("menu.json")

    menu = []

    if is_file:
        with open("menu.json", mode="r") as file:
            menu = json.load(file)

    item = {}

    item["kategori"] = input("[makanan]/[minuman]: ")
    item["nama"] = input("nama: ")
    item["harga"] = input("Rp. ")

    with open("menu.json", mode="w") as file:
        menu.append(item)

        json.dump(menu, file, indent=3)

        print("menu telah ditambahkan")

    back_to_menu()


def edit_menu():
    try:
        clear_screen()
        with open("menu.json", mode="r") as file:
            menu = json.load(file)

        draw_table(menu)

        print("\nCari menu yang ingin anda ubah")
        search_item = input("masukan nama> ")

        index = 0
        item = {}
        data_menu = []

        for data in menu:
            if data["nama"] == search_item:
                data_menu = menu[index]
                item["nama"] = data["nama"]

            index += 1
        if len(data_menu) > 0:
            print(f"Silahkan ubah data menu {search_item} diatas \n")
            item["kategori"] = input("[makanan]/[minuman]: ")
            item["nama"] = input("nama: ")
            item["harga"] = input("Rp. ")

            i = 0

            for data in menu:
                if data["nama"] == search_item:
                    menu.remove(menu[i])
                    data["kategori"] = item["kategori"]
                    data["nama"] = item["nama"]
                    data["harga"] = item["harga"]
                i += 1

            with open("menu.json", mode="w") as file:
                menu.append(item)

                json.dump(menu, file, indent=3)

                print("menu telah diubah")

            back_to_menu()
        else:
            print(f"Menu {search_item} tidak ditemukan")
            back_to_menu()
    except FileNotFoundError:
        print("Tambah menu terlebih dahulu")
        back_to_menu()


def hapus_menu():
    try:
        clear_screen()
        with open("menu.json", mode="r") as file:
            menu = json.load(file)

        draw_table(menu)

        print("\nCari menu yang ingin anda hapus")
        search_item = input("menu masakan> ")

        data_menu = []

        index = 0

        for data in menu:
            if data["nama"] == search_item:
                data_menu = menu[index]

            index += 1

        if len(data_menu) > 0:
            is_check = input(
                f"Apakah anda yakin ingin menghapus menu {search_item} diatas? (y)/(t): ")

            if is_check == "y":
                i = 0

                for data in menu:
                    if data["nama"] == search_item:
                        menu.remove(menu[i])
                    i += 1

                with open("menu.json", mode="w") as file:
                    json.dump(menu, file, indent=3)

                    print("Menu berhasil dihapus")

            back_to_menu()
        else:
            print(f"Menu {search_item} tidak ditemukan")
            back_to_menu()
    except FileNotFoundError:
        print("Tambah menu terlebih dahulu")
        back_to_menu()


def daftar_akun():
    clear_screen()
    print("\n======== Daftar Akun ========")
    print("[1] Lihat Akun")
    print("[2] Tambah Akun")
    print("[3] Hapus Akun")
    print("[4] Kembali")

    # user memilih menu yang akan di jalankan
    select_menu = input("\nPilih Menu> ")

    if select_menu == "1":
        role = "user"
        lihat_akun(role)
    elif select_menu == "2":
        tambah_akun()
    elif select_menu == "3":
        hapus_akun()
    elif select_menu == "4":
        admin_menu()
    else:
        print("Menu yang anda pilih salah")
        daftar_akun()


def lihat_akun(role):
    clear_screen()
    account = []
    with open("accounts.json", mode="r") as file:
        accounts = json.load(file)

    if role == "admin":
        for data in accounts:
            if data["role"] == "user":
                account.append(data)
        draw_table(account)
        input("Tekan enter untuk kembali")
        main()
    else:
        draw_table(accounts)
        back_to_menu()


def tambah_akun():
    clear_screen()
    accounts = []

    with open("accounts.json", mode="r") as file:
        accounts = json.load(file)

    item = {}

    item["username"] = input("username: ")
    item["password"] = input("password: ")
    item["role"] = input("role [admin]/[user]: ")

    with open("accounts.json", mode="w") as file:
        accounts.append(item)

        json.dump(accounts, file, indent=3)

        print("Akun telah ditambahkan")

    back_to_menu()


def hapus_akun():
    clear_screen()
    with open("accounts.json", mode="r") as file:
        accounts = json.load(file)

    draw_table(accounts)

    print("\nCari akun yang ingin anda hapus")
    search_item = input("> ")

    is_check = input(
        "Apakah anda yakin ingin menghapus akun diatas? (y)/(t): ")

    if is_check == "y":
        i = 0

        for data in accounts:
            if data["username"] == search_item:
                accounts.remove(accounts[i])
            i += 1

        with open("accounts.json", mode="w") as file:
            json.dump(accounts, file, indent=3)

            print("Akun berhasil dihapus")

    back_to_menu()


def daftar_transaksi():
    try:
        clear_screen()
        with open("transactions.json", mode="r") as file:
            transactions = json.load(file)

        total_transactions = 0
        print("{0:^48s}".format("-" * 80))
        print(
            "{0:10s} {1:8s} {2:15s} {3:8s} {4:8s} {5:12s} {6:10s}".format(
                "Nama", "Nomor", "Menu", "Jumlah", "Harga", "Total Harga", "Tanggal"
            )
        )
        print("{0:^48s}".format("-" * 80))
        for transaction in transactions:
            print(
                "{0:10s} {1:8s} {2:15s} {3:8s} {4:8s} {5:12s} {6:10s}".format(
                    transaction["nama"],
                    transaction["nomor"],
                    transaction["menu"],
                    transaction["jumlah"],
                    transaction["harga"],
                    transaction["total harga"],
                    transaction["tanggal"],
                )
            )

            # menjumlahkan total harga
            total_transactions += int(transaction["total harga"])

        print("{0:^48s}".format("-" * 80))
        # menampilkan total biaya transaksi
        print(f"Total Biaya Pesanan: Rp {total_transactions}")
        print("{0:^48s}".format("-" * 80))

        print("[1]Kembali")
        select_menu = input("Pilih menu> ")

        if select_menu == "1":
            back_to_menu()
        else:
            print("Menu tidak ditemukan")
            back_to_menu()
    except FileNotFoundError:
        print("tidak ada data transaksi")
        # jalankan function kembali ke menu
        back_to_menu()


def user_menu():
    try:
        clear_screen()
        with open("menu.json", mode="r") as file:
            menu = json.load(file)

        # menampilkan tampilan menu
        print("\n======== MENU NITO RESTO ========")
        print("[1] Makanan")
        print("[2] Minuman")
        print("[3] Pembayaran")
        print("[4] Logout")

        # user memilih menu yang akan di jalankan
        select_menu = input("\nPilih Menu> ")

        makanan = []
        minuman = []

        for data in menu:
            if data["kategori"] == "makanan":
                makanan.append(data)
            elif data["kategori"] == "minuman":
                minuman.append(data)

        if select_menu == "1":
            daftar_makanan(makanan)
        elif select_menu == "2":
            daftar_minuman(minuman)
        elif select_menu == "3":
            pembayaran()
        elif select_menu == "4":
            main()
        else:
            print("Menu yang anda pilih salah")
            back_to_menu()
    except FileNotFoundError:
        input("Tidak ada menu, tekan enter untuk kembali")
        main()


def daftar_makanan(makanan):
    clear_screen()
    draw_table(makanan)
    transactions = []

    is_file = os.path.exists("transactions.json")
    if is_file:
        with open("transactions.json", mode="r") as file:
            transactions = json.load(file)

    if len(makanan) > 0:
        index = 0
        item = {}
        menu = []

        pesan = input("Pilih makanan: ")

        for data in makanan:
            if data["nama"] == pesan:
                menu = makanan[index]
                item["menu"] = data["nama"]
                item["harga"] = data["harga"]

            index += 1

        if len(menu) > 0:
            item["nama"] = data_account["nama"]
            item["tanggal"] = dt.now().strftime("%d/%m/%Y")
            item["jumlah"] = input("Jumlah: ")
            item["nomor"] = data_account["username"]
            item["total harga"] = str(
                int(item["jumlah"]) * int(item["harga"]))

            with open("transactions.json", mode="w") as file:
                transactions.append(item)

                json.dump(transactions, file, indent=7, sort_keys=True)

            print("Pesanan telah ditambahkan")
            back_to_menu()
        else:
            print(f"Menu {pesan} tidak ditemukan")
            back_to_menu()
    else:
        back_to_menu()


def daftar_minuman(minuman):
    clear_screen()
    draw_table(minuman)
    transactions = []

    is_file = os.path.exists("transactions.json")
    if is_file:
        with open("transactions.json", mode="r") as file:
            transactions = json.load(file)
    if len(minuman) > 0:
        pesan = input("Pilih minuman: ")

        index = 0
        item = {}
        menu = []

        for data in minuman:
            if data["nama"] == pesan:
                menu = minuman[index]
                item["menu"] = data["nama"]
                item["harga"] = data["harga"]

            index += 1

        if len(menu) > 0:
            item["nama"] = data_account["nama"]
            item["tanggal"] = dt.now().strftime("%d/%m/%Y")
            item["jumlah"] = input("Jumlah: ")
            item["nomor"] = data_account["username"]
            item["total harga"] = str(
                int(item["jumlah"]) * int(item["harga"]))

            with open("transactions.json", mode="w") as file:
                transactions.append(item)

                json.dump(transactions, file, indent=7, sort_keys=True)

            print("Pesanan telah ditambahkan")
            back_to_menu()
        else:
            print(f"Menu {pesan} tidak ditemukan")
            back_to_menu()
    else:
        back_to_menu()


def pembayaran():
    try:
        clear_screen()
        with open("transactions.json", mode="r") as file:
            transactions = json.load(file)

        total_transactions = 0
        print("{0:^48s}".format("-" * 60))
        print(
            "{0:15s} {1:10s} {2:10s} {3:10s} {4:15s}".format(
                "Menu", "Nomor", "Jumlah", "Harga", "Total Harga"
            )
        )
        print("{0:^48s}".format("-" * 60))
        for transaction in transactions:
            if transaction["nama"] == data_account["nama"] and transaction["nomor"] == data_account["username"]:
                # menampilkan data transaksi
                print(
                    "{0:15s} {1:10s} {2:10s} {3:10s} {4:15s}".format(
                        transaction["menu"],
                        transaction["nomor"],
                        transaction["jumlah"],
                        transaction["harga"],
                        transaction["total harga"],
                    )
                )

                # menjumlahkan total harga
                total_transactions += int(transaction["total harga"])

        print("{0:^48s}".format("-" * 60))
        # menampilkan total biaya transaksi
        print(f"Total Biaya Pesanan: Rp {total_transactions}")
        print("{0:^48s}".format("-" * 60))

        print("[1]Pesan [2]Edit [3]Hapus [4]Kembali")
        select_menu = input("Pilih menu> ")

        if select_menu == "1":
            print("Pesanan sedang diproses harap lakukan pembayaran terlebih dahulu")
            exit()
        elif select_menu == "2":
            edit_pesanan(transactions)
        elif select_menu == "3":
            hapus_pesanan(transactions)
        elif select_menu == "4":
            back_to_menu()
        else:
            print("Menu tidak ditemukan")
            back_to_menu()
    except FileNotFoundError:
        print("Harap pesan terlebih dahulu")
        back_to_menu()


def edit_pesanan(transactions):
    print("\nCari pesanan yang ingin anda ubah")
    search_item = input("masukan nama menu> ")

    transaction = []
    item = {}

    index = 0

    for data in transactions:
        if data["menu"] == search_item:
            transaction = transactions[index]
            item["nama"] = data["nama"]
            item["tanggal"] = data["tanggal"]
            item["nomor"] = data["nomor"]
            item["menu"] = search_item
            item["harga"] = data["harga"]

        index += 1

    if len(transaction) > 0:
        print(f"Silahkan ubah pesanan {search_item}")

        item["jumlah"] = input("Jumlah: ")
        item["total harga"] = str(int(item["jumlah"]) * int(item["harga"]))

        a = 0
        for data in transactions:
            if data["menu"] == search_item:
                transactions.remove(transactions[a])
                data["nama"] = item["nama"]
                data["tanggal"] = item["tanggal"]
                data["jumlah"] = item["jumlah"]
                data["nomor"] = item["nomor"]
                data["menu"] = item["menu"]
                data["harga"] = item["harga"]
                data["total harga"] = item["total harga"]
            a += 1

        with open("transactions.json", mode="w") as file:
            transactions.append(item)

            json.dump(transactions, file, indent=7)

            print("Pesanan telah diubah")

        back_to_menu()
    else:
        print(f"menu {search_item} tidak ditemukan")
        back_to_menu()


def hapus_pesanan(transactions):
    print("\nCari pesanan yang ingin anda hapus")
    search_item = input("masukan nama menu> ")

    transaction = []

    index = 0

    for data in transactions:
        if data["menu"] == search_item:
            transaction = transactions[index]

        index += 1

    if len(transaction) > 0:
        index = 0
        for data in transactions:
            if data["menu"] == search_item:
                transactions.remove(transactions[index])
            index += 1

        with open("transactions.json", mode="w") as file:
            json.dump(transactions, file, indent=7)

            print("Pesanan telah dihapus")

        back_to_menu()
    else:
        print(f"menu {search_item} tidak ditemukan")
        back_to_menu()


def draw_table(data_table):
    if len(data_table) > 0:
        table = PrettyTable()
        table.field_names = data_table[0].keys()

        key = data_table[0].keys()

        for k in key:
            if k == "username":
                for data in data_table:
                    table.add_row(
                        [data["username"], data["password"], data["role"]])
            elif k == "kategori":
                for data in data_table:
                    table.add_row(
                        [data["kategori"], data["nama"], data["harga"]])
            break

        print(table)
    else:
        print("Tidak ada data")


while True:
    is_file = os.path.exists("accounts.json")

    if is_file == False:
        accounts = []
        item = {}
        with open("accounts.json", mode="w") as file:
            item["username"] = "admin1"
            item["password"] = "adminitoresto123"
            item["role"] = "admin"
            accounts.append(item)

            json.dump(accounts, file, indent=3)
    main()
