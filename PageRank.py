from bs4 import BeautifulSoup as sp
import os
import requests
import time

PREFIX = "https://en.wikipedia.org"
url_map = {}
out_sum_map = {}
in_sum_map = {}
sink = []
PR = {}
newPR = {}


def make_graph(num):
    file_path = "w" + str(num) + ".txt"

    sink_page = 0
    source_page = 0
    max_out_degree = 0
    max_in_degree = 0

    line = open(file_path, "r")
    index_list = line.readlines()

    for i in range(len(index_list)):
        if index_list[i].endswith("\n"):
            index_list[i] = index_list[i][:-1]
        url_map[index_list[i]] = set()

    index = 0

    for base_url in index_list:
        # get and parse
        response = requests.get(base_url).text
        print("get html...")
        time.sleep(0.1)
        soup = sp(response, "html.parser")
        a_list = soup.findAll('a', href=True)

        out_degree = 0

        for item in a_list:
            href = item.get("href")
            if href.startswith("#"):
                continue
            if "#" in href:
                href = href.split("#")[0]

            url = PREFIX + href
            if url == base_url:
                continue
            nei = url_map.get(url)

            if nei is not None:
                if base_url not in nei:
                    nei.add(base_url)
                    max_in_degree = max(max_in_degree, len(nei))
                    out_degree += 1
        # record sink page
        if out_degree == 0:
            sink_page += 1
            sink.append(base_url)
        else:
            out_sum_map[base_url] = out_degree
            max_out_degree = max(max_out_degree, out_degree)

        index += 1

    # write to file
    output_graph_path = "G" + str(num) + ".txt"
    fx = open(output_graph_path, 'w')
    for node, nei in url_map.items():
        node = node.split("/")[-1]
        # for task3.3
        in_sum_map[node] = len(nei)

        fx.write(node)
        for in_link in nei:
            in_link = in_link.split("/")[-1]
            fx.write("\t" + in_link)
        fx.write('\n')
    fx.close()

    # for task3.3 output in_degree map decending
    output_indegree_path = "InDegree" + str(num) + ".txt"
    fi = open(output_indegree_path, "w")
    for key, v in sorted(in_sum_map.items(), key=lambda item: item[1], reverse=True):
        fi.write(key + "\t" + str(v) + "\n")
    fi.close()

    # statistics, get source page amount
    fr = open(output_graph_path, 'r')
    for line in fr:
        list = line.split("\t")
        if len(list) == 1:
            source_page += 1
    fr.close()

    # for key, value in out_sum_map.items():
    #     print(key + "\t" + str(value))

    # write statistics to file S
    output_stat_path = "S" + str(num) + ".txt"
    fs = open(output_stat_path, "w")
    fs.write("source page sum: " + str(source_page) + "\n")
    fs.write("sink page sum: " + str(sink_page) + "\n")
    fs.write("Max in degree: " + str(max_in_degree) + "\n")
    fs.write("Max out degree: " + str(max_out_degree))
    fs.close()
    return index


def page_rank(num, n, d):

    match_count = 0
    iter_num = 0
    l_s_list = []
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

        if is_converge(l_s_list):
            match_count += 1
            if match_count == 4:
                break
        else:
            match_count = 0

        for key in PR.keys():
            PR[key] = newPR[key]

    # output to PR file
    output_PR_path = "PR" + str(num) + ".txt"
    fw = open(output_PR_path, "w")
    pr_sum = 0
    for key, v in sorted(PR.items(), key=lambda item: item[1], reverse=True):
        pr_sum += v
        fw.write(key.split("/")[-1] + "\t" + str(v))
        fw.write("\n")
    fw.write("total PR Sum is: " + str(pr_sum) + "\n")
    fw.write("Iteration time is: " + str(iter_num))
    fw.close()

    # output to file l1 and newPR sum
    output_ls_path = "l1andNewPRsum" + str(num) + ".txt"
    fls = open(output_ls_path, "w")
    for i in l_s_list:
        fls.write("l1: " + str(i[0]) + "\t" + "newPR sum: " + str(i[1]) + "\n")
    fls.close()


def is_converge(l_s_list):
    l1 = 0
    newPR_sum = 0
    for p in url_map.keys():
        l1 += abs(PR[p] - newPR[p])
        newPR_sum += newPR[p]
    # add to list
    l_s_list.append([l1, newPR_sum])

    if l1 < 0.001:
        return True
    else:
        return False


def main(task):
    num = task
    n = make_graph(num)
    print("finish making graph and N is " + str(n))
    page_rank(num, n, 0.85)


main(1)