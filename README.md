# LangGraphTemplateValidator

LangGraphTemplateValidator is a Python project designed to validate automation templates for business processes such as team rosters, invoices, meeting minutes, purchase orders, and expense reports. It leverages modular agents and tools to ensure templates meet required standards and formats.

## Features
- Modular agentic system for template validation
- Multiple validation tools for different template types
- Detailed error reporting for template issues
- Easily extensible for new template types

## Project Structure

```
LangGraphTemplateValidator/
├── agentic_system/
│   ├── __init__.py
│   ├── subagents.py
│   ├── supervisor_agent.py
│   └── template_validation_tools/
│       ├── __init__.py
│       └── validation_tools.py
├── ai_models/
│   ├── __init__.py
│   └── models.py
├── data_models/
│   ├── __init__.py
│   └── agent_data_models.py
├── pyproject.toml
└── README.md
```

## Installation
1. Clone the repository:
	```
	git clone <repo-url>
	cd LangGraphTemplateValidator
	```
2. Create and activate a virtual environment:
	```
	python -m venv .venv
	.venv\Scripts\activate  # On Windows
	```
3. Install dependencies:
	```
	pip install -e .
	```

## Usage
You can use the validation tools to check templates for common errors. Example usage:

```python
from template_validation_tools.validation_tools import validate_template_team_roster

result = validate_template_team_roster("https://example.com/team_roster_template")
print(result)
```

## Example Validation Tools
- `validate_template_team_roster(template_url)`
- `validate_template_invoice(template_url)`
- `validate_template_meeting_minutes(template_url)`
- `validate_template_purchase_order(template_url)`
- `validate_template_expense_report(template_url)`

Each tool returns a JSON response indicating validity and detailed error messages if validation fails.

## Extending
To add new validation tools, create a new function in `template_validation_tools/validation_tools.py` and decorate it with `@tool`.

## License
MIT License

## Contact
For questions or contributions, please open an issue or submit a pull request.

## Credit
Tuhin Karmakar 