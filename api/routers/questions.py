from fastapi import APIRouter, Depends
from api.schemas import QuAndAns
from api.utils import llm
from api.utils.auth import basic_auth

router = APIRouter(
    prefix= "/questions",
    tags= ["questions"]
)

@router.get("")
def get_questions(topic:str, authenticate = Depends(basic_auth)):
    prompt = """Create 5 question with 4 options and answer about {topic}. I want 2 basic, 1 intermediate and 1 hard question \n {format_instructions}"""
    result = llm.chat_completion(QuAndAns, ["topic"], prompt, {"topic" : topic})
    return result
