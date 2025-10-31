# Quick Start Guide: LangGraphTemplateValidator

This guide will help you set up and run the Supervisor Agent for automation template validation.

## Prerequisites
- Python 3.14+
- Git

1. **Clone the repository:**
    ```
    git clone <repo-url>
    cd LangGraphTemplateValidator
    ```
2. **Create and activate a virtual environment:**
    ```
    python -m venv .venv
    .venv\Scripts\activate  # On Windows
    ```
3. **Install dependencies with UV:**
    ```
    uv sync
    ```

## Running the Supervisor Agent

The Supervisor Agent oversees the automation template validation process. It classifies and validates templates using subagents.

### Example Usage

```python
from agentic_system.supervisor_agent import supervisor_agent, ServicenowToModel

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
```

## Next Steps
- Explore `agentic_system/subagents.py` for more agent tools
- Customize validation logic in `template_validation_tools/validation_tools.py`
- See `README.md` for full documentation

## Support
For issues or questions, open an issue or submit a pull request on GitHub.
