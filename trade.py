#!/usr/bin/env python3

import sys
import re
import calc

last_value_poped = []


def save_candles(temp, list_candle, period):
    candle = []
    line = temp.split()

    try:
        if line[2] == "next_candles":
            candle.append(line[3].split(';')[2].split(',')[4])
            candle.append(line[3].split(';')[2].split(',')[5])
            candle.append(line[3].split(';')[1].split(',')[4])
            candle.append(line[3].split(';')[1].split(',')[5])
            candle.append(line[3].split(';')[0].split(',')[4])
            candle.append(line[3].split(';')[0].split(',')[5])
            list_candle.append(candle)
    except IndexError:
        sys.stderr.write("Wrong Input.\n")
        exit(84)
    if len(list_candle) > period:
        list_candle = pop_oldest_value(list_candle)
    return(list_candle)


def get_total_candles(temp):
    line = temp.split()

    try:
        if line[1] == "candles_total":
            return (int(line[2]))
    except IndexError:
        return (0)


def get_given_candles(temp):
    line = temp.split()

    try:
        if line[1] == "candles_given":
            return (int(line[2]))
    except IndexError:
        return (0)


def save_stack(temp):
    line = temp.split()
    stack = []

    try:
        if line[2] == "stacks":
            stack.append(line[3].split(',')[0].split(':')[1])
            stack.append(line[3].split(',')[1].split(':')[1])
            stack.append(line[3].split(',')[2].split(':')[1])
    except IndexError:
        sys.stderr.write("Wrong Input.\n")
        exit(84)
    return(stack)


def pop_oldest_value(values):
    global last_value_poped

    if len(last_value_poped) > 0:
        last_value_poped.pop(0)
    last_value_poped.append(values[0])
    values.pop(0)
    return (values)


def convert_btc_to_eth(stack, list_candle1, list_candle2, maS, maL, last_buy, devise):
    if float(stack[2]) > 1100:
        print("no_moves")
    else:
        if len(list_candle1) == 25:
            maS.append(calc.calc_mobile_average(list_candle1, devise))
            if len(maS) > 2:
                    maS.pop(0)
        if len(list_candle1) == 25 and len(list_candle2) == 100:
            maL.append(calc.calc_mobile_average(list_candle2, devise))
            if len(maL) > 2:
                maL.pop(0)
            if len(maS) == 2 and len(maL) == 2:
                if (maL[0] > maS[0] and maL[1] < maS[1]) and float(stack[1]) != 0 and last_buy < float(list_candle2[len(list_candle2) - 1][1]):
                        print("sell USDT_" + devise, stack[0])
                        
                elif (maL[0] < maS[0] and maL[1] > maS[1]) and float(stack[0]) >= 0.04:
                    last_buy = float(list_candle2[len(list_candle2) - 1][1])
                    print("buy BTC_ETH 0.02")
                else:
                    print("no_moves")
            else:
                print("no_moves")
        else:
            print("no_moves")


def make_decision(stack, list_candle1, list_candle2, maS, maL, last_buy, devise, is_no_moves):
    if float(stack[2]) > 1100:
        return("no_moves")
    else:
        if len(list_candle1) == 25:
            maS.append(calc.calc_mobile_average(list_candle1, devise))
            if len(maS) > 2:
                    maS.pop(0)
        if len(list_candle1) == 25 and len(list_candle2) == 100:
            maL.append(calc.calc_mobile_average(list_candle2, devise))
            if len(maL) > 2:
                maL.pop(0)
            if len(maS) == 2 and len(maL) == 2:
                if (maL[0] > maS[0] and maL[1] < maS[1]):
                    if (is_no_moves == 1):
                        print(end=';')
                    if devise == "BTC" and float(stack[0]) != 0:
                        print("sell USDT_BTC", stack[0], end='')
                    elif devise == "ETH" and float(stack[1]) != 0:
                        print("sell USDT_ETH", stack[1], end='')
                    else:
                        return("no_moves")
                        
                elif (maL[0] < maS[0] and maL[1] > maS[1]) and float(stack[2]) >= 422:
                    if (is_no_moves == 1):
                        print(end=';')
                    if devise == "BTC":
                        print("buy USDT_" + devise + " 0.02", end='')
                    elif devise == "ETH":
                        print("buy USDT_" + devise + " 0.08", end='')
                else:
                    return("no_moves")
            else:
                return("no_moves")
        else:
            return("no_moves")


def main():
    informations = info()
    last_buy = 0

    while 1:
        try:
            informations.current_line = (input(""))
        except KeyboardInterrupt:
            exit(84)
        except EOFError:
            exit(84)
        informations.short_candle_list = save_candles(informations.current_line, informations.short_candle_list, 25)
        informations.long_candle_list = save_candles(informations.current_line, informations.long_candle_list, 100)
        if informations.current_line[12] == 's':
            stack = save_stack(informations.current_line)
        informations.total_candles = get_total_candles(informations.current_line)
        informations.given_candles = get_given_candles(informations.current_line)
        if informations.current_line[0] == 'a':
            if make_decision(stack, informations.short_candle_list, informations.long_candle_list, informations.short_mobile_average, informations.long_mobile_average, last_buy, "ETH", 0) == "no_moves":
                if make_decision(stack, informations.short_candle_list, informations.long_candle_list, informations.short_mobile_average, informations.long_mobile_average, last_buy, "BTC", 0) == "no_moves":
                    print("no_moves")
                else:
                    print(end='\n')
            else:
                make_decision(stack, informations.short_candle_list, informations.long_candle_list, informations.short_mobile_average, informations.long_mobile_average, last_buy, "BTC", 1)
                print(end='\n')

class info:
    current_line = 0
    short_candle_list = []
    long_candle_list = []
    total_candles = 0
    given_candles = 0
    stack = []
    short_mobile_average = []
    long_mobile_average = []

    def __init__(self):
        self.current_line = 0
        self.short_candle_list = []
        self.long_candle_list = []
        self.total_candles = 0
        self.given_candles = 0
        self.stack = []
        self.short_mobile_average = []  
        self.long_mobile_average = []


if __name__ == '__main__':
    main()
