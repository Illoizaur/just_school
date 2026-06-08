import os

with open("/home/illoi/work/test/test.txt", "r+") as f:
    text = f.read()
    print(text)

print("*"*20)

with open("/home/illoi/work/test/test.txt", "r+") as f:
    text = f.readline()
    print(text)

print("*"*20)

with open("/home/illoi/work/test/test.txt", "r+") as f:
    text = f.readlines()
    print(text)