from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from schemas import EventSchema, SocietySchema
from functools import lru_cache
import os


def get_llm():
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set. Add it to your environment or .env file.")
    return ChatOpenAI(model="gpt-4o-mini", temperature=0)


# ── Event Parser ───────────────────────────────────────────────────────────

event_parser = PydanticOutputParser(pydantic_object=EventSchema)

event_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a data extraction assistant for a college website.
Extract event details from the given WhatsApp message or raw text.
Be smart about inferring missing fields — if no registration link is found, use '#'.
If no organizer is mentioned, infer from context (e.g. 'DTU' or society name).
Today's year is 2025 — use it when parsing relative dates.

{format_instructions}"""),
    ("human", "Extract event details from this text:\n\n{text}")
])

@lru_cache(maxsize=1)
def get_event_chain():
    return event_prompt | get_llm() | event_parser


# ── Society Parser ─────────────────────────────────────────────────────────

society_parser = PydanticOutputParser(pydantic_object=SocietySchema)

society_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a data extraction assistant for a college website.
Extract society/club details from the given WhatsApp message or raw text.
Infer the category based on the society's nature:
- culturalS: dance, music, drama, art
- technicalS: coding, robotics, IEEE, ACM, tech clubs
- sportsS: cricket, football, basketball, any sport
- academicS: research, debate, quiz, academic clubs
- socialS: NSS, volunteer, community service
- creativeS: photography, writing, design
- businessS: entrepreneurship, finance, consulting

{format_instructions}"""),
    ("human", "Extract society details from this text:\n\n{text}")
])

@lru_cache(maxsize=1)
def get_society_chain():
    return society_prompt | get_llm() | society_parser
