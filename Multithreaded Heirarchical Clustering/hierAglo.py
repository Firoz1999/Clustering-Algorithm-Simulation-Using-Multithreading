import math; #For pow and sqrt
import sys;
import matplotlib.pyplot as plt
from random import shuffle, uniform;
import threading as th;
from scipy.cluster.hierarchy import dendrogram, linkage

fig=plt.figure();
# ret=[]
def ReadData(fileName):
    #Read the file, splitting by lines
    f = open(fileName,'r');
    liness = f.read().splitlines();
    f.close();

    items = [];

    for i in range(0,len(liness)):
        line = liness[i].split(',');
        itemFeatures = [];

        for j in range(len(line)-1):
            v = float(line[j]); #Convert feature value to float
            itemFeatures.append(v); #Add feature value to dict

        items.append(itemFeatures);

    # shuffle(items);

    return items;

def CutToTwoFeatures(items,indexA,indexB):
    n = len(items);
    X = [];
    for i in range(n):
        item = items[i];
        newItem = [item[indexA],item[indexB]];
        X.append(newItem);

    return X;
def distance(thno,a,b):
    x=float(a[0])-float(b[0])
    x=x*x
    y=float(a[1])-float(b[1])
    y=y*y
    dist=round(math.sqrt(x+y),2)
    ret[thno]=dist

def distance_p(a,b):
    x=float(a[0])-float(b[0])
    x=x*x
    y=float(a[1])-float(b[1])
    y=y*y
    dist=round(math.sqrt(x+y),2)
    return dist

def minimum(matrix):
    p=[0,0]
    mn=1000
    for i in range(0,len(matrix)):
        for j in range(0,len(matrix[i])):
            if (matrix[i][j]>0 and matrix[i][j]<mn):
                mn=matrix[i][j]
                p[0]=i
                p[1]=j
    return p

def newpoint(pt):
    x=float(pt[0][0])+float(pt[1][0])
    x=x/2
    y=float(pt[0][1])+float(pt[1][1])
    y=y/2
    midpoint=[x,y]
    return midpoint


if __name__ == '__main__':
    points = ReadData('data.txt');
    points = CutToTwoFeatures(points,2,3);
    print(points)
    # z=linkage(points,'ward')
    # print("z = "+str(z))
    # dendrogram(z)
    # for i in range(len(z)):
    #     print("z[i] :"+str(z[i]))
    #     # dendrogram(z[i])
    #     plt.pause(2)
    # plt.show()
    hist=[]
    for i in range (0,len(points)):
        hist.append(i);

    ret=[0]*len(points)
    outline='['
    i=0
    names={}

    for i in range(0,len(points)):
        names[str(points[i])]=i
    l=0
    last=[]
    while(len(points)>1):
        l=l+1
        matrix=list()
        print ('Distance matrix no. '+str(l)+': ')
        for i in range(0,len(points)):
            m=[0]*len(points)
            t=[0]*len(points)
            for j in range(0,len(points)):
                t[j]=th.Thread(target=distance,args=(j,points[i],points[j],))
                t[j].start()
                #m[j]=distance(points[i],points[j])
            for j in range(0,len(points)):
                t[j].join()
                m[j]=ret[j]
                #print("ret = "+str(ret))
            print (str(m))
            matrix.append(m)

        m=minimum(matrix)
        print("m = "+str(m))
        pts=list()
        p1=points[m[0]]
        p2=points[m[1]]

        print("p1 "+str(p1))
        print("p2 "+str(p2))
        pts.append(p1)
        pts.append(p2)

        points.remove(p1)
        points.remove(p2)
        midpoint=newpoint(pts)
        points.append(midpoint)
        c1=names.pop(str(p1))
        c2=names.pop(str(p2))

        print("c1 = "+str(c1))
        print("c2 = "+str(c2))

        d1=distance_p(p1,p2)
        last.append([(c1+c2)/2,d1])
        dd1=0
        dd2=0
        for ll in last:
            if(c1 == ll[0]):
                dd1=ll[1]
        for ll in last:
            if(c2 == ll[0]):
                dd2=ll[1]
        h1=[c1,c1]
        h2=[dd1,d1]
        h11=[c2,c2]
        h22=[dd2,d1]
        h111=[c1,c2]
        h222=[d1,d1]
        plt.plot(h1, h2, linewidth=0.5,c="green",gid=1)
        plt.pause(0.5)
        plt.plot(h11, h22, linewidth=0.5,c="red")
        plt.pause(0.5)
        plt.plot(h111, h222, linewidth=0.5,c="blue",gid=1)
        plt.pause(0.5)

        # names[str(midpoint)]="["+str(c1)+str(c2)+"]"
        names[str(midpoint)]=(c1+c2)/2
        outline=names[str(midpoint)]
        #z=[c1,c2,matrix[c1][c2],2.0]


    # print ("Cluster is :"+names[str(midpoint)])
    plt.show()
