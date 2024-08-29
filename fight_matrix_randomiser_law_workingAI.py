import pandas as pd
import numpy as np
import random

# List of teams for 2024 updated manually
A_list = ['RI_A1', 'RI_A2', 'NUSH_A1', 'NUSH_A2', 'NJC_A1', 'NJC_A2', 'HCI_A1', 'HCI_A2', 'RVHS_A1', 'TJC_A1']
B_list = ['RI_B1', 'RI_B2', 'NUSH_B1', 'NUSH_B2', 'HCI_B1', 'HCI_B2', 'NYGH_B1', 'RGS_B1', 'RVHS_B1', 'CHIJ_B2']


# Room setup
room_list = ['A', 'B', 'C', 'D', 'E']

# Select the team list updated manually to A_list or B_list
team_list = A_list

# Initialize dictionary to track teams from the same school
same_school = {}

# Identify teams from the same school
for i in range(len(team_list)):
    for j in range(i + 1, len(team_list)):
        if team_list[i][:-2] == team_list[j][:-2]:
            same_school[i] = j
            same_school[j] = i
            print(f"{team_list[i]} and {team_list[j]} belong to the same school.")
print()

# Function to assign a team as presenter and opponent in a round
def assign_team(assignment_matrix, team_list, team_p_count, room_list, same_school):
    proceed = False
    attempts = 0
    MAX_ATTEMPT = 1000

    while not proceed and attempts < MAX_ATTEMPT:
        # Initialize the assignment matrix and team presentation count
        assignment_matrix = pd.DataFrame("", index=team_list, columns=range(4))
        team_p_count = np.zeros(len(team_list))

        try:
            for i in range(4):  # 4 rounds
                j = 0
                while j < len(room_list):
                    remaining_teams = np.where(assignment_matrix[i] == "")[0]
                    priority_order = np.unique(team_p_count)
                    current_priority_index = 0

                    school_j = None
                    error = 0

                    while school_j is None and error < 100:
                        current_priority_count = priority_order[current_priority_index]
                        team_priority = [x for x in np.where(team_p_count == current_priority_count)[0] if x in remaining_teams]

                        if team_priority:
                            school_j = random.choice(team_priority)

                        current_priority_index += 1
                        error += 1

                    if school_j is not None:
                        print(f"Assigning {team_list[school_j]} as presenter.")
                        assignment_matrix.iloc[school_j, i] = room_list[j] + "P"
                        team_p_count[school_j] += 1

                        # Remove the same school team from remaining teams
                        if school_j in same_school:
                            same_school_team = same_school[school_j]
                            remaining_teams = remaining_teams[remaining_teams != same_school_team]

                        # Remove teams that have already fought against this team
                        for n in range(i):
                            previous_opponent = np.where(assignment_matrix[n].str.contains(assignment_matrix[n][school_j][0]))[0]
                            if previous_opponent.size > 0:
                                remaining_teams = remaining_teams[remaining_teams != previous_opponent[0]]

                        if remaining_teams.size > 0:
                            school_jO = random.choice(remaining_teams)
                            print(f"Assigned {team_list[school_jO]} as opponent.")
                            assignment_matrix.iloc[school_jO, i] = room_list[j] + "O"

                        j += 1

        except Exception as e:
            print(f"Error occurred: {e}")
            pass

        # Validate the assignment matrix
        all_okay = validate_assignment_matrix(assignment_matrix, team_list, same_school)
        if all_okay:
            proceed = True

        attempts += 1

    return assignment_matrix, all_okay, attempts

# Function to validate the assignment matrix
def validate_assignment_matrix(assignment_matrix, team_list, same_school):
    try:
        # Check that each team presents exactly twice
        for i in range(len(assignment_matrix)):
            if assignment_matrix.iloc[i].str.contains('P').sum() != 2:
                print(f"{team_list[i]} does not present exactly twice.")
                return False

        # Check for duplicate fights or same school matching
        school_matrix = pd.DataFrame(np.zeros([len(team_list), len(team_list)]), index=team_list, columns=team_list)

        for fight in range(4):
            for room in room_list:
                present = np.where(assignment_matrix[fight] == room + "P")[0][0]
                oppose = np.where(assignment_matrix[fight] == room + "O")[0][0]

                present_school = team_list[present].split('_')[0]
                oppose_school = team_list[oppose].split('_')[0]

                if school_matrix.iloc[present, oppose] != 0 or present_school == oppose_school:
                    print("Error! Duplicate fight or same school matched both times!")
                    print(assignment_matrix[assignment_matrix[fight].str.contains(room)])
                    return False
                else:
                    school_matrix.iloc[present, oppose] = str(room) + str(fight + 1)
                    school_matrix.iloc[oppose, present] = '  '

        return True
    except Exception as e:
        print(f"Validation error: {e}")
        return False

# Function to display and save the results
def display_and_save_results(assignment_matrix, attempts, all_okay):
    if all_okay:
        print(f"Number of attempts needed: {attempts}")
        print("Final fight matrix:")
        print(assignment_matrix)

        # Generate the school matrix
        school_matrix = generate_school_matrix(assignment_matrix)
        print("School matrix:")
        print(school_matrix)

        # Generate the room matrix
        room_matrix = generate_room_matrix(assignment_matrix, team_list)
        print("Room matrix:")
        print(room_matrix)

        # Transpose and display room matrix
        transposed_room_matrix = room_matrix.transpose()
        print("Transposed room matrix:")
        print(transposed_room_matrix)

        # Save matrices to CSV files
        school_matrix.to_csv('./fight_matrix_randomiser/School_matrix.csv')
        room_matrix.to_csv('./fight_matrix_randomiser/Room_matrix.csv')
        transposed_room_matrix.to_csv('./fight_matrix_randomiser/Room_matrix_transposed.csv')
        assignment_matrix.to_csv('./fight_matrix_randomiser/Assignment_matrix.csv')
    else:
        print(f"Failed after {attempts} attempts")

# Function to generate the school matrix
def generate_school_matrix(assignment_matrix):
    school_matrix = pd.DataFrame(np.zeros([len(team_list), len(team_list)]), index=team_list, columns=team_list)
    for fight in range(4):
        for room in room_list:
            present = np.where(assignment_matrix[fight] == room + "P")[0][0]
            oppose = np.where(assignment_matrix[fight] == room + "O")[0][0]
            school_matrix.iloc[present, oppose] = str(room) + str(fight + 1)
            school_matrix.iloc[oppose, present] = '  '
    return school_matrix.replace(0, '')

# Function to generate the room matrix
def generate_room_matrix(assignment_matrix, team_list):
    room_matrix = pd.DataFrame(np.zeros([len(room_list), 8]), index=room_list)
    for fight in range(4):
        for room in room_list:
            room_matrix.loc[room, fight * 2] = team_list[np.where(assignment_matrix[fight] == room + "P")[0][0]]
            room_matrix.loc[room, fight * 2 + 1] = team_list[np.where(assignment_matrix[fight] == room + "O")[0][0]]
    return room_matrix

# Main execution
assignment_matrix, all_okay, attempts = assign_team(pd.DataFrame(), team_list, np.zeros(len(team_list)), room_list, same_school)
display_and_save_results(assignment_matrix, attempts, all_okay)
