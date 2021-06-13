import pprint
import mnemonic
import bip32utils
import requests
import random
import os
from decimal import Decimal
from multiprocessing.pool import ThreadPool as Pool
import threading
from Bip39Gen import Bip39Gen
from time import sleep
import ctypes
import datetime

# Database Source: http://addresses.loyce.club/?C=M;O=D

# Script #1: https://github.com/Py-Project/Bitcoin-wallet-cracker
# Script #2: https://github.com/Anarbb/BitGen

class Settings():
    resultsPath = 'results'
    databaseFile = 'resources/_database_5to1.txt'
    seedsFile = 'resources/_seeds-BIP0039.txt'
    checksMadeCounter = 0
    walletsWithBalance = 0
    walletsWithoutBalance = 0


def makeDir():
    if not os.path.exists(Settings.resultsPath):
        os.makedirs(Settings.resultsPath)

lock = threading.Lock()

datetime_timestamp = datetime.datetime.now()
start_time = datetime_timestamp.strftime("%d.%m.%y %H:%M")

def bip39(mnemonic_words):
    mobj = mnemonic.Mnemonic("english")
    seed = mobj.to_seed(mnemonic_words)

    bip32_root_key_obj = bip32utils.BIP32Key.fromEntropy(seed)
    bip32_child_key_obj = bip32_root_key_obj.ChildKey(
        44 + bip32utils.BIP32_HARDEN
    ).ChildKey(
        0 + bip32utils.BIP32_HARDEN
    ).ChildKey(
        0 + bip32utils.BIP32_HARDEN
    ).ChildKey(0).ChildKey(0)

    return bip32_child_key_obj.Address()


def addressInDB(addr):
    with open(Settings.databaseFile) as f:
        adresses = f.read().split()
    return addr in adresses


def check():
    while True:
        with open(Settings.seedsFile) as f:
            dictionary = [l.strip() for l in f.readlines()]

        mnemonic_words = Bip39Gen(dictionary).mnemonic
        address = bip39(mnemonic_words)
    
        with lock:
            Settings.checksMadeCounter += 1

            current_timestamp = datetime.datetime.now()
            event_time = current_timestamp.strftime("%d.%m.%y %H:%M:%S")

            run_time = str(current_timestamp-datetime_timestamp);

            if addressInDB(address):
                Settings.walletsWithBalance += 1

                print(
                    f'{event_time} -> Address: {address} | Balance: Found | Phrase: {mnemonic_words}')

                with open("results/_wallets_found.txt", "a") as w:
                    w.write(
                        f'{event_time} -> Address: {address}, phrase: {mnemonic_words}\n\n')
            else:
                Settings.walletsWithoutBalance += 1

                print(
                    f'{event_time} -> Address: {address} | Balance: Not Found | Phrase: {mnemonic_words}')

                # with open("results/_wallets_empty.txt", "a") as w:
                #     w.write(
                #         f'{event_time} -> Address: {address}, phrase: {mnemonic_words}\n\n')


            ctypes.windll.kernel32.SetConsoleTitleW(
                f"{Settings.walletsWithBalance} / {Settings.checksMadeCounter} | {run_time} | {start_time}")


def start():
    threads = int(os.cpu_count())
    pool = Pool(threads)

    for _ in range(threads):
        pool.apply_async(check, ())
    pool.close()
    pool.join()


if __name__ == '__main__':
    makeDir()
    start()
