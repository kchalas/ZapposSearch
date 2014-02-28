import urllib2
import json
from math import ceil
from collections import Counter


#iteration count
def iterations(lol):
    iteration = 1
    for i in lol:
        size = len(i)
        iteration *= size
    return iteration

#finds the new indeces to make a combo for
def maker(lol, make):
    new_make = []
    mk=make[:]
    mk.reverse()
    
    #find missing combinations
    for i in range(len(make)):
        #the length of list at index i from back of list
        lst = lol[len(lol)-i-1]
        list_at_i_len= len(lst) - 1
        
        #don't have to worry about restarting first list because
        #iterations in recursive method stops it
        if(mk[i] < list_at_i_len):
            mk[i] = mk[i] + 1
            break
        else:
            #increase index value
            mk[i] = 0
    mk.reverse()
    return mk


#recursive method for all combinations
def comb(lol, iteration, make, combos, times):
    #break statement that should end on all
    if(iteration == times):
        return combos
    
    #create next combination
    new_list = []
    for i in range(len(make)):
        new_list += [lol[i][make[i]]]

    combos+=[new_list]
    new_make = maker(lol, make)
    #recursive call to make the next combination
    times+=1
    return comb(lol, iteration, new_make, combos, times)

#finds unique values that are valid sums
def unique(products, total, tolerance):
    compare = lambda x,y:Counter(x) == Counter(y)
    indx = []
    for i in range(len(products)):
        for x in range(i+1, len(products)):
            if(compare(products[i], products[x])):
                if x not in indx:
                    indx+=[x]
    new_lst = []
    for i in range(len(products)):
        if i not in indx:
            if (sum(products[i]) <= (total+tolerance)):
                new_lst+=[products[i]]
        
    return new_lst

#Given a list of price ceilings and a dollar amount
#Finds combinations of prices that make a dollar amount

def find_index(target, prices, stride):
    val = -1
    counter = 0
    diff = 10000000000000000000000000
    indx = 0
    while(True):
        counter+=1
        try:
            val = prices.index(target)
            break
        except ValueError:
            target+=stride
        if(counter >= 100):
            #don't split list
            #giving the last index is most expensive
            #fails if statement and returns originals
            for i in range(len(prices)):
                difference=abs(target-prices[i])
                if (difference < diff):
                    indx = i
                    diff = difference
            return indx
    return val


def shift_two(ttl, target, prices, stride, tolerance):
    #shift two numbers away from each other a proportional amount
    for i in range(len(prices)):
        t1=find_index(target+stride, prices, stride)
        left_over = ttl-prices[t1]
        t2 = 0
        if (left_over > 0):
            t2=find_index(ttl-prices[t1], prices, (-stride))
        
    return [prices[t1], prices[t2]]
    



def value_findr(split_up, split_down, prices, stride, total, tolerance):
    threads = split_up+split_down
    avg = total/threads
    record = []
    array = []
    
    for i in range(threads):
        array+=[avg]
    record+=[array]
    
    upper_bound = total+tolerance
    lower_bound = total-tolerance
    
    #start in the middle and work outwards, keeping interim values
    up_indx = split_down
    dn_indx = split_down-1
    toggle = True
    down = True
    up = True
    for i in range(threads-1):
        #different beginning case
        if (toggle):
            #middle should have same values returned(bigger, smaller)
            ttl = array[up_indx]+array[dn_indx]
            two = shift_two(ttl, array[up_indx], prices, stride, tolerance)
            array[up_indx] = two[0]
            array[dn_indx] = two[1]
            record+=[array] #should be one valid solution
            toggle = False
        else:
            #need temps because they return valid solutions,
            #so save modifying array until it comes time to combine
            temp_up = array[:]
            temp_down = array[:]
            #solutions that mostly focus on lower values
            if(down):
                ttl = temp_down[dn_indx+1]+temp_down[dn_indx]
                two = shift_two(ttl, temp_down[dn_indx+1], prices, stride, tolerance)
                temp_down[dn_indx+1] = two[0] 
                temp_down[dn_indx] = two[1]
                record+=[temp_down]
            #solutions with more expensive items
            if(up):
                ttl = temp_up[up_indx]+temp_up[up_indx-1]
                two = shift_two(ttl, temp_up[up_indx-1], prices, stride, tolerance)
                temp_up[up_indx] = two[0] 
                temp_up[up_indx-1] = two[1]
                record+=[temp_up]
            #combination
            if (up and down):
                for i in range(threads):
                    if (i < split_down):
                        array[i] = temp_down[i]
                    else:
                        array[i] = temp_up[i]
                record+=[array]
                    
            #recombine into single array and make that a separate solution
        #continuity checks
        if (dn_indx-1 >= 0):
            dn_indx-=1
        else:
            down = False
        if (up_indx+1 < len(array)):
            up_indx+=1
        else:
            up = False 
    return record



#combines the results of different splits of expensive and inexpensive
def combine_vals(prices, total, n):
    #given the list of price ceilings find valid combinations
    tolerance = int(ceil(total * .1))
    #make stride 1 percent of total
    stride = int(ceil((total+tolerance) * .01))
    #first ask if val is a valid value, find closest index
    #val is the most expensive item you can buy given that you buy with
    cheap = (prices[0] * (n-1)) #the cheapest items
    val = total - cheap #limit
    index = find_index(val, prices, stride)
    subset = prices[0:index] #hopefully smaller set to work with
    #insert as first solution
    temp = []
    for i in range(n):
        temp+=[prices[0]]
        
    temp[0] = prices[index]
    record = [temp]
    for i in range(1, n):
        #want to get combinations of cheap and expensive items if valid
        #case: all average price range = even relationship with people = friends
        #case: boss and workers, wife and kids unevenness 
        record+=(value_findr(n-i, i, subset, stride, total, tolerance))
    
    record = unique(record, total, tolerance)
    return record  


######################################SEARCH#####################################

def searchZappos(n, total):
    #check valid inputs
    if(n <= 0 or total <= 0):
        return "Invalid Inputs"
    
    #url for request and setup
    limit = 10
    parse = []
    url = 'http://api.zappos.com/Search?term=&key=a73121520492f88dc3d33daf2103d7574f1a3166&page='
    for i in range(limit):
        try:
            val = url + str(i)
            get = urllib2.urlopen(val).read()
            #Interpret response
            data = json.loads(get.decode('utf8'))
            #accumulate results
            parse += data["results"]
        except urllib2.HTTPError:
            #gone too far, no pages 
            break
    
    prices = []
    diction = {}
    
    if (parse == []):
        #when I was testing, API results were being throttled
        print "HTTP ERROR: results not found"
        return
    
    #keep only products and prices
    for i in parse:
        prod = i["productId"]
        string = i["price"]
        string = int(ceil(float(string[1:])))
        if (string in diction):
            lst = diction[string]
            lst+= [prod]
            diction[string] = lst
        else:
            diction[string] = [prod]
            prices+=[string]
    #special case
    if (n == 1):
        indx = find_index(total, prices, 1)
        return diction[prices[indx]]
        
    prices.sort()
    record = combine_vals(prices, int(ceil(total)), n)
    
    #should have valid price combinations in record, now construct products
    make = [] #indexing for combinations
    for i in range(n):
        make+=[0]
    finals = []
    
    for i in range(len(record)):
        prods = []
        for x in range(len(record[i])):
            prods+=[diction[record[i][x]]]
        iterate = iterations(prods)
        #cap at 100 per price combination
        if (iterate > 100):
            iterate = 100
        finals+=comb(prods, iterate, make, [], 0)
    print finals
    return finals
