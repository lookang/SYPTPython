# SYPTPython
Python code organisers first version by Nic Wong [original coder's repository](https://github.com/not-even-wong) 

## Tournament Randomizer https://github.com/lookang/SYPTPython/blob/main/fight_matrix_randomiser.py

This Python script organizes teams into presentation and opponent slots for a debating tournament. The script ensures that each team presents twice and faces different opponents in each round. The code uses randomization with certain constraints to achieve a fair and diverse distribution of teams.

## Prerequisites

- Python 3.x
- pandas
- numpy
- random

## Run the script:
python fight_matrix_randomiser.py

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

### Acknowledgements
Credit and thanks to Nic Wong for his original code and help to provide a first version of the python code.


Part 2/3
# Cat A/B Juror Assignment 

This Python script automates the assignment of jurors for a debate competition in different rooms and categories.

## Overview

The script reads data about the debate competition, including the assignment matrix and juror information. It then performs the assignment of head jurors and regular jurors, considering various constraints such as previous assignments, school affiliations, and more.

## Prerequisites

- Python 3.x
- pandas
- numpy
- random

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/cat_A_juror_assignment.git
   cd cat_A_juror_assignment

      ```bash
   git clone https://github.com/your-username/cat_B_juror_assignment.git
   cd cat_B_juror_assignment

## Run the A/B script:
python cat_A_juror_assignment.py
python cat_B_juror_assignment.py

## Usage
The script is designed to automate the assignment of jurors for debate competitions. Customize the script by adjusting variables such as A_list, room_list, and file paths.
The script is designed to automate the assignment of jurors for debate competitions. Customize the script by adjusting variables such as B_list, room_list, and file paths.
## Configuration A/B
A_list: List of debate school/categories.
B_list: List of debate school/categories.
room_list: List of rooms.
assignment_matrix.csv: CSV file containing the assignment matrix.
juror_data.csv: CSV file containing juror information.

### Acknowledgements
Credit and thanks to Nic Wong for his original code and help to provide a first version of the python code.
