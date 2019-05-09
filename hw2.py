import numpy
import time
import copy

# working for test0 and test2
i = open("input4.txt", "r")

start = time.time()


######################    Defining Input    #####################################
def inp():
    global b, p, l, s, a
    #
    global size_spla
    global size_lahsa
    global lahsa_init  # =[]
    global spla_init  # =[]
    global total  # ={}
    b = int(i.readline().rstrip())  # no of beds <=40
    p = int(i.readline().rstrip())  # no of spaces in parking
    l = int(i.readline())  # no of applicants by LAHSA
    for k in range(l):
        lahsa_init.append(i.readline().rstrip())
    s = int(i.readline())  # no of applicants by SPLA
    for k in range(s):
        spla_init.append(i.readline().rstrip())
    a = int(i.readline())  # total number of applicants
    for k in range(a):
        total.append(i.readline().rstrip())

    #bed_lahsa = numpy.array([0] * 7)
    #bed_spla = numpy.array([0] * 7)
    size_spla=numpy.array([p]*7)
    size_lahsa=numpy.array([b]*7)
    # print("LAHSA :",bed_lahsa)
    # print("SPLA:",bed_spla)



#############################    Partitioning Applicant Data    #####################
def bifurcate():
    global app
    # print(total)
    # print range(len(total))

    for k in range(len(total)):

        c = []
        app[total[k][0:5]] = {"Gender": total[k][5], "Age": int(total[k][6:9]), "Pets": total[k][9],
                              "Medical": total[k][10], "Cars": total[k][11], "Lic": total[k][12],
                              "Request": total[k][13:20]}

        temp = list((app[total[k][0:5]]['Request']))
        sums = 0
        for ch in temp:
            c.append(int(ch))
            sums = sums + int(ch)
            # print(c)
        app[total[k][0:5]]["Sum"] = sums
        app[total[k][0:5]]["Requests"] = c


def initial():
    global bed_lahsa, bed_spla
    global app
    global lahsa_init, spla_init
    global total
    global lahsa_pool, spla_pool
    lahsa_pool = {}
    spla_pool = {}

    #   Removing applicant chosen by lahsa and adding sum to bed

    for k in lahsa_init:
        bed_lahsa = bed_lahsa + (app[k]["Requests"])
        del app[k]

    # print("Bed LAHSA:",bed_lahsa)
    #   Removing applicant chosen by spla and adding sum to bed

    for k in spla_init:
        bed_spla = bed_spla + (app[k]["Requests"])
        del app[k]

    # print("Bed SPLA:",bed_spla)

    for k in app:
        appln.append(k)

    for k in appln:
        if (app[k]["Cars"] == 'Y' and app[k]["Lic"] == 'Y' and app[k]["Medical"] == 'N'):
            spla_pool[k] = {"Request": app[k]["Requests"], "Visited": 0}
        if (app[k]["Gender"] == 'F' and app[k]["Age"] > 17 and app[k]["Pets"] == 'N'):
            # print(k)
            lahsa_pool[k] = {"Request": app[k]["Requests"], "Visited": 0}


def sums(beds):
    s = 0
    for i in range(7):
        s = s + beds[i]
    return s







##################################################################################
##################            Recursion         #################################
##################################################################################





def recursion(spla_pool, lahsa_pool, bed_spla, bed_lahsa, spla_eff, lahsa_eff, chance):
    global path_lahsa
    global path_spla
    # temp_b_s1 = copy.deepcopy(temp_b_s)
    # temp_b_l1 = copy.deepcopy(temp_b_l)
    node = '999999'

    #print("SPLA pool",spla_pool)
    #print("LAHSA pool",lahsa_pool)
    #print("SPLA eff:", spla_eff)
    #print("LAHSA eff:", lahsa_eff)
    #print("SPLA beds:",bed_spla)
    #print("LAHSA beds:",bed_lahsa)
    if (chance == 1):  ##    SPLA

        #print("###############  IN SPLA ")
        # l = spla_eff
        # s = lahsa_eff
        spla_max = spla_eff
        lahsa_max = lahsa_eff
        for k in spla_pool:
            if (spla_pool[k]["Visited"]) == 0:
                bed_spla = bed_spla + spla_pool[k]["Request"]
                large = numpy.all(numpy.asarray(size_spla) >= numpy.asarray(bed_spla))
                if (large == False):
                    #print("\t\t\t\tBED_spla does not satifies")
                    bed_spla = bed_spla - spla_pool[k]["Request"]
                    continue

                spla_pool[k]["Visited"] = 1
                # path_lahsa.append(k)
                #print("SPLA Visited:", k)
                if k in lahsa_pool.keys():  # print(k," is common")
                    lahsa_pool[k]["Visited"] = 1
                spla_eff = sums(bed_spla)
                lahsa_eff = sums(bed_lahsa)
                temp_s, temp_l = recursion(spla_pool, lahsa_pool, bed_spla, bed_lahsa, spla_eff, lahsa_eff, 2)
                bed_spla = bed_spla - spla_pool[k]["Request"]
                spla_pool[k]["Visited"] = 0
                # path_lahsa.append(k)
                #print("SPLA Backtracked:", k)
                # print("SPLA_e:",spla_eff)
                # print("Temp_s:",temp_s)
                if k in lahsa_pool.keys():  # print(k," is common")
                    lahsa_pool[k]["Visited"] = 0

                if (temp_s > spla_max):
                    spla_max = temp_s
                    lahsa_max = temp_l
                    node = k
                elif (temp_s == spla_max):
                    if (k < node):
                        node = k
                        spla_max = temp_s
                        lahsa_max = temp_l

        #print("Returned from SPLA", spla_eff)
        return (spla_max, lahsa_max)












    else:

        #print("********************   IN LAHSA")
        # l = spla_eff
        # s = lahsa_eff
        lahsa_max = lahsa_eff
        spla_max = spla_eff
        flag = 0
        for k in lahsa_pool:
            if (lahsa_pool[k]["Visited"]) == 0:
                bed_lahsa = bed_lahsa + lahsa_pool[k]["Request"]
                large = numpy.all(numpy.asarray(size_lahsa) >= numpy.asarray(bed_lahsa))
                if(large==False):
                    bed_lahsa = bed_lahsa - lahsa_pool[k]["Request"]
                    continue

                lahsa_pool[k]["Visited"] = 1
                # path_lahsa.append(k)
                flag = 1

                #print("LAHSA Visited:", k)
                if k in spla_pool.keys():  # print(k," is common")
                    spla_pool[k]["Visited"] = 1

                spla_eff = sums(bed_spla)
                lahsa_eff = sums(bed_lahsa)
                temp_s, temp_l = recursion(spla_pool, lahsa_pool, bed_spla, bed_lahsa, spla_eff, lahsa_eff, 1)
                bed_lahsa = bed_lahsa - lahsa_pool[k]["Request"]
                lahsa_pool[k]["Visited"] = 0
                # path_lahsa.append(k)
                #print("LAHSA Backtracked:", k)
                # print("LAHSA_e:", lahsa_eff)
                # print("Temp_l:", temp_l)

                if k in spla_pool.keys():  # print(k," is common")
                    spla_pool[k]["Visited"] = 0
                if (temp_l > lahsa_max):
                    lahsa_max = temp_l
                    spla_max = temp_s
                    node = k
                elif (temp_l == lahsa_max):
                    if (k < node):
                        node = k
                        lahsa_max = temp_l
                        spla_max = temp_s
                    # node2=k
        if (flag == 0):
            return recursion(spla_pool, lahsa_pool, bed_spla, bed_lahsa, spla_eff, lahsa_eff, 1)
        #     spla_eff=temp_s
        #     lahsa_eff=temp_l
        # print("Returned from LAHSA",spla_eff,temp_s)
        return (spla_max, lahsa_max)
    # return(spla_e,lahsa_e)








########################################################################################
#############################    Main Function begins here    ##########################
########################################################################################

start = time.time()
global b, p, l, s, a
global lahsa_init, spla_init, total, app, bed_lahsa, bed_spla, appln
global lahsa_pool, spla_pool,size_spla,size_lahsa

b_l1 = 0
b_s1 = 0
spla_eff = 0
lahsa_eff = 0
bed_lahsa = numpy.array([0] * 7)
bed_spla = numpy.array([0] * 7)
lahsa_init = []
spla_init = []
total = []
app = {}
appln = []
# path_spla = []
# path_lahsa = []
inp()
bifurcate()
initial()
#print("SPLA pool size",len(spla_pool))
#print("SPLA bed size",p)

node = '999999'
maxi=0
print(spla_pool)
print(lahsa_pool)
if(p>=len(spla_pool)):
    for k in spla_pool:
        mini=sums(spla_pool[k]["Request"])
        #if (spla_pool[k]["Visited"]) == 0:
            # bed_spla = bed_spla + spla_pool[k]["Request"]
            # large = numpy.all(numpy.asarray(size_spla) > numpy.asarray(bed_spla))
            # if (large == False):
            #     # print("\t\t\t\tBED_spla does not satifies")
            #     bed_spla = bed_spla - spla_pool[k]["Requests"]
            #     continue
            #
            # spla_pool[k]["Visited"] = 1
            # path_lahsa.append(k)
            # print("SPLA Visited:", k)
        if k in lahsa_pool.keys():  # print(k," is common")
            if(mini>maxi):
                node=k
                maxi=mini
            elif(mini==maxi):
                if(k<node):
                    node = k
else:
    chance = 2
    bed = 0

    print("In ELSE function")
    for z in spla_pool:
        bed_spla = bed_spla + spla_pool[z]["Request"]
        large = numpy.all(numpy.asarray(size_spla) >= numpy.asarray(bed_spla))
        if (large == False):
            #print("\t\t\t\tBED_spla does not satifies")
            bed_spla = bed_spla - spla_pool[z]["Request"]
            continue

        spla_pool[z]["Visited"] = 1
        if z in lahsa_pool.keys():  # print(k," is common")
            lahsa_pool[z]["Visited"] = 1

        spla_eff = sums(bed_spla)
        lahsa_eff = sums(bed_lahsa)
        #print("Z=", z)
        print("SPLA beds before", bed_spla)

        bed_s1, bed_l1 = recursion(spla_pool, lahsa_pool, bed_spla, bed_lahsa, spla_eff, lahsa_eff, chance)

        print("SPLA received from :",bed_s1,z)
        spla_pool[z]["Visited"] = 0
        bed_spla = bed_spla - spla_pool[z]["Request"]
        #print("SPLA beds after ", bed_spla)
        if z in lahsa_pool.keys():  # print(k," is common")
            lahsa_pool[z]["Visited"] = 0
        if (bed_s1 > bed):
            # spla_eff=bed_s1
            # lahsa_eff=bed_l1
            bed = bed_s1
            node = z
        elif (bed_s1 == bed):
            if (z < node):
                # spla_eff = bed_s1
                # lahsa_eff = bed_l1
                bed = bed_s1
                node = z


print("NODE:", node)

o = open("output.txt", "w")
o.write(node)
o.close()
end = time.time()
#print("SPLA leaf totol beds:", bed)
print("Total time=", end - start)
