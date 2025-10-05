import math
import itertools
from functions_didaktoriko import bfs, create_Cij, create_Wij, create_fmn, directLinkWith, \
    create_x_y_forEveryRegion, new_g, findAllRequestsUsingThisLink, brokenPaths, sum2, sum1, \
    checksIfTheNetworkIsNotCutOff, isThisLinkCritical, new_links, calculate_laying_cost, \
    is_this_link_in_min_combination, checksIfTheNetworkIsNotCutOff_EAFFB, create_fmn2, create_Wij_Aij, create_Wmn, \
    create_Cij_new, create_Wmn_Lmn_new, calculate_energy_consumption, return_critical_regions, return_critical_links, \
    findAllRequestsUsingThisNode, calculate_repair_cost, calculate_repair_cost_for_nodes

Mx = 5
My = 4
T = 5
t_study = 58


#
# R_COST = 90000
# T_COST = 25000
# EDFA_COST = 1500
# COST_FOR_REPAIR = 50000


# use the new method of bfs to calculate the shortestPaths better than EAFFB.
def EAFFB2(nodes, g, traffic, critical_regions, original_shortest_paths):
    shortestPaths = []

    backup_links = []
    links_that_need_repair = []

    # import the initial shortestPaths
    for shortestPath in original_shortest_paths:
        shortestPaths.append(shortestPath)


    # Creating the backup paths, for the links inside the regions that have over the lowerThresholdValue possibility.
    backup_paths_for_critical_regions = []
    for critical_region in critical_regions:
        for link in critical_region:
            links_that_need_repair.append(link)

            for path in brokenPaths(findAllRequestsUsingThisLink(shortestPaths, link)):
                new_path = bfs(path[0], path[1], new_g(critical_region, g))
                if not new_path:
                    return False, 0, 0, 0

                backup_paths_for_critical_regions.append(new_path)

                for link in new_path[1]:
                    backup_links.append(link)

    print("eaffb2 backup_paths_for_critical_regions size: " + str(len(backup_paths_for_critical_regions)))

    shortestPaths += backup_paths_for_critical_regions

    # Calculating the average hops.
    # total_hops = 0
    # for path in shortestPaths:
    #     total_hops += len(path[1])

    eTotal, num_rooters, num_tran, num_edfa = calculate_energy_consumption(traffic, shortestPaths, nodes)
    laying_cost = calculate_laying_cost(backup_links)
    repair_cost, repair_hours = calculate_repair_cost(links_that_need_repair)

    return eTotal, laying_cost, repair_cost, repair_hours


def EAFFB2_with_critical_nodes(nodes, g, traffic, critical_regions, original_shortest_paths, critical_nodes):

    # Vars for calculating laying and repair cost.
    backup_links = []
    links_that_need_repair = []
    nodes_need_repair = 0

    # import the initial shortestPaths
    shortestPaths = []
    for shortestPath in original_shortest_paths:
        shortestPaths.append(shortestPath)

    # Creating the backup paths, for the links inside the regions that have over the lowerThresholdValue possibility.
    backup_paths_for_critical_regions = []
    for critical_region in critical_regions:
        for link in critical_region:
            links_that_need_repair.append(link)

            for path in brokenPaths(findAllRequestsUsingThisLink(shortestPaths, link)):
                new_path = bfs(path[0], path[1], new_g(critical_region, g))
                if not new_path:
                    return False, 0, 0, 0

                backup_paths_for_critical_regions.append(new_path)

                for link in new_path[1]:
                    backup_links.append(link)

    shortestPaths += backup_paths_for_critical_regions

    new_shortestPaths_for_critical_nodes = []
    for node in critical_nodes:
        nodes_need_repair += 1
        for path in brokenPaths(findAllRequestsUsingThisNode(shortestPaths, node)):
            new_path = bfs(path[0], path[1], new_g(directLinkWith(node, g)[1], g))
            if not new_path:
                return False, 0, 0, 0

            new_shortestPaths_for_critical_nodes.append(new_path)

            for link in new_path[1]:
                backup_links.append(link)

    shortestPaths += new_shortestPaths_for_critical_nodes

    # Calculating the average hops.
    total_hops = 0
    for path in shortestPaths:
        total_hops += len(path[1])

    eTotal, num_rooters, num_tran, num_edfa = calculate_energy_consumption(traffic, shortestPaths, nodes)
    laying_cost = calculate_laying_cost(backup_links)

    repair_cost, repair_hours = calculate_repair_cost(links_that_need_repair)

    # print("laying_cost for backup paths= " + str(laying_cost))
    #
    # print("repair_cost for damaged links= " + str(repair_cost))
    # print("repair_hours for damaged links= " + str(repair_hours))

    nodes_repair_cost, nodes_repair_hours = calculate_repair_cost_for_nodes(nodes_need_repair)

    # print("nodes_repair_cost for damaged nodes= " + str(nodes_repair_cost))

    return eTotal, laying_cost, repair_cost + nodes_repair_cost, repair_hours + nodes_repair_hours


# original EAFFB algorithm with the addition of critical nodes logic.
def EAFFB_with_critical_nodes(nodes, g, traffic, critical_regions, original_shortest_paths, critical_nodes):

    backup_links = []
    links_that_need_repair = []

    nodes_need_repair = 0

    # # Creating the paths, between all the nodes.
    shortestPaths = []
    for shortestPath in original_shortest_paths:
        shortestPaths.append(shortestPath)



    # Creating the backup paths, for the links inside the regions that have over the lowerThresholdValue possibility.
    backup_paths_for_critical_regions = []
    for critical_region in critical_regions:
        for link in critical_region:
            links_that_need_repair.append(link)

            for path in brokenPaths(findAllRequestsUsingThisLink(shortestPaths, link)):
                new_path = bfs(path[0], path[1], new_g(critical_region, g))
                if not new_path:
                    return False, 0, 0, 0

                backup_paths_for_critical_regions.append(new_path)

                for link in new_path[1]:
                    backup_links.append(link)

    shortestPaths += backup_paths_for_critical_regions

    new_shortestPaths_for_critical_nodes = []
    for node in critical_nodes:
        nodes_need_repair += 1
        for path in brokenPaths(findAllRequestsUsingThisNode(shortestPaths, node)):
            new_path = bfs(path[0], path[1], new_g(directLinkWith(node, g)[1], g))
            if not new_path:
                return False, 0, 0, 0

            new_shortestPaths_for_critical_nodes.append(new_path)

            for link in new_path[1]:
                backup_links.append(link)

    shortestPaths += new_shortestPaths_for_critical_nodes

    # Calculating the average hops.
    # total_hops = 0
    # for path in shortestPaths:
    #     total_hops += len(path[1])

    eTotal, num_rooters, num_tran, num_edfa = calculate_energy_consumption(traffic, shortestPaths, nodes)

    laying_cost = calculate_laying_cost(backup_links)

    repair_cost, repair_hours = calculate_repair_cost(links_that_need_repair)

    # print("laying_cost for backup paths= " + str(laying_cost))
    #
    # print("repair_cost for damaged links= " + str(repair_cost))
    # print("repair_hours for damaged links= " + str(repair_hours))

    nodes_repair_cost, nodes_repair_hours = calculate_repair_cost_for_nodes(nodes_need_repair)

    # print("nodes_repair_cost for damaged nodes= " + str(nodes_repair_cost))

    return eTotal, laying_cost, repair_cost + nodes_repair_cost, repair_hours + nodes_repair_hours


def EAFFB_with_critical_nodes_and_fire_and_flood_disasters(nodes, g, traffic, critical_regions, original_shortest_paths, critical_nodes, critical_regions_fire, critical_regions_flood):

    backup_links = []
    links_that_need_repair = []

    nodes_need_repair = 0

    # import the initial shortestPaths
    shortestPaths = []
    for shortestPath in original_shortest_paths:
        shortestPaths.append(shortestPath)

    # Creating the backup paths, for the links inside the regions that have over the lowerThresholdValue possibility.
    backup_paths_for_critical_regions = []
    for critical_region in critical_regions:
        for link in critical_region:
            links_that_need_repair.append(link)

            for path in brokenPaths(findAllRequestsUsingThisLink(shortestPaths, link)):
                new_path = bfs(path[0], path[1], new_g(critical_region, g))
                if not new_path:
                    return False, 0, 0, 0

                backup_paths_for_critical_regions.append(new_path)

                for link in new_path[1]:
                    backup_links.append(link)

    shortestPaths += backup_paths_for_critical_regions

    # calculating new paths for node disasters.
    new_shortestPaths_for_critical_nodes = []
    for node in critical_nodes:
        nodes_need_repair += 1
        for path in brokenPaths(findAllRequestsUsingThisNode(shortestPaths, node)):
            new_path = bfs(path[0], path[1], new_g(directLinkWith(node, g)[1], g))
            if not new_path:
                return False, 0, 0, 0

            new_shortestPaths_for_critical_nodes.append(new_path)

            for link in new_path[1]:
                backup_links.append(link)

    shortestPaths += new_shortestPaths_for_critical_nodes

    # calculating new paths for fire disasters.
    new_shortestPaths_critical_regions_fire = []
    for region in critical_regions_fire:
        for link in region:
            for path in brokenPaths(findAllRequestsUsingThisLink(shortestPaths, link)):
                new_path = bfs(path[0], path[1], new_g(region, g))
                if not new_path:
                    return False, 0, 0, 0

                new_shortestPaths_critical_regions_fire.append(new_path)

                for link in new_path[1]:
                    backup_links.append(link)

    shortestPaths += new_shortestPaths_critical_regions_fire

    # calculating new paths for flood disasters.
    new_shortestPaths_critical_regions_flood = []
    for region in critical_regions_flood:
        for link in region:
            for path in brokenPaths(findAllRequestsUsingThisLink(shortestPaths, link)):
                new_path = bfs(path[0], path[1], new_g(region, g))
                if not new_path:
                    return False, 0, 0, 0

                new_shortestPaths_critical_regions_flood.append(new_path)

                for link in new_path[1]:
                    backup_links.append(link)

    shortestPaths += new_shortestPaths_critical_regions_flood

    # Calculating the average hops.
    # total_hops = 0
    # for path in shortestPaths:
    #     total_hops += len(path[1])

    eTotal, num_rooters, num_tran, num_edfa = calculate_energy_consumption(traffic, shortestPaths, nodes)

    laying_cost = calculate_laying_cost(backup_links)

    repair_cost, repair_hours = calculate_repair_cost(links_that_need_repair)

    # print("laying_cost for backup paths= " + str(laying_cost))
    #
    # print("repair_cost for damaged links= " + str(repair_cost))
    # print("repair_hours for damaged links= " + str(repair_hours))

    nodes_repair_cost, nodes_repair_hours = calculate_repair_cost_for_nodes(nodes_need_repair)

    # print("nodes_repair_cost for damaged nodes= " + str(nodes_repair_cost))

    return eTotal, laying_cost, repair_cost + nodes_repair_cost, repair_hours + nodes_repair_hours


#
def EAFFB2_with_critical_nodes_and_fire_and_flood_disasters(nodes, g, traffic, critical_regions, original_shortest_paths, critical_nodes, critical_regions_fire, critical_regions_flood):

    backup_links = []
    links_that_need_repair = []

    nodes_need_repair = 0

    # import the initial shortestPaths
    shortestPaths = []
    for shortestPath in original_shortest_paths:
        shortestPaths.append(shortestPath)

    # Creating the backup paths, for the links inside the regions that have over the lowerThresholdValue possibility.
    backup_paths_for_critical_regions = []
    for critical_region in critical_regions:
        for link in critical_region:
            links_that_need_repair.append(link)

            for path in brokenPaths(findAllRequestsUsingThisLink(shortestPaths, link)):
                new_path = bfs(path[0], path[1], new_g(critical_region, g))
                if not new_path:
                    return False, 0, 0, 0

                backup_paths_for_critical_regions.append(new_path)

                for link in new_path[1]:
                    backup_links.append(link)

    shortestPaths += backup_paths_for_critical_regions

    # calculating new paths for node disasters.
    new_shortestPaths_for_critical_nodes = []
    for node in critical_nodes:
        nodes_need_repair += 1
        for path in brokenPaths(findAllRequestsUsingThisNode(shortestPaths, node)):
            new_path = bfs(path[0], path[1], new_g(directLinkWith(node, g)[1], g))
            if not new_path:
                return False, 0, 0, 0

            new_shortestPaths_for_critical_nodes.append(new_path)

            for link in new_path[1]:
                backup_links.append(link)

    shortestPaths += new_shortestPaths_for_critical_nodes

    # calculating new paths for fire disasters.
    new_shortestPaths_critical_regions_fire = []
    for region in critical_regions_fire:
        for link in region:
            for path in brokenPaths(findAllRequestsUsingThisLink(shortestPaths, link)):
                new_path = bfs(path[0], path[1], new_g(directLinkWith(node, g)[1], g))
                if not new_path:
                    return False, 0, 0, 0

                new_shortestPaths_critical_regions_fire.append(new_path)

                for link in new_path[1]:
                    backup_links.append(link)

    shortestPaths += new_shortestPaths_critical_regions_fire

    # calculating new paths for flood disasters.
    new_shortestPaths_critical_regions_flood = []
    for region in critical_regions_flood:
        for link in region:
            for path in brokenPaths(findAllRequestsUsingThisLink(shortestPaths, link)):
                new_path = bfs(path[0], path[1], new_g(directLinkWith(node, g)[1], g))
                if not new_path:
                    return False, 0, 0, 0

                new_shortestPaths_critical_regions_flood.append(new_path)

                for link in new_path[1]:
                    backup_links.append(link)

    shortestPaths += new_shortestPaths_critical_regions_flood

    # Calculating the average hops.
    # total_hops = 0
    # for path in shortestPaths:
    #     total_hops += len(path[1])

    eTotal, num_rooters, num_tran, num_edfa = calculate_energy_consumption(traffic, shortestPaths, nodes)

    laying_cost = calculate_laying_cost(backup_links)

    repair_cost, repair_hours = calculate_repair_cost(links_that_need_repair)

    # print("laying_cost for backup paths= " + str(laying_cost))
    #
    # print("repair_cost for damaged links= " + str(repair_cost))
    # print("repair_hours for damaged links= " + str(repair_hours))

    nodes_repair_cost, nodes_repair_hours = calculate_repair_cost_for_nodes(nodes_need_repair)

    # print("nodes_repair_cost for damaged nodes= " + str(nodes_repair_cost))

    return eTotal, laying_cost, repair_cost + nodes_repair_cost, repair_hours + nodes_repair_hours


