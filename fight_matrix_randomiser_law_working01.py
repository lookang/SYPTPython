import pandas as pd
import numpy as np
import random

# list of teams for 2024
A_list = ['RI_A1', 'RI_A2', 'NUSH_A1', 'NUSH_A2', 'NJC_A1', 'NJC_A2', 'HCI_A1', 'HCI_A2', 'RVHS_A1', 'TJC_A1']
# A_list = ['RI_A1', 'RI_A2', 'RI_A3', 'RI_A4', 'NJC_A1', 'NJC_A2', 'HCI_A1', 'HCI_A2', 'RVHS_A1', 'RGS_A1']
B_list = ['RI_B1', 'RI_B2', 'NUSH_B1', 'NUSH_B2', 'HCI_B1', 'HCI_B2', 'NYGH_B1', 'RGS_B1', 'RVHS_B1', 'CHIJ_B2']
# B_list = ['RI_B1', 'RI_B2', 'RI_B3', 'RI_B4', 'HCI_B1', 'HCI_B2', 'NYGH_B1', 'RGS_B1', 'RVHS_B1', 'CHIJ_B2']


# setup for sorting
room_list = ['A', 'B', 'C', 'D', 'E']
# the code cannot run with Room_A, strange.
#room_list = ['Room_A', 'Room B', 'Room C', 'Room D', 'Room E']

# change manually
#team_list = A_list
team_list = B_list

# check for duplicate schools
# print("Schools sending more than one team:")
# same_school = {}
# same_school = {0: 2,2: 0,0: 3,3: 0,1: 2, 2:1,1: 3,3: 1}
same_school = {0: 2, 2: 0, 3: 0, 1: 0,0: 3, 2: 0, 3: 0, 1: 0,0: 3, 2: 1, 3: 0, 1: 2,0: 3, 2: 1, 3: 1, 1: 3}
# print(same_school)
# {0: 1, 1: 0}
# {0: 2, 1: 0, 2: 0}
# {0: 3, 1: 0, 2: 0, 3: 0}
# {0: 3, 1: 2, 2: 1, 3: 0} #RI_B2 and RI_B3
# {0: 3, 1: 3, 2: 1, 3: 1} #RI_B2 and RI_B4
# 
for i in range(len(team_list)):
    for j in range(len(team_list) - i - 1):
        text_i = team_list[i]
        text_j = team_list[j + i + 1]
        if text_i[0:len(text_i) - 1] == text_j[0:len(text_j) - 1]:
            same_school[i] = j + i + 1
            same_school[j + i + 1] = i
            print(text_i + " and " + text_j)
            print(same_school)
            #wait = input("Press Enter to continue.")
        else:
            pass
print()

proceed = False
attempts = 0

MAX_ATTEMPT = 500
while not proceed and attempts < MAX_ATTEMPT:
    # set up empty frames
    assignment_matrix = pd.DataFrame(np.zeros([len(team_list), 4]), index=team_list)
    team_p_count = np.zeros(len(team_list))

    try:
        for i in range(0, 4):
            j = 0

            while j < len(room_list):
                # assign presenter
                print("Choose from teams:")
                remaining_list = np.where(assignment_matrix[i] == 0)[0]
                print(remaining_list)
                priority_order = np.unique(team_p_count)
                current_priority_index = 0

                school_j = 99
                error = 0
                while school_j == 99 and error < 100:
                    current_priority_count = priority_order[current_priority_index]
                    print("Current priority count: " + str(current_priority_count))

                    team_priority = np.where(team_p_count == current_priority_count)[0]
                    print("These teams have priority:")
                    print(team_priority)

                    for x in team_priority:
                        if len(np.where(remaining_list == x)[0]) == 0:
                            team_priority = np.delete(team_priority, np.where(team_priority == x))

                    print("After checking eligibility of teams:")
                    print(team_priority)

                    if len(team_priority) != 0:
                        school_j = team_priority[random.randint(0, len(team_priority) - 1)]

                    print()
                    current_priority_index += 1
                    error += 1

                print("Assigning " + team_list[school_j] + " as presenter")

                if assignment_matrix.iloc[school_j, i] == 0:
                    assignment_matrix.iloc[school_j, i] = room_list[j] + "P"

                    # update priority list
                    team_p_count[school_j] += 1
                    team_priority = np.where(team_p_count == team_p_count.min())[0]

                    remaining_list = np.where(assignment_matrix[i] == 0)[0]
                    try:
                        print("removing:")
                        print(team_list[same_school[school_j]])
                        remaining_list = np.delete(remaining_list,
                                                   np.where(remaining_list == same_school[school_j])[0][0])
                        print("Remaining schools for opponents:")
                        print(remaining_list)
                        for m in remaining_list:
                            print(team_list[m])

                    except:
                        print("no duplicate school found")

                    for n in range(0, i):
                        previous_fight = np.delete(
                            np.where(assignment_matrix[n].str.contains(assignment_matrix[n][school_j][0]))[0],
                            np.where(np.where(
                                assignment_matrix[n].str.contains(assignment_matrix[n][school_j][0]))[0] == school_j)[0])[
                            0]
                        print("Previous opponent: " + str(previous_fight))

                        try:
                            remaining_list = np.delete(remaining_list,
                                                       np.where(remaining_list == previous_fight)[0][0])
                            print("previous fight found")
                        except:
                            print("no previous fight found")

                        print(remaining_list)

                    school_jO = remaining_list[random.randint(0, len(remaining_list) - 1)]
                    print("Assigned " + team_list[school_jO] + " as opponent")
                    assignment_matrix.iloc[school_jO, i] = room_list[j] + "O"

                    j += 1

                else:
                    pass

                print(assignment_matrix)
                print()

    except:
        pass

    # check count for each row
    presenter_count_check = np.zeros(len(team_list))
    all_okay = True

    try:
        for i in range(len(assignment_matrix)):
            presentation_count = assignment_matrix.iloc[i].str.contains('P').value_counts()[True]
            presenter_count_check[i] = presentation_count
            if presentation_count != 2:
                all_okay = False
                print(team_list[i] + " has " + str(presentation_count) + " presentations")
        print(presenter_count_check)
    except:
        all_okay = False

    # check for duplicates and same school matching both times
    school_matrix = pd.DataFrame(np.zeros([len(team_list), len(team_list)]), index=team_list, columns=team_list)

    try:
        for fight in range(0, 4):
            for room in room_list:
                present = np.where(assignment_matrix[fight] == room + "P")[0][0]
                oppose = np.where(assignment_matrix[fight] == room + "O")[0][0]

                present_school = team_list[present].split('_')[0]
                oppose_school = team_list[oppose].split('_')[0]

                if (school_matrix.iloc[present, oppose] != 0 or school_matrix.iloc[oppose, present] != 0 or
                        present_school == oppose_school):
                    print("Error! Duplicate fight or same school matched both times!")
                    print(assignment_matrix[assignment_matrix[fight].str.contains(room)])
                    print()
                    all_okay = False
                else:
                    school_matrix.iloc[present, oppose] = str(room) + str(fight + 1)
                    # replace  with n/a to see the code attempts/workings
                    school_matrix.iloc[oppose, present] = '  '
    except:
        all_okay = False

    if all_okay:
        proceed = True
    else:
        pass

    print()
    print('Attempts: ' + str(attempts))
    attempts += 1
    print()

# Output
if all_okay:
    school_matrix = school_matrix.replace(0, '')
    print("Number of attempts needed: " + str(attempts))
    print("Final fight matrix:")
    print()
    print(assignment_matrix)
    print("School matrix:")
    print()
    print(school_matrix)

    # also present fight matrix as rooms and rounds
    room_matrix = pd.DataFrame(np.zeros([len(room_list), 8]), index=room_list)

    for fight in range(0, 4):
        for room in room_list:
            room_matrix.loc[room, fight * 2] = team_list[np.where(assignment_matrix[fight] == room + "P")[0][0]]
            room_matrix.loc[room, fight * 2 + 1] = team_list[np.where(assignment_matrix[fight] == room + "O")[0][0]]
    print("Room matrix:")
    print()
    print(room_matrix)
    # Transpose the rows as columns
    transposed_room_matrix = room_matrix.transpose()
    print("Transposed room_matrix:\n",transposed_room_matrix)

else:
    print("Failed after " + str(attempts) + " attempts")

school_matrix.to_csv('./fight_matrix_randomiser/School matrix.csv')
room_matrix.to_csv('./fight_matrix_randomiser/Room matrix.csv')
transposed_room_matrix.to_csv('./fight_matrix_randomiser/Room matrix_transposed.csv')
assignment_matrix.to_csv('./fight_matrix_randomiser/Assignment matrix.csv')
#output
# after output, excel replace RI_B3 to NUSH_B1 and RI_B4 to NUSH_B2
'''
Number of attempts needed: 416
Final fight matrix:

          0   1   2   3
RI_B1    DO  AO  AP  CP
RI_B2    EO  CP  BO  AP
RI_B3    AO  BP  EP  EO
RI_B4    BO  DP  DO  BP
HCI_B1   AP  CO  DP  CO
HCI_B2   CP  EO  CO  EP
NYGH_B1  CO  AP  EO  DP
RGS_B1   EP  EP  AO  BO
RVHS_B1  DP  DO  CP  AO
CHIJ_B2  BP  BO  BP  DO
School matrix:

        RI_B1 RI_B2 RI_B3 RI_B4 HCI_B1 HCI_B2 NYGH_B1 RGS_B1 RVHS_B1 CHIJ_B2
RI_B1                               C4            n/a     A3     n/a        
RI_B2                               C2                   n/a      A4     n/a
RI_B3                              n/a    n/a      E3                     B2
RI_B4                              n/a                    B4      D2     n/a
HCI_B1    n/a   n/a    A1    D3                                             
HCI_B2                 E4                          C1    n/a     n/a        
NYGH_B1    A2         n/a                 n/a                             D4
RGS_B1    n/a    E1         n/a            E2                               
RVHS_B1    D1   n/a         n/a            C3                               
CHIJ_B2          B3   n/a    B1                   n/a                       
Room matrix:

         0        1        2        3        4        5        6        7
A   HCI_B1    RI_B3  NYGH_B1    RI_B1    RI_B1   RGS_B1    RI_B2  RVHS_B1
B  CHIJ_B2    RI_B4    RI_B3  CHIJ_B2  CHIJ_B2    RI_B2    RI_B4   RGS_B1
C   HCI_B2  NYGH_B1    RI_B2   HCI_B1  RVHS_B1   HCI_B2    RI_B1   HCI_B1
D  RVHS_B1    RI_B1    RI_B4  RVHS_B1   HCI_B1    RI_B4  NYGH_B1  CHIJ_B2
E   RGS_B1    RI_B2   RGS_B1   HCI_B2    RI_B3  NYGH_B1   HCI_B2    RI_B3
'''