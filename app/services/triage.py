import os
import json
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import Setting


class TriageResult(BaseModel):
    category: str = Field(description="Billing | Technical | Account | Other")
    priority: str = Field(description="Low | Medium | High")

parser = PydanticOutputParser(pydantic_object=TriageResult)

llm = ChatGroq(
    temperature=0,
    model= Setting.MODEL_NAME,
    api_key=Setting.GROQ_API_KEY
)

prompt_template = ChatPromptTemplate.from_template(
    """
    You are a support ticket triage assistant.
    Analyze the following support query and return only a JSON object:
    {{
        "category": "Billing | Technical | Account | Other",
        "priority": "Low | Medium | High"    
    }}
    Query: "{query}"
"""
)

async def classify_ticket(text: str) -> dict:

    try: 
        prompt= prompt_template.format_messages(
            query=text, format_instructions=parser.get_format_instructions()
        )
        response =llm.invoke(prompt)
        result =parser.parse(response.content.strip())

        return {"classification": result.dict()}
    
    except Exception as e:

        return {"classification": {"category": "Error", "priority": "Low"}, "error": str(e)}