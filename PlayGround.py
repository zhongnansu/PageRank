import time
from bs4 import BeautifulSoup as sp
import requests
from collections import deque
import os

# soup = sp(open("w1_folder/623.txt", "r"), 'html.parser')
# a_list = soup.findAll('a', href=True)
# for item in a_list:
#     href = item.get("href")
#     if href.startswith("#"):
#         continue
#     if "#" in href:
#         href = href.split("#")[0]

url_map = {"A": {"D", "E", "F"}, "B": {"A", "F"}, "C": {"A", "B", "D"}, "D": {"B", "C"}, "E": {"B", "C", "D", "F"}, "F": {"A", "B", "D"}}
out_sum_map = {"A": 3, "B": 4, "C": 2, "D": 4, "E": 1, "F": 3}
sink = []
PR = {}
newPR = {}

def page_rank(n, d):

    match_count = 0
    iter_num = 0
    for p in url_map.keys():
        PR[p] = 1 / n

    while True:
        iter_num += 1
        sinkPR = 0
        for s in sink:
            sinkPR += PR[s]

        for page in url_map.keys():
            newPR[page] = (1 - d) / n
            newPR[page] += d * sinkPR / n

            for q in url_map[page]:
                newPR[page] += d * PR[q] / out_sum_map[q]

        if is_converge():
            match_count += 1
            if match_count == 4:
                break
        else:
            match_count = 0



        for key in PR.keys():
            PR[key] = newPR[key]

    # output to file
    print("iter num is: " + str(iter_num))
    pr_sum = 0
    for key, v in sorted(PR.items(), key=lambda item: item[1], reverse=True):
        pr_sum += v
        print(key + "\t" + str(v))

    print("total PR Sum is: " + str(pr_sum))

def is_converge():
    l1 = 0

    for p in url_map.keys():
        print(str(PR[p]) + "\t" +  str(newPR[p]))
        l1 += abs(PR[p] - newPR[p])

    if l1 < 0.001:
        print("l1: " + str(l1))
        return True
    else:
        return False


page_rank(6, 0.85)