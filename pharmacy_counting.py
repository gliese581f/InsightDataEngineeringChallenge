import numpy as np

def readdata(files):
    #This function reads in the data sequentially and stores relevant data to a dictionary/hash table
    dic = {}
    with open(files,'rb') as data:
        for num,lines in enumerate(data):
            fields = str(lines).split(',')
            if num == 1:
                dic[fields[-2]] = []
                dic[fields[-2]].append([fields[-3],fields[1],float(fields[-1][:-3])])
            elif num > 1 and fields[-2] in dic.keys():
                dic[fields[-2]].append([fields[-3],fields[1],float(fields[-1][:-3])])
            elif num > 1 and fields[-2] not in dic.keys():
                dic[fields[-2]] = []
                dic[fields[-2]].append([fields[-3],fields[1],float(fields[-1][:-3])])
    return dic

def total_cost(data,keys):
    #This function calculates the total cost of each prescribed medication
    temp = [ float(values[2]) for values in data[keys] ]    
    return int(round(np.sum(temp)))
        
def num_prescribed(data,keys):
    #This function calculates the number of unique prescribers for each medication
    temp = [ values[0]+values[1] for values in data      ]  
    return len(set(temp))

def printdata(data):
    #This function prints the data to file according the specified format
    print('drug_name,num_prescriber,total_cost',file=open('top_cost_drug.txt','a'))

    for keys in data.keys():
        print(keys+','+str(total_cost(data,keys))+','+str(num_prescribed(data,keys)),file=open('top_cost_drug.txt','a'))
      
if __name__ == "__main__":
    
    datas = readdata('de_cc_data.txt')
    printdata(datas)
    
    

def readdata(files):
    #This function reads in the data sequentially and stores relevant data to a dictionary/hash table
    temp = []
    with open(files,'rb') as data:
        for num,lines in enumerate(data):
            fields = str(lines).split(',')
            if num == 1:
                temp.append( fields[-2] )
            elif num > 1 and fields[-2] not in temp:
                temp.append (fields[-2] )
    return temp




def process_and_print_data(prescript,files):
    dic = {}
    dic[prescript] = []
    with open(files,'rb') as data:
        for num,lines in enumerate(data):
            fields = str(lines).split(',')
            if fields[-2] == prescript:
                dic[prescript].append([fields[-3],fields[1],float(fields[-1][:-3])])
               
    return dic



if __name__ == "__main__":
    
    #datas = readdata('de_cc_data.txt')
    for ii in te:
        printdata(process_and_print_data(ii,'de_cc_data.txt.txt'))
    
    
