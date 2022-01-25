from inspect import currentframe


def get_log_message_by_function_name(current_frame=currentframe, **kwargs):
    """
    호출한 router 함수의 이름에 해당하는 log message를 반환합니다.
    인자는 log_message에 선언된 이름으로 하시고 값을 넣어주시면 됩니다.
    :param current_frame: 자동 삽입됩니다.
    """
    function_name = str(current_frame().f_back.f_back).split(' ')[-1][:-1]
    if function_name in log_message:
        msg = log_message[str(current_frame().f_back.f_back).split(' ')[-1][:-1]]
        try:
            return msg.format(**kwargs)
        except:
            print('로그 메세지에 해당 키워드가 없습니다.')
    else:
        print(f'{function_name} 의 로그 메세지 양식이 없습니다.')
        return None


log_message = {
    # route name
    'route_function_name': "error msg{keyword}",
}
