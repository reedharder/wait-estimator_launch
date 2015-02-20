# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 20:16:02 2014

@author: Reed
"""


import numpy as np


'''
#acute, prev, chron
#number of patient categories (not differentiated by visit type)
num_classes=96
#patient urgency by index (True or False, i.e. whether they qualify for same day appointments)
urgencies=np.array([True]*num_classes + [False]*(num_classes*2))
#frequencies for each category (including visit type)
freqs=np.array([.013]*(num_classes*3))
#visit durations for each category (including visit type)
durs=np.array([20]*(num_classes*3))
nums=np.array([30]*(num_classes*3))
phys_mins={1:580,2:580,3:520, 4:520} # PHYS MINS CALCULATED TAKING INTO ACCOUNT CARVEOUT
#urgent patient time set aside
phys_carve_out={1:0,2:0,3:60, 4:60} 
# minutes available per day for each nurse
non_phys_mins={1:480,2:480}
#keys: patients, values: nurses that can see them
nurse_dict={1:[1,2],2:[2]}
#index is class, value is affiliated doctor. 0 is ANY DOCTOR
doc_lookup=np.array([1,2,3,4]*(24*3))
'''

#np.repeat(np.array([0,1,2,3,4]),np.array([0,72,72,72,72]))
#cutoffs for wait times for each class and overall, (percentage, limit)
'''
exp_sload={'Acute':(100,50), 'Preventative':(100,50) , 'Chronic': (100,50), 'Overall':(100,50) ,} 
'''
days=100

def mat_sim(cut_off, carve_out, days, freqs, durs,  nums, num_classes, nurse_dict, doc_lookup, phys_mins, non_phys_mins, shared_categories):
    #initialize matrix of distrubution of waiting times for all classes
    waited=np.zeros((days, num_classes), dtype=int)
    #idles times per day for each doctor
    ##idle_time_dict={k:[0]*days for k in phys_mins}
    #backlog for each doctor
    doc_lines={key:0 for key in phys_mins.keys()}
    ##print(doc_lines)
    # number of urgent patients not seen same day
    urgent_patients_missed = 0 #CALCULATE URGENT PATIENTS TOTAL
    # ADD PATIENT WAITING CUTTOFFS AND TOTAL CUTTOFFS. STOP SIM? OR JUST ALERT    
    
    #get matrix of demand for each patient class (cols) each day (rows)
    np.random.seed()
    demand_matrix=np.random.binomial(nums, freqs, (days, num_classes))
    #get daily demands
    ##daily_demands=np.sum(demand_matrix, axis=1)
    #initialize daily supplies
    daily_supplys=[0]*days
    
    #go through each day
    
    for ind, day in enumerate(demand_matrix):
        #if delegation is possible, make copy of nurse capacity for calculations   
        if nurse_dict:
            curr_nurse_mins=non_phys_mins.copy()
        
        #if using carve outs, set aside time for the day by initializing carve out slots
        if carve_out:
            curr_carve_out={}  ##phys_carve_out.copy()
        
        # get randomized list of patient classes calling in today, in order of call        
        new_patients=np.repeat(range(0,num_classes),day).tolist()
       
        wait_times=[]
        #go thru patients arriving, schedule them
        for patient in new_patients:
            #durs[patient] is expected duration of patient visit
            #doc_lookup[patient] is doc assigned to patient, where zero is any
            #lookup doc
            relevant_doc = doc_lookup[patient]
            #if any doc can be used, assign to doc with shortest backlog
            if patient in shared_categories:
                #build dictionary of doctors and the length of their queue (in days, so relative to hours worked per day)                
                    #pass relative wait function v=minutes in backlog, and phys_mins[k]=mins worked per day by physician k
                ##print(doc_lines)
                doc_backlogs={k:relative_wait(v, phys_mins[k]) for k,v in doc_lines.items()}
                ##print(doc_lines)
                #take doc with smallest number of days in backlog                
                relevant_doc = min(doc_backlogs.keys(), key=(lambda key: doc_backlogs[key]))
            
            #get expected patient duration
            curr_dur=durs[patient]
            #if following carve out policy and patient is urgent, attempt to put in a same day carve_out KEEP TRACK OF URGENT PATIENTS THAT WERE NOT SEEN            
            if carve_out:    
                #if urgent patient can be accomadated in carve out...
                if curr_carve_out[relevant_doc] - curr_dur > 0 :
                    
                    if ind >= cut_off:
                        waited[0,patient] +=1 #mark patient as waiting zero days
                    daily_supplys[ind]+=1 #increment number served today
                    #update current carve out with reduced openings
                    curr_carve_out[relevant_doc] = curr_carve_out[relevant_doc] - curr_dur
                    curr_dur = None #set duration to None
                else:
                    #add to urgent patients not seen same day
                    urgent_patients_missed +=1                
                    #OTHERWISE PATIENT SCHEDULED NORMALLY?   
            if curr_dur is not None: #with no carving out, or failure to carve out, schedule normally..                       
                #add patient duration to relevant doctors backlog
                doc_lines[relevant_doc]=doc_lines[relevant_doc] + curr_dur
                #get number of days patient must wait                   
                wait_time, rem  = divmod(doc_lines[relevant_doc], phys_mins[relevant_doc])
                #if patient cant be seen by doctor that day and can be delegated to nurse, and a relevant nurse has time, do so
                if wait_time > 0 and (patient in nurse_dict) and any([min(curr_nurse_mins[nurse]-curr_dur, 0) for nurse in nurse_dict[patient]]):
                    # get available times of relevant nurses 
                    pat_nurse_dict={k:v for k,v in curr_nurse_mins.items() if k in nurse_dict[patient]}                    
                    #get relevant nurse with most time available
                    max_nurse=max(pat_nurse_dict.keys(), key=(lambda key: pat_nurse_dict[key]))
                    #decrement nurse time available
                    curr_nurse_mins[max_nurse] = curr_nurse_mins[max_nurse] - curr_dur
                    if ind >= cut_off:
                        waited[0,patient] +=1 #mark patient as waiting zero days
                    daily_supplys[ind]+=1 #increment number served today
                    #remove patient time from main queue
                    doc_lines[relevant_doc]=doc_lines[relevant_doc] - curr_dur
                else:
                    #add patient to days waited list 
                    if ind >= cut_off:
                        try:
                            waited[wait_time, patient] +=1
                        except IndexError:
                            pass
                    #try to add to daily demand list, unless patient is scheduled outside timeframe
                    try:
                        daily_supplys[int(ind)+int(wait_time)] +=1
                    except IndexError:
                        pass
            wait_times.append(wait_time)
        ##print(max(wait_times))

                    
            #RECORD WASTED TIME FOR DOCTORS THAT HAVE LESS THAN DAY WAIT AND ALSO RECORD UNUSED TIME SET ASIDE
            #THEN, REDUCE
            # SHOULD WE ALSO CONSIDER ADDED OVERTIME? i.e. do you want to have flex time (for urgent patients?)
            #update doc queues for new day
                    
        for doc in doc_lines:
            #get current queue length and doctor's capacity in minutes per day
            mins_in_q=doc_lines[doc]
            mins_per_day=phys_mins[doc]
            #get wait time in days for each doc
            wait_time, rem = divmod(mins_in_q, mins_per_day)
            #record idle time (difference between time serving patients and total available time, plus any unused carved out time)
            '''
            if wait_time == 0:
                idle_time_dict[doc][ind] = (mins_per_day - rem) + curr_carve_out[doc]
                '''
            #reset doctors schedule (i.e. serve anybody scheduled for today, go to next day)
            doc_lines[doc] = max(mins_in_q - mins_per_day, 0)
                
    
    #see if simulation passed service load parameters 
    '''
    sload_dict={}
    overall_dist=np.sum(waited, axis=1)
    overall_percentile=int(round(np.percentile(np.repeat(np.array(range(0,days)),overall_dist), exp_sload['Overall'][0])))
    if overall_percentile > exp_sload['Overall'][1]:
        sload_dict['Overall']=False
    else:
        sload_dict['Overall']=True
    '''
    
    return (waited, demand_matrix)
        

        
    
    #EXTEND TO OTHE CONDITIONS, SAY URGENT            
            
                    
                    
            
# take mins a physician has in his queue and return number of days (with fractional values) in queue            
def relative_wait(mins_in_q, mins_per_day):
    days, rem = divmod(mins_in_q, mins_per_day)            
    return days + (rem/mins_per_day)
    
        
            
            
    #get patient 
#get coding for provider    
def coding_for_provider(provider_type):
    if provider_type == "Physician":
        coding = 0
    else: 
        coding = 1
    return coding
    
    
#sorts age into an age bin    
def visit_bracket(visit):
            
    if visit == 'Acute':
        visit_bracket = 1
    elif visit == 'Preventative':
        visit_bracket = 2
    else:
        visit_bracket = 3
    return visit_bracket
    
#sorts age into an age bin    
def age_bracket(age):
    age= int(age)        
    if age <15:
        age_bracket = 1
    elif age >= 15 and age <=24:
        age_bracket = 2
    elif age >= 25 and age <=44:
        age_bracket =3
    elif age >= 45 and age <=64:
        age_bracket =4
    elif age >= 65 and age <=74:
        age_bracket =5
    else:
        age_bracket = 6
    return age_bracket
    
   
    
#sorts number of chronic conditions into bin
def chron_bracket(chron):
    chron=int(chron)
    if chron == 0:
        chron_bracket = 0
    elif chron == 1:
        chron_bracket = 1
    elif chron == 2:
        chron_bracket = 2
    elif chron >= 3:
        chron_bracket = 3
    return chron_bracket
        
        

    
# function that retrieves value at requested key, or returns zero if key does not exist
def dict_get(dictionary, key):
    try:
        value=dictionary[key]
    except KeyError:
        value=0
    return value
    
#function to graph distribution and get expected wait time, takes wait_log
    #PERHAPS ANIMATE WITH BINS, need to record each wait log
def wait_estimator(wait_log):
    wait_times=np.array(list(wait_log.keys()))
    num_waiting=np.array(list(wait_log.values()))
    exp_wait=sum(wait_times*num_waiting)/sum(num_waiting)   
    
    return exp_wait