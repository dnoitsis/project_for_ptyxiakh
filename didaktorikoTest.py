from functions_didaktoriko import createTrafficMatrix, return_critical_nodes, return_critical_regions, \
    createTrafficMatrix2, return_critical_links, bfs, perCalc, bfs_avoid_critical_links, \
    bfs_avoid_critical_links_and_nodes, calc_new_traffic, directLinkWith, createRealisticTrafficMatrix
from algorithms import EAFFB, proposedAlgorithm
from algorithms_didaktoriko import EAFFB2, EAFFB2_with_critical_nodes, \
    EAFFB2_with_critical_nodes_and_fire_and_flood_disasters, EAFFB_with_critical_nodes, \
    EAFFB_with_critical_nodes_and_fire_and_flood_disasters

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

critical_regions_fire = [['73']]
critical_regions_flood = [['236']]



# for test code here

# print(str(directLinkWith('ATH', g)[1]))


#

# you can change the lower threshold value here.
lowerThresholdValue = 0.2

# you can change the times that you want to run the simulation here.
test_times = 10

# calculating all the critical nodes.
critical_nodes = return_critical_nodes(nodes, lowerThresholdValue)

# calculating all the critical links.
critical_links = return_critical_links(regionLinks, lowerThresholdValue)

# calculating critical regions.
critical_regions = return_critical_regions(regionLinks, lowerThresholdValue)
print("return_critical_regions: " + str(critical_regions))

# Creating the paths, between all the nodes avoiding critical links.
original_shortest_paths = []
for i in nodes:
    for j in nodes:
        if i != j:
            path = bfs(i, j, g)
            if not path:
                print("not path")
            original_shortest_paths.append(path)

print("original_shortest_paths size: " + str(len(original_shortest_paths)))

# Creating the paths, between all the nodes avoiding critical links.
original_shortest_paths_avoid_critical_links = []
for i in nodes:
    for j in nodes:
        if i != j:
            path = bfs_avoid_critical_links(i, j, g, critical_links)
            if not path:
                print("not path")
            original_shortest_paths_avoid_critical_links.append(path)

print("original_shortest_paths_avoid_critical_links size: " + str(len(original_shortest_paths_avoid_critical_links)))

# Creating the paths, between all the nodes avoiding critical links and nodes.
original_shortest_paths_avoid_critical_links_and_nodes = []
for i in nodes:
    for j in nodes:
        if i != j:
            path = bfs_avoid_critical_links_and_nodes(i, j, g, critical_links, critical_nodes)
            if not path:
                print("not path")
            original_shortest_paths_avoid_critical_links_and_nodes.append(path)

print("original_shortest_paths_avoid_critical_links_and_nodes size: " + str(len(original_shortest_paths_avoid_critical_links_and_nodes)))

print("For lowerThresholdValue: " + str(lowerThresholdValue))
for i in range(1, 7):
    print("///  For avg traffic = " + str(20 * i))
    sum_of_EAFFB = 0    # original EAFFB
    sum_of_EAFFB_realistic_traffic = 0

    sum_of_EAFFB2 = 0   # EAFFB with new shortest path calculation scheme.
    sum_of_EAFFB2_laying_cost = 0
    sum_of_EAFFB2_repair_cost = 0
    sum_of_EAFFB2_repair_hours = 0
    sum_of_EAFFB2_realistic_traffic = 0
    sum_of_EAFFB2_realistic_traffic_laying_cost = 0
    sum_of_EAFFB2_realistic_traffic_repair_cost = 0
    sum_of_EAFFB2_realistic_traffic_repair_hours = 0


    sum_of_EAFFB_with_critical_nodes_and_fire_and_flood_disasters = 0
    sum_of_EAFFB_with_critical_nodes_and_fire_and_flood_disasters_laying_cost = 0
    sum_of_EAFFB_with_critical_nodes_and_fire_and_flood_disasters_repair_cost = 0
    sum_of_EAFFB_with_critical_nodes_and_fire_and_flood_disasters_repair_hours = 0
    sum_of_EAFFB_with_critical_nodes_and_fire_and_flood_disasters_realistic_traffic = 0
    sum_of_EAFFB_with_critical_nodes_and_fire_and_flood_disasters_realistic_traffic_laying_cost = 0
    sum_of_EAFFB_with_critical_nodes_and_fire_and_flood_disasters_realistic_traffic_repair_cost = 0
    sum_of_EAFFB_with_critical_nodes_and_fire_and_flood_disasters_realistic_traffic_repair_hours = 0


    sum_of_EAFFB2_with_critical_nodes = 0
    sum_of_EAFFB2_with_critical_nodes_laying_cost = 0
    sum_of_EAFFB2_with_critical_nodes_repair_cost = 0
    sum_of_EAFFB2_with_critical_nodes_repair_hours = 0
    sum_of_EAFFB2_with_critical_nodes_realistic_traffic = 0
    sum_of_EAFFB2_with_critical_nodes_realistic_traffic_laying_cost = 0
    sum_of_EAFFB2_with_critical_nodes_realistic_traffic_repair_cost = 0
    sum_of_EAFFB2_with_critical_nodes_realistic_traffic_repair_hours = 0


    sum_of_EAFFB_with_critical_nodes = 0
    sum_of_EAFFB_with_critical_nodes_laying_cost = 0
    sum_of_EAFFB_with_critical_nodes_repair_cost = 0
    sum_of_EAFFB_with_critical_nodes_repair_hours = 0
    sum_of_EAFFB_with_critical_nodes_realistic_traffic = 0
    sum_of_EAFFB_with_critical_nodes_realistic_traffic_laying_cost = 0
    sum_of_EAFFB_with_critical_nodes_realistic_traffic_repair_cost = 0
    sum_of_EAFFB_with_critical_nodes_realistic_traffic_repair_hours = 0


    sum_of_proposed_alg = 0
    sum_of_proposed_alg_realistic_traffic = 0


    sum_of_EAFFB2_with_critical_nodes_and_fire_and_flood_disasters = 0
    sum_of_EAFFB2_with_critical_nodes_and_fire_and_flood_disasters_laying_cost = 0
    sum_of_EAFFB2_with_critical_nodes_and_fire_and_flood_disasters_repair_cost = 0
    sum_of_EAFFB2_with_critical_nodes_and_fire_and_flood_disasters_repair_hours = 0
    sum_of_EAFFB2_with_critical_nodes_and_fire_and_flood_disasters_realistic_traffic = 0
    sum_of_EAFFB2_with_critical_nodes_and_fire_and_flood_disasters_realistic_traffic_laying_cost = 0
    sum_of_EAFFB2_with_critical_nodes_and_fire_and_flood_disasters_traffic_repair_cost = 0
    sum_of_EAFFB2_with_critical_nodes_and_fire_and_flood_disasters_realistic_traffic_repair_hours = 0


    for j in range(test_times):
        traffic, total_traffic = createTrafficMatrix(nodes, 20*i)
        realistic_traffic_calculated, total_realistic_traffic_calculated = createRealisticTrafficMatrix(nodes_pop, scale=20*i, noise=True, self_traffic_factor=1)
        # scale it to the original traffic calculation method number.
        realistic_traffic = calc_new_traffic(total_traffic, total_realistic_traffic_calculated, realistic_traffic_calculated)

        # start executing algorithms.

        # ////////////////////////////////////////////
        # EAFFB
        eaffb_result, dummy_num_rooters, dummy_num_tran, dummy_num_edfa = EAFFB(nodes, links, g, traffic, regionLinks, lowerThresholdValue)
        sum_of_EAFFB += eaffb_result

        # EAFFB with realistic_traffic
        eaffb_realistic_traffic_result, dummy_num_rooters, dummy_num_tran, dummy_num_edfa = EAFFB(nodes, links, g, realistic_traffic, regionLinks,lowerThresholdValue)
        sum_of_EAFFB_realistic_traffic += eaffb_realistic_traffic_result
        # ////////////////////////////////////////////

        # ////////////////////////////////////////////
        # proposedAlgorithm (ON PTYXIAKI)
        proposedAlgorithm_result, original_power, num_rooters, num_tran, num_edfa, original_num_rooters, original_num_tran, original_num_edfa = proposedAlgorithm(nodes, links, g, traffic, regionLinks, lowerThresholdValue)
        sum_of_proposed_alg += proposedAlgorithm_result

        # proposedAlgorithm (ON PTYXIAKI) with realistic_traffic
        proposedAlgorithm_realistic_traffic_result, original_power, num_rooters, num_tran, num_edfa, original_num_rooters, original_num_tran, original_num_edfa = proposedAlgorithm(nodes, links, g, realistic_traffic, regionLinks, lowerThresholdValue)
        sum_of_proposed_alg_realistic_traffic += proposedAlgorithm_realistic_traffic_result
        # ////////////////////////////////////////////

        # ////////////////////////////////////////////
        # EAFFB2 (NEW PATH CALCULATION SCHEME AT THE START)
        eaffb2_result, eaffb2_laying_cost, eaffb2_repair_cost, eaffb2_repair_hours = EAFFB2(nodes, g, traffic, critical_regions, original_shortest_paths_avoid_critical_links)
        sum_of_EAFFB2 += eaffb2_result
        sum_of_EAFFB2_laying_cost += eaffb2_laying_cost
        sum_of_EAFFB2_repair_cost += eaffb2_repair_cost
        sum_of_EAFFB2_repair_hours += eaffb2_repair_hours

        # EAFFB2 with realistic_traffic (NEW PATH CALCULATION SCHEME AT THE START)
        eaffb2_realistic_traffic_result, eaffb2_realistic_traffic_laying_cost, eaffb2_realistic_traffic_repair_cost, eaffb2_realistic_traffic_repair_hours  = EAFFB2(nodes, g, realistic_traffic, critical_regions, original_shortest_paths_avoid_critical_links)
        sum_of_EAFFB2_realistic_traffic += eaffb2_realistic_traffic_result
        sum_of_EAFFB2_realistic_traffic_laying_cost += eaffb2_realistic_traffic_laying_cost
        sum_of_EAFFB2_realistic_traffic_repair_cost += eaffb2_realistic_traffic_repair_cost
        sum_of_EAFFB2_realistic_traffic_repair_hours += eaffb2_realistic_traffic_repair_hours
        # ////////////////////////////////////////////

        # ////////////////////////////////////////////
        # EAFFB with critical nodes
        eaffb_with_critical_nodes_result, eaffb_with_critical_nodes_laying_cost, eaffb_with_critical_nodes_repair_cost, eaffb_with_critical_nodes_repair_hours = EAFFB_with_critical_nodes(nodes, g, traffic, critical_regions, original_shortest_paths, critical_nodes)
        sum_of_EAFFB_with_critical_nodes += eaffb_with_critical_nodes_result
        sum_of_EAFFB_with_critical_nodes_laying_cost += eaffb_with_critical_nodes_laying_cost
        sum_of_EAFFB_with_critical_nodes_repair_cost += eaffb_with_critical_nodes_repair_cost
        sum_of_EAFFB_with_critical_nodes_repair_hours += eaffb_with_critical_nodes_repair_hours

        # EAFFB with critical nodes with realistic_traffic
        eaffb_with_critical_nodes_realistic_traffic_result, eaffb_with_critical_nodes_realistic_traffic_laying_cost, eaffb_with_critical_nodes_realistic_traffic_repair_cost, eaffb_with_critical_nodes_realistic_traffic_repair_hours = EAFFB_with_critical_nodes(nodes, g, realistic_traffic, critical_regions, original_shortest_paths, critical_nodes)
        sum_of_EAFFB_with_critical_nodes_realistic_traffic += eaffb_with_critical_nodes_realistic_traffic_result
        sum_of_EAFFB_with_critical_nodes_realistic_traffic_laying_cost += eaffb_with_critical_nodes_realistic_traffic_laying_cost
        sum_of_EAFFB_with_critical_nodes_realistic_traffic_repair_cost += eaffb_with_critical_nodes_realistic_traffic_repair_cost
        sum_of_EAFFB_with_critical_nodes_realistic_traffic_repair_hours += eaffb_with_critical_nodes_realistic_traffic_repair_hours
        # ////////////////////////////////////////////

        # ////////////////////////////////////////////
        # EAFFB with critical nodes and fire and flood disasters logic
        eaffb_with_critical_nodes_and_fire_and_flood_disasters_result, eaffb_with_critical_nodes_and_fire_and_flood_disasters_laying_cost, eaffb_with_critical_nodes_and_fire_and_flood_disasters_repair_cos, eaffb_with_critical_nodes_and_fire_and_flood_disasters_repair_hours = EAFFB_with_critical_nodes_and_fire_and_flood_disasters(nodes, g, traffic, critical_regions, original_shortest_paths, critical_nodes, critical_regions_fire, critical_regions_flood)
        sum_of_EAFFB_with_critical_nodes_and_fire_and_flood_disasters += eaffb_with_critical_nodes_and_fire_and_flood_disasters_result
        sum_of_EAFFB_with_critical_nodes_and_fire_and_flood_disasters_laying_cost += eaffb_with_critical_nodes_and_fire_and_flood_disasters_laying_cost
        sum_of_EAFFB_with_critical_nodes_and_fire_and_flood_disasters_repair_cost += eaffb_with_critical_nodes_and_fire_and_flood_disasters_repair_cos
        sum_of_EAFFB_with_critical_nodes_and_fire_and_flood_disasters_repair_hours += eaffb_with_critical_nodes_and_fire_and_flood_disasters_repair_hours

        # EAFFB with critical nodes and fire and flood disasters logic
        eaffb_with_critical_nodes_and_fire_and_flood_disasters_realistic_traffic_result, eaffb_with_critical_nodes_and_fire_and_flood_disasters_realistic_traffic_laying_cost, eaffb_with_critical_nodes_and_fire_and_flood_disasters_realistic_traffic_repair_cost, eaffb_with_critical_nodes_and_fire_and_flood_disasters_realistic_traffic_repair_hours = EAFFB_with_critical_nodes_and_fire_and_flood_disasters(nodes, g, realistic_traffic, critical_regions, original_shortest_paths, critical_nodes,critical_regions_fire, critical_regions_flood)
        sum_of_EAFFB_with_critical_nodes_and_fire_and_flood_disasters_realistic_traffic += eaffb_with_critical_nodes_and_fire_and_flood_disasters_realistic_traffic_result
        sum_of_EAFFB_with_critical_nodes_and_fire_and_flood_disasters_realistic_traffic_laying_cost += eaffb_with_critical_nodes_and_fire_and_flood_disasters_realistic_traffic_laying_cost
        sum_of_EAFFB_with_critical_nodes_and_fire_and_flood_disasters_realistic_traffic_repair_cost += eaffb_with_critical_nodes_and_fire_and_flood_disasters_realistic_traffic_repair_cost
        sum_of_EAFFB_with_critical_nodes_and_fire_and_flood_disasters_realistic_traffic_repair_hours += eaffb_with_critical_nodes_and_fire_and_flood_disasters_realistic_traffic_repair_hours
        # ////////////////////////////////////////////

    print("========== EAFFB2 vs EAFFB vs Proposed ==========")
    print(f"EAFFB : {(sum_of_EAFFB / test_times) / 1000}")
    print(f"EAFFB realistic_traffic : {(sum_of_EAFFB_realistic_traffic / test_times) / 1000}")
    print(f"EAFFB vs EAFFB realistic_traffic: {perCalc(sum_of_EAFFB, sum_of_EAFFB_realistic_traffic, test_times)}% lower energy")
    print(f"Proposed algorithm on paper: {(sum_of_proposed_alg / test_times) / 1000}")
    print(f"Proposed algorithm on paper realistic_traffic: {(sum_of_proposed_alg_realistic_traffic / test_times) / 1000}")
    print(f"Proposed algorithm on pape vs Proposed algorithm on pape realistic_traffic: {perCalc(sum_of_proposed_alg, sum_of_proposed_alg_realistic_traffic, test_times)}% lower energy")
    print(f"EAFFB with new shortest path calculation scheme : {(sum_of_EAFFB2 / test_times) / 1000}")
    print(f"EAFFB with new shortest path calculation scheme laying_cost: {(sum_of_EAFFB2_laying_cost / test_times) / 1000}")
    print(f"EAFFB with new shortest path calculation scheme repair_cost: {(sum_of_EAFFB2_repair_cost / test_times) / 1000}")
    print(f"EAFFB with new shortest path calculation scheme repair_hours: {(sum_of_EAFFB2_repair_hours / test_times) / 1000}")

    print(f"EAFFB with new shortest path calculation scheme realistic_traffic: {(sum_of_EAFFB2_realistic_traffic / test_times) / 1000}")
    print(f"EAFFB with new shortest path calculation scheme realistic_traffic laying_cost: {(sum_of_EAFFB2_realistic_traffic_laying_cost / test_times) / 1000}")
    print(f"EAFFB with new shortest path calculation scheme realistic_traffic repair_cost: {(sum_of_EAFFB2_realistic_traffic_repair_cost / test_times) / 1000}")
    print(f"EAFFB with new shortest path calculation scheme realistic_traffic repair_hours: {(sum_of_EAFFB2_realistic_traffic_repair_hours / test_times) / 1000}")

    print(f"EAFFB with new shortest path calculation scheme vs EAFFB with new shortest path calculation scheme realistic_traffic: {perCalc(sum_of_EAFFB2, sum_of_EAFFB2_realistic_traffic, test_times)}% lower energy")
    print(f"EAFFB2 vs EAFFB: {perCalc(sum_of_EAFFB, sum_of_EAFFB2, test_times)}% lower energy")
    print(f"EAFFB2 vs Proposed: {perCalc(sum_of_proposed_alg, sum_of_EAFFB2, test_times)}% lower energy")


    print("========== EAFFB with critical nodes logic vs EAFFB vs Proposed ==========")
    print(f"EAFFB : {(sum_of_EAFFB / test_times) / 1000}")
    print(f"EAFFB realistic_traffic : {(sum_of_EAFFB_realistic_traffic / test_times) / 1000}")
    print(f"EAFFB vs EAFFB realistic_traffic: {perCalc(sum_of_EAFFB, sum_of_EAFFB_realistic_traffic, test_times)}% lower energy")
    print(f"Proposed algorithm on paper: {(sum_of_proposed_alg / test_times) / 1000}")
    print(f"Proposed algorithm on paper realistic_traffic: {(sum_of_proposed_alg_realistic_traffic / test_times) / 1000}")
    print(f"Proposed algorithm on pape vs Proposed algorithm on pape realistic_traffic: {perCalc(sum_of_proposed_alg, sum_of_proposed_alg_realistic_traffic, test_times)}% lower energy")
    print(f"EAFFB with critical nodes logic : {(sum_of_EAFFB_with_critical_nodes / test_times) / 1000}")
    print(f"EAFFB with critical nodes logic laying_cost: {sum_of_EAFFB_with_critical_nodes_laying_cost / test_times}")
    print(f"EAFFB with critical nodes logic repair_cost: {sum_of_EAFFB_with_critical_nodes_repair_cost / test_times}")
    print(f"EAFFB with critical nodes logic repair_hours: {sum_of_EAFFB_with_critical_nodes_repair_hours / test_times}")

    print(f"EAFFB with critical nodes logic realistic_traffic: {(sum_of_EAFFB_with_critical_nodes_realistic_traffic / test_times) / 1000}")
    print(f"EAFFB with critical nodes logic realistic_traffic laying_cost: {sum_of_EAFFB_with_critical_nodes_realistic_traffic_laying_cost / test_times}")
    print(f"EAFFB with critical nodes logic realistic_traffic repair_cost: {sum_of_EAFFB_with_critical_nodes_realistic_traffic_repair_cost / test_times}")
    print(f"EAFFB with critical nodes logic realistic_traffic repair_hours: {sum_of_EAFFB_with_critical_nodes_realistic_traffic_repair_hours / test_times}")

    print(f"EAFFB with critical nodes logic vs EAFFB with critical nodes logic realistic_traffic: {perCalc(sum_of_EAFFB_with_critical_nodes, sum_of_EAFFB_with_critical_nodes_realistic_traffic, test_times)}% lower energy")
    print(f"EAFFB with critical nodes logic vs EAFFB: {perCalc(sum_of_EAFFB, sum_of_EAFFB_with_critical_nodes, test_times)}% lower energy")
    print(f"EAFFB with critical nodes logic vs Proposed: {perCalc(sum_of_proposed_alg, sum_of_EAFFB_with_critical_nodes, test_times)}% lower energy")


    print("========== EAFFB with critical nodes and fire and flood disasters logic vs EAFFB vs Proposed ==========")
    print(f"EAFFB : {(sum_of_EAFFB / test_times) / 1000}")
    print(f"EAFFB realistic_traffic : {(sum_of_EAFFB_realistic_traffic / test_times) / 1000}")
    print(f"EAFFB vs EAFFB realistic_traffic: {perCalc(sum_of_EAFFB, sum_of_EAFFB_realistic_traffic, test_times)}% lower energy")
    print(f"Proposed algorithm on paper: {(sum_of_proposed_alg / test_times) / 1000}")
    print(f"Proposed algorithm on paper realistic_traffic: {(sum_of_proposed_alg_realistic_traffic / test_times) / 1000}")
    print(f"Proposed algorithm on pape vs Proposed algorithm on pape realistic_traffic: {perCalc(sum_of_proposed_alg, sum_of_proposed_alg_realistic_traffic, test_times)}% lower energy")
    print(f"EAFFB with critical nodes and fire and flood disasters logic : {(sum_of_EAFFB_with_critical_nodes_and_fire_and_flood_disasters / test_times) / 1000}")
    print(f"EAFFB with critical nodes and fire and flood disasters logic laying_cost: {sum_of_EAFFB_with_critical_nodes_and_fire_and_flood_disasters_laying_cost / test_times}")
    print(f"EAFFB with critical nodes and fire and flood disasters logic repair_cost: {sum_of_EAFFB_with_critical_nodes_and_fire_and_flood_disasters_repair_cost / test_times}")
    print(f"EAFFB with critical nodes and fire and flood disasters logic repair_hours: {sum_of_EAFFB_with_critical_nodes_and_fire_and_flood_disasters_repair_hours / test_times}")

    print(f"EAFFB with critical nodes and fire and flood disasters logic realistic_traffic: {(sum_of_EAFFB_with_critical_nodes_and_fire_and_flood_disasters_realistic_traffic / test_times) / 1000}")
    print(f"EAFFB with critical nodes and fire and flood disasters logic realistic_traffic laying_cost: {sum_of_EAFFB_with_critical_nodes_and_fire_and_flood_disasters_realistic_traffic_laying_cost / test_times}")
    print(f"EAFFB with critical nodes and fire and flood disasters logic realistic_traffic repair_cost: {sum_of_EAFFB_with_critical_nodes_and_fire_and_flood_disasters_realistic_traffic_repair_cost / test_times}")
    print(f"EAFFB with critical nodes and fire and flood disasters logic realistic_traffic repair_hours: {sum_of_EAFFB_with_critical_nodes_and_fire_and_flood_disasters_realistic_traffic_repair_hours / test_times}")

    print(f"EAFFB with critical nodes and fire and flood disasters logic vs EAFFB with critical nodes and fire and flood disasters logic realistic_traffic: {perCalc(sum_of_EAFFB_with_critical_nodes_and_fire_and_flood_disasters, sum_of_EAFFB_with_critical_nodes_and_fire_and_flood_disasters_realistic_traffic, test_times)}% lower energy")
    print(f"EAFFB with critical nodes and fire and flood disasters logic vs EAFFB: {perCalc(sum_of_EAFFB, sum_of_EAFFB_with_critical_nodes_and_fire_and_flood_disasters, test_times)}% lower energy")
    print(f"EAFFB with critical nodes and fire and flood disasters logic vs Proposed: {perCalc(sum_of_proposed_alg, sum_of_EAFFB_with_critical_nodes_and_fire_and_flood_disasters, test_times)}% lower energy")


    # print(f"Proposed algorithm: {sum_of_proposed_alg / test_times}")
    #
    # print(f"EAFFB2 vs EAFFB: {perCalc(sum_of_EAFFB, sum_of_EAFFB2, test_times)}% lower energy")
    # print(f"Proposed vs EAFFB: {perCalc(sum_of_EAFFB, sum_of_proposed_alg, test_times)}% lower energy")
    # print(f"EAFFB2 vs Proposed: {perCalc(sum_of_proposed_alg, sum_of_EAFFB2, test_times)}% lower energy")

    # print("///////// CRITICAL NODES (no traffic3) /////////")
    # print(f"EAFFB2_with_critical_nodes 30%: {sum_of_EAFFB2_with_critical_nodes_30 / test_times}")
    # print(f"EAFFB_with_critical_nodes 30%: {sum_of_EAFFB_with_critical_nodes_30 / test_times}")
    #
    # print("///////// TRAFFIC3 /////////")
    # print(f"EAFFB_30_traffic3: {sum_of_EAFFB_30_traffic3 / test_times}")
    # print(f"EAFFB2_30_traffic3: {sum_of_EAFFB2_30_traffic3 / test_times}")
    # print(f"Proposed_alg_traffic3: {sum_of_proposed_alg_traffic3 / test_times}")
    #
    # print(
    #     f"EAFFB2 vs EAFFB (traffic3): {perCalc(sum_of_EAFFB_30_traffic3, sum_of_EAFFB2_30_traffic3, test_times)}% lower energy")
    # print(
    #     f"Proposed vs EAFFB (traffic3): {perCalc(sum_of_EAFFB_30_traffic3, sum_of_proposed_alg_traffic3, test_times)}% lower energy")
    # print(
    #     f"EAFFB2 vs Proposed (traffic3): {perCalc(sum_of_proposed_alg_traffic3, sum_of_EAFFB2_30_traffic3, test_times)}% lower energy")
    #
    # print("///////// CRITICAL NODES + TRAFFIC3 /////////")
    # print(f"EAFFB2_with_critical_nodes_30_traffic3: {sum_of_EAFFB2_with_critical_nodes_30_traffic3 / test_times}")
    # print(f"EAFFB_with_critical_nodes_30_traffic3: {sum_of_EAFFB_with_critical_nodes_30_traffic3 / test_times}")
    # print(f"EAFFB2 vs EAFFB (with critical nodes, traffic3): {perCalc(sum_of_EAFFB_with_critical_nodes_30_traffic3, sum_of_EAFFB2_with_critical_nodes_30_traffic3, test_times)}% lower energy")
    #
    # print("///////// EAFFB3 /////////")
    # print(f"EAFFB3_with_critical_nodes_30: {sum_of_EAFFB3_with_critical_nodes / test_times}")
    # print(f"EAFFB3_with_critical_nodes_30_traffic3: {sum_of_EAFFB3_with_critical_nodes_traffic3 / test_times}")
    # print("============================================")
    #
    # print("///////// EAFFB2_with_critical_nodes_and_fire_and_flood_disasters /////////")
    # print(f"EAFFB2_with_critical_nodes_and_fire_and_flood_disasters: {sum_of_EAFFB2_with_critical_nodes_and_fire_and_flood_disasters / test_times}")
    # print("============================================")























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


