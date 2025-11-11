from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Any
import logging

# Import your existing modules
from langchain.agents import create_agent
from data_models.agent_data_models import ModelToServicenow, ServicenowToModel
from supervisor_agent import supervisor_agent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Automation Template Validation API",
    description="API for validating automation templates using AI agents",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model for the API
class TicketRequest(BaseModel):
    ticket_number: str = Field(..., description="ServiceNow ticket number")
    automation_name: str = Field(..., description="Name of the automation template")
    status: str = Field(default="Open", description="Current ticket status")
    requested_by: str = Field(..., description="Email of the requester")
    template_urls: List[str] = Field(..., description="URLs of automation templates")

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "ticket_number": "INC123456",
                "automation_name": "Purchase Order Processing for Vendor X",
                "status": "Open",
                "requested_by": "john.doe@example.com",
                "template_urls": ["http://example.com/template1"]
            }
        }

# Response model for the API
class TicketResponse(BaseModel):
    ticket_number: str
    result: List[Any]
    status: str = "processed"

# Health check endpoint
@app.get("/",tags=["Health"])
def health_check():
    """Health check endpoint to verify API is running. """
    return {"status": "healthy",
            "service":"Automation Template Validation API",
            "version":"1.0.0"}

# Main endpoint to process tickets
@app.post("/api/v1/process-ticket", response_model=TicketResponse, tags=["Automation"])
async def process_ticket(request: TicketRequest):
    """ Process an automation template validation ticket.
    
    This endpoint:
    1. Receives ticket information from the frontend
    2. Creates a state object from the payload
    3. Invokes the Supervisor Agent
    4. Returns the structured response"""
    try:
        state = ServicenowToModel(
        ticket_number=request.ticket_number,
        automation_name=request.automation_name,
        status=request.status,
        requested_by=request.requested_by,
        template_urls=request.template_urls)

        # Prepare the message for the agent
        user_message = (
                f"Please process the following ticket:\n"
                f"Ticket Number: {state.ticket_number}\n"
                f"Automation Name: {state.automation_name}\n"
                f"Status: {state.status}\n"
                f"Requested By: {state.requested_by}\n"
                f"Template URLs: {', '.join(state.template_urls)}"
            )

        # invoke the supervisor agent
        result = supervisor_agent.invoke({
            "messages":[{
                "role":"user",
                "content": user_message
            }]
        })

        logger.info(f"Processed ticket {request.ticket_number}")

        logger.info("user message sent to agent:")
        logger.info(user_message)
        logger.info(f"Result: {result.get('structured_response', result)}")

        return TicketResponse(
            ticket_number=request.ticket_number,
            result=[result.get("structured_response", result)],
            status="Processed",
        )
    except Exception as e:
        logger.error(f"Error processing ticket {request.ticket_number} : {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing ticket: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)