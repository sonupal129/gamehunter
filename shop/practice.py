list1 = [1, 2, 3, 4, 5, 6]
list2 = [5, 6, 6, 7, 9, 6]


for a,b in zip(list1, list2):
    if a == b:
        print(a,b)
    continue

print(tuple(range(7,12)))