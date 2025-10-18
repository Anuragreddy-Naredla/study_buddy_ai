from typing import List
from pydantic import BaseModel,Field,validator#validate for datamodels

class MCQQuestions(BaseModel):

    question: str=Field(description="The question text")
    options:List[str] =Field(description="List of 4 options")
    correct_answer:str=Field(description="The correct answer from the options")

    @validator("question",pre=True)#works on only on question
    def clean_question(cls,v):
        if isinstance(v,dict):#sometimes LLM give the output in the dictionary aswell to extract the description we will use this
            return v.get("description", str(v))
        return str(v)
    
class FillBlankQuestion(BaseModel):
    question: str=Field(description="The question text with '___' for the blank")
    answer:str=Field(description="The correct word or phrase the blank")

    @validator("question",pre=True)
    def clean_question(cls,v):
        if isinstance(v,dict):#sometimes LLM give the output in the dictionary aswell to extract the description we will use this
            return v.get("description", str(v))
        return str(v)
