![image](https://github.com/lookang/SYPTPython/assets/20143558/e95118ed-13bc-47f7-9329-0c04566b8eb7)# SYPTPython The Singapore Young Physicists' Tournament (SYPT) https://iyptsypt.wixsite.com/sypt/ modlled after International Young Physicists' Tournament (IYPT) 

- Python code for organisers
- First version by Nic Wong [original coder's repository](https://github.com/not-even-wong)
- output and data has been anonymised to just Lawrence etc... so you need to use your own data source

## Tournament Randomizer [https://github.com/lookang/SYPTPython/blob/main/python/fight_matrix_randomiser_law_working01.py](https://github.com/lookang/SYPTPython/blob/main/fight_matrix_randomiser_law_working01.py)

This Python script organizes teams into presentation and opponent slots for a debating tournament. The script ensures that each team presents twice and faces different opponents in each round. The code uses randomization with certain constraints to achieve a fair and diverse distribution of teams.

## Prerequisites

- Python 3.x
- pandas
- numpy
- random

## Run the script:

To run the Python script, you first need to navigate to the folder where the script is located using the command line. Here’s how you can do that and then run the script:

1. **Open Command Line or Terminal**: 
   - On Windows, you can use **Command Prompt** or **PowerShell**.
   - On macOS or Linux, open the **Terminal**.

2. **Navigate to the folder**: 
   Use the `cd` (change directory) command to navigate to the folder where your script is saved. For example, if your script is located in a folder called `Desktop/NicWong/SYPTPython-main` on your desktop, you would enter:

   - Windows:
     ```bash
     cd Desktop/NicWong/SYPTPython-main
     ```
   - macOS/Linux:
     ```bash
     cd /Users/lookang/Desktop/NicWong/SYPTPython-main
     ```

3. **Run the script**: 
   Once you are in the correct folder, you can run the script by typing the following command:

   ```bash
   python fight_matrix_randomiser_law_working01.py
   ```

This will execute the Python script in that directory.


### Usage

1. **Team Lists:**
   - Modify the `A_list` and `B_list` variables to include the names of participating teams for 2024. Adjust the lists as needed.

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

- The script allows for a maximum of 500 randomization attempts (`MAX_ATTEMPTS`). If successful, the matrices are displayed; otherwise, a failure message is shown.

- The final matrices are saved as CSV files in the `fight_matrix_randomiser` directory: 
  - `School matrix.csv`
  - `Room matrix.csv`
  - `Transposed room_matrix.csv` for copy paste into emails
  - `Assignment matrix.csv`

Feel free to customize the code to fit your specific tournament requirements. For any issues or improvements, please refer to the  or open an issue.
### sample output
Attempts: 3

Number of attempts needed: 4

  **Final fight matrix:**

|          |  0  |  1  |  2  |  3  |
|----------|-----|-----|-----|-----|
| **RI_A1**   |  AO |  AP |  CO |  CP |
| **RI_A2**   |  DP |  BO |  BO |  AP |
| **NUSH_A1** |  AP |  DO |  BP |  EO |
| **NUSH_A2** |  DO |  CP |  EP |  DO |
| **NJC_A1**  |  CP |  AO |  DP |  BO |
| **NJC_A2**  |  EP |  EP |  EO |  CO |
| **HCI_A1**  |  EO |  DP |  CP |  AO |
| **HCI_A2**  |  CO |  CO |  AP |  EP |
| **RVHS_A1** |  BP |  EO |  DO |  DP |
| **TJC_A1**  |  BO |  BP |  AO |  BP |

School matrix:

|         | RI_A1 | RI_A2 | NUSH_A1 | NUSH_A2 | NJC_A1 | NJC_A2 | HCI_A1 | HCI_A2 | RVHS_A1 | TJC_A1 |
|---------|-------|-------|---------|---------|--------|--------|--------|--------|---------|--------|
| **RI_A1**   |       |       |         |         |   A2   |   C4   |        |        |         |        |
| **RI_A2**   |       |       |         |   D1    |        |        |   A4   |        |         |        |
| **NUSH_A1** |   A1  |   B3  |         |         |        |        |        |        |         |        |
| **NUSH_A2** |       |       |         |         |   E3   |        |   C2   |        |         |        |
| **NJC_A1**  |       |       |         |         |        |   C1   |        |        |   D3    |        |
| **NJC_A2**  |       |       |         |         |        |        |   E1   |        |         |   E2   |
| **HCI_A1**  |   C3  |       |   D2    |         |        |        |        |        |         |        |
| **HCI_A2**  |       |       |   E4    |         |        |        |        |        |   A3    |        |
| **RVHS_A1** |       |       |         |   D4    |        |        |        |        |         |   B1   |
| **TJC_A1**  |       |   B2  |         |         |   B4   |        |        |        |         |        |

Room matrix:

|   |    0   |    1   |    2   |    3   |    4   |    5   |    6   |    7   |
|---|--------|--------|--------|--------|--------|--------|--------|--------|
| A | NUSH_A1 | RI_A1  | RI_A1  | NJC_A1 | HCI_A2 | TJC_A1 | RI_A2  | HCI_A1 |
| B | RVHS_A1 | TJC_A1 | TJC_A1 | RI_A2  | NUSH_A1 | RI_A2 | TJC_A1 | NJC_A1 |
| C | NJC_A1  | HCI_A2 | NUSH_A2 | HCI_A2 | HCI_A1 | RI_A1  | RI_A1  | NJC_A2 |
| D | RI_A2   | NUSH_A2 | HCI_A1 | NUSH_A1 | NJC_A1 | RVHS_A1 | RVHS_A1 | NUSH_A2 |
| E | NJC_A2  | HCI_A1 | NJC_A2 | RVHS_A1 | NUSH_A2 | NJC_A2 | HCI_A2 | NUSH_A1 |


Transposed room_matrix:
|   |    A    |    B    |    C    |    D    |    E    |
|---|---------|---------|---------|---------|---------|
| 0 | NUSH_A1 | RVHS_A1 | NJC_A1  | RI_A2   | NJC_A2  |
| 1 | RI_A1   | TJC_A1  | HCI_A2  | NUSH_A2 | HCI_A1  |
| 2 | RI_A1   | TJC_A1  | NUSH_A2 | HCI_A1  | NJC_A2  |
| 3 | NJC_A1  | RI_A2   | HCI_A2  | NUSH_A1 | RVHS_A1 |
| 4 | HCI_A2  | NUSH_A1 | HCI_A1  | NJC_A1  | NUSH_A2 |
| 5 | TJC_A1  | RI_A2   | RI_A1   | RVHS_A1 | NJC_A2  |
| 6 | RI_A2   | TJC_A1  | RI_A1   | RVHS_A1 | HCI_A2  |
| 7 | HCI_A1  | NJC_A1  | NJC_A2  | NUSH_A2 | NUSH_A1 |


### Acknowledgements
Credit and thanks to Nic Wong for his original code and help to provide a first working version of the python code.


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

1. Prepare the files cat_A Assignment matrix.csv and cat_B Assignment matrix.csv into the root of the folder
2. cd to the Folder
3.**Run the script**: 
   Once you are in the correct folder, you can run the script by typing the following command:

   ```bash
   python preparecatAcsv.py
   ```
This will execute the Python script in that directory and prepare the file cat_A Assignment matrix.csv at the root of the folder.
or 
 ```bash
   python preparecatBcsv.py
   ```
This will execute the Python script in that directory and prepare the file cat_B Assignment matrix.csv at the root of the folder.

# CSV Row Index Modifier

This Python script loads a CSV file, replaces the substring `'_A'` in the row index with an empty string, and saves the modified DataFrame both in the current directory and one level up in the folder structure as new CSV files.

## How It Works

- The script reads a CSV file named `Assignment matrix.csv`.
- It processes the row indices to remove the substring `'_A'`.
- The modified data is saved as `cat_A Assignment matrix.csv` in the current directory and also in the parent directory (one level up).


4. 
## Run the A/B script:
- https://github.com/lookang/SYPTPython/blob/main/cat_A_juror_assignment.py
- https://github.com/lookang/SYPTPython/blob/main/cat_B_juror_assignment.py
- python cat_A_juror_assignment.py
- need these files to work
-    cat_A Assignment matrix.csv (from the eariler fight_matrix_randomiser folder rename file `Assignment matrix.csv` to `cat_A Assignment matrix.csv`)
-    cat_A jurors.csv (need to capture these data on email google form and copy over in similar format )
- python cat_B_juror_assignment.py
-    cat_B Assignment matrix.csv (from the eariler fight_matrix_randomiser folder rename file `Assignment matrix.csv` to `cat_B Assignment matrix.csv`)
-    cat_B jurors20240129.csv (need to capture these data on email google form and copy over in similar format )

## Usage
The script is designed to automate the assignment of jurors for debate competitions. Customize the script by adjusting variables such as A_list, room_list, and file paths.
The script is designed to automate the assignment of jurors for debate competitions. Customize the script by adjusting variables such as B_list, room_list, and file paths.

## Configuration A/B
- cat_A Assignment matrix.csv: CSV file containing the assignment matrix of debate school/categories.
- cat_B Assignment matrix.csv: CSV file containing the assignment matrix of debate school/categories.
- cat_A jurors.csv: CSV file containing juror information.
- cat_B jurors20240129.csv: CSV file containing juror information.
- room_list: List of rooms.



## Steps to work the Cat A assignment (Documentation)
- copy out the file /Users/lookang/Desktop/NicWong/randomisation_stuff/fight_matrix_randomiser/ArchiveCatAFullRandom/Assignment matrix.csv to the root of the folder say /Users/lookang/Desktop/NicWong/randomisation_stuff/Assignment matrix.csv
- rename Cat A Assignment matrix.csv as Cat A Assignment matrix_old.csv to protect old working files
- rename just copied file as Cat A Assignment matrix.csv so as to do minimum edits to the file cat_A_juror_assignment.py
- open up  cat_A_juror_assignment.py and noticed that the school names are RI1 and not RI_A1, so do a replace _A to blank to prepare the data file format
the data should look like this


|      |  0  |  1  |  2  |  3  |
|------|-----|-----|-----|-----|
| RI1  |  CP |  DO |  BO |  EP |
| RI2  |  BP |  BO |  AO |  DP |
| NUSH1|  DO |  CP |  BP |  AO |
| NUSH2|  AO |  BP |  DP |  BO |
| NJC1 |  DP |  AO |  CP |  DO |
| NJC2 |  EP |  EP |  DO |  EO |
| HCI1 |  CO |  CO |  AP |  BP |
| HCI2 |  BO |  AP |  EP |  CO |
| RVHS1|  AP |  EO |  CO |  CP |
| TJC1 |  EO |  DP |  EO |  AP |




### Acknowledgements
Credit and thanks to Nic Wong for his original code and help to provide a first version of the python code.
