from langchain.pydantic_v1 import BaseModel, Field
from typing import List, Union
from pydantic import BaseModel as bM

class SummaryPayload(bM):
    expertise : str
    role : str


class OneQuAndAns(BaseModel):
    question : str = Field(description="Query generated for the user's input")
    Options : List[Union[str, int]] = Field(description="Options")
    Answer : str = Field(description="Correct answer")
    level : str = Field(description="Basic or Intermediate or Hard type of query")


class QuAndAns(BaseModel):
    questions : List[OneQuAndAns] = Field(description="List of questions")

class RoadmapList(BaseModel):
    items : List[str] = Field(description="List of developer roadmap")

class TopicList(BaseModel):
    items : List[str] = Field(description="List of roadmap topics")

class RoadmapSummary(BaseModel):
    Advantages : List[str] = Field(description="List of advantages based on the user input")
    Concentrate : List[str] = Field(description="List of suggestion to concentrate and timeline to  complete the topics based on the user input")
    summary : str = Field(description="Overall summary of the user input")