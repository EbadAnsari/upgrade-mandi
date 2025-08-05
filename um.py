from inquirer import List, prompt

from PDF import PDF

menu = [
    List(
        "operation",
        message="Select operation",
        choices=["Invoice (PDF)", "Generate Report"],
    )
]

# operation = prompt(menu)["operation"]

# if operation == "Invoice (PDF)":
#     pass
# elif operation == "Generate Report":
#     pass
