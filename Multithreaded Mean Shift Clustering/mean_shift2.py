import math #For pow and sqrt
import sys
import matplotlib.pyplot as plt
from random import shuffle, uniform
import threading as th
import numpy as np
import time

X=[]
no_th=10
look_distance=3   #0.8
kernel_bandwidth=2
no_iter=6
circles=[]
ind=0
fig=plt.figure()
plt.suptitle('Mean Shift Clustering',fontsize=20)
plt.xlabel('x---> Axis')
plt.ylabel('y---> Axis')
###_Pre-Processing_###
def ReadData(fileName):
    #Read the file, splitting by lines
    f = open(fileName,'r');
    liness = f.read().splitlines();
    f.close();

    items = [];

    for i in range(0,len(liness)):
        line = liness[i].split(',');
        itemFeatures = [];

        for j in range(len(line)):
            v = float(line[j]); #Convert feature value to float
            itemFeatures.append(v); #Add feature value to dict

        items.append(itemFeatures);

    shuffle(items);
    return items;


def euclid_distance(x,y):
    S = 0; #The sum of the squared differences of the elements
    for i in range(len(x)):
        S += math.pow(x[i]-y[i],2);
    ret=math.sqrt(S)
    #print("euuci"+str(ret))
    return ret; #The square root of the sum

def neighbourhood_points(X, x_centroid, distance):
    eligible_X = []
    for x in X:
        distance_between = euclid_distance(x, x_centroid)
        # print('Evaluating: [%s vs %s] yield dist=%.2f' % (x, x_centroid, distance_between))
        if distance_between <= distance:
            eligible_X.append(x)
    return eligible_X

def gaussian_kernel(distance, bandwidth):
    val = (1/(bandwidth*math.sqrt(2*math.pi))) * np.exp(-0.5*((distance / bandwidth))**2)
    return val

def runner(X,x,i):
    ### Step 1. For each datapoint x E X, find the neighbouring points N(x) of x.
    neighbours = neighbourhood_points(X, x, look_distance)

    ### Step 2. For each datapoint x E X, calculate the mean shift m(x).
    numerator = [0,0]
    denominator = 0
    for neighbour in neighbours:
        distance = euclid_distance(neighbour, x)
        weight = gaussian_kernel(distance, kernel_bandwidth)
        numerator[0] += (weight * neighbour[0])
        numerator[1] += (weight * neighbour[1])
        denominator += weight

    new_x=[0,0]
    new_x[0] = numerator[0] / denominator
    new_x[1] = numerator[1] / denominator

        ### Step 3. For each datapoint x E X, update x <- m(x).
    X[i] = new_x

    print(new_x)


def meanShift(original_X):

    X = np.copy(original_X)
    past_X = [[0,0]]*len(X)
    print("l = "+str(len(X)))
    already_joined=[]
    for it in range(no_iter):
        t=[0]*len(X)

        for i in range(0,len(X)):       #for i, x in enumerate(X):

            #for j in range(no_th):
            print("i = "+str(i))
                # print("i+j = "+str(i+j))
                # print("Xi+j = "+str(X[i+j]))

            t[i]=th.Thread(target=runner , args=(X,X[i],i,))
            t[i].start()
            if(past_X[i][0]==X[i][0] and past_X[i][1]==X[i][1]):
                t[i].join()
                    # plt.scatter(X[i+j][0],X[i+j][1],c="red",alpha=0.5,s=50,marker="D")
                circle=plt.Circle((X[i][0],X[i][1]),radius=look_distance,fill=False,color='b')
                plt.gcf().gca().add_artist(circle)
                circles.append(circle)
                plt.pause(0.0001)
                already_joined.append(i)
                #time.sleep(5)
                #t[j].join()
        for i in range(len(X)):
            if (i not in already_joined):
                t[i].join()
                # plt.scatter(X[i+j][0],X[i+j][1],c="red",alpha=0.5,s=50,marker="D")
                circle=plt.Circle((X[i][0],X[i][1]),radius=look_distance,fill=False,color='b')
                plt.gcf().gca().add_artist(circle)
                circles.append(circle)
                plt.pause(0.0001)

        for c in circles:
            c.remove()
            plt.pause(0.0001)
        circles.clear()

        past_X=np.copy(X)
    unique=[]
    color=["red","blue","green","purple","yellow","orange","pink","cyan","black","magenta"]
    for i in range(len(X)):
        flag=0
        for j in range(len(unique)):
            if(euclid_distance(X[i],unique[j]) < 0.1 ):
                flag=1
                break
        if(flag==0):
            unique.append(X[i])
    print(unique)
    for i in range(len(X)):
        for j in range(len(unique)):
            if(euclid_distance(X[i],unique[j]) < 0.1):
                ind=j
        plt.scatter(original_X[i][0],original_X[i][1],c=color[ind],alpha=0.5,s=10)
        plt.pause(0.0001)




def CutToTwoFeatures(items,indexA,indexB):
    n = len(items);
    X = [];
    for i in range(n):
        item = items[i];
        newItem = [item[indexA],item[indexB]];
        X.append(newItem);

    return X;

def main():

    items = ReadData('data1.txt')
    items = CutToTwoFeatures(items,0,1)
    print(items)
    for item in items:
        plt.scatter(item[0],item[1],c="gray",alpha=0.5,s=10)
        plt.pause(0.00001)

    meanShift(items)
    plt.show();

if __name__ == "__main__":
    main();
