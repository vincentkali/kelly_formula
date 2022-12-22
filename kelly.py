import random
import seaborn as sns, numpy as np
import matplotlib.pyplot as plt
import statistics
from math import sqrt, log
from datetime import date, timedelta

def kelly():
    return ((win_return*win_rate) - (1-win_rate)) / win_return

def kellySlow():
    return kelly() / kellySlowRatio

"""
若用少數幾種交易策略 -> win_rate要到 0.87, 才能以 SD_rate<0.2 的方式達到 x2000 before 2023/6/15
-> cons: 策略尋找成本高

若用超級多交易策略去分擔風險 -> win_rate只要到 0.63, 就能達到 x2000 before 2023/6/15
-> cons: 高維護成本
"""

# input
win_rate = 0.63
spend_time = 4 * 30
InGameIteration = 123

kellySlowRatio = 5

fee_rate = 0.04 * 0.01
win_return = 1 - fee_rate*2

bet_rate = kelly()


# config
target_rate = 2000
init_balance = 100
gameIteration = 10000
today = date.today()
goal = date(year=2023, month=6, day=15)
min_SD_rate = 5

# print info
print(f'Today: {today}')
print(f'goal: {goal}')
print()
print(f'InGameIteration: {InGameIteration}')
print(f'win_return: {win_return}')
print(f'win_rate: {win_rate}')
print()



print(f'kellySlowRatio: {kellySlowRatio}')
print(f'bet_rate: {bet_rate}')

def colored(text, r=0, g=0, b=0):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

def betAmount(balance):
    return balance * bet_rate

def playGame():
    balance = init_balance
    for i in range(InGameIteration):
        rand = random.random() 
        bet = betAmount(balance=balance)
        if rand < win_rate:
            # win
            balance += bet * win_return
        else:
            # loss
            balance -= bet
    return balance

def analysis(results):
    average = sum(results) / len(results)
    variance = statistics.variance(results)

    
    SD = sqrt(variance)
    
    average_rate = average / init_balance
    SD_rate = SD / init_balance
    SD_rate_compare = SD_rate / average_rate

    if average_rate > 1:
        """
        day_rate^spend_time = average_rate
        -> day_rate = average_rate^(1/spend_time)

        day_rate^target_spend_time = target_rate
        target_spend_time = log(target_rate, day_rate)
        """
        day_rate = pow(average_rate, 1/spend_time)
        target_spend_time = int(log(target_rate, day_rate))
        target_time = today + timedelta(days=target_spend_time)
    else:
        target_spend_time = None
        target_time = None

    return average, SD, average_rate, SD_rate, SD_rate_compare, target_spend_time, target_time

def get_target_time_pass(target_time):
    target_time_pass = target_time < goal if target_time else None
    target_time_pass = colored(target_time_pass, g=255) if target_time_pass else colored(target_time_pass, r=255)
    return target_time_pass

def get_min_SD_rate_pass(SD_rate_compare):
    SD_rate_pass = SD_rate_compare < min_SD_rate
    SD_rate_pass = colored(SD_rate_pass, g=255) if SD_rate_pass else colored(SD_rate_pass, r=255)
    return SD_rate_pass


results = []
for i in range(gameIteration):
    results.append(playGame())

results.sort()
high_partition = int(len(results) * 0.8)
low_partition = int(len(results) * 0.2)

mid_results = results[low_partition : high_partition]
high_results = results[high_partition : ]
low_results = results[ : low_partition]

average, SD, average_rate, SD_rate, SD_rate_compare, target_spend_time, target_time = analysis(results=results)
high_average, high_SD, high_average_rate, high_SD_rate, high_SD_rate_compare, high_target_spend_time, high_target_time = analysis(results=high_results)
mid_average, mid_SD, mid_average_rate, mid_SD_rate, mid_SD_rate_compare, mid_target_spend_time, mid_target_time = analysis(results=mid_results)
low_average, low_SD, low_average_rate, low_SD_rate, low_SD_rate_compare, low_target_spend_time, low_target_time = analysis(results=low_results)

print()
print(f'average: {init_balance} -> {average}, average_rate: 1 -> {average_rate}, target_spend_time: {target_spend_time}, target_time: {target_time}')
print(f'SD: {SD}, SD_rate: {SD_rate}, SD_rate_compare: {SD_rate_compare}')
print(f'target_time_pass: {get_target_time_pass(target_time)}')
print(f'SD_rate_pass: {get_min_SD_rate_pass(SD_rate_compare)}')
print()
print(f'high_average: {init_balance} -> {high_average}, high_average_rate: 1 -> {high_average_rate}, high_target_spend_time: {high_target_spend_time}, high_target_time: {high_target_time}')
print(f'high_SD: {high_SD}, high_SD_rate: {high_SD_rate}, high_SD_rate_compare: {high_SD_rate_compare}')
print(f'target_time_pass: {get_target_time_pass(high_target_time)}')
print(f'SD_rate_pass: {get_min_SD_rate_pass(high_SD_rate_compare)}')
print()
print("="*150)
print(f'mid_average: {init_balance} -> {mid_average}, mid_average_rate: 1 -> {mid_average_rate}, mid_target_spend_time: {mid_target_spend_time}, mid_target_time: {mid_target_time}')
print(f'mid_SD: {mid_SD}, mid_SD_rate: {mid_SD_rate}, mid_SD_rate_compare: {mid_SD_rate_compare}')
print(f'target_time_pass: {get_target_time_pass(mid_target_time)}')
print(f'SD_rate_pass: {get_min_SD_rate_pass(mid_SD_rate_compare)}')
print("="*150)
print()
print(f'low_average: {init_balance} -> {low_average}, low_average_rate: 1-> {low_average_rate}, low_target_spend_time: {low_target_spend_time}, low_target_time: {low_target_time}')
print(f'low_SD: {low_SD}, low_SD_rate: {low_SD_rate}, low_SD_rate_compare: {low_SD_rate_compare}')
print(f'target_time_pass: {get_target_time_pass(low_target_time)}')
print(f'SD_rate_pass: {get_min_SD_rate_pass(low_SD_rate_compare)}')
print()