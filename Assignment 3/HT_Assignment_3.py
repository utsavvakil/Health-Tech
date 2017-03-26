
# coding: utf-8

# In[1]:

import xml.etree.ElementTree as ET
from matplotlib import pyplot as plt
import scipy.stats
tree = ET.parse('export.xml')
root = tree.getroot()


# In[2]:

data_type = []
data_start_date = []
data_end_date = []
data_value = []
for record in root.findall('Record'):
    data_type.append(record.get('type'))
    data_start_date.append(record.get('startDate'))
    data_end_date.append(record.get('endDate'))
    data_value.append(record.get('value'))
    


# In[3]:

dict_type = {}
for i in range(len(data_type)):
    val = data_type[i]
    if dict_type.get(val,-1) == -1:
        dict_type[val] = []
    dict_type[val].append([data_start_date[i],data_end_date[i],data_value[i]])


# In[4]:

dict_type.keys()


# In[5]:

def getDaily(identifier):
    dict_identifier = {}
    for record in (identifier):
        if dict_identifier.get(record[1][:10],-1) == -1:
            dict_identifier[record[1][:10]] = 0.0
        dict_identifier[record[1][:10]] += float(record[2])
    return dict_identifier


# In[6]:

dict_dist_daily = getDaily(dict_type['HKQuantityTypeIdentifierDistanceWalkingRunning'])
dict_calories_daily = getDaily(dict_type['HKQuantityTypeIdentifierActiveEnergyBurned'])


# In[7]:

dict_dist_hourly = {}
for record in (dict_type['HKQuantityTypeIdentifierDistanceWalkingRunning']):
    if dict_dist_hourly.get(record[1][:10],-1) == -1:
        dict_dist_hourly[record[1][:10]] = [0]*24
    dict_dist_hourly[record[1][:10]][int(record[1][11:13])] += float(record[2])


# In[8]:

dict_sleep_daily = {}
days = []
for record in (dict_type['HKQuantityTypeIdentifierDistanceWalkingRunning']):
    day = record[1][:10]
    if day not in days:
        days.append(day)
    if dict_sleep_daily.get(day,-1) == -1:
        dict_sleep_daily[day] = [0]*2
    count = 0
    for val in dict_dist_hourly[day][:12]:
        if val == 0:
            count += 1
    dict_sleep_daily[day][0] = count
    count = 0
    for val in dict_dist_hourly[day][12:]:
        if val == 0:
            count += 1
    dict_sleep_daily[day][1] = count


# In[9]:

dict_day_sleep = {}
for i in range(len(days)-1):
    dict_day_sleep[days[i]] = dict_sleep_daily[days[i]][1] + dict_sleep_daily[days[i+1]][0]


# In[10]:

days_common = []
for record in (dict_type['HKQuantityTypeIdentifierActiveEnergyBurned']):
    day = record[1][:10]
    if day in days and day not in days_common:
        days_common.append(day)


# In[11]:

data_dist, data_calories, data_sleep = [], [], []
for i in range(len(days_common)-1):
    data_dist.append(dict_dist_daily[days_common[i]])
    data_calories.append(dict_calories_daily[days_common[i]])
    data_sleep.append(dict_day_sleep[days_common[i+1]])
    


# In[12]:

data_dist = [(float(x)-min(data_dist))/(max(data_dist)-min(data_dist)) for x in data_dist]
data_calories = [(float(x)-min(data_calories))/(max(data_calories)-min(data_calories)) for x in data_calories]
data_sleep = [(float(x)-min(data_sleep))/(max(data_sleep)-min(data_sleep)) for x in data_sleep]


# In[13]:

plt.plot(data_dist[::3],'g',label = "Distance walked (miles)")
plt.plot(data_sleep[::3],'b', label = "Hours of sleep")
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.xlabel("Day #")
plt.savefig("dist_vs_sleep.png",figsize=(8,40),transparent = True, bbox_inches='tight', pad_inches=0)
plt.show()


# In[14]:

plt.plot(data_calories[::3],'orange',label = "Calories burned (kcal)")
plt.plot(data_sleep[::3],'b', label = "Hours of sleep")
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.xlabel("Day #")
plt.savefig("cal_vs_sleep.png",figsize=(8,40),transparent = True, bbox_inches='tight', pad_inches=0)
plt.show()


# In[15]:

plt.scatter(data_dist,data_calories)
plt.xlabel("Distance walked (miles)")
plt.ylabel("Calories burned (kcal)")
plt.savefig("dist_vs_cal.png",figsize=(8,40),transparent = True, bbox_inches='tight', pad_inches=0)
plt.show()


# In[16]:

scipy.stats.pearsonr(data_dist, data_calories)

