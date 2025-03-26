import pandas as pd

# Load the Excel workbook
workbook_path = 'mappings/Employee Skill Mapping Template.xlsx'

# Read the mapping sheets into DataFrames
m_skill_type = pd.read_excel(workbook_path, sheet_name='m_skill_type')
m_skill = pd.read_excel(workbook_path, sheet_name='m_skill')
m_emp_id = pd.read_excel(workbook_path, sheet_name='m_emp_ids')

# Save each mapping to a separate CSV file
m_skill_type.to_csv('mappings/m_skill_type.csv', index=False)
m_skill.to_csv('mappings/m_skill.csv', index=False)
m_emp_id.to_csv('mappings/m_emp_id.csv', index=False)

print("Mappings extracted and saved as CSV files:")
print("- m_skill_type.csv")
print("- m_skill.csv")
print("- m_emp_id.csv")