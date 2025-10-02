from functions_didaktoriko import createTrafficMatrix, return_critical_nodes, return_critical_regions, \
    createTrafficMatrix2, return_critical_links, bfs, perCalc, bfs_avoid_critical_links, \
    bfs_avoid_critical_links_and_nodes, calc_new_traffic
from algorithms import EAFFB, proposedAlgorithm
from algorithms_didaktoriko import EAFFB2, EAFFB2_with_critical_nodes, \
    EAFFB2_with_critical_nodes_and_fire_and_flood_disasters, EAFFB_with_critical_nodes

links_location = {
    "236": "plain",
    "147": "plain",
    "73": "plain",
    "51": "plain",
    "62": "plain",
    "153": "sea",
    "157": "sea",
    "0111": "sea",
    "160": "sea",
    "130": "sea",
    "182": "sea",
    "270": "sea",
    "341": "sea",
    "251": "sea",
    "60": "plain",
    "45": "plain",
    "279": "sea",
    "70": "plain",
    "69": "plain",
    "63": "plain",
    "125": "plain",
    "54": "plain",
    "111": "plain",
    "31": "sea",
    "110": "plain",
    "57": "plain",
    "109": "plain",
    "99": "plain",
    "00105": "sea",
    "00134": "plain",
    "00237": "sea",
    "00143": "plain",
    "00229": "sea",
    "00212": "sea"
}

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
                ['153'], [], ['153'], ['157'], ['0111'], ['160'], ['182'], ['160', '182', '251'], ['130'],
                ['279'], ['279'], ['251'], ['341'], ['270'], ['111']]

nodes = ['ATH', 'LAR', 'THE', 'SER', 'DRA', 'XAN', 'LIM', 'MIT', 'CHI', 'SYR', 'SAM', 'RHO', 'HER', 'RET', 'CHA',
         'KOZ', 'IOA', 'LOU', 'MES', 'PAT', 'LEH', 'KAL', 'TRI', 'COR']

nodes_pop = [['ATH', 4324695], ['LAR', 688255], ['THE', 1644545], ['SER', 151124], ['DRA', 215942], ['XAN', 345924], ['LIM', 17262], ['MIT', 83755], ['CHI', 52590], ['SYR', 112615], ['SAM', 42423], ['RHO', 190071], ['HER', 382836], ['RET', 84866], ['CHA', 156706],
         ['KOZ', 254595], ['IOA', 305971], ['LOU', 224912], ['MES', 192345], ['PAT', 305979], ['LEH', 150408], ['KAL', 161288], ['TRI', 162020], ['COR', 231360]]

critical_regions_fire = [19]
critical_regions_flood = [14]

# crating the traffic matrix.
traffic, total_traffic = createTrafficMatrix(nodes, 20*6)
traffic2, total_traffic2 = createTrafficMatrix2(nodes_pop, scale=0.1, noise=True, self_traffic_factor=1)

# you can change the lower threshold value here.
lowerThresholdValue = 0.3

# you can change the times that you want to run the simulation here.
test_times = 1

sum_pop = 0
for node_pop in nodes_pop:
    sum_pop += node_pop[1]

# print("sum_pop = " + str(sum_pop))

# return_critical_regions(regionLinks,lowerThresholdValue)

critical_nodes = return_critical_nodes(nodes,lowerThresholdValue)

critical_links = return_critical_links(regionLinks,lowerThresholdValue)

# print("critical_links" + str(critical_links))
#
# print("critical_nodes" + str(critical_nodes))

# print("traffic" + str(traffic))
# print("total_traffic " + str(total_traffic))
# print("traffic2" + str(traffic2))
# print("total_traffic2 " + str(total_traffic2))

target_total = total_traffic
current_total = total_traffic2
factor = target_total / current_total

for k in traffic:
    traffic2[k] = int(traffic2[k] * factor)

# New total
new_total = sum(traffic2.values())
# print("new_traffic" +str(traffic2))
# print("new_total_traffic" +str(new_total))


shortestPaths = []

# Creating the paths, between all the nodes.
for i in nodes:
    for j in nodes:
        if i != j:
            path = bfs(i, j, g)
            if not path:
                print("not path")
            shortestPaths.append(path)

# print("shortestPaths" + str(shortestPaths))

shortestPaths_avoid_critical = []

# Creating the paths, between all the nodes.
for i in nodes:
    for j in nodes:
        if i != j:
            path = bfs_avoid_critical_links(i, j, g, critical_links)
            # path = bfs_avoid_critical(i, j, g, return_critical_links(regionLinks, 0.3))
            if not path:
                print("not path")
            shortestPaths_avoid_critical.append(path)

# print("shortestPaths_avoid_critical" + str(shortestPaths_avoid_critical))

original_shortest_paths = shortestPaths_avoid_critical


shortestPaths_avoid_critical_links_and_nodes = []

# Creating the paths, between all the nodes.
for i in nodes:
    for j in nodes:
        if i != j:
            path = bfs_avoid_critical_links_and_nodes(i, j, g, critical_links, critical_nodes)
            # path = bfs_avoid_critical(i, j, g, return_critical_links(regionLinks, 0.3))
            if not path:
                print("not path")
            shortestPaths_avoid_critical_links_and_nodes.append(path)

# print("shortestPaths_avoid_critical" + str(shortestPaths_avoid_critical))

original_shortest_paths_avoid_critical_links_and_nodes = shortestPaths_avoid_critical_links_and_nodes


for i in range(1, 7):
    print("For avg traffic = " + str(20 * i))
    sum_of_test_IP_SB = 0
    sum_of_SZFB = 0
    sum_of_SZFB2 = 0
    sum_of_IP_SB = 0
    sum_of_EAFFB_30 = 0
    sum_of_EAFFB_40 = 0
    sum_of_EAFFB_50 = 0
    sum_of_EAFFB2_30 = 0
    sum_of_EAFFB2_40 = 0
    sum_of_EAFFB2_50 = 0

    sum_of_EAFFB3_with_critical_nodes_30 = 0
    sum_of_EAFFB3_with_critical_nodes_30_traffic3 = 0

    sum_of_EAFFB2_with_critical_nodes_30 = 0
    sum_of_EAFFB_with_critical_nodes_30 = 0

    sum_of_EAFFB_30_traffic3 = 0
    sum_of_EAFFB2_30_traffic3 = 0
    sum_of_proposed_alg_traffic3 = 0
    sum_of_EAFFB2_with_critical_nodes_30_traffic3 = 0
    sum_of_EAFFB_with_critical_nodes_30_traffic3 = 0

    # _traffic2

    sum_of_proposed_alg = 0

    sum_of_EAFFB2_with_critical_nodes_and_fire_and_flood_disasters = 0

    for j in range(test_times):
        traffic, total_traffic = createTrafficMatrix(nodes, 20*i)
        traffic3, total_traffic3 = createTrafficMatrix2(nodes_pop, scale=20*i, noise=True, self_traffic_factor=1)

        traffic3 = calc_new_traffic(total_traffic, total_traffic3, traffic3)
        # print("new_traffic" + str(traffic3))
        print("new_total_traffic" + str(sum(traffic3.values())))

        # EAFFB
        eaffb_result, dummy_num_rooters, dummy_num_tran, dummy_num_edfa = EAFFB(nodes, links, g, traffic, regionLinks, lowerThresholdValue)
        sum_of_EAFFB_30 += eaffb_result

        # EAFFB2 (NEW PATH CALCULATION SCHEME AT THE START)
        eaffb2_result, dummy_num_rooters, dummy_num_tran, dummy_num_edfa = EAFFB2(nodes, links, g, traffic, regionLinks, lowerThresholdValue, original_shortest_paths)
        sum_of_EAFFB2_30 += eaffb2_result

        # proposedAlgorithm (ON PTYXIAKI)
        proposedAlgorithm_result, original_power, num_rooters, num_tran, num_edfa, original_num_rooters, original_num_tran, original_num_edfa = proposedAlgorithm(nodes, links, g, traffic, regionLinks, lowerThresholdValue)
        sum_of_proposed_alg +=proposedAlgorithm_result

        # EAFFB2 with critical nodes logic
        eaffb2_with_critical_nodes_result, dummy_num_rooters, dummy_num_tran, dummy_num_edfa = EAFFB2_with_critical_nodes(nodes, links, g, traffic, regionLinks, lowerThresholdValue, original_shortest_paths, critical_nodes)
        sum_of_EAFFB2_with_critical_nodes_30 += eaffb2_with_critical_nodes_result

        # EAFFB with critical nodes logic
        eaffb_with_critical_nodes_result, dummy_num_rooters, dummy_num_tran, dummy_num_edfa = EAFFB_with_critical_nodes(nodes, links, g, traffic, regionLinks, lowerThresholdValue, critical_nodes)
        sum_of_EAFFB_with_critical_nodes_30 += eaffb_with_critical_nodes_result

        # EAFFB with traffic3
        eaffb_traffic3_result, dummy_num_rooters, dummy_num_tran, dummy_num_edfa = EAFFB(nodes, links, g, traffic3, regionLinks, lowerThresholdValue)
        sum_of_EAFFB_30_traffic3 += eaffb_traffic3_result

        eaffb2_traffic3_result, dummy_num_rooters, dummy_num_tran, dummy_num_edfa = EAFFB2(nodes, links, g, traffic3, regionLinks, lowerThresholdValue, original_shortest_paths)
        sum_of_EAFFB2_30_traffic3 += eaffb2_traffic3_result

        proposedAlgorithm_traffic3_result, original_power, num_rooters, num_tran, num_edfa, original_num_rooters, original_num_tran, original_num_edfa = proposedAlgorithm(nodes, links, g, traffic3, regionLinks, lowerThresholdValue)
        sum_of_proposed_alg_traffic3 += proposedAlgorithm_traffic3_result

        eaffb2_with_critical_nodes_traffic3_result, dummy_num_rooters, dummy_num_tran, dummy_num_edfa = EAFFB2_with_critical_nodes(nodes, links, g, traffic3, regionLinks, lowerThresholdValue, original_shortest_paths, critical_nodes)
        sum_of_EAFFB2_with_critical_nodes_30_traffic3 += eaffb2_with_critical_nodes_traffic3_result

        eaffb_with_critical_nodes_traffic3_result, dummy_num_rooters, dummy_num_tran, dummy_num_edfa = EAFFB_with_critical_nodes(nodes, links, g, traffic3, regionLinks, lowerThresholdValue, critical_nodes)
        sum_of_EAFFB_with_critical_nodes_30_traffic3 += eaffb_with_critical_nodes_traffic3_result



        eaffb3_with_critical_nodes_result, dummy_num_rooters, dummy_num_tran, dummy_num_edfa = EAFFB2_with_critical_nodes(nodes, links, g, traffic, regionLinks, lowerThresholdValue, original_shortest_paths_avoid_critical_links_and_nodes, critical_nodes)
        sum_of_EAFFB3_with_critical_nodes_30 += eaffb3_with_critical_nodes_result

        eaffb3_with_critical_nodes_traffic3_result, dummy_num_rooters, dummy_num_tran, dummy_num_edfa = EAFFB2_with_critical_nodes(nodes, links, g, traffic3, regionLinks, lowerThresholdValue, original_shortest_paths_avoid_critical_links_and_nodes, critical_nodes)
        sum_of_EAFFB3_with_critical_nodes_30_traffic3 += eaffb3_with_critical_nodes_traffic3_result

        EAFFB2_with_critical_nodes_and_fire_and_flood_disasters_result, dummy_num_rooters, dummy_num_tran, dummy_num_edfa = EAFFB2_with_critical_nodes_and_fire_and_flood_disasters(nodes, links, g, traffic3, regionLinks, lowerThresholdValue, original_shortest_paths_avoid_critical_links_and_nodes, critical_nodes, critical_regions_fire, critical_regions_flood)
        sum_of_EAFFB2_with_critical_nodes_and_fire_and_flood_disasters += EAFFB2_with_critical_nodes_and_fire_and_flood_disasters_result


    # print("EAFFB 30%: " + str(sum_of_EAFFB_30 / test_times))
    #
    # print("EAFFB2 30%: " + str(sum_of_EAFFB2_30 / test_times))
    #
    # print("proposed_alg: " + str(sum_of_proposed_alg / test_times))
    #
    # sum_of_original_power = sum_of_EAFFB_30
    # sum_of_result = sum_of_EAFFB2_30
    # per = (int(sum_of_original_power / test_times) - int(sum_of_result / test_times)) / int(sum_of_original_power / test_times)
    # print("didakt: NEW energy cost is lower " + str(int(per * 100)) + "%")
    #
    # sum_of_original_power = sum_of_EAFFB_30
    # sum_of_result = sum_of_proposed_alg
    # per2 = (int(sum_of_original_power / test_times) - int(sum_of_result / test_times)) / int(sum_of_original_power / test_times)
    # print("proposed_alg: NEW energy cost is lower " + str(int(per2 * 100)) + "%")
    #
    # sum_of_original_power = sum_of_proposed_alg
    # sum_of_result = sum_of_EAFFB2_30
    # per3 = (int(sum_of_original_power / test_times) - int(sum_of_result / test_times)) / int(sum_of_original_power / test_times)
    # print("NEW energy cost is lower " + str(float(per3 * 100)) + "%")
    #
    # # print("npa_nea: " + str(e4))
    # print("///////")
    #
    # print("EAFFB2_with_critical_nodes 30%: " + str(sum_of_EAFFB2_with_critical_nodes_30 / test_times))
    #
    # print("EAFFB_with_critical_nodes 30%: " + str(sum_of_EAFFB_with_critical_nodes_30 / test_times))
    #
    # print("///////")
    #
    # print("EAFFB_30_traffic3 30%: " + str(sum_of_EAFFB_30_traffic3 / test_times))
    #
    # print("EAFFB2_30_traffic3 30%: " + str(sum_of_EAFFB2_30_traffic3 / test_times))
    #
    # print("EAFFB2 vs EAFFB energy cost is lower " + str(perCalc(sum_of_EAFFB_30_traffic3, sum_of_EAFFB2_30_traffic3, test_times)) + "%")
    #
    # print("proposed_alg_traffic3 30%: " + str(sum_of_proposed_alg_traffic3 / test_times))
    #
    # print("proposed_alg vs EAFFB energy cost is lower " + str(perCalc(sum_of_EAFFB_30_traffic3, sum_of_proposed_alg_traffic3, test_times)) + "%")
    #
    # print("EAFFB2 vs proposed_alg energy cost is lower " + str(perCalc(sum_of_proposed_alg_traffic3, sum_of_EAFFB2_30_traffic3, test_times)) + "%")
    #
    # print("EAFFB2_with_critical_nodes_30_traffic3 30%: " + str(sum_of_EAFFB2_with_critical_nodes_30_traffic3 / test_times))
    #
    # print("EAFFB_with_critical_nodes_30_traffic3 30%: " + str(sum_of_EAFFB_with_critical_nodes_30_traffic3 / test_times))
    #
    # print("EAFFB2_with_critical_nodes vs EAFFB_with_critical_nodes energy cost is lower " + str(perCalc(sum_of_EAFFB_with_critical_nodes_30_traffic3, sum_of_EAFFB2_with_critical_nodes_30_traffic3, test_times)) + "%")
    #
    # print("///////")
    #
    # sum_of_EAFFB3_with_critical_nodes_30
    #
    # sum_of_EAFFB3_with_critical_nodes_30_traffic3
    #
    # print("EAFFB3_with_critical_nodes_30 30%: " + str(sum_of_EAFFB3_with_critical_nodes_30 / test_times))
    #
    # print("EAFFB3_with_critical_nodes_30_traffic3 30%: " + str(sum_of_EAFFB3_with_critical_nodes_30_traffic3 / test_times))
    #
    # print("///////")

    print("========== BASE COMPARISON ==========")
    print(f"EAFFB 30%: {sum_of_EAFFB_30 / test_times}")
    print(f"EAFFB2 30%: {sum_of_EAFFB2_30 / test_times}")
    print(f"Proposed algorithm: {sum_of_proposed_alg / test_times}")

    print(f"EAFFB2 vs EAFFB: {perCalc(sum_of_EAFFB_30, sum_of_EAFFB2_30, test_times)}% lower energy")
    print(f"Proposed vs EAFFB: {perCalc(sum_of_EAFFB_30, sum_of_proposed_alg, test_times)}% lower energy")
    print(f"EAFFB2 vs Proposed: {perCalc(sum_of_proposed_alg, sum_of_EAFFB2_30, test_times)}% lower energy")

    print("///////// CRITICAL NODES (no traffic3) /////////")
    print(f"EAFFB2_with_critical_nodes 30%: {sum_of_EAFFB2_with_critical_nodes_30 / test_times}")
    print(f"EAFFB_with_critical_nodes 30%: {sum_of_EAFFB_with_critical_nodes_30 / test_times}")

    print("///////// TRAFFIC3 /////////")
    print(f"EAFFB_30_traffic3: {sum_of_EAFFB_30_traffic3 / test_times}")
    print(f"EAFFB2_30_traffic3: {sum_of_EAFFB2_30_traffic3 / test_times}")
    print(f"Proposed_alg_traffic3: {sum_of_proposed_alg_traffic3 / test_times}")

    print(
        f"EAFFB2 vs EAFFB (traffic3): {perCalc(sum_of_EAFFB_30_traffic3, sum_of_EAFFB2_30_traffic3, test_times)}% lower energy")
    print(
        f"Proposed vs EAFFB (traffic3): {perCalc(sum_of_EAFFB_30_traffic3, sum_of_proposed_alg_traffic3, test_times)}% lower energy")
    print(
        f"EAFFB2 vs Proposed (traffic3): {perCalc(sum_of_proposed_alg_traffic3, sum_of_EAFFB2_30_traffic3, test_times)}% lower energy")

    print("///////// CRITICAL NODES + TRAFFIC3 /////////")
    print(f"EAFFB2_with_critical_nodes_30_traffic3: {sum_of_EAFFB2_with_critical_nodes_30_traffic3 / test_times}")
    print(f"EAFFB_with_critical_nodes_30_traffic3: {sum_of_EAFFB_with_critical_nodes_30_traffic3 / test_times}")
    print(f"EAFFB2 vs EAFFB (with critical nodes, traffic3): {perCalc(sum_of_EAFFB_with_critical_nodes_30_traffic3, sum_of_EAFFB2_with_critical_nodes_30_traffic3, test_times)}% lower energy")

    print("///////// EAFFB3 /////////")
    print(f"EAFFB3_with_critical_nodes_30: {sum_of_EAFFB3_with_critical_nodes_30 / test_times}")
    print(f"EAFFB3_with_critical_nodes_30_traffic3: {sum_of_EAFFB3_with_critical_nodes_30_traffic3 / test_times}")
    print("============================================")

    print("///////// EAFFB2_with_critical_nodes_and_fire_and_flood_disasters /////////")
    print(f"EAFFB2_with_critical_nodes_and_fire_and_flood_disasters: {sum_of_EAFFB2_with_critical_nodes_and_fire_and_flood_disasters / test_times}")
    print("============================================")























    # sum_of_EAFFB_30_traffic3 = 0
    # sum_of_EAFFB2_30_traffic3 = 0
    # sum_of_proposed_alg_traffic3 = 0
    # sum_of_EAFFB2_with_critical_nodes_30_traffic3 = 0
    # sum_of_EAFFB_with_critical_nodes_30_traffic3 = 0
# for i in range(1, 7):
#     print("For avg traffic = " + str(20 * i))
#     sum_of_result = 0
#     sum_of_original_power = 0
#     sum_of_no_seismic_zones_eaffb = 0
#     sum_of_num_rooters = 0
#     sum_of_num_tran = 0
#     sum_of_num_edfa = 0
#     sum_of_original_num_rooters = 0
#     sum_of_original_num_tran = 0
#     sum_of_original_num_edfa = 0
#     for j in range(test_times):
#         traffic = createTrafficMatrix(nodes, 20*i)
#         result, original_power, num_rooters, num_tran, num_edfa, original_num_rooters, original_num_tran, original_num_edfa = proposedAlgorithm(nodes, links, g, traffic, regionLinks, lowerThresholdValue)
#         no_seismic_zones_eaffb, dummy_num_rooters, dummy_num_tran, dummy_num_edfa = EAFFB(nodes, links, g, traffic, regionLinks, 0.9)
#         sum_of_result += result/1000
#         sum_of_original_power += original_power/1000
#         sum_of_no_seismic_zones_eaffb += no_seismic_zones_eaffb/1000
#         sum_of_num_rooters += num_rooters
#         sum_of_num_tran += num_tran
#         sum_of_num_edfa += num_edfa
#         sum_of_original_num_rooters += original_num_rooters
#         sum_of_original_num_tran += original_num_tran
#         sum_of_original_num_edfa += original_num_edfa
#
#     print("no_seismic_zones EAFFB " + str(int(lowerThresholdValue*100)) + "%: " + str(sum_of_no_seismic_zones_eaffb / test_times))
#     print("new EAFFB " + str(int(lowerThresholdValue*100)) + "%: " + str(sum_of_result / test_times))
#     print("original EAFFB " + str(int(lowerThresholdValue*100)) + "%: " + str(sum_of_original_power / test_times))
#
#     per2 = (int(sum_of_original_power / test_times) - int(sum_of_no_seismic_zones_eaffb / test_times)) / int(
#         sum_of_original_power / test_times)
#     print("EAFFB energy cost from backup paths " + str(int(per2 * 100)) + "%")
#
#     per = (int(sum_of_original_power / test_times)-int(sum_of_result / test_times)) / int(sum_of_original_power / test_times)
#     print("NEW energy cost is lower " + str(int(per * 100)) + "%")
#
#     print("NEW num_rooters " + str(int(sum_of_num_rooters / test_times)))
#     print("NEW num_tran " + str(int(sum_of_num_tran / test_times)))
#     print("NEW num_edfa " + str(int(sum_of_num_edfa / test_times)))
#     print("OLD num_rooters " + str(int(sum_of_original_num_rooters / test_times)))
#     print("OLD num_tran " + str(int(sum_of_original_num_tran / test_times)))
#     print("OLD num_edfa " + str(int(sum_of_original_num_edfa / test_times)))
#
#
#     print("///////")


