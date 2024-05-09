from web3 import Web3
from web3.middleware import geth_poa_middleware
from  contract_info import abi, contract_address

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware,layer=0)

contract = w3.eth.contract(address=contract_address,abi=abi)

def login():
    while (True):
        try:
            public_key = input(" Введите публичный ключ: ")
            password = input(" Введите пароль: ")
            w3.geth.personal.unlock_account(public_key,password)
            return public_key
            break
        except Exception as e:
            print(f" Ошибка авторизации: {e}\n Ваш ключ или пороль неверны")
            return None

def register():
    while(True):
        password = input("Придумайте пароль\n Пороль должен соответсвовать следующим требованиям:\n  1. Пороль должени состоять из болле, чем 9 символолов\n  2. Пороль должен включать в себя как минмум одну заглавную буквву, строчную букву, цифру, специальный символ.\n  3. Пороль не следовать простым шаблонам (qwerty123, password123 и т.д.)\n")
        if any(c.isdigit() for c in password) and any(c.isupper() for c in password) and any(not c.isalnum() for c in password) and len(password)>=9 and password!="qwerty123!" and password!="password123!":
            account = w3.geth.personal.new_account(password)
            print(f" Ваш публичный ключ: {account}")
            break
        else:
            print(f" Ваш пороль {password} не соответсвует условиям. Попробуйте еще раз\n")

def send_eth (account):
    try:
        value = int(input(" Введите колличество эфира для отправки: "))
        tx_hash = contract.functions.sendEth().transact({
            'from': account,
            'value': value,
        })
        print(f"Транзакция {tx_hash.hex()} отправлена")
    except Exception as e:
        print(f" Ошибка пополнения: {e}\n Возможно вы ввели не число или на вашем счете недостаточно средств")
def get_balance (account):
    balance = contract.functions.getBalance().call({
        "from" : account,
    })
    print(f" Ваш баланс на смарт-контракте: {balance}")

def withdraw (account):
    try:
        to = input(" Введите адрес для перевода: ")
        amount = int(input(" Введите колличесвто эфира для отправки: "))
        tx_hash = contract.functions.withdrawll(to,amount).transact({
            "from" : account,
        })
        print(f" Транзакция {tx_hash.hex()} отправлена")
    except Exception as e:
        print(f" Ошибка перевода средств: {e}\n Возможно вы ввели неверный адрес или на вашем счете недостаточно средств")
def withdraw_me (account):
    try:
        amount = int(input(" Введите колличесвто эфиров для отправки: "))
        tx_hash = contract.functions.withdrawll(account,amount).transact({
            "from" : account,
        })
        print(f" Транзакция {tx_hash.hex()} отправлена")
    except Exception as e:
        print(f" Ошибка снятия средств: {e}\n Возможно на вашем счете недостаточно средств или вы ввели не число")

def create_Estate(account):
    try:
        size = int(input(" Введите размер недвижимости: "))
        address = str(input(" Введите адрес недвижимости: "))
        type_id = int(input(" Выберите тип недвижимости:\n  1. Дом\n  2. Квартира\n  3. Лофт\n"))
        if type_id > 3 or type_id < 1:
            print(" Ошибка создания недвижимости: Нужно вводить вариант из предоставленных")
        else:
            tx_hash = contract.functions.createEstate(size,address,type_id-1).transact({
                'from': account                })
            print(f" Недвижимость {tx_hash.hex()} создана ")
    except Exception as e:
        print(f"Ошибка создания недвижимости: {e}\n Возсожно вы неверно указали размер или id")
def get_Estate(account):
    estates = contract.functions.getEstate().call({
    })
    for estate in estates:
        if estate[2] == account and estate[4]== True:
            print(f"----------------Недвижимость №{estate[5]}-----------------")
            print(f" Размер: {estate[0]} кв. м")
            print(f" Адрес: {estate[1]}")
            if estate[3] == 0:
                print(" Тип: Дом")
            elif estate[3] == 1:
                print(" Тип: Квартира")
            elif estate[3] == 2:
                print(" Тип: Лофт")
def izmen_stat_estate(account):
    try:
        id_estate = int(input("Введите id недвижимости: "))
        vibor = str(input(" Выберите: \n  1. Использовать\n  2. Закрыть \n"))
        stat = False
        if vibor=="1":
            stat= True
            tx_hash = contract.functions.updateEstateStatus(id_estate - 1, stat).transact({
                'from': account
            })
            print(f" Активность недвижимости изменена : {tx_hash.hex()} ")
        elif vibor=="2":
            stat= False
            tx_hash = contract.functions.updateEstateStatus(id_estate - 1, stat).transact({
                'from': account
            })
            print(f" Активность недвижимости изменена : {tx_hash.hex()} ")
        else:
            print(" Ошибка изменения активности: Нужно вводить номер варианта")
    except Exception as e:
        print(f" Ошибка изменения активности : {e}\n Возможно вы неверно указали id")
def izmen_stat_ads(account):
    try:
        id_ad = int(input("Введите id объявления: "))
        vibor = str(input(" Выберите: \n  1. Использовать\n  2. Закрыть \n"))
        stat = 1
        if vibor=="1":
            stat= 0
            tx_hash = contract.functions.updateAdStatus(id_ad - 1, stat).transact({
                'from': account
            })
            print(f" Активность объявления изменена : {tx_hash.hex()} ")
        elif vibor=="2":
            stat= 1
            tx_hash = contract.functions.updateAdStatus(id_ad - 1, stat).transact({
                'from': account
            })
            print(f" Активность объявления изменена : {tx_hash.hex()} ")
        else:
            print(" Ошибка изменения активности: Нужно вводить номер варианта")
    except Exception as e:
        print(f" Ошибка изменения активности : {e}\n Возможно вы неверно указали id")
def create_add(account):
    try:
        try:
            price = int(input(" Введите цену недвижимости: "))
            id_estate = int(input(" Введите id недвижимости: "))
        except:
            print(" Ошибка создания объявления: Возможно вы неверно указали цену и id")
            return
        tx_hash = contract.functions.createAd(id_estate-1, price).transact({
            'from': account
        })
        tx_hash = contract.functions.updateEstateStatus(id_estate - 1, False).transact({
            'from': account
        })
        print(f" Объявление {tx_hash.hex()} создано ")
    except Exception as e:
        print(f"Ошибка создания объявления: {e}\n Возможно дааный дом закрыт или уже имеет объявление")
def get_add():
    adds = contract.functions.getAds().call({
    })
    i =0
    for add in adds:
        if add[5]==0:
            i=1+i
            print(f"----------------Объявление №{i}-----------------")
            print(f" Собственник: {add[0]}")
            print(f" Цена: {add[2]}")
def bue(account):
    try:
        id_add = int(input(" Введите id объявления: "))
        tx_hash = contract.functions.bueEstate(id_add-1).transact({
            'from': account
        })
        print(f" Транзакция {tx_hash.hex()} выполнена")
    except Exception as e:
        print(f" Ошибка покупки {e}\n Возможно вы неверно указали id")

def main():
    account = ""
    while True:
        if account == "" or account == None:
            choice = str(input(" Выберите: \n  1. Авторизация \n  2. Регистрация \n  3. Выйти\n"))
            match choice:
                case "1":
                    account = login()
                case "2":
                    register()
                case "3":
                    exit()
                case _:
                    print(" Выберите от 1 до 3")
        else:
            print("---------------------------------------")
            choice= str(input(" Выберите: \n  1. Отправить эфир на контракт\n  2. Посмотреть баланс на смарт-контракте\n  3. Посмотреть баланс аккаунта\n  4. Снять средства с контракта\n  5. Перевести эфир другому пользователю\n  6. Создать недвижимость\n  7. Посмотреть свои доступные недвижимости\n  8. Создать объявление\n  9. Посмотреть все объявления\n  10. Купить недвижимость\n  11. Изменить статус недвижимотси\n  12. Изменить статус объявления\n  13. Выйти\n"))
            print("---------------------------------------")
            match choice:
                case "1":
                    send_eth(account)
                case "2":
                    get_balance(account)
                case "3":
                    print(f" Баланс аккаунта: {w3.eth.get_balance(account)}")
                case "4":
                    withdraw_me(account)
                case "5":
                    withdraw (account)
                case "6":
                    create_Estate(account)
                case "7":
                    get_Estate(account)
                case "8":
                    create_add(account)
                case "9":
                    get_add()
                case "10":
                    bue(account)
                case "11":
                    izmen_stat_estate(account)
                case "12":
                    izmen_stat_ads(account)
                case "13":
                    account=""
                case _:
                    print(" Выберите от 1 до 13")

if __name__ == "__main__":
    main()