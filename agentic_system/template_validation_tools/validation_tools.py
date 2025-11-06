from langchain_core.tools import tool
from agentic_system.data_models.agent_data_models import ModelToServicenow, ValidationToolResponse

@tool
def validate_template_team_roster(template_url: str) -> ValidationToolResponse:
    '''Use this tool to validate team roster automation templates.'''
    # Implement your template validation logic here
    # Example: Simulate a missing field error
    return ValidationToolResponse(
        tool_name="Team Roster Validator",
        is_valid=False,
        error_message="Validation failed: 'team_lead' field missing in template at {}.".format(template_url)
    ).model_dump_json()

@tool
def validate_template_invoice(template_url: str) -> ValidationToolResponse:
    '''Use this tool to validate invoice automation templates.'''
    # Implement your template validation logic here
    # Example: Simulate a formatting error
    return ValidationToolResponse(
        tool_name="Invoice Validator",
        is_valid=False,
        error_message="Validation failed: Invoice number format incorrect in template at {}. Expected format: INV-YYYYMMDD.".format(template_url)
    ).model_dump_json()

@tool
def validate_template_meeting_minutes(template_url: str) -> ValidationToolResponse:
    '''Use this tool to validate meeting minutes automation templates.'''
    # Implement your template validation logic here
    return ValidationToolResponse(
        tool_name="Meeting Minutes Validator",
        is_valid=False,
        error_message="Validation failed: The template at {} is missing the 'Attendees' section and does not specify meeting date.".format(template_url)
    ).model_dump_json()
@tool
def validate_template_purchase_order(template_url: str) -> ValidationToolResponse:
    '''Use this tool to validate purchase order automation templates.'''
    # Example: Simulate a missing approval signature
    return ValidationToolResponse(
        tool_name="Purchase Order Validator",
        is_valid=False,
        error_message="Validation failed: 'approval_signature' missing in purchase order template at {}.".format(template_url)
    ).model_dump_json()

@tool
def validate_template_expense_report(template_url: str) -> ValidationToolResponse:
    '''Use this tool to validate expense report automation templates.'''
    # Example: Simulate a missing total amount
    return ValidationToolResponse(
        tool_name="Expense Report Validator",
        is_valid=False,
        error_message="Validation failed: 'total_amount' field missing in expense report template at {}.".format(template_url)
    ).model_dump_json()