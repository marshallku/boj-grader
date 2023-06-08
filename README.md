# [BOJ](https://www.acmicpc.net/) Grader

A tool to test if your code prints expected output as a given input.

Requirements: gcc, python3

## Usage

1. Run `./start` and enter the id of the problem to solve.
    - You can pass the id just in command line like `./start 1000`
    - It removes old test cases and creates new cases.
    - You can add test cases by adding `input/$FILE_NAME` and `output/$FILE_NAME`.
2. Write your solution in `solution.cpp` or `solution.py`.
3. Run `./test` to test your code.
    - It tries to run C++ by default.
    - You can specify language with -l argument like `./test -l cpp(or c++)` or `./test -l py(or python)`

### Adding solution files to github

1. Set up github correctly
    - Go to Settings > Actions > General and check Workflow permissions and check if it has write permission
    - Go to Actions and check if is enabled
2. Add your solution file written in supported languages in `solutions/**/$PROBLEM_ID.$EXTENSION`.
    - e.g. `solutions/marshallku/1000.cpp`, `solutions/numerical/easy/1000.py`
3. The README file with scoring result will be automatically generated with github actions
