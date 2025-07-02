from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date, timedelta
from app.agent import create_agent_executor
from app.calendar_tools import check_calendar_availability

app = FastAPI(
    title="Calendo API",
    description="API for the conversational booking agent.",
    version="1.0.0"
)

agent_executor = create_agent_executor()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """Receives a user message and returns the agent's reply."""
    today = date.today().strftime("%Y-%m-%d")
    response = agent_executor.invoke({
        "input": request.message,
        "today": today
    })
    return ChatResponse(reply=response['output'])

@app.get("/slots")
async def get_slots():
    """Returns available slots for today and tomorrow."""
    today = date.today()
    tomorrow = today + timedelta(days=1)
    
    today_str = today.strftime("%Y-%m-%d")
    tomorrow_str = tomorrow.strftime("%Y-%m-%d")

    slots_today = check_calendar_availability.run(today_str)
    slots_tomorrow = check_calendar_availability.run(tomorrow_str)

    return {"tomorrow": slots_tomorrow}


@app.get("/")
def read_root():
    return {"message": "Welcome to the Calendo API"}