def crypt(n):
    if n < 0:
        return '1' + bin(int(n * 10 ** 10))[3:]
    return '0' + bin(int(n * 10 ** 10))[2:]


def decrypt(a):
    if a[0] == '1':
        return -float(int(a[1:], 2)) / 10 ** 10
    return float(int(a[1:], 2)) / 10 ** 10
