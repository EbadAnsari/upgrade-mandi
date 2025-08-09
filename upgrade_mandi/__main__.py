from inquirer import List, prompt

from PDF import PDF

# Raw Sheet to Notion

# Notion to Invoice PDF
# Notion to Report PDF

menu = [
    List(
        "operation",
        message="Select operation",
        choices=["Raw Sheet to Notion", "Notion to Invoice and Report"],
    )
]

operation = prompt(menu)["operation"]

# if operation == "Invoice (PDF)":
#     pass
# elif operation == "Generate Report":
#     pass
