from fastapi import APIRouter, Depends
from api.schemas import RoadmapList, TopicList, SummaryPayload, RoadmapSummary
from api.utils import llm
from api.utils.auth import basic_auth



router = APIRouter(
    prefix= "/roadmap",
    tags= ["code generation"]
)

@router.get("")
def get_developer_roadmap_list(authenticate = Depends(basic_auth)):
    prompt = """Retrieve list of software developer roadmaps\n{format_instructions}"""
    result = llm.chat_completion(RoadmapList, [], prompt, {})
    return result

@router.get("/{role}")
def get_roadmap(role : str, authenticate = Depends(basic_auth)):
    prompt = """{role} roadmap\n{format_instructions}"""
    result = llm.chat_completion(TopicList, ["role"], prompt, {"role" : role})
    return result


@router.post("/summary")
def get_roadmap_summary(payload : SummaryPayload, authenticate = Depends(basic_auth)):
    prompt = """I know only {expertise}, what can I do to become {role}. What are my advantages on my learning journey and places I have to concentrate. \n{format_instructions}"""
    input = {
                "expertise" : payload.expertise,
                "role" : payload.role
            }
    print(input)
    result = llm.chat_completion(RoadmapSummary, ["expertise", "role"], prompt, input)
    return result