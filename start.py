import requests
import re
import os


def get_file_group(n):
    return n // 2 if n % 2 == 0 else (n + 1) // 2


def clear_files_with_extension(directory, extension):
    for file_name in os.listdir(directory):
        if file_name.endswith(extension):
            file_path = os.path.join(directory, file_name)
            os.remove(file_path)


def main():
    # Convert to int just for validating input
    problem_id = int(input("Problem ID: "))

    # Clear every txt files
    current_path = os.getcwd()
    path_in = f"{current_path}/input"
    path_out = f"{current_path}/output"
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
