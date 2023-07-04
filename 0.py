from datetime import datetime
import time
import asyncio

def main():
    store = None
    def hook(input):
        nonlocal store
        store = input
    def get():
        nonlocal store
        return store
    return hook,get

h,g = main()
h2,g2 = main()

h("iiiiii")

h2("hhhhh")

print(g(),g2())