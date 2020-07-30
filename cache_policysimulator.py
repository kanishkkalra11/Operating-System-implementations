# -*- coding: utf-8 -*-
"""CS301_Assignment2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1q59JuOJKTWTF_oDdFTrJdKHhWZboaeIZ
"""

import random
import math
import matplotlib.pyplot as plt
from tabulate import tabulate

class BaseSimulator:

    def __init__(self, workload, cache_size):
        self.workload = workload
        self.cache_size = cache_size

    def LRU(self):
        workload = self.workload
        cache_size = self.cache_size
        cache = [0]*cache_size
        hits = 0
        cache_left = cache_size
        hitmiss = []
        evict = []
        resultingcache = []
        for i in workload:
            if i not in cache:
                hitmiss.append('Miss')
                if cache_left == 0:
                    evict.append(cache[-1])
                    cache = [i] + cache[:-1]
                else:
                    evict.append(0)
                    cache = [i] + cache[:-1]
                    cache_left -= 1
            else:
                hitmiss.append('Hit')
                hits += 1
                index = cache.index(i)
                cache = [i] + cache[:index] + cache[index+1:]
                evict.append(0)
            resultingcache.append(cache)
        return (hits/len(workload))*100 , hitmiss , evict , resultingcache

    def approx_LRU(self):
        workload = self.workload
        cache_size = self.cache_size
        cache = [0]*cache_size
        hits = 0
        cache_left = cache_size
        usebits = [0]*100
        useind = 0
        hitmiss = []
        evict = []
        resultingcache = []
        for i in workload:
            if i not in cache:
                hitmiss.append('Miss')
                if cache_left == 0:
                    work = cache[useind]
                    while(usebits[work-1] != 0):
                        usebits[work-1] = 0
                        useind = (useind+1)%cache_size
                        work = cache[useind]
                    evict.append(work)
                    cache[useind] = i
                else:
                    evict.append(0)
                    cache[cache_size-cache_left] = i
                    usebits[i-1] = 1
                    cache_left -= 1
            else:
                evict.append(0)
                hitmiss.append('Hit')
                hits += 1
                usebits[i-1] = 1
            resultingcache.append(cache)
        return (hits/len(workload))*100 , hitmiss , evict , resultingcache

    def FIFO(self):
        workload = self.workload
        cache_size = self.cache_size
        cache = [0]*cache_size
        hits = 0
        cache_left = cache_size
        hitmiss = []
        evict = []
        resultingcache = []
        for i in workload:
            if i not in cache:
                hitmiss.append('Miss')
                evict.append(cache[0])
                cache = cache[1:]
                cache.append(i)
                if cache_left != 0:
                    cache_left -= 1
            else:
                evict.append(0)
                hitmiss.append('Hit')
                hits += 1
            resultingcache.append(cache)
        return (hits/len(workload))*100 , hitmiss , evict , resultingcache

    def LFU(self):
        workload = self.workload
        cache_size = self.cache_size
        cache = [0]*cache_size
        hits = 0
        cache_left = cache_size
        freqlist = [0]*100
        hitmiss = []
        evict = []
        resultingcache = []
        for i in workload:
            if i not in cache:
                hitmiss.append('Miss')
                if cache_left == 0:
                    index_to_be_removed = 0
                    minimum = freqlist[cache[0]-1]
                    for j in range(1,len(cache)):
                        if freqlist[cache[j]-1]<minimum:
                            minimum = freqlist[cache[j]-1]
                            index_to_be_removed = j
                    evict.append(cache[index_to_be_removed])
                    cache[index_to_be_removed] = i
                    freqlist[i-1] += 1
                else:
                    evict.append(0)
                    cache[cache_size-cache_left] = i
                    freqlist[i-1] += 1
                    cache_left -= 1
            else:
                evict.append(0)
                hitmiss.append('Hit')
                hits += 1
                freqlist[i-1] += 1
            resultingcache.append(cache)
        return (hits/len(workload))*100 , hitmiss , evict , resultingcache

    def Random(self):
        workload = self.workload
        cache_size = self.cache_size
        cache = [0]*cache_size
        hits = 0
        cache_left = cache_size
        hitmiss = []
        evict = []
        resultingcache = []
        for i in workload:
            if i not in cache:
                hitmiss.append('Miss')
                if cache_left == 0:
                    index_to_be_replaced = random.randint(0,cache_size-1)
                    evict.append(cache[index_to_be_replaced])
                    cache[index_to_be_replaced] = i
                else:
                    evict.append(0)
                    cache[cache_size-cache_left] = i
                    cache_left -= 1
            else:
                evict.append(0)
                hitmiss.append('Hit')
                hits += 1
            resultingcache.append(cache)
        return (hits/len(workload))*100 , hitmiss , evict , resultingcache

    def Oracle(self):
        workload = self.workload
        cache_size = self.cache_size
        cache = [0]*cache_size
        hits = 0
        cache_left = cache_size
        hitmiss = []
        evict = []
        resultingcache = []
        already_read = 0
        for i in workload:
            already_read += 1
            if i not in cache:
                hitmiss.append('Miss')
                if cache_left == 0:
                    nextwork = workload[already_read:]
                    if cache[0] in nextwork:
                        nextindex = nextwork.index(cache[0])
                    else:
                        nextindex = math.inf
                    index_to_be_replaced = 0
                    for j in range(1,len(cache)):
                        if cache[j] in nextwork:
                            index = nextwork.index(cache[j])
                        else:
                            index = math.inf
                        if index > nextindex:
                            index_to_be_replaced = j
                            nextindex = index
                    evict.append(cache[index_to_be_replaced])
                    cache[index_to_be_replaced] = i
                else:
                    evict.append(0)
                    cache[cache_size-cache_left] = i
                    cache_left -= 1
            else:
                evict.append(0)
                hitmiss.append('Hit')
                hits += 1
            resultingcache.append(cache)
        return (hits/len(workload))*100 , hitmiss , evict , resultingcache

class WorkloadSimulator:

    def __init__(self, workload_type):
        self.workload_type = workload_type

    def workloadcreator(self):
        workload_type = self.workload_type
        if workload_type == 'No-Locality':
            workload = [random.randint(1,100) for i in range(10000)]
            random.shuffle(workload)
        elif workload_type == '80-20':
            workload1 = [random.randint(1,20) for i in range(8000)]
            workload2 = [random.randint(21,100) for i in range(2000)]
            workload = workload1 + workload2
            random.shuffle(workload)
        elif workload_type == 'Looping-Sequential':
            workload = []
            for i in range(50):
                workload.append(i+1)
            workload *= 200
        return workload

    def plot(self):
        workload_type = self.workload_type
        cache_sizes = range(1,101)
        hitrates_LRU = []
        hitrates_approx_LRU = []
        hitrates_FIFO = []
        hitrates_LFU = []
        hitrates_Random = []
        hitrates_Oracle = []
        for i in cache_sizes:
            simulator = BaseSimulator(self.workloadcreator(),i)
            hit , hitmiss , evict , resultingcache = simulator.LRU()
            hitrates_LRU.append(hit)
            hit , hitmiss , evict , resultingcache = simulator.approx_LRU()
            hitrates_approx_LRU.append(hit)
            hit , hitmiss , evict , resultingcache = simulator.FIFO()
            hitrates_FIFO.append(hit)
            hit , hitmiss , evict , resultingcache = simulator.LFU()
            hitrates_LFU.append(hit)
            hit , hitmiss , evict , resultingcache = simulator.Random()
            hitrates_Random.append(hit)
            hit , hitmiss , evict , resultingcache = simulator.Oracle()
            hitrates_Oracle.append(hit)
        plt.plot(cache_sizes,hitrates_LRU)
        plt.plot(cache_sizes,hitrates_approx_LRU)
        plt.plot(cache_sizes,hitrates_FIFO)
        plt.plot(cache_sizes,hitrates_LFU)
        plt.plot(cache_sizes,hitrates_Random)
        plt.plot(cache_sizes,hitrates_Oracle)
        plt.legend(['LRU','approx_LRU','FIFO','LFU','Random','Oracle'])
        plt.xlabel('Cache Size')
        plt.ylabel('Hit Rate')
        plt.title(workload_type)
        plt.show()

a = WorkloadSimulator('No-Locality')
a.plot()

a = WorkloadSimulator('80-20')
a.plot()

a = WorkloadSimulator('Looping-Sequential')
a.plot()

trace_workload = [1,2,3,1,2,4,1,4,2,3,2]
cache_size = 3
a = BaseSimulator(trace_workload,cache_size)

hit , hitmis , evict , resultingcache = a.LRU()
final = []
for i in range(len(trace_workload)):
    l = []
    l.append(trace_workload[i])
    l.append(hitmis[i])
    if(evict[i] == 0):
        l.append('')
    else:
        l.append(evict[i])
    l.append(resultingcache[i])
    final.append(l)
print('Tracking the LRU Policy\n')
print(tabulate(final, headers=['Access', 'Hit/Miss?' , 'Evict' , 'Resulting Cache State']))

hit , hitmis , evict , resultingcache = a.approx_LRU()
final = []
for i in range(len(trace_workload)):
    l = []
    l.append(trace_workload[i])
    l.append(hitmis[i])
    if(evict[i] == 0):
        l.append('')
    else:
        l.append(evict[i])
    l.append(resultingcache[i])
    final.append(l)
print('Tracking the Approx. LRU Policy\n')
print(tabulate(final, headers=['Access', 'Hit/Miss?' , 'Evict' , 'Resulting Cache State']))

hit , hitmis , evict , resultingcache = a.FIFO()
final = []
for i in range(len(trace_workload)):
    l = []
    l.append(trace_workload[i])
    l.append(hitmis[i])
    if(evict[i] == 0):
        l.append('')
    else:
        l.append(evict[i])
    l.append(resultingcache[i])
    final.append(l)
print('Tracking the FIFO Policy\n')
print(tabulate(final, headers=['Access', 'Hit/Miss?' , 'Evict' , 'Resulting Cache State']))

hit , hitmis , evict , resultingcache = a.LFU()
final = []
for i in range(len(trace_workload)):
    l = []
    l.append(trace_workload[i])
    l.append(hitmis[i])
    if(evict[i] == 0):
        l.append('')
    else:
        l.append(evict[i])
    l.append(resultingcache[i])
    final.append(l)
print('Tracking the LFU Policy\n')
print(tabulate(final, headers=['Access', 'Hit/Miss?' , 'Evict' , 'Resulting Cache State']))

hit , hitmis , evict , resultingcache = a.Random()
final = []
for i in range(len(trace_workload)):
    l = []
    l.append(trace_workload[i])
    l.append(hitmis[i])
    if(evict[i] == 0):
        l.append('')
    else:
        l.append(evict[i])
    l.append(resultingcache[i])
    final.append(l)
print('Tracking the Random Policy\n')
print(tabulate(final, headers=['Access', 'Hit/Miss?' , 'Evict' , 'Resulting Cache State']))

hit , hitmis , evict , resultingcache = a.Oracle()
final = []
for i in range(len(trace_workload)):
    l = []
    l.append(trace_workload[i])
    l.append(hitmis[i])
    if(evict[i] == 0):
        l.append('')
    else:
        l.append(evict[i])
    l.append(resultingcache[i])
    final.append(l)
print('Tracking the Oracle Policy\n')
print(tabulate(final, headers=['Access', 'Hit/Miss?' , 'Evict' , 'Resulting Cache State']))