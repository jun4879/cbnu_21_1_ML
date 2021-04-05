# 출처 : https://leedakyeong.tistory.com/entry/%EB%B0%91%EB%B0%94%EB%8B%A5%EB%B6%80%ED%84%B0-%EC%8B%9C%EC%9E%91%ED%95%98%EB%8A%94-%EB%94%A5%EB%9F%AC%EB%8B%9D-%ED%8D%BC%EC%85%89%ED%8A%B8%EB%A1%A0%EC%9C%BC%EB%A1%9C-XOR-%EA%B2%8C%EC%9D%B4%ED%8A%B8-%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0-in-python-%ED%8C%8C%EC%9D%B4%EC%8D%AC
# 논리 게이트 내용 참고 블로그 : http://www.terms.co.kr/logicgate.htm
import numpy as np


def AND(x1, x2):
    x = np.array([x1,x2])
    w = np.array([0.5,0.5])  # weight
    b = -0.7  # bias
    tmp = np.sum(w*x)+b  # wx+b
    print('AND weighted sum :', tmp)
    if tmp <= 0:  # classification 역할
        return 0
    else:
        return 1


def NAND(x1, x2):
    x = np.array([x1,x2])
    w = np.array([-0.5,-0.5])
    b = 0.7
    tmp = np.sum(w*x)+b
    print('NAND weighted sum :',tmp)
    if tmp <= 0:
        return 0
    else:
        return 1


def OR(x1, x2):
    x = np.array([x1, x2])
    w = np.array([0.5, 0.5])
    b = -0.2
    tmp = np.sum(w*x)+b
    print('OR weighted sum :', tmp)
    if tmp <= 0:
        return 0
    else:
        return 1


def XOR(x1, x2):
    s1 = NAND(x1, x2)
    s2 = OR(x1, x2)
    y = AND(s1, s2)  # 2 Layer
    return y


print(XOR(0, 0))
print(XOR(0, 1))
print(XOR(1, 0))
print(XOR(1, 1))
