import unittest

import os
from pathlib import Path


def sys_path_init():
    import sys
    # For tests/main.py Path
    path = Path(os.path.realpath(__file__)).parent.parent.parent.absolute()
    sys.path.append(str(path))
    # For test.sh Path
    path = Path(os.path.realpath(__file__)).parent.parent.absolute()
    sys.path.append(str(path))


def db_init():
    from app.database import manage
    print('============ DB Initialize Start    ============')
    manage.delete_all()
    manage.create_all()
    print('============ DB Initialize Complete ============')
    print()


def print_errors(elements):
    for element in elements:
        print(element[0])  # Error class.function_name
        print(element[1])  # Error Trace Back
        print()


def print_progress_line(first, second, third):
    print(f'============ {first:5s} {second:7s} {third:8s} ============')


def run_test_by_folder_name(folder_name: str, test_name: str, module_strings):
    print_progress_line(test_name, 'Test', 'Start')

    testSuite = unittest.TestSuite()

    module_strings = [folder_name + '.' + model_str for model_str in module_strings]
    [__import__(model_str) for model_str in module_strings]
    suites = [unittest.TestLoader().loadTestsFromName(model_str) for model_str in module_strings]
    [testSuite.addTest(suite) for suite in suites]

    result = unittest.TestResult()
    testSuite.run(result)

    print_progress_line(test_name, 'Result', 'Count')
    print(result)

    if len(result.errors) != 0:
        print_progress_line(test_name, 'Error', 'List')
        print_errors(result.errors)

    if len(result.failures) != 0:
        print_progress_line(test_name, 'Failure', 'List')
        print_errors(result.failures)

    print()


def service_test():
    # Crud Test module 이름을 생성 순서에 맞게 작성합니다
    module_strings = [
        'alarm',
        'audit_program',
        'auth',
        'company',
        'control',
        'control_attribute',
        'email_test',
        'evidence',
        'log',
        'possible_result',
        'request',
        's3',
        'sample',
        'test_attribute',
        'test_issue',
        'test_sheet',
        'test_term',
    ]

    run_test_by_folder_name('service', 'Service', module_strings)


def api_test():
    # API Test module 이름들을 생성 순서에 맞게 작성합니다
    # 1. auth.py
    # 2. testing.py
    # 3. request.py
    # 4. lead.py
    # 5. admin.py
    # 6. dashboard.py
    # 7. navigation.py
    module_strings = [
        'admin',
        'auth',
        'dashboard',
        'lead',
        'navigation',
        'request',
        'testing',
        'testsheet',
        'testsheet_conclusions',
        'testsheet_information',
        'testsheet_test',
    ]
    run_test_by_folder_name('api', 'API', module_strings)


def init_dummy_data():
    sys_path_init()

    db_init()

    service_test()

    api_test()


if __name__ == "__main__":
    init_dummy_data()
