from functions import createTrafficMatrix, directLinkWith, bfs, findAllRequestsUsingThisLink
from algorithms import IP_SB, EAFFB, SZFB, npa_nea, newAlgorithm22, IP_SB2
import math


links_location = {
    "236": "land",
    "147": "land",
    "73": "land",
    "51": "land",
    "62": "land",
    "153": "sea",
    "157": "sea",
    "0111": "sea",
    "160": "sea",
    "130": "sea",
    "182": "sea",
    "270": "sea",
    "341": "sea",
    "251": "sea",
    "60": "land",
    "45": "land",
    "279": "sea",
    "70": "land",
    "69": "land",
    "63": "land",
    "125": "land",
    "54": "land",
    "111": "land",
    "31": "sea",
    "110": "land",
    "57": "land",
    "109": "land",
    "99": "land",
    "00105": "sea",
    "00134": "land",
    "00237": "sea",
    "00143": "land",
    "00229": "sea",
    "00212": "sea"
}

test_nodes = ['0', '1', '2', '3', '4', '5']
test_links = ['324', '368', '432', '592', '632', '464', '336', '384']
test_g = [['0', '324'], ['0', '368'], ['1', '324'], ['1', '432'], ['1', '592'], ['2', '368'], ['2', '432'],
          ['2', '632'], ['3', '592'], ['3', '464'], ['3', '384'], ['4', '464'], ['4', '632'], ['4', '336'],
          ['5', '384'], ['5', '336']]

nodes = ['ATH', 'LAR', 'THE', 'SER', 'DRA', 'XAN', 'LIM', 'MIT', 'CHI', 'SYR', 'SAM', 'RHO', 'HER', 'RET', 'CHA',
         'KOZ', 'IOA', 'LOU', 'MES', 'PAT', 'LEH', 'KAL', 'TRI', 'COR']

links = ['236', '147', '73', '51', '62', '153', '157', '0111', '160', '130', '182', '270', '341', '251', '60', '45',
         '279', '70', '69', '63', '125', '54', '111', '31', '110', '57', '109', '99']

g = [['ATH', '236'], ['ATH', '279'], ['ATH', '130'], ['ATH', '70'], ['LAR', '236'], ['LAR', '147'], ['THE', '147'],
     ['THE', '99'], ['THE', '73'], ['SER', '73'], ['SER', '51'], ['DRA', '51'], ['DRA', '62'], ['XAN', '62'],
     ['XAN', '153'], ['LIM', '153'], ['LIM', '157'], ['MIT', '157'], ['MIT', '0111'], ['CHI', '0111'], ['CHI', '160'],
     ['SYR', '160'], ['SYR', '130'], ['SYR', '251'], ['SYR', '182'], ['SAM', '182'], ['SAM', '270'], ['RHO', '270'],
     ['RHO', '341'], ['HER', '341'], ['HER', '251'], ['HER', '60'], ['RET', '60'], ['RET', '45'], ['CHA', '45'],
     ['CHA', '279'], ['COR', '70'], ['COR', '69'], ['COR', '111'], ['TRI', '69'], ['PAT', '111'], ['TRI', '63'],
     ['PAT', '54'], ['KAL', '63'], ['PAT', '31'], ['KAL', '125'], ['LEH', '125'], ['LEH', '54'], ['MES', '31'],
     ['MES', '110'], ['LOU', '110'], ['LOU', '57'], ['IOA', '57'], ['IOA', '109'], ['KOZ', '109'], ['KOZ', '99']]

regionLinks = [['341'], ['60', '251'], ['45'], ['279'], ['63'], ['69'], ['125'], ['54'], ['70', '279', '130'], ['31'],
               ['236'], ['110'], ['57'], ['236'], ['236'], ['236'], ['109'], ['147', '99'], ['73'], ['51'], ['62'],
               ['153', '43'], ['66'], ['153'], ['157'], ['0111'], ['160'], ['182'], ['160', '182', '251'], ['130'],
               ['279'], ['279'], ['251'], ['341'], ['270'], ['111']]

regionLinks2 = [['341'], ['60', '251'], ['45'], ['279'], ['63'], ['69'], ['125'], ['54'], ['70', '279', '130'], ['31'],
                ['236'], ['110'], ['57'], ['236'], ['236'], ['236'], ['109'], ['147', '99'], ['73'], ['51'], ['62'],
                ['153'], [], ['153'], ['157'], ['0111'], ['160'], ['182'], ['160', '182', '251'], ['130'],
                ['279'], ['279'], ['251'], ['341'], ['270'], ['111']]

regionLinks40 = [['341'], ['279'], ['125'], ['236'], ['236'], ['236'], ['147', '99'], ['157'], ['279'], ['341'], ['270']]

seismicRegions = [['341'], ['60', '251'], ['45'], ['279'], ['69'], ['125'], ['54'], ['70', '279', '130'], ['31'],
                  ['236'], ['110'], ['236'], ['236'], ['73'], ['153', '43'], ['153'], ['157'], ['0111'], ['182'],
                  ['341'], ['270'], ['111']]

seismicRegions2 = [['341'], ['60', '251'], ['45'], ['279'], ['69'], ['125'], ['54'], ['70', '279', '130'], ['31'],
                   ['236'], ['110'], ['236'], ['236'], ['236'], ['73'], ['153'], ['153'], ['157'], ['0111'], ['182'],
                   ['341'], ['270'], ['111']]

seismicRegions3 = [['341'], ['60'], ['45'], [], ['69'], ['125'], ['54'], ['70', '279', '130'], ['31'],
                   ['236'], ['110'], ['236'], ['236'], ['236'], ['73'], ['153'], ['153'], ['157'], ['0111'], ['182'],
                   ['341'], ['270'], ['111']]


#test_nodes = ['A', 'C', 'D']
#test_links = ['100', '0100', '150']
#test_g = [['A', '100'], ['A', '150'], ['C', '0100'], ['C', '100'], ['D', '0100'], ['D', '150']]
#test_regions = [['100'], ['0100'], ['150']]


#pt = 1 - math.pow(math.e, -5 / 5.55)
#print(pt)


#count1 = 0
#print(directLinkWith('ATH', g))
#shortestPaths = []
#for i in nodes:
#    for j in nodes:
#        if i != j:
#            count1 += 1
#            shortestPaths.append(bfs(i, j, g))

#print(shortestPaths)
#print(len(shortestPaths))
#print(count1)

# k = findAllRequestsUsingThisLink(shortestPaths, '')

# traffic1 = createTrafficMatrix(test_nodes, 20*6)
#traffic2 = createTrafficMatrix(test_nodes, 20*1)
#print(IP_SB(test_nodes, test_links, test_g, traffic2, links_location))
#print(EAFFB(nodes, links, g, traffic2, regionLinks2, links_location, 0.3))
#IP_SB(nodes, links, g, traffic, links_location)
#e3 = SZFB(nodes, links, g, traffic, seismicRegions2, links_location)
#print("SZFB: " + str(e3))
#e5 = SZFB3(nodes, links, g, traffic, seismicRegions2, links_location)
#print("SZFB2: " + str(e5))
#e5 = SZFB_new2(nodes, links, g, traffic2, seismicRegions2, links_location)
#print("SZFB 40 %: " + str(e5))
#e4 = npa_nea(nodes, links, g, traffic, regionLinks2, links_location)
#print("npa_nea: " + str(e4))
#"""


for i in range(1, 7):
    print("For avg traffic = " + str(20 * i))
    sum_of_test_IP_SB = 0
    sum_of_SZFB = 0
    sum_of_SZFB2 = 0
    sum_of_IP_SB = 0
    sum_of_EAFFB_30 = 0
    sum_of_EAFFB_40 = 0
    sum_of_EAFFB_50 = 0
    for j in range(10):
        traffic = createTrafficMatrix(nodes, 20*i)
        #traffic2 = createTrafficMatrix(test_nodes, 20 * i)
        #sum_of_test_IP_SB += IP_SB(test_nodes, test_links, test_g, traffic2, links_location)/1000
        #sum_of_IP_SB += IP_SB(nodes, links, g, traffic, links_location)/1000
        #sum_of_EAFFB_30 += EAFFB(nodes, links, g, traffic, regionLinks2, links_location, 0.3)/1000
        #sum_of_EAFFB_40 += EAFFB(nodes, links, g, traffic, regionLinks2, links_location, 0.4)/1000
        #sum_of_EAFFB_50 += EAFFB(nodes, links, g, traffic, regionLinks2, links_location, 0.5)/1000
        sum_of_SZFB += SZFB(nodes, links, g, traffic, seismicRegions2, links_location)/1000
        sum_of_SZFB2 += SZFB(nodes, links, g, traffic, seismicRegions3, links_location) / 1000
        # e4 = npa_nea(nodes, links, g, traffic, regionLinks2, links_location)

    #print("test_IP-SB: " + str(sum_of_test_IP_SB / 10000))
    #print("IP-SB: " + str(sum_of_IP_SB / 10))
    #print("EAFFB 30%: " + str(sum_of_EAFFB_30 / 10))
    #print("EAFFB 40%: " + str(sum_of_EAFFB_40 / 10))
    #print("EAFFB 50%: " + str(sum_of_EAFFB_50 / 10))
    print("SZFB: " + str(sum_of_SZFB / 10))
    print("SZFB2: " + str(sum_of_SZFB2 / 10))
    # print("npa_nea: " + str(e4))
    print("///////")
#"""

# pt = 1 - math.pow(math.e, -5 / 21.42)
# print(pt)

