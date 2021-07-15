import json
import itertools

def main():
    with open('resources/_seeds-BIP0039.txt') as f:
        dictionary = [l.strip() for l in f.readlines()]
        permutation_list = list(itertools.permutations(dictionary, 12))

        with open('results/permutations.json', 'a') as a:
            a.write(
                f'{json.dumps(permutation_list)}\n')

if __name__ == '__main__':
    main()
