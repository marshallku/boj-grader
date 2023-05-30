import sys
import os
import subprocess

mode = sys.argv[1]


def run_cpp_file(input_data):
    output_file = './a.out'
    process = subprocess.Popen(
        ['g++', 'solution.cpp'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, compile_errors = process.communicate()

    if compile_errors:
        print("Compilation Error:")
        print(compile_errors.decode('utf-8'))
        return None

    process = subprocess.Popen(
        ['./a.out'], stdin=input_data, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, runtime_errors = process.communicate()

    os.remove(output_file)

    if runtime_errors:
        print("Runtime Error:")
        print(runtime_errors.decode('utf-8'))
        return None

    return output.decode('utf-8').rstrip()


def run_python_file(input_data):
    process = subprocess.run(
        ["python3", "solution.py"],
        input=input_data,
        capture_output=True,
        encoding='utf-8',
    )

    return process.stdout.rstrip()


def main():
    current_path = os.getcwd()
    path_in = f"{current_path}/input"
    path_out = f"{current_path}/output"

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
                f)if mode == 'cpp' else run_python_file(f.read())

        expected_output = open(
            output_file, 'rt', encoding='utf-8').read().rstrip()

        passed = actual_output == expected_output

        # Remove previous line
        sys.stdout.write("\033[F")
        print(f"Case {i}: {'PASS' if passed else 'FAIL'}     ")

        if not passed:
            print("expected")
            print(expected_output)
            print("but got")
            print(actual_output)

        print('━━━━━━━━━━━━━━')
        i += 1


if __name__ == '__main__':
    main()
