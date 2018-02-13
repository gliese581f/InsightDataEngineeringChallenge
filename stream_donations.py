class ProcessDonations():    
    
    import numpy as np   #only dependency and almost always included in Python installations
        
    def __init__(self,donor_data,stat_data,output):  #create a list of passable files and data structures used between functions
        self.donor_data = donor_data
        self.stat_data  = stat_data
        self.container = {}
        self.qualified_donors = []
        self.output = output
        
    def readdata(self):   
        #Create a function designed to read election data and save to a dictionary only relevant, well-formed data.
        with open(self.donor_data,'rb') as election_data:
            #this with statement allows us to read data line by line
            for num,data in enumerate(election_data):
                fields = data.split('|')
                if fields[15] == '' and fields[10] >= 5 and fields[7] != '' and fields[13] != '' and fields[0] != '':
                    #this if statement culls only well-formed data, but note that it likely isn't exhaustive with respect to potential errors within large data pools
                    self.container[num] = {'CMTE_ID': fields[0], 'NAME':fields[7], 'ZIP_CODE':fields[10][0:5],'TRANSACTION_DT':fields[13],'TRANSACTION_AMT':fields[14]}
                    #ordering dictionary keys is necessary to at least try to maintain order of data later
        return self.container   #pass the cleaned election data
    
    def repeat_donors(self):
        #This function determines which donors are repeat donors and then passes a list of data containing the receipients, date of donation, amount of donation, and zipcode, which is the only data needed to generate output file.
        
        container = self.readdata()
        unique = []
        receipients = []

        #this O(n^2) loop sorts through the election data from readdata and determines which donors are 'unique', i.e. unique individuals, by looking for equivalent ordered pairs of name and zipcode. I then append relevant data to a list.
        for num in container.keys():
            for mun in container.keys():
                if [container[num]['NAME'],container[num]['ZIP_CODE']] == [container[mun]['NAME'],container[mun]['ZIP_CODE']] and mun != num:
                    unique.append( [container[num]['TRANSACTION_AMT'],int(container[num]['TRANSACTION_DT'][4:]),container[num]['CMTE_ID'],container[num]['NAME'],container[num]['ZIP_CODE']] )
   
               
        donorlist = dict([key,[]] for key in set(np.array(unique).T[3]))
        
        #for my sanity I convert 'unique' into a dictionary called donorlist. The entries in the list are, in order, 1) transaction amount, 2) transaction date, 3) cmte_id, and 4) zipcode. There's of course better ways to do this, but the list is used only for internal processing. The dictionary with have entries with donation info from each donor.
        for entry in xrange(len(unique)):
            for name in set(np.array(unique).T[3]):
                if unique[entry][3] == name:
                    donorlist[name].append( [unique[entry][0],unique[entry][1],unique[entry][2],unique[entry][4]] )
         
        #this O(n^3) loop structure looks for the receipients of the donations by looking at equivalent cmte_ids ([2]) and checks to see if the unique donors from above are also repeat donors, i.e. they've donated at least twice, which we can check by seeing if they have at least 2 donation entries. There is probably a better search algorithm, but the best case scenario is probably O(n^2) anyway. 
        for name in donorlist.keys():
            for forw in xrange(len(donorlist[name])):
                for reve in xrange(len(donorlist[name])): 
                    if donorlist[name][forw][2] == donorlist[name][reve][2] and forw != reve and len(donorlist[name])>=2:
                        receipients.append( donorlist[name][forw][2] )
        
        #by looping through the names of the donors, all of their donations, and looking for unique donor receipients (set(receipients)), I append to a list the qualified donations deliminated by the donation information we need in the ouput file.
        for name in donorlist.keys():
            for receipt in set(receipients):
                for entry in xrange(len(donorlist[name])):
                    if donorlist[name][entry][2] == receipt:
                        self.qualified_donors.append(donorlist[name][entry])
        
        receipients, donorlist,unique = None,None,None    #remove these unneeded data structures from memory (we might need to pass on the receipient list ...)
        
        return self.qualified_donors  #pass the qualified list list
    

    def outputdata(self):
        #this function creates an output file AND calculates the required statistics in one loop
        percentile = np.genfromtxt(self.stat_data)   #read the percentile you want to calculate from the file
        
        output_data = self.repeat_donors()  #call the qualifed donors from the previous function
        
        files = open(self.output,'wb')  #open an output file with a filename given in the instantiation of the class
        
        counts = 0   #old school way to generate counts needed in the output
        run_total = 0  #ditto a way to sum the donation totals
        for entry in xrange(len(output_data)-1):
            #as we loop through the output data, look for donations from 2018. This program isn't quite finished (I'm sorry) as we would need to loop through the receipients and include an if statement to cull that specific donation data for the receipients listed in the outdata list. The goal is to pass the first challenge here.
            if output_data[entry][1] == 2018:
                counts = counts+1 #create a running count
                length = len(output_data) -1
                run_total= run_total + float(output_data[entry][0]) 
                print >> files, output_data[entry][2]+'|'+output_data[entry][3]+'|'+str(output_data[entry][1])+'|'+output_data[int(np.ceil(percentile/100*counts))][0] +'|'+str(run_total)+'|'+str(counts) + '\n'
                print >> files, output_data[length][2]+'|'+output_data[length][3]+'|'+str(output_data[length][1])+'|'+output_data[int(np.ceil(percentile/100*(counts+1)))][0]+'|'+str(run_total + int(output_data[entry+1][0]))+'|'+str(counts+1)   #this prints relevant data to file using pipes. I need to separate print statement to handle the data that's cut-off by the loop.
                    
        files.close()
                    
        
donor_instance = ProcessDonations('itcont.txt','percentile.txt','donordata.txt')   
save_donordata = donor_instance.outputdata()
    
