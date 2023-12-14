# SYPTPython
Python code organisers first version by Nic Wong [original coder's repository](https://github.com/not-even-wong) 

## Tournament Randomizer https://github.com/lookang/SYPTPython/blob/main/fight_matrix_randomiser.py

This Python script organizes teams into presentation and opponent slots for a debating tournament. The script ensures that each team presents twice and faces different opponents in each round. The code uses randomization with certain constraints to achieve a fair and diverse distribution of teams.

### Usage

1. **Team Lists:**
   - Modify the `A_list` and `B_list` variables to include the names of participating teams for 2022. Adjust the lists as needed.

2. **Setup for Sorting:**
   - Modify the `room_list` and `team_list` variables based on your tournament's room and team configurations.

3. **Check for Duplicate Schools:**
   - The script checks for schools sending more than one team and prints any duplicates.

4. **Random Assignment:**
   - The script uses a randomized approach to assign presentation and opponent slots to teams for each round. It ensures that teams face different opponents in each round and prioritizes teams with fewer presentations.

5. **Error Checking:**
   - The script performs checks for the number of presentations by each team and identifies any duplicate fights. If errors are found, the randomization process is repeated.

6. **Output:**
   - If the randomization is successful, the final assignment matrix, school matrix, and room matrix are displayed. These matrices provide a comprehensive overview of the tournament schedule.

### Notes

- The script allows for a maximum of 250 randomization attempts (`MAX_ATTEMPTS`). If successful, the matrices are displayed; otherwise, a failure message is shown.

- The final matrices are saved as CSV files in the `fight_matrix_randomiser` directory: 
  - `School matrix.csv`
  - `Room matrix.csv`
  - `Assignment matrix.csv`

Feel free to customize the code to fit your specific tournament requirements. For any issues or improvements, please refer to the  or open an issue.
