from web3 import Web3
from eth_account import Account


# Общий баланс
total_balance = 0

# Все адреса
#all_address = ['0x6CEe063659FFF8a1cbB575a3Df186C295856cA62','0x6CEe063659FFF8a1cbB575a3Df186C295856cA62','0x6CEe063659FFF8a1cbB575a3Df186C295856cA62']
address_to_mnemonic = {
    '0x6CEe063659FFF8a1cbB575a3Df186C295856cA62': 'MNEMONIC_PHRASE_1',
    '0x6CEe063659FFF8a1cbB575a3Df186C295856cA63': 'MNEMONIC_PHRASE_2',
    '0x6CEe063659FFF8a1cbB575a3Df186C295856cA64': 'MNEMONIC_PHRASE_3',
}

# Адрес для перевода
to_wallet_address = '0x6CEe063659FFF8a1cbB575a3Df186C295856cA62'

def main():
    # ETH нод
    w3 = Web3(Web3.HTTPProvider('https://eth.llamarpc.com'))

    # Функция получения баланса
    def get_balance(address):

        # Получаем Аадрес
        address = address

        # Получаем баланс адреса
        balance = w3.eth.get_balance(address)
        finaly_balance = Web3.from_wei(balance, 'ether')

        return finaly_balance

    # Функция для build'a транзакции
    def build_txn(*, web3: Web3, from_address, to_address, amount):
        # цена газа
        gas_price = web3.eth.gas_price

        # количество газа
        gas = 2_000_000  # ставим побольше

        # число подтвержденных транзакций отправителя
        nonce = web3.eth.getTransactionCount(from_address)

        txn = {
            'chainId': web3.eth.chain_id,
            'from': from_address,
            'to': to_address,
            'value': int(Web3.toWei(amount, 'ether')),
            'nonce': nonce,
            'gasPrice': gas_price,
            'gas': gas,
        }
        return txn

    #Получение PRIVATE KEY с помощью Мнемонической фразы
    def get_private_key(mnemonic_phraze):
        MNEMONIC = mnemonic_phraze

        # Включение неаудируемых функций мнемонической фразы
        Account.enable_unaudited_hdwallet_features()

        account = Account.from_mnemonic(MNEMONIC)
        private_key = account._private_key.hex()  # hex адрес

        return private_key


    #Проходимся по адресам и проверяем общий баланс
    for address in address_to_mnemonic.keys():
        new_balance = get_balance(address)

        total_balance += new_balance

    #Если общий баланс больше 10 ETH
    if total_balance >= w3.toWei(10, 'ether'):
        for address, mnemonic_phrase in address_to_mnemonic.items():
            address_balance = get_balance(address)

            if address_balance == 0:
                continue

            #Получаем private key аккаунта через Мнемоническую фразу
            private_key = get_private_key(mnemonic_phraze)

            transaction = build_txn(
                web3=Web3,
                from_address = address,
                to_address = to_wallet_adress,
                amount = address_balance
            )

            #Подписываем транзакцию с приватным ключом
            signed_txn = web3.eth.account.sign_transaction(transaction, private_key)

            #Отправка транзакции
            txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)

            # Получаем хэш транзакции
            # Можно посмотреть статус тут https://testnet.bscscan.com/
            print(txn_hash.hex())


if __name__ == '__main__':
    main()

##
