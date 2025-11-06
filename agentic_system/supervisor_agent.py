
# Import necessary modules and models
from langchain.agents import create_agent
from agentic_system.ai_models.models import chat_llm
from agentic_system.data_models.agent_data_models import ModelToServicenow, ServicenowToModel
from agentic_system.subagents import classify_automation, validate_automation_template


# System prompt for the Supervisor Agent, describing its responsibilities and workflow
supervisor_agent_prompt = """
You are the Supervisor Agent overseeing the automation template validation process.
Your role is to ensure that all automation templates are properly classified and validated before deployment.
You will be working with the AutomationClassificationAgent and AutomationTemplateValidatorAgent to achieve this.
First classify the automation using the classify_automation tool, then validate the template using the validate_automation_template tool.
"""


# Create the Supervisor Agent with the specified prompt, tools, and response format
supervisor_agent = create_agent(
    name="SupervisorAgent",
    model=chat_llm,
    system_prompt=supervisor_agent_prompt,
    tools=[classify_automation, validate_automation_template],
    response_format=ModelToServicenow
)


# # Example: Creating a state object and invoking the Supervisor Agent
# state = ServicenowToModel(
#     ticket_number="INC123456",
#     automation_name="Purchase Order Processing for Vendor X",
#     status="Open",
#     requested_by="john.doe@example.com",
#     template_urls=["http://example.com/template1"]
# )

# # Pass the state information to the agent via a user message
# result = supervisor_agent.invoke({
#     "messages": [{
#         "role": "user",
#         "content": (
#             f"Please process the following ticket:\n"
#             f"Ticket Number: {state.ticket_number}\n"
#             f"Automation Name: {state.automation_name}\n"
#             f"Status: {state.status}\n"
#             f"Requested By: {state.requested_by}\n"
#             f"Template URLs: {', '.join(state.template_urls)}"
#         )
#     }]
# })

# # Print the structured response from the Supervisor Agent
# print(result["structured_response"])