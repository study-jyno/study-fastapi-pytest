from inspect import currentframe


# router 공통 사용 함수


def get_summary_location(current_frame=currentframe):
    """
    함수가 호출된 파일의 촐더 이름, 파일 이름과 함수가 위치한 라인 번호를 반환하는 함수

    사용하는 방법 : summary= FUNCTION_NAME  + " : "  + get_summary_location()
    :param current_frame: 자동 삽입됩니다
    :return: File '{folder_name.file_name}', line {line_number}
    """
    with open(current_frame().f_back.f_locals['__file__'], 'r') as source_code_file:
        function_text = source_code_file.readlines()[current_frame().f_back.f_lineno]
    function_text = function_text.split('(')[0][3:]
    return f"{function_text} | File '{current_frame().f_back.f_locals['__name__']}', line {current_frame().f_back.f_lineno}"
