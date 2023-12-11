import time

from web3 import Web3
from loguru import logger

delay = (10, 30)
max_gwei = 25
rpc = 'https://zksync-era.blockpi.network/v1/rpc/public'
rpc_eth = 'https://ethereum.blockpi.network/v1/rpc/public'
web3 = Web3(Web3.HTTPProvider(rpc))
web3_eth = Web3(Web3.HTTPProvider(rpc_eth))


def read_file(filename: str) -> list[str]:
    with open(filename) as file:
        lines = [line.strip() for line in file]

    return lines


def write_to_file(filename: str, text: str) -> None:
    with open(filename, 'a') as file:
        file.write(f'{text}\n')


def wait_normal_gwei() -> None:
    while (x := web3_eth.from_wei(web3_eth.eth.gas_price, 'gwei')) > max_gwei:
        logger.info(f'Gwei ({x}) > {max_gwei}')
        time.sleep(17)


def get_free_ticket(private: str) -> None:
    address = web3.eth.account.from_key(private).address
    try:
        tx = {
            'from': address,
            'to': web3.to_checksum_address('0xC91AAacC5adB9763CEB57488CC9ebE52C76A2b05'),
            'value': 0,
            'gasPrice': web3.eth.gas_price,
            'gas': random.randint(600_000, 700_000),
            'data': '0xc002c4d6',
            'nonce': web3.eth.get_transaction_count(address),
            'chainId': web3.eth.chain_id
        }

        tx_create = web3.eth.account.sign_transaction(tx, private)
        tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
        write_to_file('hashes.txt', tx_hash.hex())
        logger.success(f'{address} | Transaction done: {tx_hash.hex()}')
        time.sleep(random.randint(*delay))
    except Exception as e:
        logger.exception(e)
        write_to_file('errors.txt', f'{address};{private};{e}')


def main() -> None:
    privates = read_file('privates.txt')

    for private in privates:
        wait_normal_gwei()
        get_free_ticket(private)


if __name__ == '__main__':
    main()
