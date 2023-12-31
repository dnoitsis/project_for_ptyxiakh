import random
import pandas as pd
import math


# Calculates the cost for laying the networks fiber links.
def calculate_laying_cost(links, links_location):
    total_cost = 0
    cost_per_km_land = 43452
    cost_per_km_sea = 90000
    for link in links:
        if links_location[link] == 'land':
            total_cost += int(link) * cost_per_km_land
        else:
            total_cost += int(link) * cost_per_km_sea

    return total_cost


# Checks if the path contains the given link.
def contain(path, link):
    for i in path:
        if link == i:
            return True
    return False


# Finds all the requests using this link from the shortest paths.
def findAllRequestsUsingThisLink(shortestPaths, link):
    requestsUsingThisLink = []
    for path in shortestPaths:
        if contain(path[1], link):
            requestsUsingThisLink.append(path)
    return requestsUsingThisLink


# Finds the broken paths
def brokenPaths(requestsUsingThisLink):
    requests = []
    for paths in requestsUsingThisLink:
        path = [paths[0][0], paths[0][len(paths[0]) - 1]]
        requests.append(path)
    return requests


# Checks if the given link is included on the given array of links.
def equalTo(link, links):
    for discardedLink in links:
        if link == discardedLink:
            return True
    return False


# Creates a new g array, without the discarded links.
def new_g(discardedLinks, g):
    newG = []
    # print(newG)
    for path in g:
        # print(path[1])
        if not equalTo(path[1], discardedLinks):
            newG.append(path)

    return newG


# Creates a new links array, without the discarded links.
def new_links(discardedLinks, links):
    newLinks = []
    for link in links:
        if not equalTo(link, discardedLinks):
            newLinks.append(link)

    return newLinks


# Creates the traffic matrix.
def createTrafficMatrix(nodes, x):
    traffic = {}
    for i in nodes:
        for j in nodes:
            traffic[i + j] = random.randint(10, 2 * x - 10)

    return traffic


def return_critical_regions(regions, lowerThresholdValue):
    Mx = 5
    T = 5
    t_study = 58
    xR, yR, n, tesssst = create_x_y_forEveryRegion(len(regions))

    out = []
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
            out.append(regions[i])

    return out


def calculate_energy_consumption(traffic, shortestPaths, nodes):
    num_rooters = 0
    num_tran = 0
    num_edfa = 0
    for path in shortestPaths:
        i = path[0][0]
        j = path[0][len(path[0]) - 1]
        c_ij = int((traffic[i + j] / 40) + 0.999999)
        f_nm = int((c_ij / 80) + 0.999999)
        num_rooters_for_the_path = int((c_ij + (traffic[i + j] / 40)) + 0.999999)
        num_tran_for_the_path = int((c_ij * (len(path[1]))) + 0.999999)
        sum_Lmn = 0
        for link in path[1]:
            sum_Lmn += int(link)
        num_edfa_for_the_path = int((f_nm * ((2*len(path[1])) + (sum_Lmn / 80 - 1))) + 0.999999)
        num_rooters += num_rooters_for_the_path
        num_tran += num_tran_for_the_path
        num_edfa += num_edfa_for_the_path

    #for i in nodes:
     #   num_rooters += (traffic[i + i] / 40)

    eRouter = 1000 * num_rooters
    eTran = 73 * num_tran
    eEdfa = 8 * num_edfa
    eTotal = eRouter + eTran + eEdfa

    # print("num_edfa = " + str(num_edfa))
    #print("For energy")
    #print("eRouter = " + str(eRouter/1000))
    #print("eTran = " + str(eTran/1000))
    #print("eEdfa = " + str(eEdfa/1000))
    #print("eRouter% = " + str(eRouter / eTotal))
    #print("eTran% = " + str(eTran / eTotal))
    #print("eEdfa% = " + str(eEdfa / eTotal))

    return eTotal


# Creates the Cij matrix.
def create_Cij(traffic):
    c_ij = {}
    for i in traffic.keys():
        c_ij[i] = int((traffic[i] / 40) + 0.999999)

    return c_ij


# Creates the Cij matrix.
def create_Cij_new(traffic, shortestPaths, nodes):
    c_ij = {}
    for i in nodes:
        for j in nodes:
            if i != j:
                c_ij[i + j] = 0
    for path in shortestPaths:
        i = path[0][0]
        j = path[0][len(path[0])-1]
        c_ij[i + j] += int((traffic[i + j] / 40) + 0.999999)

    return c_ij


# just for testing
def create_Wmn_Lmn_new(shortestPaths, c_ij, nodes):
    w_mn = {}
    l_mn = {}

    for i in nodes:
        for j in nodes:
            if i != j:
                w_mn[i + j] = 0

    for path in shortestPaths:
        print(path)

        for i in range(1, len(path[0])):
            print(path[0][i - 1] + path[0][i])
            l_mn[path[0][i - 1] + path[0][i]] = path[1][i - 1]
            w_mn[path[0][i - 1] + path[0][i]] += c_ij[path[0][0] + path[0][len(path[0]) - 1]]

    return w_mn, l_mn


# Creates the Wij matrix.
def create_Wij(shortestPaths, c_ij):
    w_ij = {}
    for path in shortestPaths:
        for link in path[1]:
            if link in w_ij:
                w_ij[link] += c_ij[path[0][0] + path[0][len(path[0]) - 1]] + c_ij[
                    path[0][len(path[0]) - 1] + path[0][0]]  #
            else:
                w_ij[link] = c_ij[path[0][0] + path[0][len(path[0]) - 1]] + c_ij[path[0][len(path[0]) - 1] + path[0][0]]

    return w_ij


# Creates the Wmn matrix.
def create_Wmn(shortestPaths, c_ij, links):
    w_mn = {}
    for link in links:
        w_mn[link] = 0

    for path in shortestPaths:
        for link in path[1]:
            w_mn[link] += c_ij[path[0][0] + path[0][len(path[0]) - 1]]

    return w_mn


# just for testing
def create_Wij_Aij(shortestPaths, c_ij):
    w_ij = {}
    a_ij = {}
    for path in shortestPaths:
        if len(path[0]) == 2:
            a_ij[path[0][0] + path[0][1]] = path[1][0]
            if path[0][0] + path[0][1] in w_ij:
                w_ij[path[0][0] + path[0][1]] += c_ij[path[0][0] + path[0][1]]
            else:
                w_ij[path[0][0] + path[0][1]] = c_ij[path[0][0] + path[0][1]]

        for i in range(1, len(path[0]) - 1):
            a_ij[path[0][i - 1] + path[0][i]] = path[1][i - 1]
            if path[0][i - 1] + path[0][i] in w_ij:
                w_ij[path[0][i - 1] + path[0][i]] += c_ij[path[0][0] + path[0][len(path[0]) - 1]]
            else:
                w_ij[path[0][i - 1] + path[0][i]] = c_ij[path[0][0] + path[0][len(path[0]) - 1]]

    return w_ij, a_ij


# Creates the fmn matrix.
def create_fmn(w_ij, links):
    f_mn = {}
    for link in links:
        f_mn[link] = int((w_ij[link] / 80) + 0.999999)

    return f_mn


# just for testing
def create_fmn2(w_ij):
    f_mn = {}
    for i in w_ij.keys():
        f_mn[i] = int((w_ij[i] / 80) + 0.999999)

    return f_mn


# Finds the direct links that connect a node with neighboring nodes, and return the links and the neighboring nodes.
def directLinkWith(start, g):
    directLinks = [[]]
    startLinks = []
    for pair in g:
        if pair[0] == start:
            startLinks.append(pair[1])

    for link in startLinks:
        for pair in g:
            if (pair[0] != start) and (pair[1] == link):
                directLinks[0].append(pair[0])

    directLinks.append(startLinks)
    return directLinks


# Bfs algorithm for finding the shorter path between two nodes.
def bfs(start, end, g):
    shortestPath = []
    explored = [[]]
    queue = [[start]]
    linkQueue = [[]]
    while queue:
        path = queue.pop(0)
        linkPath = linkQueue.pop(0)
        node = path[-1]
        if node not in explored:
            neighbours = directLinkWith(node, g)
            for i in range(len(neighbours[0])):
                new_path = list(path)
                link_path = list(linkPath)
                link_path.append(neighbours[1][i])
                new_path.append(neighbours[0][i])
                queue.append(new_path)
                linkQueue.append(link_path)
                if neighbours[0][i] == end:
                    shortestPath.append(new_path)
                    shortestPath.append(link_path)
                    return shortestPath
            explored.append(node)
    return False


# Calculates and create the x and y arrays for every region, after loading the data.
def create_x_y_forEveryRegion(numberOfRegions):
    xRegions = []
    yRegions = []
    test = []
    test2 = []
    for i in range(1, numberOfRegions + 1):
        # print(i)
        df = pd.read_csv("regions_data/" + str(i) + ".csv", header=0)
        earthquakes = df.loc[df['Magnitude (ML)'] >= 4.0]
        earthquakes = earthquakes['Magnitude (ML)'].values
        d = {}
        for j in earthquakes:
            if j in d:
                d[j] += 1
            else:
                d[j] = 1

        y = []
        for x_count in d.values():
            y.append(math.log(x_count, 10))

        xRegions.append(list(d.keys()))
        yRegions.append(y)
        test.append(len(earthquakes))
        test2.append(list(d.values()))

    return xRegions, yRegions, test, test2


def sum1(x):
    s = 0.0
    for k in x:
        s = s + k

    return s


def sum2(x, y):
    s = 0.0
    for k in range(0, len(x)):
        s = s + x[k] * y[k]

    return s


def sum3(x, y, z):
    s = 0.0
    for k in range(0, len(x)):
        s = s + (x[k] * y[k]) - z

    return s


# Checks if the network is not cut off.
def checksIfTheNetworkIsNotCutOff(nodes, g):
    for i in nodes:
        for j in nodes[nodes.index(i):]:
            if i != j:
                if not bfs(i, j, g):
                    return False

    return True


# Checks if the network is not cut off, for the EAFFB algorithm.
def checksIfTheNetworkIsNotCutOff_EAFFB(nodes, g, regions):
    for region in regions:
        if not checksIfTheNetworkIsNotCutOff(nodes, new_g(region, g)):
            return False

    return True


# Removes given links from a given array of links.
def newDiscardedLinks(discardedlinks, linkToRemove):
    links = []
    for link in discardedlinks:
        if link != linkToRemove:
            links.append(link)

    return links


# Finds the link that can keep the network not cut off.
def findTheLinkForKeepingTheNetworkNotCutOff(nodes, discardedLinks, g):
    for link in discardedLinks:
        if checksIfTheNetworkIsNotCutOff(nodes, new_g(newDiscardedLinks(discardedLinks, link), g)):
            return [link]

    return discardedLinks


# checks if a link is critical. A link is critical when without it the network can be cut of if any of the regions
# links are also discarded.
def isThisLinkCritical(nodes, link, regions, g):
    for region in regions:
        if not checksIfTheNetworkIsNotCutOff(nodes, new_g(region + link, g)):
            return True

    return False


# Checks if a link is on the array of min_combination links.
def is_this_link_in_min_combination(link_checked, min_combination):
    for link in min_combination:
        if link_checked == link:
            return True

    return False
