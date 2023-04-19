# Python [BOJ](https://www.acmicpc.net/) Grader

A cli tool to test if your python code prints expected output as a given input.

## Usage

1. Run `python3 start.py` and enter the id of the problem to solve.
   - It removes old test cases and creates new cases.
   - You can add test cases by adding `input/$FILE_NAME` and `output/$FILE_NAME`.
2. Write your solution in `solution.py`.
3. Run `python3 test.py` to test your code.
