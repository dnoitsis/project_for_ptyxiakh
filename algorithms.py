import math
import itertools
from functions import bfs, create_Cij, create_Wij, create_fmn, directLinkWith, \
    create_x_y_forEveryRegion, new_g, findAllRequestsUsingThisLink, brokenPaths, sum2, sum1, \
    checksIfTheNetworkIsNotCutOff, isThisLinkCritical, new_links, calculate_laying_cost, \
    is_this_link_in_min_combination, checksIfTheNetworkIsNotCutOff_EAFFB, create_fmn2, create_Wij_Aij, create_Wmn, \
    create_Cij_new, create_Wmn_Lmn_new, calculate_energy_consumption, return_critical_regions

eee = []
eeek = {}
# lowerThresholdValue = 0.3
Mx = 5
My = 4
T = 5
t_study = 58


#
R_COST = 90000
T_COST = 25000
EDFA_COST = 1500
COST_FOR_REPAIR = 50000


# Implementation of the IP-SB algorithm.
def IP_SB(nodes, links, g, traffic, links_location):
    shortestPaths = []

    # Creating the paths, between all the nodes.
    for i in nodes:
        for j in nodes:
            if i != j:
                shortestPaths.append(bfs(i, j, g))

    # print(shortestPaths)
    # Calculating the average hops.
    total_hops = 0
    for path in shortestPaths:
        total_hops += len(path[1])

    # print("avg hops = " + str(total_hops / len(shortestPaths)))
    # Calculating the energy cost.
    eTotal = calculate_energy_consumption(traffic, shortestPaths, nodes)
    return eTotal


def IP_SB2(nodes, links, g, traffic, links_location):
    shortestPaths = []

    # Creating the paths, between all the nodes.
    for i in nodes:
        for j in nodes:
            if i != j:
                shortestPaths.append(bfs(i, j, g))

    # Calculating the average hops.
    total_hops = 0
    for path in shortestPaths:
        total_hops += len(path[1])

    # print("avg hops = " + str(total_hops / len(shortestPaths)))

    # Initialization of cost counters.
    rooter_cost = 0
    tran_cost = 0
    edfa_cost = 0

    # Creation of Cij, Wij and fnm.
    C_ij = create_Cij(traffic)
    w_ij = create_Wmn(shortestPaths, C_ij, links)
    f_nm = create_fmn(w_ij, links)
    #print(traffic)
    sumtr = 0
    for i in traffic.keys():
        sumtr += traffic[i]
    #print(sumtr / len(traffic.keys()))
    #print(C_ij)
    #print(w_ij)
    #print(f_nm)

    # print("////")

    # Calculating the energy cost.
    eRouter = 0
    for i in nodes:
        Di = 0
        c_ij_sum = 0
        for d in nodes:
            Di += traffic[i + d]
            #if i != d:
                #Di += traffic[i + d]

        for j in nodes:
            if i != j:
                #Di += traffic[i + d]
                c_ij_sum += C_ij[i + j]

        eRouter += 1000 * ((Di / 40) + c_ij_sum)
        #rooter_cost += R_COST * ((Di / 40) + c_ij_sum)

    eTran = 0
    eEdfa = 0
    for m in nodes:
        #print(m)
        for n in directLinkWith(m, g)[1]:
            #print(n)
            eTran += 73 * w_ij[n]
            tran_cost += T_COST * w_ij[n]
            eEdfa += 8 * ((int(n) / 80 - 1) + 2) * f_nm[n]
            edfa_cost += EDFA_COST * ((int(n) / 80 - 1) + 2) * f_nm[n]

    eTotal = eRouter + eTran + eEdfa

    # Printing the calculated total cost.
    #total_cost = rooter_cost + tran_cost + edfa_cost + calculate_laying_cost(links, links_location)
    #print("total cost IP-SB = " + str(total_cost))
    #print("For IP-SB")
    #print("eRouter = " + str(eRouter))
    #print("eTran = " + str(eTran))
    #print("eEdfa = " + str(eEdfa))
    return eTotal


#
def EAFFB(nodes, links, g, traffic, regions, lowerThresholdValue):
    count = 0
    total_cost = 0
    regions_list = []
    shortestPaths = []

    # Creating the paths, between all the nodes.
    for i in nodes:
        for j in nodes:
            if i != j:
                path = bfs(i, j, g)
                if not path:
                    return False, 0, 0, 0
                shortestPaths.append(path)

    xR, yR, n, tesssst = create_x_y_forEveryRegion(len(regions))

    # Creating the backup paths, for the links inside the regions that have over the lowerThresholdValue possibility.
    new_shortestPaths = []
    for i in range(len(regions)):
        # Calculating the values of, D, at and b.
        sum_x = 0
        sum_y = 0
        sum_xy = 0
        sum_x_pow_of_2 = 0
        for j in range(len(xR[i])):
            sum_x += xR[i][j]
            sum_y += yR[i][j]
            sum_xy += xR[i][j] * yR[i][j]
            sum_x_pow_of_2 += xR[i][j] * xR[i][j]

        N = len(xR[i])
        D = N * sum_x_pow_of_2 - (sum_x * sum_x)
        b = (N * sum_xy - sum_x * sum_y) / D
        at = (sum_x_pow_of_2 * sum_y - sum_x * sum_xy) / D

        # Calculating the values of, a, tmx and pt.
        a = at - math.log(t_study, 10)
        tmx = math.pow(10, -b * Mx) / math.pow(10, a)
        pt = 1 - math.pow(math.e, -T / tmx)

        if pt >= lowerThresholdValue:
            regions_list.append(i+1)
            count += 1
            for link in regions[i]:
                if is_this_link_in_min_combination(link, links):
                    total_cost += COST_FOR_REPAIR

                for path in brokenPaths(findAllRequestsUsingThisLink(shortestPaths, link)):
                    new_path = bfs(path[0], path[1], new_g(regions[i], g))
                    if not new_path:
                        return False, 0, 0, 0

                    new_shortestPaths.append(new_path)

    print("proposed backup_paths_for_critical_regions size: " + str(len(new_shortestPaths)))

    shortestPaths += new_shortestPaths

    # Calculating the average hops.
    total_hops = 0
    for path in shortestPaths:
        total_hops += len(path[1])

    eTotal, num_rooters, num_tran, num_edfa = calculate_energy_consumption(traffic, shortestPaths, nodes)
    return eTotal, num_rooters, num_tran, num_edfa


def SZFB(nodes, links, g, traffic, seismicRegions):
    shortestPaths = []
    # Creating the paths, between all the nodes.
    for i in nodes:
        for j in nodes:
            if i != j:
                shortestPaths.append(bfs(i, j, g))

    # Creating the backup paths, for the links inside the seismic regions.
    new_shortestPaths = []
    for seismicRegion in seismicRegions:
        for link in seismicRegion:
            for path in brokenPaths(findAllRequestsUsingThisLink(shortestPaths, link)):
                new_shortestPaths.append(bfs(path[0], path[1], new_g(seismicRegion, g)))

    shortestPaths += new_shortestPaths

    eTotal = calculate_energy_consumption(traffic, shortestPaths, nodes)
    return eTotal


# just for test.
def npa_nea(nodes, links, g, traffic, regions):
    return SZFB(nodes, links, g, traffic, regions)


def proposedAlgorithm(nodes, links, g, traffic, regions, lowerThresholdValue):
    critical_links = []
    critical_links_dict = {}
    for region in return_critical_regions(regions, lowerThresholdValue):
        critical_links += region
        for link in region:
            critical_links_dict[link] = 1

    critical_links = list(critical_links_dict.keys())

    new_critical_links = []
    for link in critical_links:
        result_1, dummy_num_rooters, dummy_num_tran, dummy_num_edfa = EAFFB(nodes, new_links([link], links), new_g([link], g), traffic, regions, lowerThresholdValue)
        if result_1 > 0:
            new_critical_links.append(link)

    critical_links = new_critical_links

    combinations = []
    for i in range(int(len(critical_links)), 0, -1):
        oc = itertools.combinations(critical_links, i)
        for c in oc:
            combinations.append(list(c))

    powers = []
    powers_dict = {}
    for combination in combinations:
        result, dummy_num_rooters, dummy_num_tran, dummy_num_edfa = EAFFB(nodes, new_links(combination, links), new_g(combination, g), traffic, regions, lowerThresholdValue)
        if result > 0:
            powers.append(result)
            powers_dict[result] = combination

    powers.sort()
    print("////////////////////////")
    result, num_rooters, num_tran, num_edfa = EAFFB(nodes, new_links(powers_dict[powers[0]], links), new_g(powers_dict[powers[0]], g), traffic, regions, lowerThresholdValue)
    print("////////////////////////")
    original_power, original_num_rooters, original_num_tran, original_num_edfa = EAFFB(nodes, links, g, traffic, regions, lowerThresholdValue)
    return result, original_power, num_rooters, num_tran, num_edfa, original_num_rooters, original_num_tran, original_num_edfa

