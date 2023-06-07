import sys
import os
import subprocess
import re

_, mode, path, output_status = sys.argv


def run_cpp_file(input_data, directory):
    output_file = f"{directory}tmp.out"
    process = subprocess.Popen(
        ['g++', f"{directory}solution.cpp", '-o', output_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, compile_errors = process.communicate()

    if compile_errors:
        print("Compilation Error:")
        print(compile_errors.decode('utf-8'))
        return None

    process = subprocess.Popen(
        [f"./{output_file}"], stdin=input_data, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, runtime_errors = process.communicate()

    os.remove(output_file)

    if runtime_errors:
        print("Runtime Error:")
        print(runtime_errors.decode('utf-8'))
        return None

    return output.decode('utf-8').rstrip()


def run_python_file(input_data, directory):
    process = subprocess.run(
        ["python3", f"{directory}solution.py"],
        input=input_data,
        capture_output=True,
        encoding='utf-8',
    )

    return process.stdout.rstrip()


def main():
    local_path = f"{path}/" if path else ''
    target_path = f"{os.getcwd()}{'/' + path if path else ''}"
    path_in = f"{target_path}/input"
    path_out = f"{target_path}/output"
    pass_status = []

    print('━━━━━━━━━━━━━━')

    # Use variable instead using `enumerate` to skip hidden files
    i = 1
    for file in sorted(os.listdir(path_in)):
        output_file = f"{path_out}/{file}"

        # Skip if path is not a file, or it's hidden
        if not os.path.isfile(output_file) or file[0] == '.':
            continue

        print(f"Running case {i}...")

        with open(f"{path_in}/{file}", 'r') as f:
            actual_output = run_cpp_file(
                f, local_path)if mode == 'cpp' else run_python_file(f.read(), local_path)

        expected_output = open(
            output_file, 'rt', encoding='utf-8').read().rstrip()

        passed = actual_output == expected_output

        # Remove previous line
        sys.stdout.write("\033[F")
        print(f"Case {i}: {'PASS' if passed else 'FAIL'}     ")
        pass_status.append(passed)

        if not passed:
            print("expected")
            print(expected_output)
            print("but got")
            print(actual_output)

        print('━━━━━━━━━━━━━━')
        i += 1

    # Write markdown output
    if output_status == 'true':
        id_pattern = r'/(\d+)'
        match_result = re.search(id_pattern, path)

        if not match_result:
            return

        problem_id = match_result.group(1)
        markdown_content = f"# Scoring result of [{problem_id}](https://www.acmicpc.net/problem/{problem_id})\n\n| Case | Passed |\n| - | - |"
        markdown_table = ''

        for i in range(len(pass_status)):
            markdown_table += f"\n| {i + 1} | {'✅' if pass_status[i] else '❌'} |"

        markdown_path = f"{local_path}README.md"

        with open(markdown_path, "w") as file:
            file.write(markdown_content + markdown_table + '\n')


if __name__ == '__main__':
    main()
