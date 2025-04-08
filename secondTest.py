from functions import createTrafficMatrix
from algorithms import EAFFB, proposedAlgorithm

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

# crating the traffic matrix.
traffic = createTrafficMatrix(nodes, 20*6)

# you can change the lower threshold value here.
lowerThresholdValue = 0.2

# you can change the times that you want to run the simulation here.
test_times = 10
for i in range(1, 7):
    print("For avg traffic = " + str(20 * i))
    sum_of_result = 0
    sum_of_original_power = 0
    sum_of_no_seismic_zones_eaffb = 0
    sum_of_num_rooters = 0
    sum_of_num_tran = 0
    sum_of_num_edfa = 0
    sum_of_original_num_rooters = 0
    sum_of_original_num_tran = 0
    sum_of_original_num_edfa = 0
    for j in range(test_times):
        traffic = createTrafficMatrix(nodes, 20*i)
        result, original_power, num_rooters, num_tran, num_edfa, original_num_rooters, original_num_tran, original_num_edfa = proposedAlgorithm(nodes, links, g, traffic, regionLinks, lowerThresholdValue)
        no_seismic_zones_eaffb, dummy_num_rooters, dummy_num_tran, dummy_num_edfa = EAFFB(nodes, links, g, traffic, regionLinks, 0.9)
        sum_of_result += result/1000
        sum_of_original_power += original_power/1000
        sum_of_no_seismic_zones_eaffb += no_seismic_zones_eaffb/1000
        sum_of_num_rooters += num_rooters
        sum_of_num_tran += num_tran
        sum_of_num_edfa += num_edfa
        sum_of_original_num_rooters += original_num_rooters
        sum_of_original_num_tran += original_num_tran
        sum_of_original_num_edfa += original_num_edfa

    print("no_seismic_zones EAFFB " + str(int(lowerThresholdValue*100)) + "%: " + str(sum_of_no_seismic_zones_eaffb / test_times))
    print("new EAFFB " + str(int(lowerThresholdValue*100)) + "%: " + str(sum_of_result / test_times))
    print("original EAFFB " + str(int(lowerThresholdValue*100)) + "%: " + str(sum_of_original_power / test_times))

    per2 = (int(sum_of_original_power / test_times) - int(sum_of_no_seismic_zones_eaffb / test_times)) / int(
        sum_of_original_power / test_times)
    print("EAFFB energy cost from backup paths " + str(int(per2 * 100)) + "%")

    per = (int(sum_of_original_power / test_times)-int(sum_of_result / test_times)) / int(sum_of_original_power / test_times)
    print("NEW energy cost is lower " + str(int(per * 100)) + "%")

    print("NEW num_rooters " + str(int(sum_of_num_rooters / test_times)))
    print("NEW num_tran " + str(int(sum_of_num_tran / test_times)))
    print("NEW num_edfa " + str(int(sum_of_num_edfa / test_times)))
    print("OLD num_rooters " + str(int(sum_of_original_num_rooters / test_times)))
    print("OLD num_tran " + str(int(sum_of_original_num_tran / test_times)))
    print("OLD num_edfa " + str(int(sum_of_original_num_edfa / test_times)))


    print("///////")


