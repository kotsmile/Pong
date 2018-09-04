def crypt(a):
    if a == 0: return '0'
    num = str(abs(a)).split('.')
    n = '0' + bin(int(num[0]))[2:] + '.' + bin(int((num[1] + '0' * 4)[3::-1]))[2:]
    if a < 0:
        n = '1' + n[1:]
    return n


def decrypt(c):
    if c == '0': return 0
    n = c[1:].split('.')
    a = str(int(n[0], 2)) + '.' + str(int(n[1], 2))[::-1]
    if c[0] == '1':
        a = '-' + a
    return float(a)  