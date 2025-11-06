from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import logging

# Import your existing modules
from langchain.agents import create_agent
from agentic_system.ai_models.models import chat_llm
from agentic_system.data_models.agent_data_models import ModelToServicenow, ServicenowToModel
from agentic_system.supervisor_agent import supervisor_agent

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

