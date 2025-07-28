import os
import json
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import LLMSetting


class TriageResult(BaseModel):
    category: str = Field(description="One of: Billing, Technical, Account, Other")
    priority: str = Field(description="One of: Low, Medium, High")

parser = PydanticOutputParser(pydantic_object=TriageResult)

llm = ChatGroq(
    temperature=0,
    model= LLMSetting.MODEL_NAME,
    api_key=LLMSetting.GROQ_API_KEY
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
    """
    Classifies a support ticket using Groq LLM (via LangChain).
    Returns a safe dictionary even on failure.
    """
    try:
        # Format the prompt
        prompt = prompt_template.format_messages(query=text, 
                                                 format_instruction=parser.get_format_instructions())

        # Get response from Groq
        response = llm.invoke(prompt)

        # Raw content from the model
        content = (response.content or "").strip()

        result = parser.parse(content)

        # Convert to dict for API output
        return {"classification": result.dict()}

    except Exception as e:
        return {
            "classification": {"category": "Error", "priority": "Low"},
            "error": str(e),
        }