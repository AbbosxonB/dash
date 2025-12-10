import openpyxl

def generate_sample_excel(filename="sample_test_import.xlsx"):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Tests and Questions"

    # Define headers
    headers = [
        "Test Name",
        "Duration (minutes)",
        "Description",
        "Question Text",
        "Option A",
        "Option B",
        "Option C",
        "Option D",
        "Correct Answer",
        "Points",
    ]
    sheet.append(headers)

    # Sample data
    sample_data = [
        {
            "Test Name": "Mathematics Test 1",
            "Duration (minutes)": 60,
            "Description": "Basic algebra and geometry questions.",
            "Question Text": "What is 2 + 2?",
            "Option A": "3",
            "Option B": "4",
            "Option C": "5",
            "Option D": "6",
            "Correct Answer": "B",
            "Points": 10,
        },
        {
            "Test Name": "Mathematics Test 1",
            "Duration (minutes)": 60,
            "Description": "Basic algebra and geometry questions.",
            "Question Text": "What is the capital of France?",
            "Option A": "London",
            "Option B": "Berlin",
            "Option C": "Paris",
            "Option D": "Rome",
            "Correct Answer": "C",
            "Points": 15,
        },
        {
            "Test Name": "Physics Quiz",
            "Duration (minutes)": 30,
            "Description": "Fundamental physics concepts.",
            "Question Text": "What is the SI unit of force?",
            "Option A": "Joule",
            "Option B": "Watt",
            "Option C": "Newton",
            "Option D": "Pascal",
            "Correct Answer": "C",
            "Points": 12,
        },
    ]

    for row_data in sample_data:
        row = [row_data[header] for header in headers]
        sheet.append(row)

    workbook.save(filename)
    print(f"Sample Excel file '{filename}' generated successfully.")

if __name__ == "__main__":
    generate_sample_excel()
