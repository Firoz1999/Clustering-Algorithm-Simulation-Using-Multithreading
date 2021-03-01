import math; #For pow and sqrt
import sys;
import matplotlib.pyplot as plt
from random import shuffle, uniform;
import threading as th;

fig=plt.figure();
ret=[[0]*2]*3
color=["red","blue","green"]
lines=[]
centroid=[]
datapoints=[]
###_Pre-Processing_###
def ReadData(fileName):
    #Read the file, splitting by lines
    f = open(fileName,'r');
    liness = f.read().splitlines();
    f.close();

    items = [];

    for i in range(1,len(liness)):
        line = liness[i].split(',');
        itemFeatures = [];

        for j in range(len(line)-1):
            v = float(line[j]); #Convert feature value to float
            itemFeatures.append(v); #Add feature value to dict

        items.append(itemFeatures);

    shuffle(items);

    return items;


###_Auxiliary Function_###
def FindColMinMax(items):
    n = len(items[0]);
    minima = [sys.maxsize for i in range(n)];
    maxima = [-sys.maxsize -1 for i in range(n)];

    for item in items:
        for f in range(len(item)):
            if(item[f] < minima[f]):
                minima[f] = item[f];

            if(item[f] > maxima[f]):
                maxima[f] = item[f];

    return minima,maxima;

def EuclideanDistance(x,y):
    S = 0; #The sum of the squared differences of the elements
    for i in range(len(x)):
        S += math.pow(x[i]-y[i],2);
    ret=math.sqrt(S)
    #print("euuci"+str(ret))

    return ret; #The square root of the sum

def InitializeMeans(items,k,cMin,cMax):
    #Initialize means to random numbers between
    #the min and max of each column/feature

    f = len(items[0]); #number of features
    means = [[0 for i in range(f)] for j in range(k)];

    j=0;
    for mean in means:
        for i in range(len(mean)):
            #Set value to a random float
            #(adding +-1 to avoid a wide placement of a mean)
            mean[i] = uniform(cMin[i]+1,cMax[i]-1);
        centroid.append(plt.scatter(mean[0],mean[1],c=color[j],alpha=0.5,s=50,marker="D"))
        plt.pause(0.1)
        j=j+1
    #plt.show();
    return means;

def UpdateMean(n,mean,item):
    for i in range(len(mean)):
        m = mean[i];
        m = (m*(n-1)+item[i])/float(n);
        mean[i] = round(m,3);

    return mean;

def FindClusters(means,items):
    clusters = [[] for i in range(len(means))]; #Init clusters

    for item in items:
        #Classify item into a cluster
        index = Classify(means,item);
        print("means "+str(means[index]))
        print("item "+str(item))
        x=[means[index][0],item[0]]
        y=[means[index][1],item[1]]
        plt.scatter(item[0],item[1],c=color[index],alpha=0.5,s=10);
        plt.pause(0.1)
        lines.append(plt.plot(x, y, linewidth=0.5,c=color[index],gid=1)[0])
        plt.pause(0.1)
        #print("firoz")
        #Add item to cluster
        clusters[index].append(item);

    return clusters;


###_Core Functions_###
def Classify(means,item):
    #Classify item to the mean with minimum distance

    minimum = sys.maxsize;
    index = -1;

    for i in range(len(means)):
        #Find distance from item to mean
        dis = EuclideanDistance(item,means[i]);
        if(dis < minimum):
            minimum = dis;
            index = i;

    return index;

def RecomputeCC(cluster,mean,i):
    mean_c=[0]*2
    for item in cluster:
        mean_c[0]=mean_c[0]+item[0]
        mean_c[1]=mean_c[1]+item[1]
    if(len(cluster)!=0):
        mean_c[0]=mean_c[0]/len(cluster)
        mean_c[1]=mean_c[1]/len(cluster)
    #return mean_c
    ret[i]=mean_c


def CalculateMeans(k,items,maxIterations=10):
    #Find the minima and maxima for columns
    cMin, cMax = FindColMinMax(items);
    #Initialize means at random points
    means = InitializeMeans(items,k,cMin,cMax);
    #print(means)
    #Calculate means
    for e in range(maxIterations):
        #If no change of cluster occurs, halt
        noChange = True;
        clusters = FindClusters(means,items);
        #print(clusters)
        t=[0]*k
        print(lines)
        for line in lines:
            #print(line)
            line.remove()
            plt.pause(0.1)
        lines.clear()
        for c in centroid:
            c.remove()
            plt.pause(0.1)
        centroid.clear()
        for i in range(len(means)):
            t[i]=th.Thread(target=RecomputeCC , args=(clusters[i],means[i],i,))
            #print("tid = "+str(t[i]))
            t[i].start()
        means_cth=[0]*k
        for i in range(len(means)):
            t[i].join()
            centroid.append(plt.scatter(ret[i][0],ret[i][1],c=color[i],alpha=0.5,s=50,marker="D"))
            #print(centroid)
            plt.pause(0.1)
            #print("means + "+str(ret[i]))
            if(means[i] != ret[i]):
                noChange = False


        #Nothing changed, return
        if(noChange):
            print("completedddddddddddddddddddddddddddd")
            break;
        for i in range(len(means)):
            means[i] = ret[i]
    FindClusters(means,items)
    return means;

def CutToTwoFeatures(items,indexA,indexB):
    n = len(items);
    X = [];
    for i in range(n):
        item = items[i];
        newItem = [item[indexA],item[indexB]];
        X.append(newItem);

    return X;


###_Main_###
def main():

    items = ReadData('data.txt');
    items = CutToTwoFeatures(items,2,3);
    #print(items)
    for item in items:
        plt.scatter(item[0],item[1],c="gray",alpha=0.5,s=10);
        plt.pause(0.1)
    k = 3;

    means = CalculateMeans(k,items);
    print (means);
    # for c in plt.collections:
    #     if(c.get_gid()==1):
    #         c.remove()
    #print (clusters);

    plt.show();
    #newItem = [5.4,3.7,1.5,0.2];
    #print Classify(means,newItem);

if __name__ == "__main__":
    main();
