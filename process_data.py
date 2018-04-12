f = open('data.txt')
names = ''
for line in f:
    line = line.strip().split()
    col_name = line[0]
    col_name = col_name[1:-1]
    print("    " + col_name + ' = info["' + col_name + '"]')
    names = names + ',' + col_name
print(names)
