
# coding: utf-8

# In[1]:


import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from apyori import apriori
import warnings
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import scale
from IPython.lib.pretty import pretty
import pprint
import csv
import pyfpgrowth
import itertools as itertools


# In[2]:


def readMainData(filePath): #READS THE MAIN DATA
    mainData = pd.read_csv(filePath)
    return mainData


# In[3]:


def readSKUData(filePath): #READS THE SKU DATA
    SKUData = pd.read_csv(filePath)
    return SKUData


# In[4]:


def setUpMainData(mainData):
    apriori_cols = ['Order Number', 'Seller SKU','CATEGORY']
    apriori_list = mainData[apriori_cols]

    #REPLACES SPACES WITH UNDERSCORES
    apriori_list.columns = [c.replace(' ', '_') for c in apriori_list.columns]
    return apriori_list


# In[5]:


#This function does not remove bundles. It tags products to an SKU

def mapProductAndSKU(apriori_list):
    ret = {}
    BOMFilteredList = []
    categoryDictionary = {}
    #pprint.pprint(sku_list)
    SKUList = apriori_list["Seller_SKU"]
    #print(type(SKUList))
    SKUs = list(set(SKUList.tolist()))

    for x in SKUs:
        if "-" in x: # "-" is the identifier for BOMS in the dataset
              pass
        else:
            BOMFilteredList.append(x)
    for x in BOMFilteredList:
        item = apriori_list[apriori_list.Seller_SKU == x]
        category = (item.iloc[0]["CATEGORY"])
        categoryDictionary[x] = category

    ret = categoryDictionary

    return ret


# In[6]:


def setUpSKUDescriptionData(SKUData):
    sku_cols = ['BARCODE' , 'DESCRIPTION']

    sku_list = SKUData[sku_cols]

    SKUList = sku_list["BARCODE"]

    SKUs2 = list(set(SKUList.tolist()))

    BOMFilteredList2 = []
    descriptionDictionary = {}

    for x in SKUs2:
        if "-" in x:
            pass
        else:
            BOMFilteredList2.append(x)

    for x in BOMFilteredList2:
        item = sku_list[sku_list.BARCODE == x]
        description = (item.iloc[0]["DESCRIPTION"])
        descriptionDictionary[x] = description

    return descriptionDictionary



# In[7]:


#TODO ADD PARAMETER IF USER WANTS TO REMOVE EXISTING BUNDLES
def removeBundles(items):
    bundleFilteredList = []
    for x in items:
        string = ""
        temp = []
        for y in x:
            if "-" in y:
                pass
            else:
                temp.append(y)
        if temp != []:
            bundleFilteredList.append(temp)

    return bundleFilteredList


# In[8]:


def filterByCategory(items, category):
    categoryFilteredList = []
    for x in items:
        string = ""
        temp = []
        for y in x:
            if categoryDictionary[y] == category:
                temp.append(y)
            else:
                pass
        if temp != []:
            tempSet = list(set(temp))
            categoryFilteredList.append(tempSet)
    return categoryFilteredList


# In[9]:


#TODO ADD PARAMETER IF USER WANTS TO REMOVE BASKETS WITH SPECIFIC NUMBER OF ITEMS
def removeByNumberOfItems(items , count):
    itemCountFilteredList = []
    for x in items:
        if len(x) > count:
            itemCountFilteredList.append(x)
    return itemCountFilteredList


# In[10]:


#ONLY ADD BASKETS WITH DIFFERENT CATEGORY FOR EACH ITEM

def filterBasketWithDifferentItems(items, categoryDictionary):
   categoryFilteredList = []
   for basket in items:
       string = ""
       temp = []
       iterable_list = basket

       for x,y in itertools.combinations(iterable_list, 2):
           if categoryDictionary[x] != categoryDictionary[y]:
               temp.append(x)
               temp.append(y)
           else:
               pass
       if temp != []:
           tempSet = list(set(temp))
           categoryFilteredList.append(temp)
   return categoryFilteredList


# In[11]:


#RemoveBundles, CategoryFilter, MinimumCategory, ItemsWithDifferentCategory
def finalizeList(mainDataPath, filterBundles, filterByNumberOfItems, filterBasketWithDifferentItemCategories):
    finalList = []
    returnedList  = []
    aprioriList = readMainData(mainDataPath) #INSRT PATH
    aprioriList = setUpMainData(aprioriList)
    groupedAprioriList = aprioriList.groupby("Order_Number")["Seller_SKU"].apply(list)


    categoryDictionary = mapProductAndSKU(aprioriList)
    #pprint.pprint(grouped_apriori_list)

    finalList = groupedAprioriList.values.tolist()


    if(filterBundles == True):
        finalList = removeBundles(finalList)
    #category_filtered_list = filterByCategory(new_unfiltered_list, CATEGORY)
    finalList = removeByNumberOfItems(finalList, filterByNumberOfItems)

#     if(filterItemsWithDifferentItemCategories == True):
#         finalList = filterBasketWithDifferentItems(finalList, categoryDictionary)

    for x in finalList:
        if len(x) > 1:
            returnedList.append(x)

    #pprint.pprint(final_list)

    return returnedList


# In[15]:



def aprioriAlgorithm(mainDataPath, SKUDataPath, filterBundles, filterByNumberOfItems, filterByCategory, filterBasketWithDifferentItemCategories):
    final_list = finalizeList(mainDataPath , filterBundles, filterByNumberOfItems, filterBasketWithDifferentItemCategories)
    association_rules = apriori(final_list, min_support=0.005, min_confidence=0.001, min_lift=0.01)
    association_results = list(association_rules)
    pprint.pprint(association_results)
    # skuData = readSKUData(SKUDataPath)
    # descriptionDictionary = setUpSKUDescriptionData(skuData)
    # out = ""
    # print(association_results)
    # for x in association_results:
    #     sets = x[0]
    #     #print(sets)
    #     support =  str(x[1])
    #     #print(support)
    #     confidence = str(x[2][0][2])
    #     test = ([y for y in sets])
    #     string = ""
    #     if(len(sets) > 1):
    #         for z in test:
    #             itemName = descriptionDictionary[z]
    #             string += itemName + " | "
    #             string += z + " | "
    #         out += string + "," + support + "," + confidence + "\n"
    #         #print(string + "\n")
    #     else:
    #         pass
    # #print(out)
    # csv = open("aprioriOut.csv" , "w")
    # csv.write(out)
    # csv.close()


# In[16]:


mainDataPath = "/home/adrian/Documents/Thesis Software/Thesis_Jupyters/00 - 2018 Compiled - Seller center data.csv"
SKUDataPath = "/home/adrian/Documents/Thesis Software/Thesis_Jupyters/SKUList.csv"
filterBundles = True
filterByNumberOfItems = 1
filterByCategory = ""
filterBasketWithDifferentItemCategories = True
aprioriAlgorithm(mainDataPath, SKUDataPath, filterBundles, filterByNumberOfItems, filterByCategory ,filterBasketWithDifferentItemCategories)
