class TitleTooLing(Exception):
    pass  # 게시글의 title이 max_length를 초과한 경우


class ValidationError(Exception):
    pass  # pydantic이 아닌 로직에서 validationerror 발생시 사용
