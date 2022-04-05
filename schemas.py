import strawberry

@strawberry.type
class Members:
    member_id: str
    state: str
    sex: str
    birth_date: str