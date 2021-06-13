from multiprocessing.pool import ThreadPool as Pool
import threading
import json
import itertools

lock = threading.Lock()

def main():
    while True:
        with open("resources/_seeds-BIP0039.txt") as f:
            dictionary = [l.strip() for l in f.readlines()]

            with open("file.json", "a") as w:
                permutation_list = list(itertools.permutations(dictionary, 12))

                w.write(
                    f'{json.dumps(permutation_list)}')

def start():
    try:
        threads = int(input("Number of threads (1 - 666): "))
        if threads > 666:
            print("You can only run 666 threads at once")
            start()
    except ValueError:
        print("Enter an interger!")
        start()

    pool = Pool(threads)
    for _ in range(threads):
        pool.apply_async(main, ())
    pool.close()
    pool.join()


if __name__ == '__main__':
    start()
