import math

from functions import bfs, create_Cij, create_Wij, create_fmn, directLinkWith, \
    create_x_y_forEveryRegion, new_g, findAllRequestsUsingThisLink, brokenPaths, sum2, sum1, \
    checksIfTheNetworkIsNotCutOff, isThisLinkCritical, new_links, calculate_laying_cost, \
    is_this_link_in_min_combination, checksIfTheNetworkIsNotCutOff_EAFFB

lowerThresholdValue = 0.3
Mx = 5
My = 4
T = 5
t_study = 57


#
def IP_SB(nodes, links, g, traffic):
    shortestPaths = []

    for i in nodes:
        for j in nodes[nodes.index(i):]:
            if i != j:
                shortestPaths.append(bfs(i, j, g))

    # print("////")
    # print(len(shortestPaths))

    # print("////")
    C_ij = create_Cij(traffic)
    w_ij = create_Wij(shortestPaths, C_ij)
    f_nm = create_fmn(w_ij, links)
    # print(traffic)
    # print(C_ij)
    # print(w_ij)
    # print(f_nm)

    # print("////")

    eRouter = 0
    for i in nodes:
        Di = 0
        c_ij_sum = 0
        for d in nodes:
            if i != d:
                Di += traffic[i + d]
                c_ij_sum += C_ij[i + d]

        eRouter += 1000 * (Di / 40) + c_ij_sum

    eTran = 0
    eEdfa = 0
    for m in nodes:
        for n in directLinkWith(m, g)[1]:
            # print("aaaa" + str(n))
            eTran += 73 * w_ij[n]
            eEdfa += 8 * ((int(n) / 80 - 1) + 2) * f_nm[n]

    eTotal = eRouter + eTran + eEdfa
    # print(eTotal)
    return eTotal


#
def EAFFB(nodes, links, g, traffic, regions):
    shortestPaths = []

    for i in nodes:
        for j in nodes[nodes.index(i):]:
            if i != j:
                shortestPaths.append(bfs(i, j, g))

    xR, yR, n, tesssst = create_x_y_forEveryRegion(len(regions))

    # for test
    # for i in range(len(xR)):
        #print("region: " + str(i + 1))
        #print(xR[i])
        #print(yR[i])
        #print(n[i])
        #print(tesssst[i])

    # print()
    # """

    new_shortestPaths = []
    for i in range(len(regions)):
        # print('For region: ' + str(i + 1))

        D = len(xR[i]) * sum2(xR[i], xR[i]) - sum1(xR[i]) * sum1(xR[i])
        at = (sum2(xR[i], xR[i]) * sum1(yR[i]) - sum1(xR[i]) * sum2(xR[i], yR[i])) / D
        b = (len(xR[i]) * sum2(xR[i], yR[i]) - sum1(xR[i]) * sum1(yR[i])) / D

        # print("D=" + str(D))
        # print("at=" + str(at))
        # print("b=" + str(b))

        a = at - math.log(t_study, 10)
        tmx = math.pow(10, -b * Mx) / math.pow(10, a)
        pt = 1 - math.pow(math.e, -T / tmx)

        # print("a=" + str(a))
        # print("tmx=" + str(tmx))
        # print("pt=" + str(pt))

        if pt >= lowerThresholdValue:
            for link in regions[i]:
                for path in brokenPaths(findAllRequestsUsingThisLink(shortestPaths, link)):
                    new_shortestPaths.append(bfs(path[0], path[1], new_g(regions[i], g)))

    # print("////")
    shortestPaths += new_shortestPaths
    # print(len(shortestPaths))

    # print("////")
    C_ij = create_Cij(traffic)
    w_ij = create_Wij(shortestPaths, C_ij)
    f_nm = create_fmn(w_ij, links)
    # print(traffic)
    # print(C_ij)
    # print(w_ij)
    # print(f_nm)

    # print("////")

    eRouter = 0
    for i in nodes:
        Di = 0
        c_ij_sum = 0
        for d in nodes:
            if i != d:
                Di += traffic[i + d]
                c_ij_sum += C_ij[i + d]

        eRouter += 1000 * (Di / 40) + c_ij_sum

    eTran = 0
    eEdfa = 0
    for m in nodes:
        for n in directLinkWith(m, g)[1]:
            eTran += 73 * w_ij[n]
            eEdfa += 8 * ((int(n) / 80 - 1) + 2) * f_nm[n]

    eTotal = eRouter + eTran + eEdfa
    # print("eRouter" + str(eRouter))
    # print("eTran" + str(eTran))
    # print("eEdfa" + str(eEdfa))
    # print(eTotal)
    return eTotal


#
def SZFB(nodes, links, g, traffic, seismicRegions):
    shortestPaths = []

    for i in nodes:
        for j in nodes[nodes.index(i):]:
            if i != j:
                shortestPaths.append(bfs(i, j, g))

    # print("/////////////////////////////////////////////////")
    # print(len(shortestPaths))

    new_shortestPaths = []
    for seismicRegion in seismicRegions:
        for link in seismicRegion:
            for path in brokenPaths(findAllRequestsUsingThisLink(shortestPaths, link)):
                new_shortestPaths.append(bfs(path[0], path[1], new_g(seismicRegion, g)))

    shortestPaths += new_shortestPaths
    # print(len(shortestPaths))

    # print("////")
    C_ij = create_Cij(traffic)
    w_ij = create_Wij(shortestPaths, C_ij)
    f_nm = create_fmn(w_ij, links)
    # print(traffic)
    # print(C_ij)
    # print(w_ij)
    # print(f_nm)

    # print("////")

    eRouter = 0
    for i in nodes:
        Di = 0
        c_ij_sum = 0
        for d in nodes:
            if i != d:
                Di += traffic[i + d]
                c_ij_sum += C_ij[i + d]

        eRouter += 1000 * (Di / 40) + c_ij_sum

    eTran = 0
    eEdfa = 0
    for m in nodes:
        for n in directLinkWith(m, g)[1]:
            eTran += 73 * w_ij[n]
            eEdfa += 8 * ((int(n) / 80 - 1) + 2) * f_nm[n]

    eTotal = eRouter + eTran + eEdfa
    #print("eRouter" + str(eRouter))
    #print("eTran" + str(eTran))
    #print("eEdfa" + str(eEdfa))
    #print(eTotal)
    return eTotal


#
def newAlgorithm(nodes, links, g, traffic, regions, number_of_total_links_acceptable, links_location):
    notCriticalLinks = []
    for link in links:
        if not isThisLinkCritical(nodes, [link], regions, g):
            notCriticalLinks.append(link)

    combinations = []
    min_combination = []
    for i in range(len(links) - number_of_total_links_acceptable):
        links_power_dict = {}
        links_power = []
        for link in notCriticalLinks:
            if not is_this_link_in_min_combination(link, min_combination):
                if checksIfTheNetworkIsNotCutOff_EAFFB(nodes, new_g(min_combination + [link], g), regions):
                    # link_power = IP_SB(nodes, new_links(min_combination + [link], links), new_g(min_combination + [link], g), traffic)
                    link_power = EAFFB(nodes, new_links(min_combination + [link], links), new_g(min_combination + [link], g), traffic, regions)
                    links_power.append(link_power)
                    links_power_dict[link_power] = link

        links_power.sort()
        min_combination.append(links_power_dict[links_power[0]])

    # min_power = IP_SB(nodes, new_links(min_combination, links), new_g(min_combination, g), traffic)
    min_power = EAFFB(nodes, new_links(min_combination, links), new_g(min_combination, g), traffic, regions)

    laying_cost = calculate_laying_cost(new_links(min_combination, links), links_location)

    return notCriticalLinks, combinations, min_combination, min_power, laying_cost


