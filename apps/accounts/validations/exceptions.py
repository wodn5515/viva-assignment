class PasswordNotMatched(Exception):
    pass  # 회원가입시 패스워드/패스워드체크 불일치


class EmailPasswordWrong(Exception):
    pass  # 로그인시 입력값으로 로그인 실패
