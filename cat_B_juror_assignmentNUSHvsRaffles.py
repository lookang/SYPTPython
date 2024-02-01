# Cat B Assignment matrix.csv must be cleaned up first by doing a replace _B by 
# expected output of Cat B Assignment matrix.csv is
'''	0	1	2	3
RI1	DP	EP	EO	AO
RI2	EO	CP	CP	DO
NUSH1	BP	DO	EP	BO
NUSH2	CP	EO	DP	EO
HCI1	AP	CO	BO	AP
HCI2	EP	DP	AO	CO
NYGH1	AO	BP	CO	BP
RGS1	CO	AO	BP	DP
RVHS1	DO	BO	AP	EP
CHIJ2	BO	AP	DO	CP
'''
# data in csv are Head, Exp, New for jurors
# very important! cannot have duplcicate names as it jams the code, name must be unique
# serial number is not unique
# delete the New instead, need Head, Exp, etc
# best practice more than 10 Heads
# more than 3 Exp
# more than 3 New
# data must be arrange in Heads, Schools, (Exp and New mixed) else it cannot find a solution


# need to check database in https://docs.google.com/spreadsheets/d/1ASSO4-JUB_DvYulyEnFGLg0UX-RFbZHCVEgULxbJVZ8/edit#gid=897356845 against csv


import pandas as pd

import numpy as np
import random

# A_list=['ACJC', 'HCI', 'NJC', 'NUSH', 'RI', 'RVHS', 'RGS'] #Cat A
# B_list = ['RI_B1', 'RI_B2', 'NUSH_B1', 'NUSH_B2', 'HCI_B1', 'HCI_B2', 'NYGH_B1', 'RGS_B1', 'RVHS_B1', 'CHIJ_B2']
# B_list = ['RI_B1', 'RI_B2', 'RI_B3', 'RI_B4', 'HCI_B1', 'HCI_B2', 'NYGH_B1', 'RGS_B1', 'RVHS_B1', 'CHIJ_B2']

#A_list=['SNGS', 'HCI', 'NUSH', 'RGS', 'RI', 'RVHS'] #Cat B but I already used "A_list" everywhere so I'll stick with that variable name
room_list=['A','B','C','D','E']

#import data




    
solved=0
MAX_ATTEMPT = 300
while solved<MAX_ATTEMPT:
    # taken from the fight_matrix_randomiser_law_working01.py output file called Assignment matrix.csv
    assignment_matrix=pd.read_csv("Cat B Assignment matrix.csv")
    #assignment_matrix=pd.read_csv("Cat B Assignment matrix_old.csv")
    assignment_matrix.columns=['0','1','2','3','4']
    
    for i in range(assignment_matrix.shape[0]):
        for j in range(1,assignment_matrix.shape[1]):
            assignment_matrix.iloc[i,j]=assignment_matrix.iloc[i,j][0]
    assignment_matrix_original=assignment_matrix.copy(deep=True)
    
    for i in range(assignment_matrix.shape[0]):
        assignment_matrix.iloc[i,0]=assignment_matrix.iloc[i,0][:-1]
    
        
    assignment_matrix_original=assignment_matrix.copy(deep=True)
    assignment_matrix_original['0']=pd.read_csv("Cat B Assignment matrix.csv")['Unnamed: 0']
    # assignment_matrix_original['0']=pd.read_csv("Cat B Assignment matrix_old.csv")['Unnamed: 0']
    # assignment_matrix=assignment_matrix.replace('RI','Raffles').replace('RGS','Raffles')
    assignment_matrix=assignment_matrix.replace('RI','Raffles')
    #print(assignment_matrix)
    
    # juror_data=pd.read_csv("Cat B jurors.csv",delimiter=";")
    juror_data=pd.read_csv("Cat B jurors20240129.csv",delimiter=";")
    # juror_data=pd.read_csv("cat_BJurors2024.csv",delimiter=";")
    print(juror_data)
    #juror_data=pd.read_csv("cat_BJurors2024formatted.csv",delimiter=";")
    #print(juror_data)
    #wait = input("Press Enter to continue.")
    
    juror_data_original=juror_data.copy(deep=True)
    # control if RI can match
    # juror_data=juror_data.replace('RI','Raffles').replace('RGS','Raffles')
    juror_data=juror_data.replace('RI','Raffles')
    # pretend NUSH is Raffles to prevent Juror each other
    # juror_data=juror_data.replace('NUSH','Raffles')
    #print(juror_data)
    #wait = input("Press Enter to continue.")
    #set up list to track number of times each juror has taken a role
    juror_data.loc[juror_data['Affiliation']=="Head"]
    head_assignment_count=np.zeros(len(juror_data.loc[juror_data['Affiliation']=="Head"]))
    juror_assignment_count=np.zeros(len(juror_data))
    
    #set up array to track number of times each juror has judged each school
    #school_juror_matrix=pd.DataFrame(np.zeros([len(juror_data),len(assignment_matrix['0'].unique())]),columns=assignment_matrix['0'].unique(),index=juror_data['Full name'])
    #team_juror_matrix=pd.DataFrame(np.zeros([len(juror_data),len(assignment_matrix_original['0'].unique())]),columns=assignment_matrix_original['0'].unique(),index=juror_data['Full name'])

    school_juror_matrix=pd.DataFrame(np.zeros([len(juror_data),len(assignment_matrix['0'].unique())]),columns=assignment_matrix['0'].unique(),index=juror_data['Name'])
    team_juror_matrix=pd.DataFrame(np.zeros([len(juror_data),len(assignment_matrix_original['0'].unique())]),columns=assignment_matrix_original['0'].unique(),index=juror_data['Name'])
    
    """
    structure for assignment:
    juror_assignments[round][room][H,1,2,3 or 4]
    set up empty nested dictionary first
    """
    
    
    juror_assignments={}
    for PF in [1,2,3,4]:
        juror_assignments[PF]={}
        for room in room_list:
            juror_assignments[PF][room]={}
            for juror in ['H',1,2,3,4]:
                juror_assignments[PF][room][juror]='none'
    
    try:
        del(affiliated_jurors,priority_order,rival_jurors,participants,room)
    except:
        pass
    
    #do HEAD assignments
    try:
        for PF in [1,2,3,4]: #assign all head jurors first, since this is priority - avoid situation of having assigned head jurors as normal jurors and running out of staff
            for room in room_list:
                current_priority_index=0 #this is the position in the priority order
                priority_order=np.unique(head_assignment_count)
                participants=assignment_matrix.iloc[np.where(assignment_matrix[str(PF)]==room)[0]]['0']
                teams=assignment_matrix_original.iloc[np.where(assignment_matrix_original[str(PF)]==room)[0]]['0']
                
                """
                print("")
                print("--------")
                print(str(PF)+room)
                print("")
                """
                
                while juror_assignments[PF][room]['H']=='none':
                    current_priority_count=priority_order[current_priority_index]
                    head_juror_priority_index=np.where(head_assignment_count==current_priority_count)[0]
                    #print("These jurors have priority: "+juror_data.iloc[head_juror_priority_index]['Name'].str.cat(sep=', '))
                    
                    #check for repeat schools
                    """for juror in head_juror_priority_index:
                        for school in participants:
                            if school_juror_matrix.loc[juror_data['Name'][juror],school]>0:
                                print(juror_data['Name'][juror]+' has already been head juror for '+school)
                                head_juror_priority_index=np.delete(head_juror_priority_index,np.where(head_juror_priority_index==juror))"""
    
                    for juror_a in head_juror_priority_index:
                        for team in teams:
                            if team_juror_matrix.loc[juror_data['Name'][juror_a],team]>0:
                                #print(juror_data['Name'][juror_a]+' has already been juror for '+team)
                                head_juror_priority_index=np.delete(head_juror_priority_index,np.where(head_juror_priority_index==juror_a))
                                
                    #check for juror being in more than one place at the same time
                    for room_temp in room_list:
                        if len(juror_data.loc[juror_data['Name']==juror_assignments[PF][room_temp]['H']])!=0:
                            juror_a=juror_data.loc[juror_data['Name']==juror_assignments[PF][room_temp]['H']].index[0]
                            if len(np.where(head_juror_priority_index==juror_a)[0])>0:
                                head_juror_priority_index=np.delete(head_juror_priority_index,np.where(head_juror_priority_index==juror_a))
                                #print("Remove "+juror_data.iloc[juror_a]['Name']+" who is already assigned elsewhere this round")
                    
                    #print('Remaining jurors: '+juror_data.iloc[head_juror_priority_index]['Name'].str.cat(sep=', '))
        
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
                    #print("Raising priority index")
                #print("Assigned "+juror_assignments[PF][room]['H']+" as Head Juror for room "+room+" for PF "+str(PF))
                print()
        print("Juror alloc done")
        print(school_juror_matrix)
        print(team_juror_matrix)
    
    except:
        print("Error occured: Cannot assign head juror for "+str(PF)+room)
        
    
    print(juror_assignments)
    
    
    
    
    
    
    
    #not_overworked_jurors=[7,8,9,17] #CatA
    #not_overworked_jurors=[0,1,2,12] #catB
        
    if juror_assignments[4]['E']['H']!="none":
        
        #do regular assignments
        
        try:
            print(solved)
            solved+=1
        
            juror3_index=0
            for PF in [1,2,3,4]:
                PF_count=PF
                for room in room_list:
                    teams=assignment_matrix_original.iloc[np.where(assignment_matrix_original[str(PF)]==room)[0]]['0']
                    participants=assignment_matrix.iloc[np.where(assignment_matrix[str(PF)]==room)[0]]['0']
                    assignment_matrix
                    room_count=room
                            
                    for juror in [1,2,3,4]:
                        juror_count=juror
                        """
                        print('-----------')
                        print('Fight '+str(PF))
                        print("Room "+room)
                        print('Juror '+str(juror))
                        """
                        current_priority_index=0
                        
                        #put new jurors on lower priority
                        new_jurors=np.where(juror_data['Affiliation']=='New')[0]
                        for name in new_jurors:
                            juror_assignment_count[name]+=0.001
                        
                        priority_order=np.unique(juror_assignment_count)
                        #print(priority_order)
    
                        while juror_assignments[PF][room][juror]=='none':
                            current_priority_count=priority_order[current_priority_index]
                            #print("Choose from jurors with "+str(current_priority_count)+" previous sessions")
                            juror_priority_index=np.where(juror_assignment_count==current_priority_count)[0]
                            #print("These jurors have priority: "+juror_data.iloc[juror_priority_index]['Name'].str.cat(sep=', '))
                            
                            #human beings should not be in more than one place at the same time
                            for room_temp in room_list:
                                for key in juror_assignments[PF][room_temp]:
                                    if len(juror_data.loc[juror_data['Name']==juror_assignments[PF][room_temp][key]])!=0:
                                        juror_a=juror_data.loc[juror_data['Name']==juror_assignments[PF][room_temp][key]].index[0]
                                        if len(np.where(juror_priority_index==juror_a)[0])>0:
                                            juror_priority_index=np.delete(juror_priority_index,np.where(juror_priority_index==juror_a))
                                            #print("Remove "+juror_data.iloc[juror_a]['Name']+" who is already assigned elsewhere this round")
                            
                            #print('Remaining jurors: '+juror_data.iloc[juror_priority_index]['Name'].str.cat(sep=', '))
                            
                            #remove jurors that have done 3 rounds
                            
                            overworked_jurors=np.where(juror_assignment_count>2.5)[0]
                            # overworked_jurors=np.where(juror_assignment_count>1.5)[0]
                            #for juror_not_index in not_overworked_jurors:
                                #overworked_jurors=np.delete(overworked_jurors,np.where(overworked_jurors==juror_not_index))
                            #print("Overworked jurors: "+juror_data.iloc[overworked_jurors]['Name'].str.cat(sep=', '))
                            for juror_index in overworked_jurors:
                                juror_priority_index=np.delete(juror_priority_index,np.where(juror_priority_index==juror_index))
                            #print('Remaining jurors: '+juror_data.iloc[juror_priority_index]['Name'].str.cat(sep=', '))
    
                            
    
                            #remove new jurors from first round
                            if PF==1:
                                new_jurors=np.concatenate((np.where(juror_data['Affiliation']=='SJI')[0],np.where(juror_data['Affiliation']=='New')[0],[17,12,13]),axis=0)
                                for name in new_jurors:
                                    if len(np.where(juror_priority_index==name)[0])>0:
                                        juror_priority_index=np.delete(juror_priority_index,np.where(juror_priority_index==name))
                                #print("Remove new for round 1")
                                #print('Remaining jurors: '+juror_data.iloc[juror_priority_index]['Name'].str.cat(sep=', '))
                            #print()
                            
                            
                            #avoid too many 'new' jurors in subsequent rounds
                                        """
                            if PF>1:
                                if juror==1:
                                    new_jurors=np.concatenate((np.where(juror_data['Affiliation']=='SJI')[0],np.where(juror_data['Affiliation']=='New')[0]),axis=0)
                                    for name in new_jurors:
                                        if len(np.where(juror_priority_index==name)[0])>0:
                                            juror_priority_index=np.delete(juror_priority_index,np.where(juror_priority_index==name))
                                    #print("Remove new")
                                    #print('Remaining jurors: '+juror_data.iloc[juror_priority_index]['Name'].str.cat(sep=', '))
                            #print()
                                   """
                           
                            
                            
                            
                            
                            
                            
                            #remove conflict of interest
                            #print('Schools participating: '+assignment_matrix.iloc[np.where(assignment_matrix[str(PF)]==room)[0]]['0'].str.cat(sep=', '))
                            for school in participants:
                                affiliated_jurors=np.where(juror_data['Affiliation']==school)[0]
                                #print("Affiliated jurors: "+juror_data.iloc[affiliated_jurors]['Name'].str.cat(sep=', '))
                                for juror_index in affiliated_jurors:
                                    juror_priority_index=np.delete(juror_priority_index,np.where(juror_priority_index==juror_index))
                                #print('Remaining jurors: '+juror_data.iloc[juror_priority_index]['Name'].str.cat(sep=', '))
                            #print()
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            #remove Raffles VS NUSH
                            if np.sum(participants.str.find("Raffles"))>-2:
                                #print("Raffles found, NUSH shouldn't be juror")
                                #rival_jurors=np.where(juror_data['Affiliation']=='NUSHS')[0]
                                rival_jurors=np.where(juror_data['Affiliation']=='NUSH')[0]
                                #print("Rival jurors in priority list: "+juror_data.iloc[rival_jurors]['Name'].str.cat(sep=', '))
                                for juror_index in rival_jurors:
                                    juror_priority_index=np.delete(juror_priority_index,np.where(juror_priority_index==juror_index))
                                #print('Remaining jurors: '+juror_data.iloc[juror_priority_index]['Name'].str.cat(sep=', '))
                            #print()
                            

                            
                            # if np.sum(participants.str.find("NUSH"))>-2:
                            if np.sum(participants.str.find("NUSH"))>-2:
                                #print("NUSH found, Raffles shouldn't be juror")
                                rival_jurors=np.where(juror_data['Affiliation']=='Raffles')[0]
                                #print("Rival jurors in priority list: "+juror_data.iloc[rival_jurors]['Name'].str.cat(sep=', '))
                                for juror_index in rival_jurors:
                                    juror_priority_index=np.delete(juror_priority_index,np.where(juror_priority_index==juror_index))
                                #print('Remaining jurors: '+juror_data.iloc[juror_priority_index]['Name'].str.cat(sep=', '))
                            #print()
                            
                            #at least two independent jurors
                            if (juror==1 or juror==2):
                                school_jurors=np.where((juror_data['Affiliation']!='Head')^(juror_data['Affiliation']!='Exp')^(juror_data['Affiliation']!='New'))[0]
                                for name in school_jurors:
                                    if len(np.where(juror_priority_index==name)[0])>0:
                                        juror_priority_index=np.delete(juror_priority_index,np.where(juror_priority_index==name))
                                #print("Remove school jurors")
                            #print(juror_data.iloc[juror_priority_index]['Name'].str.cat(sep=', '))
                            #print()
                                
                            
                            #no two jurors from same school
                            if juror==4:
                                jurors_from_same_school=juror_data.loc[juror_data['Affiliation']==juror_data.iloc[juror3_index]['Affiliation']]
                                jurors_from_same_school=jurors_from_same_school.index
                                
                                for juror_a in jurors_from_same_school:
                                    if len(np.where(juror_priority_index==juror_a)[0])>0:
                                        juror_priority_index=np.delete(juror_priority_index,np.where(juror_priority_index==juror_a))
                                        print("Remove "+juror_data.iloc[juror_a]['Name']+" who is "+str(juror_a))
                            
            
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
                                                #print(juror_data['Name'][juror_a]+' has already been juror for '+team)
                                                juror_priority_index=np.delete(juror_priority_index,np.where(juror_priority_index==juror_a))
                                                
                                        else:
                                            if team_juror_matrix.loc[juror_data['Name'][juror_a],team]>1: #for new independent or school, max once #relaxed
                                                #print(juror_data['Name'][juror_a]+' has already been juror for '+team)
                                                juror_priority_index=np.delete(juror_priority_index,np.where(juror_priority_index==juror_a))
                            
                            if len(juror_priority_index)>0:
                                #print("Enough jurors")
                                assigned_juror_index=juror_priority_index[random.randint(0,len(juror_priority_index)-1)]
                                #print("assign juror ID "+str(assigned_juror_index)+": "+juror_data.iloc[assigned_juror_index]['Name'])
                                if juror==3:
                                    juror3_index=assigned_juror_index
                                juror_assignments[PF][room][juror]=juror_data.iloc[assigned_juror_index]['Name']
                                juror_assignment_count[assigned_juror_index]+=1
            
                                for team in teams:
                                    team_juror_matrix.loc[juror_data['Name'][assigned_juror_index],team]+=1 #this is to make sure jurors don't judge the same team more than once
                                
                                current_priority_index=0
                            
                            else:   
                                #print("--")
                                #print("Juror not assigned, raising priority index")
                                current_priority_index+=1
                                #print("Priority index: "+str(current_priority_index))
                     
    
            #output data as organised by juror
            juror_data_original['Count']=np.round(juror_assignment_count)
            for PF in [1,2,3,4]:
                for room_label in room_list:
                    for key in juror_assignments[PF][room_label]:
                        juror_data_original.loc[juror_data_original['Name']==juror_assignments[PF][room_label][key],PF]=room_label
            juror_data_original=juror_data_original.fillna("-")
            #print(juror_data_original)
        
            juror_data_original.to_csv("./cat_B_juror_assignment/Juror schedule.csv")
            
            list_output=pd.DataFrame(['a'])
            row=0
            for PF in [1,2,3,4]:
                for room in room_list:
                    list_output[row]='PF'+str(PF)+' room '+room
                    list_output[row+1]='Participants: '+assignment_matrix_original.iloc[np.where(assignment_matrix_original[str(PF)]==room)[0]]['0'].str.cat(sep=', ')
                    juror_list=",,,"+juror_assignments[PF][room]['H']+" ("+juror_data_original.loc[juror_data_original['Name']==juror_assignments[PF][room]['H']]['Affiliation'].reset_index(drop=True)[0]+")"
                    
                    for juror in [1,2,3,4]:
                        juror_list+=", "
                        juror_list+=juror_assignments[PF][room][juror]+" ("+juror_data_original.loc[juror_data_original['Name']==juror_assignments[PF][room][juror]]['Affiliation'].reset_index(drop=True)[0]+")"
                    
                    list_output[row+2]=juror_list
                    list_output[row+3]=""
                    row+=4
            list_output.transpose().to_csv("./cat_B_juror_assignment/juror_assignment_list.csv")
            
            
            
            
            table_output=pd.DataFrame(np.zeros([20,9]))
            row=0
            for PF in [1,2,3,4]:
                for room in room_list:
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
                    
                    #print()
                    #print('These jurors can be reserves for '+str(PF)+room+': '+table_output.iloc[row,8])
                    #print()
        
                    row+=1
        
            #print(table_output)        
            table_output.to_csv("./cat_B_juror_assignment/juror_assignment_list_table.csv")
            
            solved=2000
            
        
        except:
            print("Error occured: Cannot assign for "+str(PF)+room)


print("")
print(juror_assignments)
#solved +=1
#for qwerty in range (1,20):
#    print(solved)    
#    print()
        
# pd.set_option('max_columns', None)
# pd.set_option('display.expand_frame_repr', False) 
# https://pandas.pydata.org/pandas-docs/stable/user_guide/options.html
# pd.set_option("display.max_rows", 999)
# pd.set_option("display.precision", 5)

juror_data_original['Count']=np.round(juror_assignment_count)
for room_label in room_list:
    for key in juror_assignments[PF][room_label]:
        for PF in [1,2,3,4]:
            juror_data_original.loc[juror_data_original['Name']==juror_assignments[PF][room_label][key],PF]=room_label
juror_data_original=juror_data_original.fillna("-")

for juror_index in range(len(juror_data_original)):
    #print(juror_index)
    school_list_temp=pd.DataFrame([])
    for PF in [1,2,3,4]:
        try:
            room_label=juror_data_original.loc[juror_index,PF]
            school_list_temp=pd.concat([school_list_temp,assignment_matrix_original['0'].loc[assignment_matrix_original[str(PF)]==room_label]])
            #print(", ".join(school_list_temp[0].sort_values()))
        except:
            pass
    juror_data_original.loc[juror_index,0]=", ".join(school_list_temp[0].sort_values())


print(juror_data_original)
juror_data_original.to_csv("./cat_B_juror_assignment/Juror schedule.csv")

print()


#table_output.to_csv("juror_assignment_list_table.csv")
#table_output
#juror_data_original




"""

        
#output data as organised by juror
juror_data_original['Count']=np.round(juror_assignment_count)
for PF in [1,2,3,4]:
    for room_label in room_list:
        for key in juror_assignments[PF][room_label]:
            juror_data_original.loc[juror_data_original['Name']==juror_assignments[PF][room_label][key],PF]=room_label
juror_data_original=juror_data_original.fillna("Break")
print(juror_data_original)

juror_data_original.to_csv("Juror schedule.csv")

list_output=pd.DataFrame(['a'])
row=0
for PF in [1,2,3,4]:
    for room in room_list:
        list_output[row]='PF'+str(PF)+' room '+room
        list_output[row+1]='Participants: '+assignment_matrix_original.iloc[np.where(assignment_matrix_original[str(PF)]==room)[0]]['0'].str.cat(sep=', ')
        juror_list=",,,"+juror_assignments[PF][room]['H']+" ("+juror_data_original.loc[juror_data_original['Name']==juror_assignments[PF][room]['H']]['Affiliation'].reset_index(drop=True)[0]+")"
        
        for juror in [1,2,3,4]:
            juror_list+=", "
            juror_list+=juror_assignments[PF][room][juror]+" ("+juror_data_original.loc[juror_data_original['Name']==juror_assignments[PF][room][juror]]['Affiliation'].reset_index(drop=True)[0]+")"
        
        list_output[row+2]=juror_list
        list_output[row+3]=""
        row+=4
list_output.transpose().to_csv("juror_assignment_list.csv")




table_output=pd.DataFrame(np.zeros([20,9]))
row=0
for PF in [1,2,3,4]:
    for room in room_list:
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
        table_output.to_csv("juror_assignment_list_table.csv")
        row+=1

print(table_output)
table_output.to_csv("juror_assignment_list_table.csv")

"""
