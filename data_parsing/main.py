#!/usr/bin/python

############################
# Created on Tue Dec 29 00:28:21 2019
# author: Gordon Cheung
# CID: 01083012
# Project: SIOT
############################


from finance import finance_data
from weather import weather_data

if __name__ == "__main__":
    weather_data()
    finance_data()
