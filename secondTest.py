import functions
from functions import createTrafficMatrix, checksIfTheNetworkIsNotCutOff, new_g, newDiscardedLinks, \
    findTheLinkForKeepingTheNetworkNotCutOff, isThisLinkCritical, new_links
from algorithms import IP_SB, EAFFB, SZFB, newAlgorithm
import itertools

nodes = ['ATH', 'LAR', 'THE', 'SER', 'DRA', 'XAN', 'LIM', 'MIT', 'CHI', 'SYR', 'SAM', 'RHO', 'HER', 'RET', 'CHA',
         'KOZ', 'IOA', 'LOU', 'MES', 'PAT', 'LEH', 'KAL', 'TRI', 'COR']

nea_links = ['236', '147', '73', '51', '62', '153', '157', '0111', '160', '130', '182', '270', '341', '251', '60', '45',
             '279', '70', '69', '63', '125', '54', '111', '31', '110', '57', '109', '99', '00105', '00134', '00237',
             '00143', '00229', '00212']

nea_g = [['ATH', '236'], ['ATH', '279'], ['ATH', '130'], ['ATH', '70'], ['LAR', '236'], ['LAR', '147'], ['THE', '147'],
     ['THE', '99'], ['THE', '73'], ['SER', '73'], ['SER', '51'], ['DRA', '51'], ['DRA', '62'], ['XAN', '62'],
     ['XAN', '153'], ['LIM', '153'], ['LIM', '157'], ['MIT', '157'], ['MIT', '0111'], ['CHI', '0111'], ['CHI', '160'],
     ['SYR', '160'], ['SYR', '130'], ['SYR', '251'], ['SYR', '182'], ['SAM', '182'], ['SAM', '270'], ['RHO', '270'],
     ['RHO', '341'], ['HER', '341'], ['HER', '251'], ['HER', '60'], ['RET', '60'], ['RET', '45'], ['CHA', '45'],
     ['CHA', '279'], ['COR', '70'], ['COR', '69'], ['COR', '111'], ['TRI', '69'], ['PAT', '111'], ['TRI', '63'],
     ['PAT', '54'], ['KAL', '63'], ['PAT', '31'], ['KAL', '125'], ['LEH', '125'], ['LEH', '54'], ['MES', '31'],
     ['MES', '110'], ['LOU', '110'], ['LOU', '57'], ['IOA', '57'], ['IOA', '109'], ['KOZ', '109'], ['KOZ', '99'],
     ['CHI', '00105'], ['SAM', '00105'], ['IOA', '00134'], ['LAR', '00134'], ['KAL', '00237'], ['CHA', '00237'],
     ['LOU', '00143'], ['LAR', '00143'], ['SYR', '00229'], ['CHA', '00229'], ['THE', '00212'], ['LIM', '00212']]

regionLinks = [['341'], ['60', '251'], ['45'], ['279'], ['63'], ['69'], ['125'], ['54'], [], ['31'], ['236'], ['110'],
               ['57'], ['236'], ['236'], ['236'], ['109'], ['147', '99'], ['73'], ['51'], ['62'], ['153', '43'], ['66'],
               ['153'], ['157'], ['0111'], ['160'], ['182', '270'], ['160', '182', '251'], ['130'], ['279'], ['279'],
               ['251'], ['341'], ['270'], ['111']]

regionLinks2 = [['341'], ['60', '251'], ['45'], ['279'], ['63'], ['69'], ['125'], ['54'], [], ['31'], ['236'], ['110'],
                ['57'], ['236'], ['236'], ['236'], ['109'], ['147', '99'], ['73'], ['51'], ['62'], ['153'],
                ['153'], ['157'], ['0111'], ['160'], ['182'], ['160', '182', '251'], ['130'], ['279'], ['279'],
                ['251'], ['341'], ['270'], ['111']]

nea_regionLinks = [['341'], ['60', '251'], ['45', '00229'], ['279', '00237'], ['63', '00237'], ['69', '00237'], ['125'], ['54'], [], ['31'], ['236'],
                   ['110'], ['57', '00134', '00143'], ['236', '00143'], ['236'], ['236'], ['109'], ['147', '99', '00134'], ['73', '00212'], ['51', '00212'], ['62'],
                   ['153', '43'], ['66'], ['153', '00212'], ['157'], ['0111'], ['160', '00134'], ['182'], ['160', '182', '251'],
                   ['130', '00229'], ['279'], ['279', '00229', '00237'], ['251'], ['341'], ['270'], ['111']]

seismicRegions = [['341'], ['60', '251'], ['45'], ['279'], ['69'], ['125'], ['54'], ['31'], ['236'], ['110'], ['236'],
                  ['236'], ['73'], ['153', '43'], ['153'], ['157'], ['0111'], ['182'], ['341'], ['270'], ['111']]


def is_this_link_in_min_combination(link_checked, min_combination):
    for link in min_combination:
        if link_checked == link:
            return True

    return False


def new_newAlgorithm(nodes, links, g, traffic, regions, number_of_total_links_acceptable):
    notCriticalLinks = []
    for link in links:
        if not isThisLinkCritical(nodes, [link], regions, g):
            notCriticalLinks.append(link)

    """
    combinations = []
    for i in range(6):
        oc = itertools.combinations(notCriticalLinks, i + 1)
        for c in oc:
            combinations.append(list(c))
    

    combinations = []
    print(len(links) - number_of_total_links_acceptable)
    oc = itertools.combinations(notCriticalLinks, len(links) - number_of_total_links_acceptable)
    for c in oc:
        combinations.append(list(c))

    min_combination = combinations[len(combinations)-1]
    # min_power = EAFFB(nodes, new_links(min_combination, links), new_g(min_combination, g), traffic, regions)
    min_power = IP_SB(nodes, new_links(min_combination, links), new_g(min_combination, g), traffic)

    for i in range(len(combinations)-1):
        if checksIfTheNetworkIsNotCutOff(nodes, new_g(combinations[i], g)):
            # combination_power = EAFFB(nodes, new_links(combinations[i], links), new_g(combinations[i], g), traffic, regions)
            combination_power = IP_SB(nodes, new_links(combinations[i], links), new_g(combinations[i], g), traffic)
            if combination_power < min_power:
                min_combination = combinations[i]
                min_power = combination_power
                
    """
    """
    links_power_dict = {}
    links_power = []
    for link in notCriticalLinks:
        link_power = IP_SB(nodes, new_links([link], links), new_g([link], g), traffic)
        links_power.append(link_power)
        links_power_dict[link_power] = link

    links_power.sort()
    2787935.4
(['236', '147', '160', '130', '182', '251', '279', '70', '111', '00105', '00134', '00237', '00143', '00229', '00212'], [], ['00105', '00134', '00229', '182', '111', '251'], 2789305.4)


2869520.6
(['236', '147', '160', '130', '182', '251', '279', '70', '111', '00105', '00134', '00237', '00143', '00229', '00212'], [], ['00134', '111', '130', '160', '70', '00143'], 2818847.8)

    """

    combinations = []
    min_combination = []
    for i in range(len(links) - number_of_total_links_acceptable):
        links_power_dict = {}
        links_power = []
        for link in notCriticalLinks:
            if not is_this_link_in_min_combination(link, min_combination):
                if checksIfTheNetworkIsNotCutOff(nodes, new_g(min_combination + [link], g)):
                    print(str(min_combination + [link]))
                    # link_power = IP_SB(nodes, new_links(min_combination + [link], links), new_g(min_combination + [link], g), traffic)
                    link_power = EAFFB(nodes, new_links(min_combination + [link], links), new_g(min_combination + [link], g), traffic, regions)
                    links_power.append(link_power)
                    links_power_dict[link_power] = link

        links_power.sort()
        min_combination.append(links_power_dict[links_power[0]])

    # min_power = IP_SB(nodes, new_links(min_combination, links), new_g(min_combination, g), traffic)
    min_power = EAFFB(nodes, new_links(min_combination, links), new_g(min_combination, g), traffic, regions)

    return notCriticalLinks, combinations, min_combination, min_power

# k = ['00134', '111', '251', '00105', '182']
k = ['182', '251']
print(checksIfTheNetworkIsNotCutOff(nodes, new_g(k, nea_g)))

print(functions.checksIfTheNetworkIsNotCutOff_EAFFB(nodes, new_g(k, nea_g), nea_regionLinks))

print(functions.bfs('SAM', 'ATH', new_g(k, nea_g)))


aaa = ['00105', '00134', '00237', '00143', '00229', '00212']
print(aaa)
print(aaa + ['aa'])
traffic = createTrafficMatrix(nodes, 120)
# print(IP_SB(nodes, new_links(['00105', '00134', '00237', '00143', '00229', '00212'], nea_links), new_g(['00105', '00134', '00237', '00143', '00229', '00212'], nea_g), traffic))
print(EAFFB(nodes, new_links(['00105', '00134', '00237', '00143', '00229', '00212'], nea_links), new_g(['00105', '00134', '00237', '00143', '00229', '00212'], nea_g), traffic, nea_regionLinks))
print(new_newAlgorithm(nodes, nea_links, nea_g, traffic, nea_regionLinks, 28))


