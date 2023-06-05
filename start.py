import requests
import re
import os
import sys


def get_file_group(n):
    return n // 2 if n % 2 == 0 else (n + 1) // 2


def clear_files_with_extension(directory, extension):
    for file_name in os.listdir(directory):
        if file_name.endswith(extension):
            file_path = os.path.join(directory, file_name)
            os.remove(file_path)


def create_folder_if_not_exists(path):
    if os.path.exists(path):
        return

    os.makedirs(path)


def main():
    # Convert to int just for validating input
    _, system_problem_id, path = sys.argv
    problem_id = int(system_problem_id) if system_problem_id else int(
        input("Problem ID: "))

    # Clear every txt files
    target_path = f"{os.getcwd()}{'/' + path if path else ''}"
    path_in = f"{target_path}/input"
    path_out = f"{target_path}/output"
    create_folder_if_not_exists(path_in)
    create_folder_if_not_exists(path_out)
    clear_files_with_extension(path_in, '.txt')
    clear_files_with_extension(path_out, '.txt')

    # Fetch and parse sample data
    url = f"https://www.acmicpc.net/problem/{problem_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers).content.decode('utf-8')
    data_pattern = re.compile(
        r'<pre.*?sampledata.*?>((.|\n)*?)<\/pre>', re.DOTALL)

    # Write sample data
    for i, match in enumerate(re.finditer(data_pattern, response), start=1):
        is_input_file = i % 2
        file_name = f"{get_file_group(i)}.txt"

        with open(f"{path_in if is_input_file else path_out}/{file_name}", "w") as file:
            file.write(match.group(1).strip())


if __name__ == '__main__':
    main()
