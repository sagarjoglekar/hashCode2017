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






if __name__ == "__main__":

    #parser = videoParser('data/me_at_the_zoo.in')
    parser = videoParser('data/me_at_the_zoo.in')
    parser.parse()
    print parser._vids
    print "EPS"

    print parser._eps

    print "pop"
    print parser._pop

    popMatrix = np.zeros((parser._noEpoints, parser._noVids))

    for k in parser._pop:
        v = parser._pop[k]
        popMatrix[int(v['epid']) , int(v['id'])] += int(v['req'])

    print popMatrix


    latMatrix = np.zeros((parser._noEpoints, parser._noCacheServers+1))

    for k in parser._eps:
        v = parser._pop[k]['serverList']
        popMatrix[k , -1 ] = parser._pop[k]['L_D']
        for i in v.keys():
            popMatrix[k , int(i)] = v[i]

    print latMatrix.shape
    print latMatrix[10]


    # fig, ax = plt.subplots()
    # fig.set_size_inches(15, 10)
    # n1 , bins1 , patches1 = plt.hist(popMatrix[1], popMatrix.shape[1], normed=0,histtype='bar', cumulative=False,linewidth = 1.0)
    #
    # plt.title("Message Activity CDF", fontsize = 20)
    # plt.xlabel("Days Since First message",fontsize = 20)
    # plt.ylabel("CDF",fontsize = 20)
    # plt.legend(['Message Volume'], loc='upper left')
    # plt.grid()
    # plt.show()
