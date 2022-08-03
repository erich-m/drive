#coding: UTF-8
import mice
from time import sleep

def main():
    print(mice.variables["sleepfor"])
    sleep(mice.variables["sleepfor"])
    return 1#return 1 on success