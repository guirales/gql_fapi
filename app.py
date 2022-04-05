from optparse import Option
from schemas import Members
from fastapi import FastAPI
import strawberry
from strawberry.asgi import GraphQL

import json
from typing import List, Optional


@strawberry.type
class User:
    name: str
    age: int

def get_user():
    return User(name="Patrick", age=100)

async def get_members(id:Optional[str]=None):
    
    with open("members.json") as members:
        members_list = json.load(members)
    print(id)
    if id:
        for idm in members_list:
            if idm["member_id"]==id:
                return [Members(**idm)]
        raise Exception(f"there is no the id {id}")

    return [Members(**memberi) for memberi in members_list]

async def new_user( 
            member_id:str,
            state:str,
            sex:str,
            birth_date:str#,
            #member_id:str
            ):
    new_member={
                "member_id":member_id,
                "state":state,
                "sex":sex,
                "birth_date":birth_date#,
                #"member_id":member_id
                }
    with open("members.json","r+") as members:
        members_list = json.load(members)
        for idm in members_list:
            if idm["member_id"]==member_id:
                raise Exception(f"Member with id {member_id} already exist")
        members_list.append(new_member)
        members.seek(0)
        json.dump(members_list,members,indent=2)
    return [Members(**new_member)]

async def del_user(id:str):
    with open("members.json","r+") as members:
        members_list = json.load(members)
    
    for i, idm in enumerate(members_list):
        if idm["member_id"]==id:
            idm_del=members_list.pop(i)
            with  open("members.json","w") as members:
                json.dump(members_list,members,indent=2)
            return [Members(**idm_del)]
        
    raise Exception(f"there is no the id {id}")

   

@strawberry.type
class Query:
    userj:User=strawberry.field(resolver=get_user)
    member: List[Members]=strawberry.field(resolver=get_members)
@strawberry.type
class Mutation:
    new_member:List[Members]=strawberry.mutation(resolver=new_user)
    del_member:List[Members]=strawberry.mutation(resolver=del_user)

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQL(schema)

app = FastAPI()
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)