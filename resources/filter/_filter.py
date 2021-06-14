with open(r'original.txt') as in_file, open(r'filtered.txt', 'w') as out_file:
    for line in in_file:
        if len(line) <= 35:
            out_file.write(line)
