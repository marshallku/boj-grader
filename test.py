import sys
import os
import subprocess


def test():
    current_path = os.getcwd()
    path_in = f"{current_path}/input"
    path_out = f"{current_path}/output"

    print('━━━━━━━━━━━━━━')

    # Use variable instead using `enumerate` to skip hidden files
    i = 1
    for file in sorted(os.listdir(path_in)):
        output_file = f"{path_out}/{file}"

        # Skip path is not file, or it's hidden
        if not os.path.isfile(output_file) or file[0] == '.':
            continue

        print(f"Running case {i}...")

        with open(f"{path_in}/{file}", 'r') as f:
            input_data = f.read()

        expected_output = open(
            output_file, 'rt', encoding='utf-8').read().rstrip()

        process = subprocess.run(
            ["python3", "solution.py"],
            input=input_data,
            capture_output=True,
            encoding='utf-8',
        )

        actual_output = process.stdout.rstrip()
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
    test()
