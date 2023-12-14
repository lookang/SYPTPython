# original code by https://github.com/not-even-wong 
import pandas as pd
import numpy as np
import random

#A_list=['ACJC', 'HCI', 'NJC', 'NUSH', 'RI', 'RVHS', 'RGS'] #Cat A
# A_list=['HCI', 'NUSH', 'RGS', 'RI', 'RVHS'] #Cat B but I already used "A_list" everywhere so I'll stick with that variable name
A_list=['HCI', 'NUSH']
room_list=['A','B','C','D']

#import data




    
#solved=0

#while solved<1000:

assignment_matrix=pd.read_csv("Cat A Assignment matrix.csv")
assignment_matrix.columns=['0','1','2','3','4','5']
assignment_matrix=assignment_matrix.fillna(0)


for i in range(assignment_matrix.shape[0]):
    for j in range(1,assignment_matrix.shape[1]):
        if assignment_matrix.iloc[i,j]==0:
            pass
        else:
            assignment_matrix.iloc[i,j]=assignment_matrix.iloc[i,j][0]
assignment_matrix_original=assignment_matrix.copy(deep=True)

for i in range(assignment_matrix.shape[0]):
    assignment_matrix.iloc[i,0]=assignment_matrix.iloc[i,0][:-1]

assignment_matrix_original=assignment_matrix.copy(deep=True)
assignment_matrix_original['0']=pd.read_csv("Cat A Assignment matrix.csv")['Unnamed: 0']
assignment_matrix=assignment_matrix.replace('RI','Raffles').replace('RGS','Raffles')
print(assignment_matrix)

juror_data=pd.read_csv("Cat A jurors.csv",delimiter=";")
print(juror_data)

juror_data_original=juror_data.copy(deep=True)
juror_data=juror_data.replace('RI','Raffles').replace('RGS','Raffles')
print(juror_data)

#set up list to track number of times each juror has taken a role
juror_data.loc[juror_data['Affiliation']=="Head"]
head_assignment_count=np.zeros(len(juror_data.loc[juror_data['Affiliation']=="Head"]))
juror_assignment_count=np.zeros(len(juror_data))

#set up array to track number of times each juror has judged each school
school_juror_matrix=pd.DataFrame(np.zeros([len(juror_data),len(assignment_matrix['0'].unique())]),columns=assignment_matrix['0'].unique(),index=juror_data['Name'])
team_juror_matrix=pd.DataFrame(np.zeros([len(juror_data),len(assignment_matrix_original['0'].unique())]),columns=assignment_matrix_original['0'].unique(),index=juror_data['Name'])

"""
structure for assignment:
juror_assignments[round][room][H,1,2,3 or 4]
set up empty nested dictionary first
"""


juror_assignments={}
for PF in [1,2,3,4,5]:
    juror_assignments[PF]={}
    for room in room_list:
        juror_assignments[PF][room]={}
        for juror in ['H',1,2,3,4]:
            juror_assignments[PF][room][juror]='none'

try:
    del(affiliated_jurors,priority_order,rival_jurors,participants,room)
except:
    pass

room_list

#do HEAD assignments
try:
    for PF in [1,2,3,4,5]: #assign all head jurors first, since this is priority - avoid situation of having assigned head jurors as normal jurors and running out of staff
        for room in room_list:
            
            print("")
            print("--------")
            print(str(PF)+room)
            print("")
            print(PF)
            print(room)
            if (PF==(1) or PF==(5)) and room==('D'):
                pass
            else:
                current_priority_index=0 #this is the position in the priority order
                priority_order=np.unique(head_assignment_count)
                participants=assignment_matrix.iloc[np.where(assignment_matrix[str(PF)]==room)[0]]['0']
                teams=assignment_matrix_original.iloc[np.where(assignment_matrix_original[str(PF)]==room)[0]]['0']
                
                
                
                while juror_assignments[PF][room]['H']=='none':
                    current_priority_count=priority_order[current_priority_index]
                    head_juror_priority_index=np.where(head_assignment_count==current_priority_count)[0]
                    print("These jurors have priority: "+juror_data.iloc[head_juror_priority_index]['Name'].str.cat(sep=', '))
                    
                    #check for repeat schools
                    """for juror in head_juror_priority_index:
                        for school in participants:
                            if school_juror_matrix.loc[juror_data['Name'][juror],school]>0:
                                print(juror_data['Name'][juror]+' has already been head juror for '+school)
                                head_juror_priority_index=np.delete(head_juror_priority_index,np.where(head_juror_priority_index==juror))"""
    
                    for juror_a in head_juror_priority_index:
                        for team in teams:
                            if team_juror_matrix.loc[juror_data['Name'][juror_a],team]>0:
                                print(juror_data['Name'][juror_a]+' has already been juror for '+team)
                                head_juror_priority_index=np.delete(head_juror_priority_index,np.where(head_juror_priority_index==juror_a))
                                
                    #check for juror being in more than one place at the same time
                    for room_temp in room_list:
                        if len(juror_data.loc[juror_data['Name']==juror_assignments[PF][room_temp]['H']])!=0:
                            juror_a=juror_data.loc[juror_data['Name']==juror_assignments[PF][room_temp]['H']].index[0]
                            if len(np.where(head_juror_priority_index==juror_a)[0])>0:
                                head_juror_priority_index=np.delete(head_juror_priority_index,np.where(head_juror_priority_index==juror_a))
                                print("Remove "+juror_data.iloc[juror_a]['Name']+" who is already assigned elsewhere this round")
                    
                    print('Remaining jurors: '+juror_data.iloc[head_juror_priority_index]['Name'].str.cat(sep=', '))
        
                    if len(head_juror_priority_index)!=0:
                        assigned_juror_index=head_juror_priority_index[random.randint(0,len(head_juror_priority_index)-1)]
                        juror_assignments[PF][room]['H']=juror_data['Name'][assigned_juror_index]
                        head_assignment_count[assigned_juror_index]+=1
                        juror_assignment_count[assigned_juror_index]+=1
        
                        for school in participants:
                            school_juror_matrix.loc[juror_data['Name'][assigned_juror_index],school]+=1
                        for team in teams:
                            team_juror_matrix.loc[juror_data['Name'][assigned_juror_index],team]+=1
                        
                    current_priority_index+=1
                    print("Raising priority index")
                print("Assigned "+juror_assignments[PF][room]['H']+" as Head Juror for room "+room+" for PF "+str(PF))
                print()
    print("Done")
    print(school_juror_matrix)
    print(team_juror_matrix)
    
except:
    print("Error occured: Cannot assign head juror for "+str(PF)+room)
    

print(juror_assignments)

juror_assignments

if juror_assignments[5]['C']['H']!="none":
    
    #do regular assignments
    
    try:
        
        juror3_index=0
        for PF in [1,2,3,4,5]:
            PF_count=PF
            for room in room_list:

                if (PF==(1) or PF==(5)) and room==('D'):
                    pass
                else:
                
                    teams=assignment_matrix_original.iloc[np.where(assignment_matrix_original[str(PF)]==room)[0]]['0']
                    participants=assignment_matrix.iloc[np.where(assignment_matrix[str(PF)]==room)[0]]['0']
                    assignment_matrix
                    room_count=room
                            
                    for juror in [1,2,3,4]:
                        juror_count=juror
                        print('-----------')
                        print('Fight '+str(PF))
                        print("Room "+room)
                        print('Juror '+str(juror))
                        current_priority_index=0
                        
                        #put new jurors on lower priority
                        new_jurors=np.where(juror_data['Affiliation']=='New')[0]
                        for name in new_jurors:
                            juror_assignment_count[name]+=0.001
                        
                        priority_order=np.unique(juror_assignment_count)
                        print(priority_order)
                        
                        
    
                        while juror_assignments[PF][room][juror]=='none':
                            current_priority_count=priority_order[current_priority_index]
                            print("Choose from jurors with "+str(current_priority_count)+" previous sessions")
                            juror_priority_index=np.where(juror_assignment_count==current_priority_count)[0]
                            print("These jurors have priority: "+juror_data.iloc[juror_priority_index]['Name'].str.cat(sep=', '))
                            
                            
                            
                            #human beings should not be in more than one place at the same time
                            for room_temp in room_list:
                                for key in juror_assignments[PF][room_temp]:
                                    if len(juror_data.loc[juror_data['Name']==juror_assignments[PF][room_temp][key]])!=0:
                                        juror_a=juror_data.loc[juror_data['Name']==juror_assignments[PF][room_temp][key]].index[0]
                                        if len(np.where(juror_priority_index==juror_a)[0])>0:
                                            juror_priority_index=np.delete(juror_priority_index,np.where(juror_priority_index==juror_a))
                                            print("Remove "+juror_data.iloc[juror_a]['Name']+" who is already assigned elsewhere this round")
                            
                            print('Remaining jurors: '+juror_data.iloc[juror_priority_index]['Name'].str.cat(sep=', '))
                            
                            
                            
                            #remove jurors that have done 3 rounds
                            """
                            overworked_jurors=np.where(juror_assignment_count>2.5)[0]
                            """
                            #for juror_not_index in not_overworked_jurors:
                                #overworked_jurors=np.delete(overworked_jurors,np.where(overworked_jurors==juror_not_index))


                            print("Overworked jurors: "+juror_data.iloc[overworked_jurors]['Name'].str.cat(sep=', '))
                            for juror_index in overworked_jurors:
                                juror_priority_index=np.delete(juror_priority_index,np.where(juror_priority_index==juror_index))
                            print('Remaining jurors: '+juror_data.iloc[juror_priority_index]['Name'].str.cat(sep=', '))
    
    
                            #remove new jurors from first round
                            """
                            if PF==1:
                                new_jurors=np.concatenate((np.where(juror_data['Affiliation']=='New')[0],[10,12]),axis=0)
                                #new_jurors=np.where(juror_data['Affiliation']=='New')[0]
                                for name in new_jurors:
                                    if len(np.where(juror_priority_index==name)[0])>0:
                                        juror_priority_index=np.delete(juror_priority_index,np.where(juror_priority_index==name))
                                print("Remove new for round 1")
                                print('Remaining jurors: '+juror_data.iloc[juror_priority_index]['Name'].str.cat(sep=', '))
                            print()
                            """
                            
                            #avoid too many 'new' jurors in subsequent rounds
                            """
                            if PF>1:
                                if juror==1:
                                    new_jurors=np.concatenate((np.where(juror_data['Affiliation']=='New')[0],[10,12]),axis=0)
                                    #new_jurors=np.where(juror_data['Affiliation']=='New')[0]
                                    for name in new_jurors:
                                        if len(np.where(juror_priority_index==name)[0])>0:
                                            juror_priority_index=np.delete(juror_priority_index,np.where(juror_priority_index==name))
                                    print("Remove new")
                                    print('Remaining jurors: '+juror_data.iloc[juror_priority_index]['Name'].str.cat(sep=', '))
                            print()
                            """
                            
                            
                            
                            
                            
                            #remove conflict of interest
                            print('Schools participating: '+assignment_matrix.iloc[np.where(assignment_matrix[str(PF)]==room)[0]]['0'].str.cat(sep=', '))
                            for school in participants:
                                affiliated_jurors=np.where(juror_data['Affiliation']==school)[0]
                                print("Affiliated jurors: "+juror_data.iloc[affiliated_jurors]['Name'].str.cat(sep=', '))
                                for juror_index in affiliated_jurors:
                                    juror_priority_index=np.delete(juror_priority_index,np.where(juror_priority_index==juror_index))
                                print('Remaining jurors: '+juror_data.iloc[juror_priority_index]['Name'].str.cat(sep=', '))
                            print()
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            #remove Raffles VS NUSH
                            if np.sum(participants.str.find("Raffles"))>-2:
                                print("Raffles found, NUSH shouldn't be juror")
                                rival_jurors=np.where(juror_data['Affiliation']=='NUSHS')[0]
                                print("Rival jurors in priority list: "+juror_data.iloc[rival_jurors]['Name'].str.cat(sep=', '))
                                for juror_index in rival_jurors:
                                    juror_priority_index=np.delete(juror_priority_index,np.where(juror_priority_index==juror_index))
                                print('Remaining jurors: '+juror_data.iloc[juror_priority_index]['Name'].str.cat(sep=', '))
                            print()
            
                            if np.sum(participants.str.find("NUSHS"))>-2:
                                print("NUSH found, Raffles shouldn't be juror")
                                rival_jurors=np.where(juror_data['Affiliation']=='Raffles')[0]
                                print("Rival jurors in priority list: "+juror_data.iloc[rival_jurors]['Name'].str.cat(sep=', '))
                                for juror_index in rival_jurors:
                                    juror_priority_index=np.delete(juror_priority_index,np.where(juror_priority_index==juror_index))
                                print('Remaining jurors: '+juror_data.iloc[juror_priority_index]['Name'].str.cat(sep=', '))
                            print()
            
                            #at least two independent jurors
                            if (juror==1 or juror==2):
                                school_jurors=np.where((juror_data['Affiliation']!='Head')^(juror_data['Affiliation']!='Exp')^(juror_data['Affiliation']!='New'))[0]
                                for name in school_jurors:
                                    if len(np.where(juror_priority_index==name)[0])>0:
                                        juror_priority_index=np.delete(juror_priority_index,np.where(juror_priority_index==name))
                                print("Remove school jurors")
                            print(juror_data.iloc[juror_priority_index]['Name'].str.cat(sep=', '))
                            print()
                                
                            """
                            #no two jurors from same school
                            if juror==4:
                                jurors_from_same_school=juror_data.loc[juror_data['Affiliation']==juror_data.iloc[juror3_index]['Affiliation']]
                                jurors_from_same_school=jurors_from_same_school.index
                                
                                for juror_a in jurors_from_same_school:
                                    if len(np.where(juror_priority_index==juror_a)[0])>0:
                                        juror_priority_index=np.delete(juror_priority_index,np.where(juror_priority_index==juror_a))
                                        print("Remove "+juror_data.iloc[juror_a]['Name']+" who is "+str(juror_a))
                            """
            
                            #check for repeat teams - independent max twice, school jurors and inexperienced jurors max once. 
                            #relax this for first round: 
                            #bottlenecked when trying to fit independent jurors since they are head. But its ok to have independent jurors judging same team more than once
                            #will not affect non-head jurors even if relaxed since it's still first round
                            if PF>1:
                                """for juror_a in juror_priority_index:
                                    for school in participants:
                                        if school_juror_matrix.loc[juror_data['Name'][juror_a],school]>0:
                                            print(juror_data['Name'][juror_a]+' has already been juror for '+school)
                                            juror_priority_index=np.delete(juror_priority_index,np.where(juror_priority_index==juror_a))
                                            
                                print('Remaining jurors: '+juror_data.iloc[juror_priority_index]['Name'].str.cat(sep=', '))"""
                
                                for juror_a in juror_priority_index:
                                    for team in teams:
                                        if juror_data['Affiliation'][juror_a]=="Head" or juror_data['Affiliation'][juror_a]=="Exp": #for head and exp, can do once before
                                            if team_juror_matrix.loc[juror_data['Name'][juror_a],team]>2:
                                                print(juror_data['Name'][juror_a]+' has already been juror for '+team)
                                                juror_priority_index=np.delete(juror_priority_index,np.where(juror_priority_index==juror_a))
                                                
                                        else:
                                            if team_juror_matrix.loc[juror_data['Name'][juror_a],team]>1: #for new independent or school, max once #relaxed
                                                print(juror_data['Name'][juror_a]+' has already been juror for '+team)
                                                juror_priority_index=np.delete(juror_priority_index,np.where(juror_priority_index==juror_a))
                            
                            if len(juror_priority_index)>0:
                                print("Enough jurors")
                                assigned_juror_index=juror_priority_index[random.randint(0,len(juror_priority_index)-1)]
                                print("assign juror ID "+str(assigned_juror_index)+": "+juror_data.iloc[assigned_juror_index]['Name'])
                                if juror==3:
                                    juror3_index=assigned_juror_index
                                juror_assignments[PF][room][juror]=juror_data.iloc[assigned_juror_index]['Name']
                                juror_assignment_count[assigned_juror_index]+=1
            
                                for team in teams:
                                    team_juror_matrix.loc[juror_data['Name'][assigned_juror_index],team]+=1 #this is to make sure jurors don't judge the same team more than once
                                
                                current_priority_index=0
                            
                            else:   
                                print("--")
                                print("Juror not assigned, raising priority index")
                                current_priority_index+=1
                                print("Priority index: "+str(current_priority_index))
                 

        #output data as organised by juror
        juror_data_original['Count']=np.round(juror_assignment_count)
        for PF in [1,2,3,4,5]:
            for room_label in room_list:
                for key in juror_assignments[PF][room_label]:
                    juror_data_original.loc[juror_data_original['Name']==juror_assignments[PF][room_label][key],PF]=room_label
        juror_data_original=juror_data_original.fillna("-")
        juror_data_original=juror_data_original.reindex(['Name','Affiliation','Index_no','Count',1,2,3,4,5,0],axis=1)
        print(juror_data_original)
    
        
        list_output=pd.DataFrame(['a'])
        row=0
        for PF in [1,2,3,4,5]:
            for room in room_list:
                list_output[row]='PF'+str(PF)+' room '+room
                list_output[row+1]='Participants: '+assignment_matrix_original.iloc[np.where(assignment_matrix_original[str(PF)]==room)[0]]['0'].str.cat(sep=', ')
                
                if len(juror_data_original.loc[juror_data_original['Name']==juror_assignments[PF][room]['H']]['Affiliation'].reset_index(drop=True))==0:
                    pass
                else:
                    juror_list=",,,"+juror_assignments[PF][room]['H']+" ("+juror_data_original.loc[juror_data_original['Name']==juror_assignments[PF][room]['H']]['Affiliation'].reset_index(drop=True)[0]+")"
                                
                for juror in [1,2,3,4]:
                    juror_list+=", "
                    
                    if len(juror_data_original.loc[juror_data_original['Name']==juror_assignments[PF][room]['H']]['Affiliation'].reset_index(drop=True))==0:
                        pass
                    else:
                        juror_list+=juror_assignments[PF][room][juror]+" ("+juror_data_original.loc[juror_data_original['Name']==juror_assignments[PF][room][juror]]['Affiliation'].reset_index(drop=True)[0]+")"

                list_output[row+2]=juror_list
                list_output[row+3]=""
                row+=4
        
        list_output.transpose().to_csv("/cat_A_juror_assignment/juror_assignment_list.csv")
                
        
        table_output=pd.DataFrame(np.zeros([20,9]))
        row=0
        for PF in [1,2,3,4,5]:
            for room in room_list:
                

                if (PF==(1) or PF==(5)) and room==('D'):
                    pass
                else:
                    
                    table_output.iloc[row,0]='PF'+str(PF)+' room '+room
                    table_output.iloc[row,1]=assignment_matrix_original.iloc[np.where(assignment_matrix_original[str(PF)]==room)[0]]['0'].reset_index(drop=True)[0]
                    table_output.iloc[row,2]=assignment_matrix_original.iloc[np.where(assignment_matrix_original[str(PF)]==room)[0]]['0'].reset_index(drop=True)[1]
                    table_output.iloc[row,3]=juror_assignments[PF][room]['H']+" ("+juror_data_original.loc[juror_data_original['Name']==juror_assignments[PF][room]['H']]['Affiliation'].reset_index(drop=True)[0]+")"
                    for q in range(1,5):
                        table_output.iloc[row,q+3]=juror_assignments[PF][room][q]+" ("+juror_data_original.loc[juror_data_original['Name']==juror_assignments[PF][room][q]]['Affiliation'].reset_index(drop=True)[0]+")"
        
                    #find possible reserves
        
                    participants=assignment_matrix.iloc[np.where(assignment_matrix[str(PF)]==room)[0]]['0']
                    available_jurors=np.array(range(len(juror_data)))
                    
                    #human beings should not be in more than one place at the same time
                    for room_temp in room_list:
                        for key in juror_assignments[PF][room_temp]:
                            if len(juror_data.loc[juror_data['Name']==juror_assignments[PF][room_temp][key]])!=0:
                                juror_a=juror_data.loc[juror_data['Name']==juror_assignments[PF][room_temp][key]].index[0]
                                if len(np.where(available_jurors==juror_a)[0])>0:
                                    available_jurors=np.delete(available_jurors,np.where(available_jurors==juror_a))
                    #no judging your own school
                    for school in participants:
                        affiliated_jurors=np.where(juror_data['Affiliation']==school)[0]
                        for juror_index in affiliated_jurors:
                            available_jurors=np.delete(available_jurors,np.where(available_jurors==juror_index))
                    #no new juror for PF1
                    if PF==1:
                        new_jurors=np.where(juror_data['Affiliation']=='New')[0]
                        for name in new_jurors:
                            if len(np.where(available_jurors==name)[0])>0:
                                available_jurors=np.delete(available_jurors,np.where(available_jurors==name))
                    
                    table_output.iloc[row,8]=juror_data.iloc[available_jurors]['Name'].str.cat(sep=', ')
                    
                    print()
                    print('These jurors can be reserves for '+str(PF)+room+': '+table_output.iloc[row,8])
                    print()
        
                    row+=1
    
        print(table_output)        
        table_output.to_csv("./cat_A_juror_assignment/juror_assignment_list_table.csv")
        
        #solved=2000
        
    
    except:
        print("Error occured: Cannot assign for "+str(PF)+room)

print("")


