import random
import pandas as pd
import math


# calculates the cost for laying the network.aaaaa
def calculate_laying_cost(links, links_location):
    total_cost = 0
    for link in links:
        if links_location[link] == 'land':
            total_cost += int(link) * 43452
        else:
            total_cost += int(link) * 90000

    return total_cost


# checks if the path contains the link.
def contain(path, link):
    for i in path:
        if link == i:
            return True
    return False


# finds all the requests using this link from the shortest paths.
def findAllRequestsUsingThisLink(shortestPaths, link):
    requestsUsingThisLink = []
    for path in shortestPaths:
        if contain(path[1], link):
            requestsUsingThisLink.append(path)
    return requestsUsingThisLink


# finds the broken paths
def brokenPaths(requestsUsingThisLink):
    requests = []
    for paths in requestsUsingThisLink:
        path = [paths[0][0], paths[0][len(paths[0]) - 1]]
        requests.append(path)
    return requests


# checks if link is included on the discarded links.
def equalTo(link, discardedLinks):
    for discardedLink in discardedLinks:
        if link == discardedLink:
            return True
    return False


# creates a new g without the discarded links.
def new_g(discardedLinks, g):
    newG = []
    # print(newG)
    for path in g:
        # print(path[1])
        if not equalTo(path[1], discardedLinks):
            newG.append(path)

    return newG


# creates a new links without the discarded links.
def new_links(discardedLinks, links):
    newLinks = []
    for link in links:
        if not equalTo(link, discardedLinks):
            newLinks.append(link)

    return newLinks


# creates the traffic matrix.
def createTrafficMatrix(nodes, x):
    traffic = {}
    for i in nodes:
        for j in nodes:
            if i != j:
                traffic[i + j] = random.randint(10, 2 * x - 10)

    return traffic


# creates the Cij matrix.
def create_Cij(traffic):
    c_ij = {}
    for i in traffic.keys():
        c_ij[i] = int((traffic[i] / 40) + 0.999999)

    return c_ij


# creates the Wij matrix.
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


# creates the fmn matrix.
def create_fmn(w_ij, links):
    f_mn = {}
    for link in links:
        f_mn[link] = int((w_ij[link] / 80) + 0.999999)

    return f_mn


# finds direct links with nodes
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


# bfs algorithm for shorter path
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


def create_x_y_forEveryRegion(numberOfRegions):
    xRegions = []
    yRegions = []
    test = []
    test2 = []
    for i in range(1, numberOfRegions + 1):
        # print(i)
        df = pd.read_csv(str(i) + ".csv", header=0)
        earthquakes = df.loc[df['Magnitude (ML)'] > 4.0]
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


def checksIfTheNetworkIsNotCutOff(nodes, g):
    for i in nodes:
        for j in nodes[nodes.index(i):]:
            if i != j:
                if not bfs(i, j, g):
                    return False

    return True


def checksIfTheNetworkIsNotCutOff_EAFFB(nodes, g, regions):
    for region in regions:
        if not checksIfTheNetworkIsNotCutOff(nodes, new_g(region, g)):
            return False

    return True


def newDiscardedLinks(discardedlinks, linkToRemove):
    links = []
    for link in discardedlinks:
        if link != linkToRemove:
            links.append(link)

    return links


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


def is_this_link_in_min_combination(link_checked, min_combination):
    for link in min_combination:
        if link_checked == link:
            return True

    return False

