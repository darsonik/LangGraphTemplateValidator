from langchain.agents import create_agent
from ai_models.models import chat_llm
from data_models.agent_data_models import AutomationClassificationAgentResponse, ValidationToolResponse
from template_validation_tools.validation_tools import validate_template_team_roster, validate_template_invoice, validate_template_meeting_minutes,validate_template_expense_report, validate_template_purchase_order
from langchain_core.tools import tool

# Ideally this metadata would be fetched from a database or external source
AUTOMATION_METADATA = {
    "Roster Automation": "Automates the process of updating and managing team rosters.",
    "Invoice Processing": "Handles the generation, sending, and tracking of invoices.",
    "Meeting Minutes Automation": "Automates the recording and distribution of meeting minutes.",
    "Purchase Order Processing": "Automates the creation, approval, and tracking of purchase orders.",
    "Expense Report Automation": "Automates the submission, approval, and reimbursement of expense reports."
}

AutomationClassificationAgentPrompt = """
You are an expert automation classification agent.
Refer to the following automation metadata to classify the given automation name:
{metadata} 
"""

AutomationClassificationAgent = create_agent(
    name="AutomationClassificationAgent",
    model=chat_llm,
    system_prompt=AutomationClassificationAgentPrompt.format(metadata="\n".join(f"{name}: {desc}" for name, desc in AUTOMATION_METADATA.items())),
    response_format=AutomationClassificationAgentResponse
)

# #testing
# automation = AutomationClassificationAgentInput(automation_name="Track Invoices")
# results =  AutomationClassificationAgent.invoke({
#         "messages": [{"role": "user", "content": automation.automation_name}]
#     })
# print(results["structured_response"].automation_classification)  

AutomationTemplateValidatorAgent = create_agent(
    name="AutomationTemplateValidatorAgent",
    model = chat_llm,
    tools = [validate_template_team_roster, 
             validate_template_invoice, 
             validate_template_meeting_minutes,
             validate_template_purchase_order,
             validate_template_expense_report],
    response_format=ValidationToolResponse,
    system_prompt="Use the appropriate tool to validate the given automation template based on its classification."
)

# results = AutomationTemplateValidatorAgent.invoke({
#     "messages": [{"role": "user", "content": "Invoice Processing"}]
# })
# print(results["structured_response"])

@tool
def classify_automation(automation_name: str) -> str:   
    '''Function to classify automation using the AutomationClassificationAgent
    Use this function to get the classification of an automation based on its name.'''
   
    result = AutomationClassificationAgent.invoke({
        "messages": [{"role": "user", "content": automation_name}]
    })
    return result["structured_response"]

@tool
def validate_automation_template(template_url: str, automation_classification: str) -> ValidationToolResponse:
    '''Function to validate automation template using the AutomationTemplateValidatorAgent.
    Use this function to validate the template URL based on the automation classification.'''
    result = AutomationTemplateValidatorAgent.invoke({
        "messages": [{"role": "user", "content": automation_classification}]
    })
    return result["structured_response"]
