import sys
import io
import os
import subprocess
import re
import time
import psutil

_, mode, path, output_status = sys.argv


def format_bytes(value: float):
    kilo_byte = 1e+3
    mega_byte = 1e+6

    if (value >= mega_byte):
        return f"{value / mega_byte:.0f} MB"

    if (value >= kilo_byte):
        return f"{value / kilo_byte:.0f} KB"

    return f"{value:.0f} B"


def format_time(value: float):
    return f"{value * 1000:.2f} ms"


def run_process(args: list[str], stdin: io.TextIOWrapper):
    start_time = time.time()
    process = subprocess.Popen(
        args, stdin=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elapsed_time = time.time() - start_time
    subprocess_process = psutil.Process(process.pid)
    memory_usage = subprocess_process.memory_info().rss
    output, runtime_errors = process.communicate()

    if runtime_errors:
        print("Runtime Error:")
        print(runtime_errors.decode('utf-8'))
        return [None, elapsed_time, memory_usage]

    return [output.decode('utf-8').rstrip(), elapsed_time, memory_usage]


def run_cpp_file(input_data: io.TextIOWrapper, directory: str):
    output_file = f"{directory}tmp.out"
    build_process = subprocess.Popen(
        ['g++', f"{directory}solution.cpp", '-o', output_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, compile_errors = build_process.communicate()

    if compile_errors:
        print("Compilation Error:")
        print(compile_errors.decode('utf-8'))
        return None

    result = run_process([f"./{output_file}"], input_data)

    os.remove(output_file)

    return result


def run_python_file(input_data: io.TextIOWrapper, directory: str):
    result = run_process(["python3", f"{directory}solution.py"], input_data)

    return result


def main():
    local_path = f"{path}/" if path else ''
    target_path = f"{os.getcwd()}{'/' + path if path else ''}"
    path_in = f"{target_path}/input"
    path_out = f"{target_path}/output"
    scoring_status = []

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
            actual_output, elapsed_time, memory_usage = run_cpp_file(
                f, local_path)if mode == 'cpp' else run_python_file(f, local_path)

        expected_output = open(
            output_file, 'rt', encoding='utf-8').read().rstrip()

        passed = actual_output == expected_output

        # Remove previous line
        sys.stdout.write("\033[F")
        print(f"Case {i}: {'PASS' if passed else 'FAIL'}     ")
        scoring_status.append([passed, elapsed_time, memory_usage])

        if not passed and actual_output is not None:
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
        markdown_content = f"# Scoring result of [{problem_id}](https://www.acmicpc.net/problem/{problem_id})\n\nLanguage: {mode}\n\n| Case | Passed | Elapsed Time | Memory Usage |\n| - | - | - | - |"
        markdown_table = ''

        for i in range(len(scoring_status)):
            passed, elapsed_time, memory_usage = scoring_status[i]
            markdown_table += f"\n| {i + 1} | {'✅' if scoring_status[i] else '❌'} | {format_time(elapsed_time)} | {format_bytes(memory_usage)} |"

        markdown_path = f"{local_path}README.md"

        with open(markdown_path, "w") as file:
            file.write(markdown_content + markdown_table + '\n')


if __name__ == '__main__':
    main()
