# original code by https://github.com/not-even-wong 
import pandas as pd
import numpy as np
import random

#list of teams for 2022
A_list=['ACJC1','HCI1','HCI2','NJC1','NUSH1','NUSH2','RGS1','RI1','RI2','RV1'] 
B_list=['SNGS1','HCI1','HCI2','NUSH1','NUSH2','RGS1','RI1','RI2','RV1','RV2'] 


#setup for sorting
room_list=['A','B','C','D','E']
team_list=B_list

#check for duplicate schools
print("Schools sending more than one team:")
same_school={}
for i in range(len(team_list)):
    for j in range(len(team_list)-i-1):
        text_i=team_list[i]
        text_j=team_list[j+i+1]
        if(text_i[0:len(text_i)-1]==text_j[0:len(text_j)-1]):
            same_school[i]=j+i+1
            same_school[j+i+1]=i
            print(text_i+" and "+text_j)
        else:
            pass
print()


proceed=False
attempts=0


MAX_ATTEMPTS = 250
while (proceed==False and attempts<MAX_ATTEMPTS):
    #set up empty frames
    assignment_matrix=pd.DataFrame(np.zeros([len(team_list),4]),index=team_list)
    team_p_count=np.zeros(len(team_list)) #keep track of number of presentations by each team to prioritise assignment of presentation slots in subsequent rounds

    try:
        for i in range(0,4):
            j=0
            
            while j<len(room_list):
                #assign presenter
                
                print("Choose from teams:")
                remaining_list=np.where(assignment_matrix[i]==0)[0]
                print(remaining_list)
                priority_order=np.unique(team_p_count)
                current_priority_index=0
        
                school_j=99
                error=0
                while (school_j==99 and error<100):
                    current_priority_count=priority_order[current_priority_index]
                    print("Current priority count: "+str(current_priority_count))
                    team_priority=np.where(team_p_count==current_priority_count)[0] #identify teams with the current least number of presentations
                    print("These teams have priority:")
                    print(team_priority)
                    
                    for x in team_priority:
                        if(len(np.where(remaining_list==x)[0])==0): #identify which items in the priority list is not in the eligible remaining list
                            team_priority=np.delete(team_priority,np.where(team_priority==x)) #remove from priority list
                    print("After checking eligibility of teams:")
                    print(team_priority)
                    
                    if len(team_priority)!=0:
                        school_j=team_priority[random.randint(0,len(team_priority)-1)]
                    
                    print()
                    current_priority_index+=1 #since all teams with the least presentations are not eligible, try next order of presentations
                    error+=1
        
                print("Assigning "+team_list[school_j]+" as presenter")
                    
                if assignment_matrix.iloc[school_j,i]==0:
                    assignment_matrix.iloc[school_j,i]=room_list[j]+"P"
                    
                    #update priority list
                    team_p_count[school_j]+=1
                    team_priority=np.where(team_p_count==team_p_count.min())[0]
                    #print(team_p_count)
            
                    #remove same school from list
                    remaining_list=np.where(assignment_matrix[i]==0)[0]
                    try:
                        print("removing:")
                        print(team_list[same_school[school_j]])
                        remaining_list=np.delete(remaining_list,np.where(remaining_list==same_school[school_j])[0][0])
                        print("Remaining schools for opponents:")
                        print(remaining_list)
                        for m in remaining_list:
                            print(team_list[m])
                        
                    except:
                        print("no duplicate school found")
                                    
                    #removing previous duplicate fights
                    for n in range(0,i):
                        previous_fight=np.delete(np.where(assignment_matrix[n].str.contains(assignment_matrix[n][school_j][0]))[0],np.where(np.where(assignment_matrix[n].str.contains(assignment_matrix[n][school_j][0]))[0]==school_j)[0])[0]
                        print("Previous opponent: "+str(previous_fight))
                        
                        try:
                            remaining_list=np.delete(remaining_list,np.where(remaining_list==previous_fight)[0][0])
                            print("previous fight found")
                        except:
                            print("no previous fight found")
                            
                        print(remaining_list)
            
                    school_jO=remaining_list[random.randint(0,len(remaining_list)-1)]
                    print("Assigned "+team_list[school_jO]+" as opponent")
                    assignment_matrix.iloc[school_jO,i]=room_list[j]+"O"
            
                    j+=1        
                
                else:
                    pass
                
                print(assignment_matrix)
                print()

    except:
        pass

    #check count for each row
    presenter_count_check=np.zeros(len(team_list))
    all_okay=True
    
    try:
        for i in range(len(assignment_matrix)):
            presentation_count=assignment_matrix.iloc[i].str.contains('P').value_counts()[True]
            presenter_count_check[i]=presentation_count
            if presentation_count!=2:
                all_okay=False
                print(team_list[i]+" has "+str(presentation_count)+" presentations")
        print(presenter_count_check)
    except:
        all_okay=False
    
    #check for duplicates
    school_matrix=pd.DataFrame(np.zeros([len(team_list),len(team_list)]),index=team_list, columns=team_list)

    try:
        for fight in range(0,4):
            for room in room_list:
                present=np.where(assignment_matrix[fight]==room+"P")[0][0]
                oppose=np.where(assignment_matrix[fight]==room+"O")[0][0]        
                if (school_matrix.iloc[present,oppose]!=0 or school_matrix.iloc[oppose,present]!=0):
                    print("Error! Duplicate fight!")
                    print(assignment_matrix[assignment_matrix[fight].str.contains(room)])
                    print()                                 
                    all_okay=False
                else:
                    school_matrix.iloc[present,oppose]=str(room)+str(fight+1) #rows are presenters, columns are opponents
                    school_matrix.iloc[oppose,present]='n/a' #rows are presenters, columns are opponents            
    except:
        all_okay=False
        
        
    if all_okay==True:
        proceed=True
    else:
        pass

    print()
    print('Attempts: '+str(attempts))
    attempts+=1
    print()

"""-------------------------------------"""
#Output below
    
if all_okay==True:
    school_matrix=school_matrix.replace(0,'')
    print("Number of attempts needed :"+str(attempts))
    print("Final fight matrix:")
    print()
    print(assignment_matrix)
    print("School matrix:")
    print()
    print(school_matrix)

    #also present fight matrix as rooms and rounds
    room_matrix=pd.DataFrame(np.zeros([len(room_list),8]),index=room_list)
    
    for fight in range(0,4):
        for room in room_list:
            room_matrix.loc[room,fight*2]=team_list[np.where(assignment_matrix[fight]==room+"P")[0][0]]
            room_matrix.loc[room,fight*2+1]=team_list[np.where(assignment_matrix[fight]==room+"O")[0][0]]
            #present=np.where(assignment_matrix[fight]==room+"P")[0][0]
            #oppose=np.where(assignment_matrix[fight]==room+"O")[0][0]        
            #room_matrix.loc[room,fight]=team_list[present]+" vs "+team_list[oppose]
    print("Room matrix:")
    print()
    print(room_matrix)
    
else:
    print("Failed after "+str(attempts)+" attempts")
    
school_matrix.to_csv('./fight_matrix_randomiser/School matrix.csv')
room_matrix.to_csv('./fight_matrix_randomiser/Room matrix.csv')
assignment_matrix.to_csv('./fight_matrix_randomiser/Assignment matrix.csv')


