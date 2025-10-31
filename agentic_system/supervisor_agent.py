from langchain.agents import create_agent
from ai_models.models import chat_llm
from data_models.agent_data_models import ModelToServicenow
from data_models.agent_data_models import ServicenowToModel
from subagents import classify_automation, validate_automation_template

supervisor_agent_prompt = """
You are the Supervisor Agent overseeing the automation template validation process.
Your role is to ensure that all automation templates are properly classified and validated before deployment.
You will be working with the AutomationClassificationAgent and AutomationTemplateValidatorAgent to achieve this.
First classify the automation using the classify_automation tool, then validate the template using the validate_automation_template tool.
"""

supervisor_agent = create_agent(
    name="SupervisorAgent",
    model=chat_llm,
    system_prompt=supervisor_agent_prompt,
    tools=[classify_automation, validate_automation_template],
    response_format=ModelToServicenow
)

# Example of passing state when invoking:

state = ServicenowToModel(
    ticket_number="INC123456",
    automation_name="Purchase Order Processing for Vendor X",
    status="Open",
    requested_by="john.doe@example.com",
    template_urls=["http://example.com/template1"]
)

result = supervisor_agent.invoke({
    "messages": [{
        "role": "user",
        "content": (
            f"Please process the following ticket:\n"
            f"Ticket Number: {state.ticket_number}\n"
            f"Automation Name: {state.automation_name}\n"
            f"Status: {state.status}\n"
            f"Requested By: {state.requested_by}\n"
            f"Template URLs: {', '.join(state.template_urls)}"
        )
    }]
})


print(result["structured_response"])