import json
import numpy as np
#import matplotlib.pyplot as plt

class videoParser:
    _filename = ''
    _noVids = 0
    _noEpoints = 0
    _noRequests = 0
    _noCacheServers = 0
    _capacity = 0
    _vids = dict()
    _eps = dict()
    _pop = dict()

    def __init__(self , path):
        self._filename = path

    def readVidSize(self, fp ):
        sizes = fp.readline()
        comps = sizes.split(' ')
        for i in range(self._noVids):
            self._vids[i] = dict()
            self._vids[i]['size'] = int(comps[i])

    def readEndpoints(self , fp):

        for i in range(self._noEpoints):
            line = fp.readline().split(' ')
            self._eps[i] = dict()
            self._eps[i]['L_D'] = int(line[0])
            self._eps[i]['K'] = int(line[1])
            #print "k = %d"%int(line[1])
            self._eps[i]['serverList'] = dict()
            for _ in range(int(line[1])):
                #print "iter%d"%_
                l = fp.readline().split(' ')
                self._eps[i]['serverList'][l[0]] = int(l[1])

    def readPop(self , fp):
        for i in range(self._noRequests):
            self._pop[i] = dict()
            line = fp.readline().split(' ')
            self._pop[i]['id'] = line[0]
            self._pop[i]['epid'] = line[1]
            self._pop[i]['req'] = int(line[2])

    def parse(self):
        print "parsing %s"%self._filename
        f = open(self._filename , 'rb')
        firstline = f.readline().strip()
        components = firstline.split(' ')
        print components
        self._noVids = int(components[0])
        self._noEpoints = int(components[1])
        self._noRequests = int(components[2])
        self._noCacheServers = int(components[3])
        self._capacity = int(components[4])

        self.readVidSize(fp=f)
        self.readEndpoints(fp=f)
        self.readPop(fp=f)

    def createPopMatrix(self):
        popMatrix = np.zeros((self._noEpoints, self._noVids))

        for k in self._pop:
            v = self._pop[k]
            popMatrix[int(v['epid']) , int(v['id'])] += int(v['req'])

        return popMatrix

    def createLatMatrix(self):
        latMatrix = np.zeros((self._noEpoints, self._noCacheServers+1))
        print self._eps[0]['L_D']
        for k in self._eps:
            v = self._eps[k]['serverList']
            latMatrix[k , -1 ] = self._eps[k]['L_D']
            for i in v.keys():
                latMatrix[k , int(i)] = v[i]
        return latMatrix

def solveGreedy(popMatrix , latMatrix , vidSizes , capacity):
    for i in range(popMatrix.shape[1]):
        nonzero = np.count_nonzero(popMatrix[:,i])
        popMatrix[:,i] *= nonzero
    mostPopVids = np.argsort(popMatrix.sum(axis=0))[::-1]
    print mostPopVids
    vidList = []
    memory = 0
    i = 0
    while int(memory) < int(capacity):

        memory += int(vidSizes[ mostPopVids[i] ] ['size'])
        print memory , capacity
        if int(memory) > int(capacity):
            print "bailing"
            break
        vidList.append(mostPopVids[i])

        i+=1
    print vidList
    eplist = []
    for i in vidList:
        eplist = eplist + np.nonzero(popMatrix[:,i])[0].tolist()

    eplist = list(set(eplist))

    cacheList = []
    for i in eplist:
        cacheList = cacheList + np.nonzero(latMatrix[i,:])[0].tolist()
    print "Cache List"
    caches = list(set(cacheList))

    return caches , vidList


def saveFile(caches , vids):
    f = open("result1.txt" , 'wb')
    line = str(len(caches)-1) + '\n'
    f.write(line)
    for cache in caches :
        line = str(cache) + ' ' +  ' '.join(str(v) for v in vids) + '\n'
        f.write(line)
    f.close()

if __name__ == "__main__":

    #parser = videoParser('data/me_at_the_zoo.in')
    parser = videoParser('data/kittens.in')
    parser.parse()
    #print parser._vids
    print "EPS"

   # print parser._eps

    print "pop"
    #print parser._pop

    print "Popularity"
    popMatrix = parser.createPopMatrix()
    print popMatrix.shape

    #print popMatrix[:,0]


    print "Latency"

    latMatrix = parser.createLatMatrix()
    print latMatrix.shape
    #print latMatrix


    caches , vids = solveGreedy(popMatrix , latMatrix , parser._vids , parser._capacity)
    print len(caches)

    saveFile(caches , vids)
