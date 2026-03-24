from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from parsers import get_event_chain, get_society_chain, event_parser, society_parser

app = FastAPI(title="DTU Hub AI Parser", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ParseRequest(BaseModel):
    text: str


@app.get("/")
def root():
    return {"status": "DTU Hub AI Service running"}


@app.post("/parse/event")
async def parse_event(req: ParseRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    try:
        result = get_event_chain().invoke({
            "text": req.text,
            "format_instructions": event_parser.get_format_instructions(),
        })
        return result.model_dump()
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/parse/society")
async def parse_society(req: ParseRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    try:
        result = get_society_chain().invoke({
            "text": req.text,
            "format_instructions": society_parser.get_format_instructions(),
        })
        return result.model_dump()
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
