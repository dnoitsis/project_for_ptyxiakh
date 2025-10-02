import math
import itertools
from functions_didaktoriko import bfs, create_Cij, create_Wij, create_fmn, directLinkWith, \
    create_x_y_forEveryRegion, new_g, findAllRequestsUsingThisLink, brokenPaths, sum2, sum1, \
    checksIfTheNetworkIsNotCutOff, isThisLinkCritical, new_links, calculate_laying_cost, \
    is_this_link_in_min_combination, checksIfTheNetworkIsNotCutOff_EAFFB, create_fmn2, create_Wij_Aij, create_Wmn, \
    create_Cij_new, create_Wmn_Lmn_new, calculate_energy_consumption, return_critical_regions, return_critical_links, findAllRequestsUsingThisNode

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


# use the new method of bfs to calculate the shortestPaths better than EAFFB
def EAFFB2(nodes, links, g, traffic, regions, lowerThresholdValue, original_shortest_paths):
    count = 0
    total_cost = 0
    regions_list = []
    shortestPaths = []

    for shortestPpath in original_shortest_paths:
        shortestPaths.append(shortestPpath)
    # shortestPaths = original_shortest_paths
    # # Creating the paths, between all the nodes.
    # for i in nodes:
    #     for j in nodes:
    #         if i != j:
    #             path = bfs_avoid_critical(i, j, g, return_critical_links(regions,lowerThresholdValue))
    #             if not path:
    #                 return False, 0, 0, 0
    #             shortestPaths.append(path)

    # print("EAFFB2 shortestPaths done")
    # print("shortestPaths " + str(shortestPaths))
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

    shortestPaths += new_shortestPaths

    # Calculating the average hops.
    total_hops = 0
    for path in shortestPaths:
        total_hops += len(path[1])

    eTotal, num_rooters, num_tran, num_edfa = calculate_energy_consumption(traffic, shortestPaths, nodes)
    return eTotal, num_rooters, num_tran, num_edfa


def EAFFB2_with_critical_nodes(nodes, links, g, traffic, regions, lowerThresholdValue, original_shortest_paths, critical_nodes):
    count = 0
    total_cost = 0
    regions_list = []
    shortestPaths = []

    for shortestPpath in original_shortest_paths:
        shortestPaths.append(shortestPpath)

    print("EAFFB2 shortestPaths done")
    print("shortestPaths " + str(shortestPaths))
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

    shortestPaths += new_shortestPaths

    # calculating new paths for node disasters.
    new_shortestPaths_for_critical_nodes = []
    for node in critical_nodes:
        for path in brokenPaths(findAllRequestsUsingThisNode(shortestPaths, node)):
            new_path = bfs(path[0], path[1], new_g(regions[i], g))
            if not new_path:
                return False, 0, 0, 0

            new_shortestPaths_for_critical_nodes.append(new_path)

    shortestPaths += new_shortestPaths_for_critical_nodes

    # calculating new paths for fire disasters.
    new_shortestPaths_critical_regions_fire = []
    for region in critical_regions_fire:
        for link in regions[region]:
            for path in brokenPaths(findAllRequestsUsingThisLink(shortestPaths, link)):
                new_path = bfs(path[0], path[1], new_g(regions[i], g))
                if not new_path:
                    return False, 0, 0, 0

                new_shortestPaths_critical_regions_fire.append(new_path)

    shortestPaths += new_shortestPaths_critical_regions_fire

    # calculating new paths for flood disasters.
    new_shortestPaths_critical_regions_flood = []
    for region in critical_regions_flood:
        for link in regions[region]:
            for path in brokenPaths(findAllRequestsUsingThisLink(shortestPaths, link)):
                new_path = bfs(path[0], path[1], new_g(regions[i], g))
                if not new_path:
                    return False, 0, 0, 0

                new_shortestPaths_critical_regions_flood.append(new_path)

    shortestPaths += new_shortestPaths_critical_regions_flood

    # Calculating the average hops.
    total_hops = 0
    for path in shortestPaths:
        total_hops += len(path[1])

    eTotal, num_rooters, num_tran, num_edfa = calculate_energy_consumption(traffic, shortestPaths, nodes)
    return eTotal, num_rooters, num_tran, num_edfa


