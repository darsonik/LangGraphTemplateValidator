from pydantic import BaseModel, Field
from typing import Optional,List,Dict,Literal

class ServicenowToModel(BaseModel):
    '''This is the information the AI model will receive from ServiceNow Ticketing System'''
    ticket_number: str = Field(..., description="The unique identifier for the ServiceNow ticket.")
    automation_name: str = Field(..., description="The name of the automation associated with the ticket.")
    status: str = Field(..., description="The current status of the ticket.")
    requested_by: str = Field(..., description="The user who requested the ticket.")
    template_urls: Optional[List[str]] = Field(None, description="List of attachment URLs associated with the ticket.")

class AutomationClassificationAgentResponse(BaseModel):
    '''This is the response from the Automation Classification Agent'''
    automation_classification: str = Field(..., description="Classification assigned to the automation template.")

class ModelToServicenow(BaseModel):
    '''This is the information the AI model will send back to ServiceNow Ticketing System'''
    ticket_number: str = Field(..., description="The unique identifier for the ServiceNow ticket.")
    is_template_valid: bool = Field(..., description="Indicates whether the template is valid or not.")
    validation_errors: Optional[Dict[str, str]] = Field(None, description="A dictionary containing any validation errors found in the template.")
    recommendations: Optional[List[str]] = Field(None, description="A list of recommendations for improving the template or addressing issues found during validation.")
    stop_workflow: bool = Field(..., description="Indicates whether to stop the workflow based on validation results.")
    automation_classification: AutomationClassificationAgentResponse | None = Field(None, description="The classification assigned to the automation template by the Automation Classification Agent.")

class ValidationToolResponse(BaseModel):
    '''This is the response from each validation tool'''
    tool_name: str = Field(..., description="The name of the validation tool.")
    is_valid: bool = Field(..., description="Indicates whether the template passed the validation check.")
    error_message: Optional[str] = Field(None, description="An error message if the template did not pass validation.")