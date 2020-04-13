# coding: utf-8

# use Qt5Agg as TkAgg really hates threads
import matplotlib
matplotlib.use('Qt5Agg')

from meggie import mainWindowMain

def main():
    mainWindowMain.main()


if __name__ == '__main__':
    mainWindowMain.main()
