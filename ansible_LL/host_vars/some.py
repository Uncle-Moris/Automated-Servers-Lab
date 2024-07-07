start = 87

n = 0

while True:
    start = start*1.25
    n += 1
    if start > 10000:
        print(f"n: {n}: ammount {start}")
        break 