import os
import subprocess
import sys


class TestHelper:
    @staticmethod
    def __show_coverage_results():
        try:
            subprocess.call(["coverage3", "combine"])
            subprocess.call(["coverage3", "report", "-m"])
        except:
            pass

    @staticmethod
    def execute_python3_file(filename, use_coverage, ignored_files):
        if sys.platform.startswith("win"):
            # On windows we won't find a python3 executable and we don't measure coverage
            return subprocess.call(["python", filename])

        if not use_coverage:
            return subprocess.call(["python3", filename])

        try:
            return subprocess.call(["coverage3",
                                    "run",
                                    "-p",  # make it collectable later
                                    "--branch",  # check branch AND statement coverage
                                    "--omit",
                                    ignored_files,
                                    filename])
        except:
            print("Coverage failed. Falling back to standard unit tests.")
            return subprocess.call(["python3", filename])

    @staticmethod
    def execute_python3_files(filenames, use_coverage, ignore_list):
        number = len(filenames)
        failures = 0
        for file in filenames:
            print("\nRunning: {} ({})\n".format(os.path.splitext(os.path.basename(file))[0], file), end='')
            result = TestHelper.execute_python3_file(file, use_coverage, ",".join(ignore_list))  # either 0 or 1
            failures += result
            print("\n" + "#" * 70)

        print("\nTests finished: failures in {} of {} test modules".format(failures, number))

        if use_coverage:
            TestHelper.__show_coverage_results()

        return failures

    @staticmethod
    def get_test_files(testdir):
        test_files = []
        for (dirpath, dirnames, filenames) in os.walk(testdir):
            for filename in filenames:
                if filename.endswith("Test.py"):
                    test_files.append(os.path.join(dirpath, filename))
        return test_files
