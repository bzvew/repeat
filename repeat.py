#!/usr/bin/python

import sys


filename = sys.argv[1]
threshhold1 = int(sys.argv[2]) #length threshhold
threshhold2 = int(sys.argv[3]) #from threshhold
outputname = sys.argv[4]

def buildDict(filename,threshhold1,threshhold2,outputname):


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

            lengthrange = int(id1replength) // threshhold1 * threshhold1
            if lengthrange not in cur1:
                cur1[lengthrange] = {}
            cur1 = cur1[lengthrange]

            if id1strand not in cur1:
                cur1[id1strand] = {}
            cur1 = cur1[id1strand]

            fromrange = int(id1from) // threshhold2 * threshhold2
            if fromrange not in cur1:
                cur1[fromrange] = {}
            else:
                addreadone = False
                
            cur1 = cur1[fromrange]

            cur2 = readDict

            if readid2 not in cur2:
                cur2[readid2] = {}
            cur2 = cur2[readid2]

            lengthrange = int(id2replength) // threshhold1 * threshhold1
            if lengthrange not in cur2:
                cur2[lengthrange] = {}
            cur2 = cur2[lengthrange]

            if id2strand not in cur2:
                cur2[id2strand] = {}
            cur2 = cur2[id2strand]

            fromrange = int(id2from) // threshhold2 * threshhold2
            if fromrange not in cur2:
                cur2[fromrange] = {}
            else:
                addreadtwo = False

            cur2 = cur2[fromrange]

            if addreadone and addreadtwo:
                cur3 = repeatDict
                repeatidcount += 1
                cur1['repeatid'] = repeatidcount
                cur2['repeatid'] = repeatidcount
                cur3[repeatidcount] = {}

                cur3 = cur3[repeatidcount]
                cur3['depth'] = 1
                cur3['pointer'] = None
                cur3['read'] = [readid1,id1from,id1to,id1strand]

            elif addreadone and not addreadtwo:
                repeatid = cur2['repeatid']

                while repeatDict[repeatid]['pointer']:
                    repeatid = repeatDict[repeatid]['pointer']

                cur1['repeatid'] = repeatid
                repeatDict[repeatid]['depth'] += 1

            elif not addreadone and addreadtwo:
                repeatid = cur1['repeatid']

                while repeatDict[repeatid]['pointer']:
                    repeatid = repeatDict[repeatid]['pointer']

                cur2['repeatid'] = repeatid
                repeatDict[repeatid]['depth'] += 1

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
        f1 = open(outputname,'w')
        for key in repeatDict:
            cur =repeatDict[key]
            if not cur['pointer']:
                if cur['depth'] > 10:
                    readid = cur['read'][0]
                    readfrom = cur['read'][1]
                    readto = cur['read'][2]
                    readlength = int(readto) - int(readfrom)
                    readstrand = cur['read'][3]
                    f1.write('read' + readid + '_0' + ' ' + readfrom + ' ' + readto + '\n')

        return

buildDict(filename,threshhold1,threshhold2, outputname)
sys.exit()






