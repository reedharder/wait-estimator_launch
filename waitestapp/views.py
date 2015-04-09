from django.shortcuts import render ##render_to_response
from django.http import HttpResponse
##from django.contrib.formtools.wizard.views import SessionWizardView
from  waitestapp import initial_data
from django.views.decorators.csrf import ensure_csrf_cookie
from itertools import product
import time
from waitestapp.models import CapacitySave, ProfileSave
import numpy as np
##from models import cap_data, prof_data
np.random.seed(42)
'''

CURRENT_TEMPLATES={'capacity':'waitestapp/waitapp_capacity.html', 
                   'aff':'waitestapp/waitapp_aff.html',
                   'attr':'waitestapp/waitapp_attr.html',
                   'cont':'waitestapp/waitapp_contrule.html',
                   'del':'waitestapp/waitapp_delrule.html',
                   'ut':'waitestapp/waitapp_utilization.html',
                   'res':'waitestapp/waitapp_utilization.html',
                   's_capacity':'waitestapp/scenario_capacity.html', 
                   's_aff':'waitestapp/scenario_aff.html',
                   's_attr':'waitestapp/scenario_attr.html',
                   's_cont':'waitestapp/scenario_contrule.html',
                   's_del':'waitestapp/scenario_delrule.html',
                   's_ut':'waitestapp/scenario_utilization.html',
                   's_res':'waitestapp/scenario_utilization.html',             
                   
                   }
                   ## ADD SCENARIO TABS!

CURRENT_FORMS = [("capacity", waitestapp.forms.CurrCapacityForm),
                 ("aff", waitestapp.forms.CurrAffForm),
                 ("attr", waitestapp.forms.CurrAttForm),
                 ("cont", waitestapp.forms.CurrContForm),
                 ("del", waitestapp.forms.CurrDelForm),
                 ("ut", waitestapp.forms.CurrDelForm),
                 ("res", waitestapp.forms.CurrDelForm),
                 ("capacity", waitestapp.forms.CurrCapacityForm),
                 ("aff", waitestapp.forms.CurrAffForm),
                 ("attr", waitestapp.forms.CurrAttForm),
                 ("cont", waitestapp.forms.CurrContForm),
                 ("del", waitestapp.forms.CurrDelForm),


]
                 #ADD SCENARIO FORMS
                 
#Get list of physicians from capacity tab                 
def get_physician_list(wizard):
     # Get cleaned data from capacity step
    cleaned_data = wizard.get_cleaned_data_for_step('capacity')
    if cleaned_data:
        phys_list=[record['Provider Name'] for record in cleaned_data['table'] if record['Position']=='Physician']
    else:
        phys_list = []
    return phys_list
    
#Get list of physicians from capacity tab                 
def get_nonphys_list(wizard):
     # Get cleaned data from capacity step
    cleaned_data = wizard.get_cleaned_data_for_step('capacity')
    if cleaned_data:
        phys_list=[record['Provider Name'] for record in cleaned_data['table'] if record['Position']!='Physician']
    else:
        phys_list = []
    return phys_list
        
class CurrentWizard(SessionWizardView):
    def get_template_names(self):
        return [CURRENT_TEMPLATES[self.steps.current]]    
        
    def get_context_data(self, form, **kwargs):
        context = super(CurrentWizard, self).get_context_data(form=form, **kwargs)
        if self.steps.current == 'aff' or self.steps.current == 'attr':
            phys_list=get_physician_list(self)
            context.update({'phys_list': phys_list})
        return context
    
    def done(self, form_list, form_dict, **kwargs):
        return render_to_response('waitestapp/waitapp_utilization.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })


wizard_view = CurrentWizard.as_view(CURRENT_FORMS)

def current_wizard_view(request):
    return wizard_view(request)
'''


def home_view(request):       
    return render(request, 'waitestapp/base_site.html')

@ensure_csrf_cookie
def waitapp_capacity(request):
    if request.method == 'POST' and request.POST['type'] =='page':
        import ast
        table = ast.literal_eval(request.POST['id_table'])
        print(table)
        #get lists of physicians, non physicians
        phys_list=[record['Provider Name'] for record in table if record['Position']=='Physician']
        nonphys_list=[record['Provider Name'] for record in table if record['Position']!='Physician']
        request.session['phys_list'] = phys_list
        request.session['nonphys_list'] = nonphys_list
        request.session['capacity_table'] = table
        
        return HttpResponse('ok')
    elif request.method == 'POST' and request.POST['type'] =='save':        
        table = request.POST['id_table']
        newcapsave = CapacitySave(table=table, savetime=str(time.time()))
        newcapsave.save()       
        #get lists of physicians, non physicians   
        
        return HttpResponse('ok')
    try: 
        table_data = request.session['capacity_table']         
    except KeyError:
        table_data = initial_data.capacity_json 
    else:
        table_data = key_clean(table_data)
        
    return render(request, 'waitestapp/waitapp_capacity.html', {'table_data':table_data})
    
@ensure_csrf_cookie
def waitapp_prof(request):
    if request.method == 'POST' and request.POST['type'] =='page':
        import ast
        table = ast.literal_eval(request.POST['datatable'])
        request.session['proftable'] = table
    elif request.method == 'POST' and request.POST['type'] =='save':        
        table = request.POST['datatable']
        newprofsave = ProfileSave(table=table, savetime=str(time.time()))
        newprofsave.save()       
        #get lists of physicians, non physicians   
        
        return HttpResponse('ok')
        
   
    return render(request, 'waitestapp/waitapp_profile.html',{'phys_list':request.session['phys_list']})
    
    
@ensure_csrf_cookie
def waitapp_aff(request):
    if request.method == 'POST':
        import ast
        table = ast.literal_eval(request.POST['id_table'])
        request.session['aff_table'] = table
    try: 
        table_data = request.session['aff_table']
    except KeyError:
        table_data = initial_data.aff_json 
    else:
        table_data = key_clean(table_data)
    return render(request, 'waitestapp/waitapp_aff.html',{'phys_list':request.session['phys_list'], 'table_data':table_data})

@ensure_csrf_cookie
def waitapp_attr(request):
    if request.method == 'POST':
        import ast
        table = ast.literal_eval(request.POST['id_table'])
        patTable = ast.literal_eval(request.POST['patTable'])
        request.session['attr_table'] = table
        request.session['patTable'] = patTable
    try: 
        table_data = request.session['attr_table']
        pat_table_data = request.session['patTable']
    except KeyError:
        table_data = initial_data.attr_json 
        pat_table_data = initial_data.pat_json 
    else:
        table_data = key_clean(table_data)
        pat_table_data = key_clean(pat_table_data)
    return render(request, 'waitestapp/waitapp_attr.html', {'phys_list':request.session['phys_list'],'table_data':table_data, 'pat_table_data':pat_table_data})

@ensure_csrf_cookie    
def waitapp_contrule(request):
    if request.method == 'POST':
        import ast
        table = ast.literal_eval(request.POST['id_table'])
        request.session['cont_table'] = table
        request.session['defCont'] = request.POST['defCont']
    try: 
        table_data = request.session['cont_table']
        defCont = request.session['defCont']
        if defCont == "share":
            Share = "selected"
            NoShare = ""
        else:
            Share = ""
            NoShare = "selected"            
    except KeyError:
        table_data = initial_data.cont_json 
        Share = "selected"
        NoShare = ""       
    else:
        table_data = key_clean(table_data)
    return render(request, 'waitestapp/waitapp_contrule.html', {'phys_list':request.session['phys_list'],'table_data':table_data, 'share':Share, 'noshare':NoShare} )

@ensure_csrf_cookie
def waitapp_delrule(request):
    if request.method == 'POST':
        import ast
        table = ast.literal_eval(request.POST['id_table'])
        request.session['del_table'] = table
    try: 
        table_data = request.session['del_table']
    except KeyError:
        table_data = initial_data.del_json 
    else:
        table_data = key_clean(table_data)
    return render(request, 'waitestapp/waitapp_delrule.html', {'phys_list':request.session['phys_list'],'nonphys_list':request.session['nonphys_list'],'table_data':table_data})

@ensure_csrf_cookie
def waitapp_utilization(request):#get doctors in list
    
    np.random.seed(42)
    import ast
    #empty data for cont_rule and del rule screens
    request.session['cont_table'] = []
    request.session['defCont'] = "noshare" #default?
    request.session['del_table'] = []
    
    if request.method == 'POST':
        #run simulator
        print("importing")
        from  waitestapp import waitsimulator
        print("preparing")
        nums=np.array(request.session['nums']) 
        freqs=np.array(request.session['freqs'] )
        durs=np.array(request.session['durs'] )
        urgents=np.array(request.session['urgents'] )
        shared_categories = request.session['shared_categories'] 
        phys_mins=ast.literal_eval(request.session['phys_mins']) 
        non_phys_mins=ast.literal_eval(request.session['non_phys_mins'])
        print(phys_mins)
        doc_lookup= np.array(request.session['doc_lookup'])
        from collections import Counter
        print(Counter(doc_lookup))
        #run simulation 
        print("simulating")
        np.random.seed(42)
        K=waitsimulator.mat_sim(urgents=urgents, cut_off=0, carve_out=True,  days=500, freqs=freqs, durs=durs,  nums=nums, num_classes=len(durs), nurse_dict={}, phys_mins=phys_mins, non_phys_mins={}, doc_lookup=doc_lookup, shared_categories=shared_categories)
        print("storing...")
        #get matrix of days waited vs patient demand class
        request.session['wait_mat']  = K[0].tolist()
        
        return HttpResponse('done')
    else:                      
        from itertools import product    
        provTable = request.session['capacity_table']       
                    
        #parse doctors and their hours
        prov_to_num={}
        num_to_prov={}
        phys_to_num={}
        num_to_phys={}
        phys_mins={}
        non_phys_mins={}
        for j, row in enumerate(provTable):
            i = j + 1 #reserve doctor code 0 for any doctor        
             #map names to numbers
            print(row)
           
            #note pprovider avg. min per day
            if row['Position'] == 'Physician': 
                phys_to_num[row['Provider Name']] = i        
                num_to_phys[i] = row['Provider Name']
                try:
                    phys_mins[i]=60*float(row['Hours Per Day'])*(float(row['Days Per Year']))/360
                except ValueError:
                    phys_mins[i] = 347 #expected from 40hrs a week 52 weeks a year
            else:
                try:
                    non_phys_mins[i]=.7*60*float(row['Hours Per Day'])*(float(row['Days Per Year']))/360
                except ValueError:
                    non_phys_mins[i] = 347*.7
                prov_to_num[row['Provider Name']] = i        
                num_to_prov[i] = row['Provider Name']
        
        #generate list of shared categories
        #share everything if default 
        if request.session['defCont'] == 'share':
            shared_categories = [categ for categ in product([1,2],[1,2,3,4,5,6], [0,1,2,3],[1,2,3],phys_to_num.values())]
        else:
            shared_categories = []
        for line in request.session['cont_table']:
            rule_dict={}
            rule_categories=[[],[],[],[],[]]
            #dictionary for each rule component
            for ind, element in enumerate(line['Rule'].split('AND')):
                element.lstrip().rstrip()
                rule_dict[element.split(':')[0]]=element.split(':')[1]
            if 'Gender' in rule_dict:
                rule_categories[0] = [2] if rule_dict['Gender']=='M' else [1] 
            else:
                rule_categories[0] = [1,2]
            if 'Age' in rule_dict:
                rule_categories[1]=list(range(age_bracket(rule_dict['Age'].split('-')[0]), age_bracket(rule_dict['Age'].split('-')[1]) + 1))
            else:
                rule_categories[1]=[1,2,3,4,5,6]
            if 'Chronic' in rule_dict:
                rule_categories[2]=list(range(chron_bracket(rule_dict['Cond'].split('-')[0]), chron_bracket(rule_dict['Cond'].split('-')[1]) + 1))
            else:
                rule_categories[2]=[0,1,2,3]
            if 'Visit' in rule_dict:
                rule_categories[3]=[visit_bracket(rule_dict['Visit'])]
            else:
                rule_categories[3]=[1,2,3]
            if 'Provider' in rule_dict:
                rule_categories[4]=[phys_to_num[rule_dict['Provider']]]
            else:
                rule_categories[4]=phys_to_num.values()
            # list of category integer indices for which the current rule applies
            rule = line['Continuity']        
            
            categories_affected=[categ for categ in product(rule_categories[0], rule_categories[1], rule_categories[2], rule_categories[3], rule_categories[4])]
            
            for category in categories_affected:
                if rule == 'Share':
                    shared_categories.append(category)
                #if default share and rule is no share, remove categry from shared list
                elif request.session['defCont'] == 'share' and rule == "Do Not Share" and (category in  shared_categories):
                    while category in shared_categories: shared_categories.remove(category)  
                        
                      
        #estimate panel composition of each based on namcs
        request.session['prov_to_num'] = prov_to_num
        request.session['phys_to_num'] = phys_to_num
        
        panelTable = request.session['proftable']
        import ast
        panelTable = ast.literal_eval(str(panelTable)) #convert string to list of lists
        #generate panels:
        from collections import Counter
        #lookup index for each visit type   
        category_full_to_ind = {}
        nums = []
        freqs = []
        durs = []
        urgents = []
        doc_lookup = []
        ind = 0 # start increment counter
        phys_demand = {} #dictionary of demand per physician
        for docname, panelData in zip(request.session['phys_list'],panelTable):
            panel = panelData[0] #panelsize
            #get distributions if correct
            genarray = [int(string) for string in panelData[1]] if (all([string.isdigit() for string in panelData[1]]) and sum([int(string) for string in panelData[1]]))  else []      
            agearray =[int(string) for string in panelData[2]]  if (all([string.isdigit() for string in panelData[2]]) and sum([int(string) for string in panelData[2]]))  else [] 
            condarray = [int(string) for string in panelData[3]] if (all([string.isdigit() for string in panelData[3]]) and sum([int(string) for string in panelData[3]]))  else [] 
            agearrayF =[int(string) for string in panelData[4]]  if (all([string.isdigit() for string in panelData[4]]) and sum([int(string) for string in panelData[4]]))  else [] 
            condarrayF = [int(string) for string in panelData[5]] if (all([string.isdigit() for string in panelData[5]]) and sum([int(string) for string in panelData[5]]))  else [] 
            
            acute_demand = 0 # start counter of demand
            prev_demand = 0
            chronic_demand = 0
            doc = phys_to_num[docname]
            problem_pat =['1,1,2',
            '1,2,1',
            '1,1,3',
            '1,3,3',
            '1,2,3',
            '1,2,2',
            '2,2,1',
            '2,1,2',
            '2,1,3',
            '2,2,3']
            
            noprob_pat = ['2,5,3',
             '2,3,1',
             '2,2,0',
             '2,5,1',
             '1,3,1',
             '1,4,3',
             '1,2,0',
             '1,4,2',
             '1,6,3',
             '1,5,3']
            #generate panel accordin to male female ratio and namcs proportions
            np.random.seed(42)
            prng = np.random.RandomState(42)
            panel_dict = Counter(prng.choice(initial_data.full_cats_str, int(panel),adjust_ratios(full_p = initial_data.full_p, full_cats=initial_data.full_cats, sex=genarray, age=agearray,chronic=condarray, ageF=agearrayF,chronicF=condarrayF)))
            #uneven the distributions            
            if docname == 'Doctor 1':
                for prob, noprob in zip(problem_pat, noprob_pat):
                    transf = min(40, panel_dict[noprob])
                    panel_dict[noprob] -= transf
                    panel_dict[prob] += transf
               
            if docname == 'Doctor 3':
                 for prob, noprob in zip(problem_pat, noprob_pat):
                    transf = min(10, panel_dict[noprob])
                    panel_dict[noprob] -= transf
                    panel_dict[prob] += transf
            
            
            '''
            docnum = docname.split()[1]
            with open('C:/Users/Reed/Desktop/doc%spanel.txt' % docnum,'w') as outfile:
                outfile.write('\t'.join(['Gender','Agegroup','Conditions','Num Patients']) + '\n')
                for cat, num in panel_dict.items():
                    catsplit = cat.split(",")
                    if catsplit[0] == '1':
                        catsplit[0] = 'F'
                    else:
                        catsplit[0] = 'M'
                    catsplit=catsplit + [str(num)]
                    outfile.write('\t'.join(catsplit)  + '\n')
            '''    
            
            #get full distribution of patient types on panel
            ##panel_dict = Counter(np.random.choice(initial_data.full_cats_str, int(panel),adjust_ratios(full_p = initial_data.full_p, full_cats=initial_data.full_cats, sex=genarray, age=agearray,chronic=condarray, ageF=agearrayF,chronicF=condarrayF)))
            #generate import simulation data
            for patient_category in panel_dict:
                #ACUTE            
                #input sex,age,chron,visit, doc   
                ##print((str(patient_category[0]),str(patient_category[2]),str(patient_category[4]),1,doc))
                category_full_to_ind[(int(patient_category[0]),int(patient_category[2]),int(patient_category[4]),1,int(doc))] = ind
                nums.append(int(panel_dict[patient_category])) #append number represented
                #input sex, age, chron, visit
                try:
                    freq =initial_data.freq_dict[(int(patient_category[0]),int(patient_category[2]),int(patient_category[4]),1)]
                except KeyError:
                    freq = 0
                try:
                    dur =initial_data.durs_dict[(int(patient_category[0]),int(patient_category[2]),int(patient_category[4]),1)]
                except KeyError:
                    dur = 0
                freqs.append(freq)
                durs.append(dur)  
                urgents.append(1)
                #add to acute demand
                acute_demand += int(panel_dict[patient_category])*freq*360*dur*(1/60)
                doc_lookup.append(int(doc))            
                ind += 1 #increment index
                #PREV
                #input sex,age,chron,visit, doc
                category_full_to_ind[(int(patient_category[0]),int(patient_category[2]),int(patient_category[4]),2,int(doc))] = ind
                nums.append(panel_dict[patient_category]) #append number represented
                #input sex, age, chron, visit
                try:
                    freq = initial_data.freq_dict[(int(patient_category[0]),int(patient_category[2]),int(patient_category[4]),2)]
                except KeyError:
                    freq = 0
                try:
                    dur = initial_data.durs_dict[(int(patient_category[0]),int(patient_category[2]),int(patient_category[4]),2)]
                except KeyError:
                    dur = 0
                freqs.append(freq)
                durs.append(dur) 
                urgents.append(0)
                #add to prev demand
                prev_demand += int(panel_dict[patient_category])*freq*360*dur*(1/60)
                doc_lookup.append(int(doc))
                ind +=1 #increment index
                #CHRONIC
                #input sex,age,chron,visit, doc
                category_full_to_ind[(int(patient_category[0]),int(patient_category[2]),int(patient_category[4]),3,int(doc))] = ind
                nums.append(panel_dict[patient_category]) #append number represented
                #input sex, age, chron, visit
                try:
                    freq =initial_data.freq_dict[(int(patient_category[0]),int(patient_category[2]),int(patient_category[4]),3)]
                except KeyError:
                    freq = 0
                try:
                    dur =initial_data.durs_dict[(int(patient_category[0]),int(patient_category[2]),int(patient_category[4]),3)]
                except KeyError:
                    dur = 0
                freqs.append(freq)
                durs.append(dur)   
                urgents.append(0)
                #add to acute demand
                chronic_demand += int(panel_dict[patient_category])*freq*360*dur*(1/60)
                doc_lookup.append(int(doc))
                ind +=1 #increment index
            #add doctor demand to dictionary, list is demands by visit, total demand, placeholders for total capacity, team name,  team members, and capacity-demand, and finally panel size
            phys_demand[docname] = [acute_demand, prev_demand, chronic_demand, sum((acute_demand, prev_demand, chronic_demand)), None, None, None, None , str(panel)]
        
        #convert list of shared categories to indices
        shared_categories = [category_full_to_ind[category] for category in shared_categories if category in category_full_to_ind]
        #save nums, freqs, durs,  category_full_to_ind, shared_categories, phys_mins
        print(1)
        request.session['nums'] = nums
        request.session['urgents'] = urgents
        print(2)
        request.session['freqs'] = freqs
        print(3)
        request.session['durs'] = durs
        print(4)
        request.session['shared_categories'] = shared_categories
        print(5)
        request.session['phys_mins'] = str(phys_mins)
        request.session['non_phys_mins'] = str(non_phys_mins)
        
        print(6)
        request.session['doc_lookup'] = doc_lookup
        print(7)
        request.session['category_full_to_ind'] = str(category_full_to_ind)
        print(8)
        #prepare capacity
        capacity_table = request.session['capacity_table']
        
        print(9)
        ##phys_capacity = {}
        team_capacity = {}  
        ##phys_teams = {}
        #create lookup dictionary to map patient conditions to index 
        '''
        category_product=itertools.product([1,2],[0,1,2,3,4,5],[0,1,2,3],phys_to_num.values())
        category_name_key_mapping={}
        for ind, category in enumerate(category_product):
            category_name_key_mapping[category]=ind
            ind_to_category[ind] = category 
            
        #dictionary keyed to integer representations for each key (gender, age bracket, chron condition bracket, physician)
        request.session['category_name_key_mapping'] = category_name_key_mapping
        request.session['ind_to_category'] = ind_to_category   
        '''        
        #note capacities for teams and physicians (and compile a list of physicians for each team)
        phys_capacity = {} #keeptrack of individual hours/days per year
        
        for record in capacity_table:
            if record['Position'] == 'Physician':
                phys_capacity[record['Provider Name']] = int(record['Hours Per Day'])*int(record['Days Per Year'])
                phys_demand[record['Provider Name']][4] = int(record['Hours Per Day'])*int(record['Days Per Year'])
                phys_demand[record['Provider Name']][5] = record['Team'] #team name
                #imbalance
                phys_demand[record['Provider Name']][7] = phys_demand[record['Provider Name']][4] - phys_demand[record['Provider Name']][3]
            try:
                team_capacity[record['Team']][0] += [record['Position'] + ' ' + record['Provider Name']]
                team_capacity[record['Team']][1] += int(record['Hours Per Day'])*int(record['Days Per Year'])
            except KeyError:
                team_capacity[record['Team']] = ['','']
                team_capacity[record['Team']][0] = [record['Position']  + ' ' + record['Provider Name']]
                team_capacity[record['Team']][1] = int(record['Hours Per Day'])*int(record['Days Per Year'])
        for phys in phys_demand: # get list of team members for each physician
            if phys_demand[phys][5] =='No Team':
                 phys_demand[phys][5] = ''
                 phys_demand[phys][6]  = []
            else:
                phys_demand[phys][6]=team_capacity[phys_demand[phys][5]][0]
       
        request.session['phys_capacity']=str(phys_capacity) #stor phys capacity
        print('ok')
        print(phys_demand)
        return render(request, 'waitestapp/waitapp_utilization.html', {'phys_demand': phys_demand})

@ensure_csrf_cookie    
def waitapp_results(request):
    import ast
    #import numpy as np
    np.random.seed(42)
    waited = np.array(request.session['wait_mat'])
    print("...waited")
    print(waited)
    category_full_to_ind =  ast.literal_eval(request.session['category_full_to_ind'])
    print(len(category_full_to_ind))
    print(category_full_to_ind.keys())
    phys_to_num = request.session['phys_to_num']
    doc_lookup = request.session['doc_lookup']
    if request.method == 'POST':    
        import json
               
        #change overall expected wait
        if  request.POST['type'] ==  'overall':
            doc = request.POST['doc']
            print(doc)
            q = int(request.POST['perc'])
            exp, p = overall_query( doc, waited, phys_to_num, doc_lookup, q)
            data = {'exp':exp, 'p':p}
            return HttpResponse(json.dumps(data), content_type='application/json')
        #change wait for individual row or query
        elif request.POST['type'] == 'rowselect':
            
            gender  = request.POST.get('gender')            
            age  = request.POST.get('age')
            doc = request.POST.get('doc')
            visit = request.POST.get('visit') 
            chron = request.POST.get('chron')
            #take overall or individual parameter values, depending on user selection
            if doc =="Overall":
                docs=phys_to_num.values()
            else: 
                docs = [phys_to_num[doc]]
                
            if age == "All":
                ages = [1,2,3,4,5,6]
            else:
                ages = [int(age)]
                
            if chron == "All":
                chrons = [0,1,2,3]
            else:
                chrons = [int(chron[0])]
        
            if gender  == 'All':
                genders = [1,2]
            else:
                genders = [gender_bracket(gender)]
           
            if visit == 'All':
                visits = [1,2,3]
            else:
                visits = [int(visit)]                    
            
            
            #percentile
            q = int(request.POST['perc'])
           
            
            exp, p = visit_query_generator_alls(waited, docs, ages, chrons, genders, visits, q, category_full_to_ind, phys_to_num)
            data = {'exp':exp, 'p':p}
            return HttpResponse(json.dumps(data), content_type='application/json')
    else:       
        ##table_query_generator(waited, doc, cond, gender, age, visit, q, category_full_to_ind, phys_to_num)    
        return render(request, 'waitestapp/waitapp_results.html', {'phys_list':request.session['phys_list']})



 
@ensure_csrf_cookie
def scenario_1(request):
    import ast
    #import numpy as np     
    np.random.seed(42)
    waited = np.array(request.session['wait_mat'])
    ##waited = np.array(request.session['s_wait_mat'])
    ##print("...waited")
    ##print(waited)
    category_full_to_ind =  ast.literal_eval(request.session['category_full_to_ind'])
    nums =request.session['nums']
    phys_to_num=request.session['phys_to_num'] 
    try:
        s_nums = request.session['s_nums']
    except KeyError:
        s_nums = request.session['nums'].copy()
        request.session['s_nums'] = s_nums
    ##print(len(category_full_to_ind))
    ##print(category_full_to_ind.keys())
    phys_to_num = request.session['phys_to_num']
    doc_lookup = request.session['doc_lookup']
    if request.method == 'POST':    
        import json               
        #reset to original numbers
        if  request.POST['type'] ==  'reset':  
            s_nums = request.session['nums'].copy()
            request.session['s_nums'] = s_nums
            data = {'status' : 'ok'} #respond to page
            return HttpResponse(json.dumps(data), content_type='application/json')
        
        #change overall expected wait
        if  request.POST['type'] ==  'reassign':
            #get data (i.e. requested patient categories) from post
            if request.POST.get('age') == 'all':
                age = [1,2,3,4,5,6]
            else:
                age = [int(request.POST.get('age'))]
            chron = request.POST['chron']
            if chron.lower() == 'all':
                chron = [0,1,2,3]
            else:
                chron=[int(chron[0])]
            gender = request.POST['gender']    
            if gender.lower() == 'all':
                gender = [1,2]
            else:
                gender = [gender_bracket(gender)]
            number = int(request.POST['number'])
            fromdoc = phys_to_num[request.POST['from']]
            todoc = phys_to_num[request.POST['to']]
            #categories for transfer
            categories = list(product(gender,age,chron))
            print(categories)
            print(s_nums)
            for i in range(1,4): #for each visit type
                tot_trans = 0
                for category in categories:
                    indfrom = category_full_to_ind[(category[0], category[1], category[2], i, fromdoc)] #get categories index of doctor losing patients
                    indto = category_full_to_ind[(category[0], category[1], category[2], i, todoc)] ##category from doc gaining patients
                    transfer=min(s_nums[indfrom],number) #number in category can be at min zero
                    #increment and decrement appropriate categories
                    s_nums[indfrom] = s_nums[indfrom] - transfer
                    s_nums[indto] = s_nums[indto] + transfer
                    tot_trans += transfer
            request.session['s_nums'] = s_nums #save in session variable
            response = "%s patients reassigned" % tot_trans
            data = {'num' : response} #respond to page
            return HttpResponse(json.dumps(data), content_type='application/json')
        #change wait for individual row or query
        elif request.POST['type'] == 'query': 
            doc =request.POST['doc']
            s_nums=np.array(request.session['s_nums']) #new numbers
            freqs=np.array(request.session['freqs'] )
            durs=np.array(request.session['durs'] )
            ##shared_categories = request.session['shared_categories'] 
            phys_mins=ast.literal_eval(request.session['phys_mins']) 
            ##non_phys_mins=ast.literal_eval(request.session['non_phys_mins'])
            print(phys_mins)
            doc_lookup= np.array(request.session['doc_lookup'])
            try:
                new_mat = np.array(request.session['s1_wait_mat'])
            except KeyError:
                new_mat = waited
            exp, p = overall_query( doc, new_mat, phys_to_num, doc_lookup, 100)
            exp_old, p = overall_query( doc, np.array(request.session['wait_mat']), phys_to_num, doc_lookup, 100)
           
            #get old and new demand
            old_demand=0
            new_demand=0
            for i, freq in enumerate(freqs):
               if doc_lookup[i] == phys_to_num[doc]: 
                   old_demand += nums[i]*freq*360*durs[i]*(1/60)
                   new_demand += s_nums[i]*freq*360*durs[i]*(1/60)
            #get capacity 
            capacity_info=ast.literal_eval(request.session['phys_capacity'])[doc]
            capacity =capacity_info
            data = {'dem':round(new_demand), 'olddem':round(old_demand), 'demc': round(new_demand-old_demand),'wait':exp,'waitc': (exp-exp_old), 'cap':round(capacity) }
            return HttpResponse(json.dumps(data), content_type='application/json')
        # recalculate with new nums and cont rules
        elif request.POST['type'] == 'recalculate':  
            #load and processes continuity rules
            doc =request.POST['doc']
             #run simulator
            print("importing")
            from  waitestapp import waitsimulator
            print("preparing")
            s_nums=np.array(request.session['s_nums']) #new numbers
            freqs=np.array(request.session['freqs'] )
            durs=np.array(request.session['durs'] )
            urgents=np.array(request.session['urgents'] )
            ##shared_categories = request.session['shared_categories'] 
            phys_mins=ast.literal_eval(request.session['phys_mins']) 
            ##non_phys_mins=ast.literal_eval(request.session['non_phys_mins'])
            print(phys_mins)
            doc_lookup= np.array(request.session['doc_lookup'])
            from collections import Counter
            print(Counter(doc_lookup))
            #run simulation 
            print("simulating")
            
            K=waitsimulator.mat_sim(urgents=urgents, cut_off=10, carve_out=True,  days=500, freqs=freqs, durs=durs,  nums=s_nums, num_classes=len(durs), nurse_dict={}, phys_mins=phys_mins, non_phys_mins={}, doc_lookup=doc_lookup, shared_categories=[])
            print("storing...")
            #get matrix of days waited vs patient demand class
            request.session['s1_wait_mat']  = K[0].tolist()
            
            
            #get wait for doctor, as well as change in wait
            exp, p = overall_query( doc,  K[0], phys_to_num, doc_lookup , 100)
            exp_old, p = overall_query( doc,waited, phys_to_num, doc_lookup, 100)
           
            #get old and new demand
            old_demand=0
            new_demand=0
            for i, freq in enumerate(freqs):
               if doc_lookup[i] == phys_to_num[doc]: 
                   old_demand += nums[i]*freq*360*durs[i]*(1/60)
                   new_demand += s_nums[i]*freq*360*durs[i]*(1/60)
            #get capacity 
            capacity_info=ast.literal_eval(request.session['phys_capacity'])[doc]
            capacity = capacity_info
            request.session['scenario1'] = [round(new_demand), round(new_demand-old_demand),exp,(exp-exp_old), round(capacity)]
            data = {'dem':round(new_demand), 'olddem':round(old_demand), 'demc': round(new_demand-old_demand),'wait':exp,'waitc': (exp-exp_old), 'cap':round(capacity) }
            return HttpResponse(json.dumps(data), content_type='application/json')         
        else:
            return HttpResponse('done')
            
        
    else:       
        ##table_query_generator(waited, doc, cond, gender, age, visit, q, category_full_to_ind, phys_to_num)    
        return render(request, 'waitestapp/scenario_1.html', {'phys_list':request.session['phys_list']})
        
@ensure_csrf_cookie
def scenario_2(request):
    import ast
    #import numpy as np 
    np.random.seed(42)
    del request.session['s_nums']
    import json 
    waited = np.array(request.session['wait_mat'])
    ##waited = np.array(request.session['s_wait_mat'])
    ##print("...waited")
    ##print(waited)
    ##category_full_to_ind =  ast.literal_eval(request.session['category_full_to_ind'])
    nums =request.session['nums']
    phys_to_num=request.session['phys_to_num'] 
    try:
        s_nums = request.session['s_nums']
    except KeyError:
        s_nums = request.session['nums'].copy()
        request.session['s_nums'] = s_nums
    ##print(len(category_full_to_ind))
    ##print(category_full_to_ind.keys())
    
    doc_lookup = request.session['doc_lookup']
    if request.method == 'POST':   
            
        #change overall expected wait
        if request.POST['type'] ==  'extend':  
            try:
                phys_mins=ast.literal_eval(request.session['s_phys_mins'])
            except KeyError:
                phys_mins=ast.literal_eval(request.session['phys_mins'])
            try:
                non_phys_mins=ast.literal_eval(request.session['s_non_phys_mins'])
            except KeyError:
                non_phys_mins=ast.literal_eval(request.session['non_phys_mins'])
            #get capacity 
            try:
                capacity_dict=ast.literal_eval(request.session['s_phys_capacity'])
            except KeyError:
                capacity_dict=ast.literal_eval(request.session['phys_capacity'])  
             #get additional capacity 
           
            hours = float(request.POST['hours'])
            days = float(request.POST['days'])
            prov = request.POST['prov']
            prov_to_num = request.session['prov_to_num']
            phys_to_num = request.session['phys_to_num']
           
            try:                                 
               
                phys_mins[phys_to_num[prov]]  += (60*hours*days*52)/360
                request.session['s_phys_mins'] = str(phys_mins)
                capacity_dict[prov] += hours*days*52
                request.session['s_phys_capacity'] = str(capacity_dict)
                
            except KeyError:
                non_phys_mins[prov_to_num[prov]]  += (60*hours*days*52)/360
                request.session['s_non_phys_mins'] = str(non_phys_mins)
            return HttpResponse('Hours added')
            
        elif request.POST['type'] == 'query': 
           
            
            doc =request.POST['doc']
            ##s_nums=np.array(request.session['s_nums']) #new numbers
            freqs=np.array(request.session['freqs'] )
            durs=np.array(request.session['durs'] )
            ##shared_categories = request.session['shared_categories'] 
            try:
                phys_mins=ast.literal_eval(request.session['s_phys_mins'])
            except KeyError:
                phys_mins=ast.literal_eval(request.session['phys_mins'])
            try:
                non_phys_mins=ast.literal_eval(request.session['s_non_phys_mins'])
            except KeyError:
                non_phys_mins=ast.literal_eval(request.session['non_phys_mins']) 
            ##non_phys_mins=ast.literal_eval(request.session['non_phys_mins'])
            print(phys_mins)
            doc_lookup= np.array(request.session['doc_lookup'])
            try:
                new_mat = np.array(request.session['s2_wait_mat'])
            except KeyError:
                new_mat = waited
            exp, p = overall_query( doc, new_mat, phys_to_num, doc_lookup, 100)
            exp_old, p = overall_query( doc, np.array(request.session['wait_mat']), phys_to_num, doc_lookup, 100)
           
            #get old and new demand
            old_demand=0
            new_demand=0
            for i, freq in enumerate(freqs):
               if doc_lookup[i] == phys_to_num[doc]: 
                   old_demand += nums[i]*freq*360*durs[i]*(1/60)
                   new_demand += nums[i]*freq*360*durs[i]*(1/60)
            #get capacity 
            try:
                capacity_info=ast.literal_eval(request.session['s_phys_capacity'])[doc]
            except KeyError:
                capacity_info=ast.literal_eval(request.session['phys_capacity'])[doc]
            capacity = capacity_info
            data = {'dem':round(new_demand), 'olddem':round(old_demand), 'demc': round(new_demand-old_demand),'wait':exp,'waitc': (exp-exp_old), 'cap':round(capacity) }
            return HttpResponse(json.dumps(data), content_type='application/json')
        # recalculate with new nums and cont rules
        elif request.POST['type'] == 'recalculate':  
           
            #load and processes continuity rules
            doc =request.POST['doc']
             #run simulator
            print("importing")
            from  waitestapp import waitsimulator
            print("preparing")
            s_nums=np.array(request.session['s_nums']) #new numbers
            freqs=np.array(request.session['freqs'] )
            durs=np.array(request.session['durs'] )
            urgents=np.array(request.session['urgents'] )
            ##shared_categories = request.session['shared_categories'] 
            phys_mins=ast.literal_eval(request.session['phys_mins']) 
            try:
                phys_mins=ast.literal_eval(request.session['s_phys_mins'])
            except KeyError:
                phys_mins=ast.literal_eval(request.session['phys_mins'])
            try:
                non_phys_mins=ast.literal_eval(request.session['s_non_phys_mins'])
            except KeyError:
                non_phys_mins=ast.literal_eval(request.session['non_phys_mins'])
            
            
            print(phys_mins)
            doc_lookup= np.array(request.session['doc_lookup'])
            from collections import Counter
            print(Counter(doc_lookup))
            #run simulation 
            print("simulating")
            
            K=waitsimulator.mat_sim(urgents=urgents, cut_off=0, carve_out=True,  days=500, freqs=freqs, durs=durs,  nums=nums, num_classes=len(durs), nurse_dict=[], phys_mins=phys_mins, non_phys_mins=non_phys_mins, doc_lookup=doc_lookup, shared_categories=[])
            print("storing...")
            #get matrix of days waited vs patient demand class
            request.session['s2_wait_mat']  = K[0].tolist()
            
            
            #get wait for doctor, as well as change in wait
            exp, p = overall_query( doc,  K[0], phys_to_num, doc_lookup , 100)
            exp_old, p = overall_query( doc,waited, phys_to_num, doc_lookup, 100)
           
            #get old and new demand
            old_demand=0
            new_demand=0
            for i, freq in enumerate(freqs):
               if doc_lookup[i] == phys_to_num[doc]: 
                   old_demand += nums[i]*freq*360*durs[i]*(1/60)
                   new_demand += nums[i]*freq*360*durs[i]*(1/60)
            #get capacity 
            #get capacity 
            try:
                capacity_info=ast.literal_eval(request.session['s_phys_capacity'])[doc]
                capacity_info_old = ast.literal_eval(request.session['phys_capacity'])[doc]
            except KeyError:
                capacity_info=ast.literal_eval(request.session['phys_capacity'])[doc]
                capacity_info_old=ast.literal_eval(request.session['phys_capacity'])[doc]
            capacity =  capacity_info
            request.session['scenario2'] = [round(new_demand), round(new_demand-old_demand),exp,(exp-exp_old), round(capacity)]
            data = {'dem':round(new_demand), 'oldcap':round(capacity_info_old), 'capc': round(capacity_info-capacity_info_old),'wait':exp,'waitc': (exp-exp_old), 'cap':round(capacity) }
            return HttpResponse(json.dumps(data), content_type='application/json')         
        
        else:
            return HttpResponse('done')
        
    else:       
        ##table_query_generator(waited, doc, cond, gender, age, visit, q, category_full_to_ind, phys_to_num)    
        return render(request, 'waitestapp/scenario_2.html', {'phys_list':request.session['phys_list'], 'non_phys_list':request.session['nonphys_list']})





def scenario_3(request):
    import ast
    #import numpy as np 
    del request.session['s_nums']
    np.random.seed(42)
    from itertools import product
    waited = np.array(request.session['wait_mat'])
    ##waited = np.array(request.session['s_wait_mat'])
    ##print("...waited")
    ##print(waited)
    ##category_full_to_ind =  ast.literal_eval(request.session['category_full_to_ind'])
    nums =request.session['nums']
    phys_to_num=request.session['phys_to_num'] 
    try:
        s_nums = request.session['s_nums']
    except KeyError:
        s_nums = request.session['nums'].copy()
        request.session['s_nums'] = s_nums
    ##print(len(category_full_to_ind))
    ##print(category_full_to_ind.keys())
    phys_to_num = request.session['phys_to_num']
    doc_lookup = request.session['doc_lookup']
    if request.method == 'POST':    
        import json               
        #change overall expected wait
        
        #change wait for individual row or query
        if request.POST['type'] == 'query': 
            doc =request.POST['doc']
            s_nums=np.array(request.session['s_nums']) #new numbers
            freqs=np.array(request.session['freqs'] )
            durs=np.array(request.session['durs'] )
            ##shared_categories = request.session['shared_categories'] 
            phys_mins=ast.literal_eval(request.session['phys_mins']) 
            ##non_phys_mins=ast.literal_eval(request.session['non_phys_mins'])
            print(phys_mins)
            doc_lookup= np.array(request.session['doc_lookup'])
            try:
                new_mat = np.array(request.session['s3_wait_mat'])
            except KeyError:
                new_mat = waited
            exp, p = overall_query( doc, new_mat, phys_to_num, doc_lookup, 100)
            exp_old, p = overall_query( doc, np.array(request.session['wait_mat']), phys_to_num, doc_lookup, 100)
           
            #get old and new demand
            old_demand=0
            new_demand=0
            for i, freq in enumerate(freqs):
               if doc_lookup[i] == phys_to_num[doc]: 
                   old_demand += nums[i]*freq*360*durs[i]*(1/60)
                   new_demand += nums[i]*freq*360*durs[i]*(1/60)
            #get capacity 
            capacity_info=ast.literal_eval(request.session['phys_capacity'])[doc]
            capacity = capacity_info
            data = {'dem':round(new_demand), 'olddem':round(old_demand), 'demc': round(new_demand-old_demand),'wait':exp,'waitc': (exp-exp_old), 'cap':round(capacity) }
            return HttpResponse(json.dumps(data), content_type='application/json')
        # recalculate with new nums and cont rules
        elif request.POST['type'] == 'recalculate':  
            #load and processes continuity rules
            table = ast.literal_eval(request.POST['id_table'])
            request.session['cont_table'] = table
            request.session['defCont'] = request.POST['defCont']
            doc =request.POST['doc']
                #generate list of shared categories
            #share everything if default 
            if request.session['defCont'] == 'share':
                shared_categories = [categ for categ in product([1,2],[1,2,3,4,5,6], [0,1,2,3],[1,2,3],phys_to_num.values())]
            else:
                shared_categories = []
            if request.session['cont_table'] and request.session['cont_table'][0]["Rule"][:1] != "N":
                for line in request.session['cont_table']:
                    rule_dict={}
                    rule_categories=[[],[],[],[],[]]
                    #dictionary for each rule component
                    for ind, element in enumerate(line['Rule'].split('AND')):
                        element.lstrip().rstrip()
                        rule_dict[element.split(':')[0]]=element.split(':')[1]
                    if 'Gender' in rule_dict:
                        rule_categories[0] = [2] if rule_dict['Gender']=='M' else [1] 
                    else:
                        rule_categories[0] = [1,2]
                    if 'Age' in rule_dict:
                        rule_categories[1]=list(range(age_bracket(rule_dict['Age'].split('-')[0]), age_bracket(rule_dict['Age'].split('-')[1]) + 1))
                    else:
                        rule_categories[1]=[1,2,3,4,5,6]
                    if 'Chronic' in rule_dict:
                        rule_categories[2]=list(range(chron_bracket(rule_dict['Cond'].split('-')[0]), chron_bracket(rule_dict['Cond'].split('-')[1]) + 1))
                    else:
                        rule_categories[2]=[0,1,2,3]
                    if 'Visit' in rule_dict:
                        rule_categories[3]=[visit_bracket(rule_dict['Visit'])]
                    else:
                        rule_categories[3]=[1,2,3]
                    if 'Provider' in rule_dict:
                        rule_categories[4]=[phys_to_num[rule_dict['Provider']]]
                    else:
                        rule_categories[4]=phys_to_num.values()
                    # list of category integer indices for which the current rule applies
                    rule = line['Continuity']        
                    
                    categories_affected=[categ for categ in product(rule_categories[0], rule_categories[1], rule_categories[2], rule_categories[3], rule_categories[4])]
                    
                    for category in categories_affected:
                        if rule == 'Share':
                            shared_categories.append(category)
                        #if default share and rule is no share, remove categry from shared list
                        elif request.session['defCont'] == 'share' and rule == "Do Not Share" and (category in  shared_categories):
                            while category in shared_categories: shared_categories.remove(category)  
            else:
                shared_categories = []
            request.session['shared_categories'] = shared_categories #add to session
             #run simulator
            print("importing")
            from  waitestapp import waitsimulator
            print("preparing")
            s_nums=np.array(request.session['s_nums']) #new numbers
            freqs=np.array(request.session['freqs'] )
            durs=np.array(request.session['durs'] )
            urgents=np.array(request.session['urgents'] )
            ##shared_categories = request.session['shared_categories'] 
            phys_mins=ast.literal_eval(request.session['phys_mins']) 
            ##non_phys_mins=ast.literal_eval(request.session['non_phys_mins'])
            print(phys_mins)
            doc_lookup= np.array(request.session['doc_lookup'])
            from collections import Counter
            print(Counter(doc_lookup))
            #run simulation 
            print("simulating")
            
            K=waitsimulator.mat_sim(urgents, cut_off=0, carve_out=True,  days=500, freqs=freqs, durs=durs,  nums=nums, num_classes=len(durs), nurse_dict={}, phys_mins=phys_mins, non_phys_mins={}, doc_lookup=doc_lookup, shared_categories=shared_categories)
            print("storing...")
            #get matrix of days waited vs patient demand class
            request.session['s3_wait_mat']  = K[0].tolist()
            
            
            #get wait for doctor, as well as change in wait
            exp, p = overall_query( doc,  K[0], phys_to_num, doc_lookup , 100)
            exp_old, p = overall_query( doc,waited, phys_to_num, doc_lookup, 100)
           
            #get old and new demand
            old_demand=0
            new_demand=0
            for i, freq in enumerate(freqs):
               if doc_lookup[i] == phys_to_num[doc]: 
                   old_demand += nums[i]*freq*360*durs[i]*(1/60)
                   new_demand += nums[i]*freq*360*durs[i]*(1/60)
            #get capacity 
            capacity_info=ast.literal_eval(request.session['phys_capacity'])[doc]
            capacity = capacity_info
            request.session['scenario3'] = [round(new_demand), round(new_demand-old_demand),exp,(exp-exp_old), round(capacity)]
            data = {'dem':round(new_demand), 'olddem':round(old_demand), 'demc': round(new_demand-old_demand),'wait':exp,'waitc': (exp-exp_old), 'cap':round(capacity) }
            return HttpResponse(json.dumps(data), content_type='application/json')         
        else:
            return HttpResponse('done')
            
        
    else:       
        ##table_query_generator(waited, doc, cond, gender, age, visit, q, category_full_to_ind, phys_to_num)    
        return render(request, 'waitestapp/scenario_3.html', {'phys_list':request.session['phys_list']})
        
#table for comparison of different scenarios
def scenario_table(request):
    scenario1 = request.session['scenario1']
    scenario2 = request.session['scenario2']
    scenario3 = request.session['scenario3']
    scenario4 = request.session['scenario4']
    return render(request, 'waitestapp/scenario_table.html', {'scenario1':scenario1,'scenario2':scenario2,'scenario3':scenario3,'scenario4':scenario4})
    
@ensure_csrf_cookie
def scenario_4(request):
    import ast
    #import numpy as np 
    np.random.seed(42)
    from itertools import product
    waited = np.array(request.session['wait_mat'])
    ##waited = np.array(request.session['s_wait_mat'])
    ##print("...waited")
    ##print(waited)
    category_full_to_ind =  ast.literal_eval(request.session['category_full_to_ind'])
    nums =request.session['nums']
    phys_to_num=request.session['phys_to_num'] 
    try:
        s_nums = request.session['s_nums']
    except KeyError:
        s_nums = request.session['nums'].copy()
        request.session['s_nums'] = s_nums
    ##print(len(category_full_to_ind))
    ##print(category_full_to_ind.keys())
    
    doc_lookup = request.session['doc_lookup']
    if request.method == 'POST':    
        import json               
        #change overall expected wait
        
        if request.POST['type'] == 'query': 
            
            doc =request.POST['doc']
            ##s_nums=np.array(request.session['s_nums']) #new numbers
            freqs=np.array(request.session['freqs'] )
            durs=np.array(request.session['durs'] )
            ##shared_categories = request.session['shared_categories'] 
            phys_mins=ast.literal_eval(request.session['phys_mins']) 
            ##non_phys_mins=ast.literal_eval(request.session['non_phys_mins'])
            print(phys_mins)
            doc_lookup= np.array(request.session['doc_lookup'])
            try:
                new_mat = np.array(request.session['s4_wait_mat'])
            except KeyError:
                new_mat = waited
            exp, p = overall_query( doc, new_mat, phys_to_num, doc_lookup, 100)
            exp_old, p = overall_query( doc, np.array(request.session['wait_mat']), phys_to_num, doc_lookup, 100)
           
            
           #get old and new demand
            old_demand=0
            new_demand=0
            for i, freq in enumerate(freqs):
               if doc_lookup[i] == phys_to_num[doc]: 
                   old_demand += nums[i]*freq*360*durs[i]*(1/60)
                   new_demand += nums[i]*freq*360*durs[i]*(1/60)
            #get capacity 
            capacity_info=ast.literal_eval(request.session['phys_capacity'])[doc]
            capacity = capacity_info
            
            data = data = {'dem':round(new_demand), 'olddem':round(old_demand), 'demc': round(new_demand-old_demand),'wait':exp,'waitc': (exp-exp_old), 'cap':round(capacity) }
            return HttpResponse(json.dumps(data), content_type='application/json')
        # recalculate with new nums and cont rules
        elif request.POST['type'] == 'recalculate':  
            
            #load and processes continuity rules
            table = ast.literal_eval(request.POST['id_table'])
            request.session['s_del_table'] = table
            s_nums=np.array(request.session['s_nums']) #new numbers
            doc =request.POST['doc']
                #generate list of shared categories
            #share everything if default 
            #estimate panel composition of each based on namcs
            ## = 
            ##request.session['phys_to_num'] = phys_to_num
            prov_to_num = request.session['prov_to_num']
            
            #Parse delegation rules
            nurse_dict={} #dictionary, keys: patients values: list of nurses that can provide for them
            if request.session['s_del_table'] and request.session['s_del_table'][0]["Rule"][:1] != "":
                for line in request.session['s_del_table']:
                    rule_dict={}
                    rule_categories=[[],[],[],[],[]]
                    for ind, element in enumerate(line['Rule'].split('AND')):
                        element = element.lstrip().rstrip()
                        rule_dict[element.split(':')[0]]=element.split(':')[1]
                    if 'Gender' in rule_dict:
                        rule_categories[0] = [2] if rule_dict['Gender']=='M' else [1] 
                    else:
                        rule_categories[0] = [1,2]
                    if 'Age' in rule_dict:
                        rule_categories[1]=list(range(age_bracket(rule_dict['Age'].split('-')[0]), age_bracket(rule_dict['Age'].split('-')[1]) + 1))
                    else:
                        rule_categories[1]=[1,2,3,4,5,6]
                    if 'Chronic' in rule_dict:
                        rule_categories[2]=list(range(chron_bracket(rule_dict['Cond'].split('-')[0]), chron_bracket(rule_dict['Age'].split('-')[1]) + 1))
                    else:
                        rule_categories[2]=[0,1,2,3]
                    if 'Visit' in rule_dict:
                        rule_categories[3]=[visit_bracket(rule_dict['Visit'])]
                    else:
                        rule_categories[3]=[1,2,3]
                    if 'Provider' in rule_dict:
                        rule_categories[4]=[phys_to_num[rule_dict['Provider']]]
                    else:
                        rule_categories[4]=phys_to_num.values() 
                    
                    rule = line['Delegation'] # name of delegated provider
                    # list of category integer indices for which the current rule applies
                    print("del %s" % rule)
                    categories_affected=[categ for categ in product(rule_categories[0], rule_categories[1], rule_categories[2], rule_categories[3], rule_categories[4])]
                    print("cat %s" % categories_affected)                    
                    #if provider is a physician, temporarily reassign patient                    
                    if rule in phys_to_num.keys():
                        
                     #for each visit type, transfer all patients                            
                        for category in categories_affected:
                            indfrom = category_full_to_ind[(category[0], category[1], category[2], category[3], category[4])] #get categories index of doctor losing patients
                            indto = category_full_to_ind[(category[0], category[1], category[2], category[3], phys_to_num[rule])] ##category from doc gaining patients
                            
                            #increment and decrement appropriate categories 
                            s_nums[indto] = s_nums[indto] + s_nums[indfrom]
                            print('transf %s' % s_nums[indfrom])
                            s_nums[indfrom] =  0 
                           
                            
                        request.session['s_nums'] = s_nums.tolist()
                    else: # if non_physician
                        #add nurse to approriate patient
                        for category in categories_affected:
                            if category in nurse_dict: 
                                nurse_dict[category_full_to_ind[category]] += [prov_to_num[rule]]
                            else:
                                nurse_dict[category_full_to_ind[category]] = [prov_to_num[rule]]
                        #save to session          
                        print("nurse_Dct %s" % nurse_dict)
                        request.session['s_nurse_dict'] =str(nurse_dict) #add to session
            else:
                request.session['s_nurse_dict'] =str({})
             #run simulator
            print("importing")
            from  waitestapp import waitsimulator
            print("preparing")
           
            freqs=np.array(request.session['freqs'] )
            durs=np.array(request.session['durs'] )
            urgents=np.array(request.session['urgents'] )
            ##shared_categories = request.session['shared_categories'] 
            phys_mins=ast.literal_eval(request.session['phys_mins']) 
            non_phys_mins=ast.literal_eval(request.session['non_phys_mins'])
            
            
            print(phys_mins)
            doc_lookup= np.array(request.session['doc_lookup'])
            from collections import Counter
            print(Counter(doc_lookup))
            #run simulation 
            print("simulating")
            
            K=waitsimulator.mat_sim(urgents=urgents, cut_off=0, carve_out=True,  days=500, freqs=freqs, durs=durs,  nums=s_nums, num_classes=len(durs), nurse_dict=nurse_dict, phys_mins=phys_mins, non_phys_mins=non_phys_mins, doc_lookup=doc_lookup, shared_categories=[])
            print("storing...")
            #get matrix of days waited vs patient demand class
            request.session['s4_wait_mat']  = K[0].tolist()
            
            
            #get wait for doctor, as well as change in wait
            exp, p = overall_query( doc, K[0], phys_to_num, doc_lookup , 100)
            exp_old, p = overall_query( doc, waited, phys_to_num, doc_lookup, 100)
           
            #get old and new demand
            old_demand=0
            new_demand=0
            for i, freq in enumerate(freqs):
               if doc_lookup[i] == phys_to_num[doc]: 
                   old_demand += nums[i]*freq*360*durs[i]*(1/60)
                   new_demand += s_nums[i]*freq*360*durs[i]*(1/60)
            #get capacity 
            capacity_info=ast.literal_eval(request.session['phys_capacity'])[doc]
            capacity = capacity_info
            request.session['scenario4'] = [round(new_demand), round(new_demand-old_demand),exp,(exp-exp_old), round(capacity)]
            data = {'dem':round(new_demand), 'olddem':round(old_demand), 'demc': round(new_demand-old_demand),'wait':exp,'waitc': (exp-exp_old), 'cap':round(capacity) }
            return HttpResponse(json.dumps(data), content_type='application/json')         
        
        else:
            return HttpResponse('done')
        
    else:       
        ##table_query_generator(waited, doc, cond, gender, age, visit, q, category_full_to_ind, phys_to_num)    
        return render(request, 'waitestapp/scenario_4.html', {'phys_list':request.session['phys_list'], 'nonphys_list':request.session['nonphys_list']})


@ensure_csrf_cookie
def scenario_capacity(request):
    if request.method == 'POST':
        import ast
        table = ast.literal_eval(request.POST['id_table'])
        #get lists of physicians, non physicians
        phys_list=[record['Provider Name'] for record in table if record['Position']=='Physician']
        nonphys_list=[record['Provider Name'] for record in table if record['Position']!='Physician']
        request.session['s_phys_list'] = phys_list
        request.session['s_nonphys_list'] = nonphys_list
        request.session['s_capacity_table'] = table
        print("view scenario post")
        
    try: 
        table_data = request.session['s_capacity_table']
        print("view scenario s_")
        print(table_data)
    except KeyError:
        table_data = key_clean(request.session['capacity_table']) 
        print("view scenario s")
        print(table_data)
    else:
        table_data = key_clean(table_data)
    return render(request, 'waitestapp/scenario_capacity.html', {'table_data':table_data})
    
@ensure_csrf_cookie    
def scenario_aff(request):
    if request.method == 'POST':
        import ast
        table = ast.literal_eval(request.POST['id_table'])
        request.session['s_aff_table'] = table
    try: 
        table_data = request.session['s_aff_table']
    except KeyError:
        table_data = key_clean(request.session['aff_table']) 
    else:
        table_data = key_clean(table_data)
    return render(request, 'waitestapp/scenario_aff.html',{'phys_list':request.session['s_phys_list'], 'table_data':table_data})

@ensure_csrf_cookie
def scenario_attr(request):
    if request.method == 'POST':
        import ast
        table = ast.literal_eval(request.POST['id_table'])
        patTable = ast.literal_eval(request.POST['patTable'])
        request.session['s_attr_table'] = table
        request.session['s_patTable'] = patTable
    try: 
        table_data = request.session['s_attr_table']
        pat_table_data = request.session['s_patTable']
    except KeyError:
        table_data = key_clean(request.session['attr_table']) 
        pat_table_data = key_clean(request.session['patTable'])
    else:
        table_data = key_clean(table_data)
        pat_table_data = key_clean(pat_table_data)
    return render(request, 'waitestapp/scenario_attr.html', {'phys_list':request.session['s_phys_list'],'table_data':table_data,'pat_table_data':pat_table_data})

@ensure_csrf_cookie    
def scenario_contrule(request):
    if request.method == 'POST':
        import ast
        table = ast.literal_eval(request.POST['id_table'])
        request.session['s_cont_table'] = table
        request.session['s_defCont'] = request.POST['defCont']
    try: 
        table_data = request.session['s_cont_table']
        defCont = request.session['s_defCont']
        if defCont == "share":
            Share = "selected"
            NoShare = ""
        else:
            Share = ""
            NoShare = "selected"
    except KeyError:
        table_data = request.session['cont_table']
        defCont = request.session['defCont']
        if defCont == "share":
            Share = "selected"
            NoShare = ""
        else:
            Share = ""
            NoShare = "selected"
    else:
        table_data = key_clean(table_data)
    return render(request, 'waitestapp/scenario_contrule.html', {'phys_list':request.session['s_phys_list'],'table_data':table_data,'share':Share, 'noshare':NoShare} )

@ensure_csrf_cookie
def scenario_delrule(request):
    if request.method == 'POST':
        import ast
        table = ast.literal_eval(request.POST['id_table'])
        request.session['s_del_table'] = table
    try: 
        table_data = request.session['s_del_table']
    except KeyError:
        table_data = initial_data.del_json_scenario ## NOT UNTIL IMPLEMENTED? request.session['del_table'] 
    else:
        table_data = key_clean(table_data)
    return render(request, 'waitestapp/scenario_delrule.html', {'phys_list':request.session['s_phys_list'], 'nonphys_list':request.session['s_nonphys_list'],'table_data':table_data})

    
@ensure_csrf_cookie
def scenario_utilization(request):
    #import numpy as np
    np.random.seed(42)
    import ast
    request.session['s_cont_table'] = []
    request.session['s_defCont'] = "noshare"
    request.session['s_del_table'] = []
    
    if request.method == 'POST':
        #run simulator
        print("importing")
        from  waitestapp import waitsimulator
        print("preparing")
        nums=np.array(request.session['s_nums']) 
        freqs=np.array(request.session['s_freqs'] )
        durs=np.array(request.session['s_durs'] )
        urgents=np.array(request.session['urgents'] )
        shared_categories = request.session['s_shared_categories'] 
        phys_mins=ast.literal_eval(request.session['s_phys_mins'])
        non_phys_mins=ast.literal_eval(request.session['s_non_phys_mins'])
        nurse_dict = ast.literal_eval(request.session['s_nurse_dict']) # ADD LATER TO WAITAPP
        print(phys_mins)
        doc_lookup= np.array(request.session['s_doc_lookup'])
        from collections import Counter
        print(Counter(doc_lookup))
        #run simulation 
        print("simulating")
        
        K=waitsimulator.mat_sim(urgents=urgents, cut_off=0, carve_out=True,  days=500, freqs=freqs, durs=durs,  nums=nums, num_classes=len(durs), nurse_dict=nurse_dict, phys_mins=phys_mins, non_phys_mins=non_phys_mins, doc_lookup=doc_lookup, shared_categories=shared_categories)
        print("storing...")
        #get matrix of days waited vs patient demand class
        request.session['s_wait_mat']  = K[0].tolist()
        
        return HttpResponse('done')
    else:                      
        from itertools import product    
        provTable = request.session['s_capacity_table']       
                    
        #parse doctors and their hours
        prov_to_num={}
        num_to_prov={} #non physosian providers
        phys_to_num={}
        num_to_phys={}
        phys_mins={}
        non_phys_mins={}
        for j, row in enumerate(provTable):
            i = j + 1 #reserve doctor code 0 for any doctor        
             #map names to numbers
            print(row)
            
            #note pprovider avg. min per day
            if row['Position'] == 'Physician': 
                phys_to_num[row['Provider Name']] = i        
                num_to_phys[i] = row['Provider Name']
                phys_mins[i]=60*int(row['Hours Per Day'])*(int(row['Days Per Year']))/360
            else:
                non_phys_mins[i]=60*int(row['Hours Per Day'])*(int(row['Days Per Year']))/360
                prov_to_num[row['Provider Name']] = i        
                num_to_prov[i] = row['Provider Name']
        
        #generate list of shared categories
        #share everything if default 
        if request.session['s_defCont'] == 'share':
            shared_categories = [categ for categ in product([1,2],[1,2,3,4,5,6], [0,1,2,3],[1,2,3],phys_to_num.values())]
        else:
            shared_categories = []
        for line in request.session['s_cont_table']:
            rule_dict={}
            rule_categories=[[],[],[],[],[]]
            #dictionary for each rule component
            for ind, element in enumerate(line['Rule'].split('AND')):
                element = element.lstrip().rstrip()                
                rule_dict[element.split(':')[0]]=element.split(':')[1]
            if 'Gender' in rule_dict:
                rule_categories[0] = [2] if rule_dict['Gender']=='M' else [1] 
            else:
                rule_categories[0] = [1,2]
            if 'Age' in rule_dict:
                rule_categories[1]=list(range(age_bracket(rule_dict['Age'].split('-')[0]), age_bracket(rule_dict['Age'].split('-')[1]) + 1))
            else:
                rule_categories[1]=[1,2,3,4,5,6]
            if 'Chronic' in rule_dict:
                rule_categories[2]=list(range(chron_bracket(rule_dict['Cond'].split('-')[0]), chron_bracket(rule_dict['Age'].split('-')[1]) + 1))
            else:
                rule_categories[2]=[0,1,2,3]
            if 'Visit' in rule_dict:
                rule_categories[3]=[visit_bracket(rule_dict['Visit'])]
            else:
                rule_categories[3]=[1,2,3]
            if 'Provider' in rule_dict:
                rule_categories[4]=[phys_to_num[rule_dict['Provider']]]
            else:
                rule_categories[4]=phys_to_num.values()
            # list of category integer indices for which the current rule applies
            rule = line['Continuity']        
            
            categories_affected=[categ for categ in product(rule_categories[0], rule_categories[1], rule_categories[2], rule_categories[3], rule_categories[4])]
            
            for category in categories_affected:
                if rule == 'Share':
                    shared_categories.append(category)
                #if default share and rule is no share, remove categry from shared list
                elif request.session['s_defCont'] == 'share' and rule == "Do Not Share" and (category in  shared_categories):
                    while category in shared_categories: shared_categories.remove(category)  
                        
                      
        #estimate panel composition of each based on namcs
        request.session['s_prov_to_num'] = prov_to_num
        request.session['s_phys_to_num'] = phys_to_num
        panelTable = request.session['s_attr_table']
        
        #Parse delegation rules
        nurse_dict={} #dictionary, keys: patients values: list of nurses that can provide for them
        for line in request.session['s_del_table']:
            rule_dict={}
            rule_categories=[[],[],[],[],[]]
            for ind, element in enumerate(line['Rule'].split('AND')):
                element = element.lstrip().rstrip()
                rule_dict[element.split(':')[0]]=element.split(':')[1]
            if 'Gender' in rule_dict:
                rule_categories[0] = [2] if rule_dict['Gender']=='M' else [1] 
            else:
                rule_categories[0] = [1,2]
            if 'Age' in rule_dict:
                rule_categories[1]=list(range(age_bracket(rule_dict['Age'].split('-')[0]), age_bracket(rule_dict['Age'].split('-')[1]) + 1))
            else:
                rule_categories[1]=[1,2,3,4,5,6]
            if 'Chronic' in rule_dict:
                rule_categories[2]=list(range(chron_bracket(rule_dict['Cond'].split('-')[0]), chron_bracket(rule_dict['Age'].split('-')[1]) + 1))
            else:
                rule_categories[2]=[0,1,2,3]
            if 'Visit' in rule_dict:
                rule_categories[3]=[visit_bracket(rule_dict['Visit'])]
            else:
                rule_categories[3]=[1,2,3]
            if 'Provider' in rule_dict:
                rule_categories[4]=[phys_to_num[rule_dict['Provider']]]
            else:
                rule_categories[4]=phys_to_num.values() 
            
            rule = line['Delegation'] # name of non physisian provider
            # list of category integer indices for which the current rule applies
           
            categories_affected=[categ for categ in product(rule_categories[0], rule_categories[1], rule_categories[2], rule_categories[3], rule_categories[4])]
            
            #add nurse to approriate patient
            for category in categories_affected:
                if category in nurse_dict: 
                    nurse_dict[category] += [prov_to_num[rule]]
                else:
                    nurse_dict[category] = [prov_to_num[rule]]
        #save to session          
        request.session['s_nurse_dict'] =str(nurse_dict)
        #generate panels:
        from collections import Counter
        #lookup index for each visit type   
        category_full_to_ind = {}
        nums = []
        freqs = []
        durs = []
        doc_lookup = []
        ind = 0 # start increment counter
        phys_demand = {} #dictionary of demand per physician
        for panel in panelTable:
            np.random.seed(42)
            acute_demand = 0 # start counter of demand
            prev_demand = 0
            chronic_demand = 0
            doc = phys_to_num[panel['Physician']]
            num_males = int(panel['Males'])
            num_females = int(panel['Females'])
            problem_females =['1, 1, 2',
            '1, 2, 1',
            '1, 1, 3',
            '1, 3, 3',
            '1, 2, 3',
            '1, 2, 2']
            
            noprob_females=['1,3,1',
             '1,4,3',
             '1,2,0',
             '1,4,2',
             '1,6,3',
             '1,5,3']
            problem_males = ['2, 2, 1',
            '2, 1, 2',
            '2, 1, 3',
            '2, 2, 3']
            
            noprob_males = ['2,5,3',
             '2,3,1',
             '2,2,0',
             '2,5,1',]
            #generate panel accordin to male female ratio and namcs proportions
            np.random.seed(42)
            male_dist = Counter(np.random.choice(initial_data.male_cats, num_males, initial_data.male_p))
            np.random.seed(42)
            female_dist = Counter(np.random.choice(initial_data.female_cats, num_females, initial_data.female_p))
            #uneven the distributions            
            if panel['Physician'] == 'Doctor 1':
                for prob, noprob in zip(problem_females, noprob_females):
                    transf = min(50, female_dist[noprob])
                    female_dist[noprob] -= transf
                    female_dist[prob] += transf
                for prob, noprob in zip(problem_males, noprob_males):
                    transf = min(50, male_dist[noprob])
                    male_dist[noprob] -= transf
                    male_dist[prob] += transf
            if panel['Physician'] == 'Doctor 3':
                for prob, noprob in zip(problem_females, noprob_females):
                    transf = min(10, female_dist[noprob])
                    female_dist[noprob] -= transf
                    female_dist[prob] += transf
                for prob, noprob in zip(problem_males, noprob_males):
                    transf = min(10, male_dist[noprob])
                    male_dist[noprob] -= transf
                    male_dist[prob] += transf
            #get full distribution of patient types on panel
            panel_dict = male_dist + female_dist
            #generate import simulation data
            for patient_category in panel_dict:
                #ACUTE            
                #input sex,age,chron,visit, doc   
                ##print((str(patient_category[0]),str(patient_category[2]),str(patient_category[4]),1,doc))
                category_full_to_ind[(int(patient_category[0]),int(patient_category[2]),int(patient_category[4]),1,int(doc))] = ind
                nums.append(int(panel_dict[patient_category])) #append number represented
                #input sex, age, chron, visit
                try:
                    freq =initial_data.freq_dict[(int(patient_category[0]),int(patient_category[2]),int(patient_category[4]),1)]
                except KeyError:
                    freq = 0
                try:
                    dur =initial_data.durs_dict[(int(patient_category[0]),int(patient_category[2]),int(patient_category[4]),1)]
                except KeyError:
                    dur = 0
                freqs.append(freq)
                durs.append(dur)      
                #add to acute demand
                acute_demand += int(panel_dict[patient_category])*freq*360*dur*(1/60)
                doc_lookup.append(int(doc))            
                ind += 1 #increment index
                #PREV
                #input sex,age,chron,visit, doc
                category_full_to_ind[(int(patient_category[0]),int(patient_category[2]),int(patient_category[4]),2,int(doc))] = ind
                nums.append(panel_dict[patient_category]) #append number represented
                #input sex, age, chron, visit
                try:
                    freq = initial_data.freq_dict[(int(patient_category[0]),int(patient_category[2]),int(patient_category[4]),2)]
                except KeyError:
                    freq = 0
                try:
                    dur = initial_data.durs_dict[(int(patient_category[0]),int(patient_category[2]),int(patient_category[4]),2)]
                except KeyError:
                    dur = 0
                freqs.append(freq)
                durs.append(dur) 
                #add to prev demand
                prev_demand += int(panel_dict[patient_category])*freq*360*dur*(1/60)
                doc_lookup.append(int(doc))
                ind +=1 #increment index
                #CHRONIC
                #input sex,age,chron,visit, doc
                category_full_to_ind[(int(patient_category[0]),int(patient_category[2]),int(patient_category[4]),3,int(doc))] = ind
                nums.append(panel_dict[patient_category]) #append number represented
                #input sex, age, chron, visit
                try:
                    freq =initial_data.freq_dict[(int(patient_category[0]),int(patient_category[2]),int(patient_category[4]),3)]
                except KeyError:
                    freq = 0
                try:
                    dur =initial_data.durs_dict[(int(patient_category[0]),int(patient_category[2]),int(patient_category[4]),3)]
                except KeyError:
                    dur = 0
                freqs.append(freq)
                durs.append(dur)   
                #add to acute demand
                chronic_demand += int(panel_dict[patient_category])*freq*360*dur*(1/60)
                doc_lookup.append(int(doc))
                ind +=1 #increment index
            #add doctor demand to dictionary, list is demands by visit, total demand, placeholders for total capacity, team name,  team members, and capacity-demand, and finally panel size
            phys_demand[panel['Physician']] = [acute_demand, prev_demand, chronic_demand, sum((acute_demand, prev_demand, chronic_demand)), None, None, None, None , num_males + num_females]
        
        #convert list of shared categories to indices
        shared_categories = [category_full_to_ind[category] for category in shared_categories if category in category_full_to_ind]
        #save nums, freqs, durs,  category_full_to_ind, shared_categories, phys_mins
        print(1)
        request.session['s_nums'] = nums
        print(2)
        request.session['s_freqs'] = freqs
        print(3)
        request.session['s_durs'] = durs
        print(4)
        request.session['s_shared_categories'] = shared_categories
        print(5)
        request.session['s_phys_mins'] = str(phys_mins)
        request.session['s_non_phys_mins'] = str(non_phys_mins)
        print(6)
        request.session['s_doc_lookup'] = doc_lookup
        print(7)
        request.session['s_category_full_to_ind'] = str(category_full_to_ind)
        print(8)
        #prepare capacity
        capacity_table = request.session['capacity_table']
        print(capacity_table)
        print(9)
        ##phys_capacity = {}
        team_capacity = {}  
        ##phys_teams = {}
        #create lookup dictionary to map patient conditions to index 
        '''
        category_product=itertools.product([1,2],[0,1,2,3,4,5],[0,1,2,3],phys_to_num.values())
        category_name_key_mapping={}
        for ind, category in enumerate(category_product):
            category_name_key_mapping[category]=ind
            ind_to_category[ind] = category 
            
        #dictionary keyed to integer representations for each key (gender, age bracket, chron condition bracket, physician)
        request.session['category_name_key_mapping'] = category_name_key_mapping
        request.session['ind_to_category'] = ind_to_category   
        '''        
        #note capacities for teams and physicians (and compile a list of physicians for each team)
        phys_capacity = {} #keeptrack of individual hours/days per year
        
        for record in capacity_table:
            if record['Position'] == 'Physician':
                phys_capacity[record['Provider Name']] = [int(record['Hours Per Day']), int(record['Days Per Year'])]
                phys_demand[record['Provider Name']][4] = int(record['Hours Per Day'])*int(record['Days Per Year'])
                phys_demand[record['Provider Name']][5] = record['Team'] #team name
                #imbalance
                phys_demand[record['Provider Name']][7] = phys_demand[record['Provider Name']][4] - phys_demand[record['Provider Name']][3]
            try:
                team_capacity[record['Team']][0] += [record['Position'] + ' ' + record['Provider Name']]
                team_capacity[record['Team']][1] += int(record['Hours Per Day'])*int(record['Days Per Year'])
            except KeyError:
                team_capacity[record['Team']] = ['','']
                team_capacity[record['Team']][0] = [record['Position']  + ' ' + record['Provider Name']]
                team_capacity[record['Team']][1] = int(record['Hours Per Day'])*int(record['Days Per Year'])
        for phys in phys_demand: # get list of team members for each physician
            if phys_demand[phys][5] =='No Team':
                 phys_demand[phys][5] = ''
                 phys_demand[phys][6]  = []
            else:
                phys_demand[phys][6]=team_capacity[phys_demand[phys][5]][0]
        print('ok')
        print(phys_demand)
        request.session['phys_capacity']=str(phys_capacity) #stor phys capacity
        return render(request, 'waitestapp/scenario_utilization.html', {'phys_demand': phys_demand})

@ensure_csrf_cookie    
def scenario_results(request):
    import ast
    #import numpy as np
    np.random.seed(42)
    old_waited = np.array(request.session['wait_mat'])
    waited = np.array(request.session['s_wait_mat'])
    ##print("...waited")
    ##print(waited)
    category_full_to_ind =  ast.literal_eval(request.session['s_category_full_to_ind'])
    ##print(len(category_full_to_ind))
    ##print(category_full_to_ind.keys())
    phys_to_num = request.session['s_phys_to_num']
    doc_lookup = request.session['s_doc_lookup']
    if request.method == 'POST':    
        import json
               
        #change overall expected wait
        if  request.POST['type'] ==  'overall':
            doc = request.POST['doc']
            exp = overall_query( doc, waited, phys_to_num, doc_lookup)
            exp_old = overall_query( doc, old_waited, phys_to_num, doc_lookup)
            data = {'exp':exp,'expd': (exp-exp_old)}
            return HttpResponse(json.dumps(data), content_type='application/json')
        #change wait for individual row or query
        elif request.POST['type'] == 'rowselect':
            gender  = request.POST['gender']
            gender = gender_bracket(gender)
            age  = request.POST['age']
            age=int(age)        
            chron = request.POST['chron']
            chron=int(chron[0])            
            doc = request.POST['doc']            
           
            visit = request.POST['visit']
            visit = visit_bracket(visit)
            q = int(request.POST['perc'])
            ##print(gender,age,chron,visit )
            ##print([phys_to_num[phys] for phys in phys_to_num ])
            exp, p = table_query_generator(waited, doc, chron, gender, age, visit, q, category_full_to_ind, phys_to_num)
            exp_old, p_old = table_query_generator(old_waited, doc, chron, gender, age, visit, q, category_full_to_ind, phys_to_num)
            data = {'exp':exp, 'p':p, 'expd':(exp - exp_old), 'pd': (p - p_old)}
            return HttpResponse(json.dumps(data), content_type='application/json')
    else:       
        ##table_query_generator(waited, doc, cond, gender, age, visit, q, category_full_to_ind, phys_to_num)    
        return render(request, 'waitestapp/scenario_results.html', {'phys_list':request.session['s_phys_list']})
        


# METHODS FOR VIEWS
#replaces spaces in dictionary keys with underscores for ease of use in templates
def key_clean(table):
    new_table = []
    for old_dict in table:
        new_dict = {}
        for key in old_dict:
            new_dict[key.replace(" ","_")] = old_dict[key]
        new_table.append(new_dict)
    return new_table

def coding_for_provider(provider_type):
    if provider_type == "Physician":
        coding = 1
    else: 
        coding = 2
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

def gender_bracket(gender):
            
    if gender == 'M':
        gender_bracket = 2   
    else:
        gender_bracket = 1
    return gender_bracket
    

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
        
        
#TABLE QUERY METHODS       

    
def exp_percentile( matrix, percentile):
    #import numpy as np
    np.random.seed(42)
    try:
        dist=np.sum(matrix, axis=1)
        
    except ValueError:
        dist=matrix
    ##print(dist)
    exp=sum(dist*np.array(range(0,500)))/sum(dist)
    ##percentile=int(round(np.percentile(np.repeat(np.array(range(0,500)),dist), percentile)))
    #each patient coded by their waitime
    coded_patients = np.repeat(np.array(range(0,500)),dist)
    #get percent of patients who waited less than specified number of days
    percentile = str(round(100*(coded_patients < percentile).sum()/coded_patients.size))[:-2] + "%"
    #CHECK HERE 
    try:
        exp=int(exp)
    except TypeError:
        exp=int(sum(exp))        
    return exp, percentile        
 
# get overall estimate
def overall_query( doc, waited, phys_to_num, doc_lookup, q):
    #import numpy as np
    np.random.seed(42)
    if not doc == 'Overall':
        #get provider integer code for doctor specified in dropdown
        doc_code=phys_to_num[doc]
        print("doc_lookup")
        print(doc_lookup)
        print(doc_code)
        #get column indices whose provider (mapped to by doc_pat_index) matches the comboBox selection indicated by doc_code
        columns_relevant=np.where(np.array(doc_lookup) == doc_code)[0]
        print("columns_relevant")
        print(columns_relevant)
        print(len(columns_relevant))
        print(waited)
        matrix= waited[:,columns_relevant]
        print("matrix.shape")
        print(matrix.shape)
        
    else:
        matrix= waited
    '''
    try:
        dist=np.sum(matrix, axis=1) # might fail to sum if only one column
    except ValueError:
        dist=matrix
    exp=sum(dist*np.array(range(0,500)))/sum(dist)
    #CHECK HERE 
    try:
        exp=int(exp)
    except TypeError:
        exp=int(sum(exp))
    except ValueError: #no distribution for this!
        exp='N/A'
        '''
    try: 
        exp, percentile = exp_percentile(matrix, q)
    except ValueError:
        exp, percentile = ('N/A', 'N/A')
    return exp, percentile
    
def table_query_generator(waited, doc, cond, gender, age, visit, q, category_full_to_ind, phys_to_num):
    #get integer category
    ##gender= 2 if (gender == 'M') else 1       
    if not doc == 'Overall':       
        try: # get index of patient type in question
            category=category_full_to_ind[(gender, age, cond, visit, phys_to_num[doc])]    
            ##print("...category")
            ##print(category)
        except KeyError:
            ##print('NOOOO')
            exp, percentile = ('N/A', 'N/A')
        else:
            #get expected value and percentile of appropriate column
            try: 
                exp, percentile = exp_percentile(waited[:,category], q)
            except ValueError:
                exp, percentile = ('N/A', 'N/A')
    else:
       
        indices = [category_full_to_ind[(gender,age, cond, visit, phys_to_num[phys])] for phys in phys_to_num if (gender,age, cond, visit, phys_to_num[phys]) in category_full_to_ind]         
        ##print("...indicies")
        ##print(indices) 
        try:
            exp, percentile = exp_percentile(waited[:,indices], q)
        except ValueError:
            exp, percentile = ('N/A', 'N/A')
        
    return exp, percentile

#get for overall visit type
def visit_query_generator(waited, doc, visit, q, category_full_to_ind, phys_to_num):
    #get integer category
    from itertools import product
    ##gender= 2 if (gender == 'M') else 1       
    if not doc == 'Overall': 
        indices=[category_full_to_ind[i] for i in product([1,2],[1,2,3,4,5,6],[0,1,2,3],[visit],[phys_to_num[doc]])]
    else:
        docs=phys_to_num.values()
        indices=[category_full_to_ind[i] for i in product([1,2],[1,2,3,4,5,6],[0,1,2,3],[visit],docs )]
       
    try:
        exp, percentile = exp_percentile(waited[:,indices], q)
    except ValueError:
        exp, percentile = ('N/A', 'N/A')
        
    return exp, percentile
    
    
#query some combination of all
def visit_query_generator_alls(waited, docs, ages, chrons, genders, visits, q, category_full_to_ind, phys_to_num):
    from itertools import product
    indices=[category_full_to_ind[i] for i in product(genders,ages,chrons,visits,docs)]
           
    try:
        exp, percentile = exp_percentile(waited[:,indices], q)
    except ValueError:
        exp, percentile = ('N/A', 'N/A')
        
    return exp, percentile


#function to adjust ratios
def adjust_ratios(full_p = initial_data.full_p, full_cats=initial_data.full_cats, sex=[50,50], age=[15,15,20,20,15,15],chronic=[50,20,15,15],ageF=[15,15,20,20,15,15],chronicF=[50,20,15,15]):
    np.random.seed(42)
    male_p=[]   
    female_p=[]
    for cat, p in zip(full_cats, full_p):
        if cat[0] == 1:
            female_p.append(p)
            male_p.append(0)
        else:
            female_p.append(0)
            male_p.append(p)
    mal_tot = sum(male_p)
    fem_tot = sum(female_p)
    male_p = [p/mal_tot for p in male_p]
    female_p = [p/fem_tot for p in male_p]
    if age:
        #initialize dictionary of category idenifier and values[current proportion, requested proportion, multiplicative factor]
        divisions={i+1:[0,perc*.01,0] for i,perc in enumerate(age)}
        new_p = adjust_category(1, divisions, full_cats, male_p)
        if new_p: #if no errors, replace proportions with adjusted proportions
            male_p=new_p
    
    if chronic:
        #initialize dictionary of category idenifier and values[current proportion, requested proportion, multiplicative factor]
        divisions={i:[0,perc*.01,0] for i,perc in enumerate(chronic)}
        new_p = adjust_category(2, divisions, full_cats, male_p)
        if new_p: #if no errors, replace proportions with adjusted proportions
            male_p=new_p
            
    if ageF:
        #initialize dictionary of category idenifier and values[current proportion, requested proportion, multiplicative factor]
        divisions={i+1:[0,perc*.01,0] for i,perc in enumerate(ageF)}
        new_p = adjust_category(1, divisions, full_cats, male_p)
        if new_p: #if no errors, replace proportions with adjusted proportions
            female_p=new_p
    
    if chronicF:
        #initialize dictionary of category idenifier and values[current proportion, requested proportion, multiplicative factor]
        divisions={i:[0,perc*.01,0] for i,perc in enumerate(chronicF)}
        new_p = adjust_category(2, divisions, full_cats, male_p)
        if new_p: #if no errors, replace proportions with adjusted proportions
            female_p=new_p
            
    if sex:
        male_p = [p*sex[0]*.01 for p in male_p]
        female_p = [p*sex[0]*.01 for p in female_p]
        full_p = [max(m,f) for m, f in zip(male_p,female_p)]
    else:
        male_p = [p*mal_tot for p in male_p]
        female_p = [p*fem_tot for p in female_p]
        full_p = [max(m,f) for m, f in zip(male_p,female_p)]
    '''
    
    if age:
        #initialize dictionary of category idenifier and values[current proportion, requested proportion, multiplicative factor]
        divisions={i+1:[0,perc*.01,0] for i,perc in enumerate(age)}
        new_p = adjust_category(1, divisions, full_cats, full_p)
        if new_p: #if no errors, replace proportions with adjusted proportions
            full_p=new_p
    
    if chronic:
        #initialize dictionary of category idenifier and values[current proportion, requested proportion, multiplicative factor]
        divisions={i:[0,perc*.01,0] for i,perc in enumerate(chronic)}
        new_p = adjust_category(2, divisions, full_cats, full_p)
        if new_p: #if no errors, replace proportions with adjusted proportions
            full_p=new_p  
            
            if sex:
     #initialize dictionary of category idenifier and values[current proportion, requested proportion, multiplicative factor]
        divisions={i+1:[0,perc*.01,0] for i,perc in enumerate(sex)}
        new_p = adjust_category(0, divisions, full_cats, full_p)
        if new_p: #if no errors, replace proportions with adjusted proportions
            full_p=new_p
        '''
    return full_p
    
            
def adjust_category(category, divisions, full_cats, full_p ):
    #category: specific trait (e.g. integer code for male) divisions: dictionary of proportions for e..g. sex      
    #add up current  total proportion for each category       
    for cat, proportion in zip(full_cats, full_p):
        
        divisions[cat[category]][0] += proportion
    for entry in divisions:        
        try:
           divisions[entry][2] =  divisions[entry][1]/divisions[entry][0]    
        except ZeroDivisionError:
            print("Divide by zero in category adjustment!")
            return False
    #multiply proportions of categories by expansion factor from above above, depending on category of divisions
    new_p = [] #initiialize
    for cat, proportion in zip(full_cats, full_p):
        new_p.append(proportion*divisions[cat[category]][2])
    return new_p
         
