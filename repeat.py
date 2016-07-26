#!/usr/bin/python

import sys


filename = sys.argv[1]
threshold1 = int(sys.argv[2]) #length threshold
threshold2 = int(sys.argv[3]) #from threshold
threshold3 = int(sys.argv[4]) #length difference threshold
threshold4 = int(sys.argv[5]) #depth  threshold
outputname = sys.argv[5]

def buildDict(filename,threshold1,threshold2,threshold3,threshold4,outputname):


    readDict= {}
    repeatDict= {}


    with open(filename) as f:
        repeatidcount = 0
        for line in f:
            fields = line.split(" ")
            readid1 = fields[0]
            readid2 = fields[1]

            addreadone = True
            addreadtwo = True

            id1strand = fields[4]
            id1from = fields[5]
            id1to = fields[6]
            id1replength = fields[7]

            id2strand = fields[9]
            id2from = fields[10]
            id2to = fields[11]
            id2replength = fields[12]

            cur1 = readDict

            if readid1 not in cur1:
                cur1[readid1] = {}
            cur1 = cur1[readid1]

            lengthrange1 = int(id1replength) // threshold1 * threshold1
            lengthrange2 = int(id2replength) // threshold1 * threshold1

            if abs(lengthrange1 - lengthrange2) > threshold3:
                pass


            if lengthrange1 not in cur1:
                cur1[lengthrange1] = {}
            cur1 = cur1[lengthrange1]



            if id1strand not in cur1:
                cur1[id1strand] = {}
            cur1 = cur1[id1strand]

            fromrange = int(id1from) // threshold2 * threshold2
            if fromrange not in cur1:
                cur1[fromrange] = {}
            else:
                addreadone = False
                
            cur1 = cur1[fromrange]

            cur2 = readDict

            if readid2 not in cur2:
                cur2[readid2] = {}
            cur2 = cur2[readid2]

            if lengthrange2 not in cur2:
                cur2[lengthrange2] = {}
            cur2 = cur2[lengthrange2]

            if id2strand not in cur2:
                cur2[id2strand] = {}
            cur2 = cur2[id2strand]

            fromrange = int(id2from) // threshold2 * threshold2
            if fromrange not in cur2:
                cur2[fromrange] = {}
            else:
                addreadtwo = False

            cur2 = cur2[fromrange]

            readid = readid1 if lengthrange1 > lengthrange2 else readid2
            idfrom = id1from if lengthrange1 > lengthrange2 else id2from
            idto = id1to if lengthrange1 > lengthrange2 else id2to
            idstrand = id1strand if lengthrange1 > lengthrange2 else id2strand
            idrange = lengthrange1 if lengthrange1 > lengthrange2 else lengthrange2

            if addreadone and addreadtwo:
                cur3 = repeatDict
                repeatidcount += 1
                cur1['repeatid'] = repeatidcount
                cur2['repeatid'] = repeatidcount
                cur3[repeatidcount] = {}

                cur3 = cur3[repeatidcount]
                cur3['depth'] = 1
                cur3['pointer'] = None
                cur3['read'] = [readid, idfrom, idto, idrange, idstrand]

            elif addreadone and not addreadtwo:
                repeatid = cur2['repeatid']

                while repeatDict[repeatid]['pointer']:
                    repeatid = repeatDict[repeatid]['pointer']

                cur1['repeatid'] = repeatid
                repeatDict[repeatid]['depth'] += 1
                if repeatDict[repeatid]['read'][3] < idrange:
                    repeatDict[repeatid]['read'] = [readid, idfrom, idto, idrange, idstrand]

            elif not addreadone and addreadtwo:
                repeatid = cur1['repeatid']

                while repeatDict[repeatid]['pointer']:
                    repeatid = repeatDict[repeatid]['pointer']

                cur2['repeatid'] = repeatid
                repeatDict[repeatid]['depth'] += 1
                if repeatDict[repeatid]['read'][3] < idrange:
                    repeatDict[repeatid]['read'] = [readid, idfrom, idto, idrange, idstrand]


            else:
                repeatid1 = cur1['repeatid']
                repeatid2 = cur2['repeatid']

                while repeatDict[repeatid1]['pointer']:
                    repeatid1 = repeatDict[repeatid1]['pointer']

                while repeatDict[repeatid2]['pointer']:
                    repeatid2 = repeatDict[repeatid2]['pointer']

                if repeatid1 != repeatid2:
                    repeatDict[repeatid2]['pointer'] = repeatid1
                    depth = repeatDict[repeatid2]['depth']
                    repeatDict[repeatid1]['depth'] += depth
                else:
                    repeatDict[repeatid1]['depth'] += 1

                if repeatDict[repeatid1]['read'][3] < idrange:
                    repeatDict[repeatid1]['read'] = [readid, idfrom, idto, idrange, idstrand]

        f1 = open(outputname,'w')
        for key in repeatDict:
            cur =repeatDict[key]
            if not cur['pointer']:
                if cur['depth'] > threshold4:
                    readid = cur['read'][0]
                    readfrom = cur['read'][1]
                    readto = cur['read'][2]
                    readlength = cur['read'][3]
                    readstrand = cur['read'][4]
                    f1.write('read' + readid + '_0' + ' ' + readfrom + ' ' +
                             readto + ' ' + str(readlength) + ' ' + readstrand + '\n')

        return

#buildDict('test_all',200,100,100,100,'result1')
sys.exit()






