import pandas as pd

merged_csv_path = 'new_skills_data_merged.csv'
merged_df = pd.read_csv(merged_csv_path)

m_skill_type = pd.read_csv('mappings/m_skill_type.csv')
m_skill = pd.read_csv('mappings/m_skill.csv')
m_emp_id = pd.read_csv('mappings/m_emp_id.csv')

# Replace 'Miscellaneous' with 'Programming_languages' in the category column
merged_df['category'] = merged_df['category'].replace('Miscellaneous', 'Programming_languages')

# Normalize the case of columns for case-insensitive mapping
merged_df['name_lower'] = merged_df['name'].str.lower()
merged_df['category_lower'] = merged_df['category'].str.lower()
merged_df['skill_lower'] = merged_df['skill'].str.lower()

m_emp_id['Employee Name Lower'] = m_emp_id['Employee Name'].str.lower()
m_skill_type['Skill Type Name Lower'] = m_skill_type['Skill Type'].str.lower()
m_skill['Skill Name Lower'] = m_skill['Skill Name'].str.lower()

# Map names to IDs using the lowercased columns
merged_df['Employee ID'] = merged_df['name_lower'].map(m_emp_id.set_index('Employee Name Lower')['Emp ID'])
merged_df['Skill Type ID'] = merged_df['category_lower'].map(m_skill_type.set_index('Skill Type Name Lower')['ID'])
merged_df['Skill Name'] = merged_df['skill_lower'].map(m_skill.set_index('Skill Name Lower')['ID'])

unmapped_employee_ids = merged_df[merged_df['Employee ID'].isna()][['name']].drop_duplicates()
unmapped_skill_type_ids = merged_df[merged_df['Skill Type ID'].isna()][['category']].drop_duplicates()
unmapped_skill_names = merged_df[merged_df['Skill Name'].isna()][['skill']].drop_duplicates()

if not unmapped_employee_ids.empty:
    print("\nUnmapped Employee Names (unique values):")
    print(unmapped_employee_ids.to_string(index=False))
    raise ValueError("Some employee names could not be mapped to IDs.")

if not unmapped_skill_type_ids.empty:
    print("\nUnmapped Skill Type Names (unique values):")
    print(unmapped_skill_type_ids.to_string(index=False))
    raise ValueError("Some categories could not be mapped to Skill Type IDs.")

if not unmapped_skill_names.empty:
    print("\nUnmapped Skill Names (unique values):")
    print(unmapped_skill_names.to_string(index=False))
    raise ValueError("Some skills could not be mapped to Skill IDs.")

merged_df['Start Date'] = '02/03/2023'
merged_df['End Date'] = '31/12/9999'
merged_df['Expertise'] = 1
merged_df['Experience'] = 1

final_df = merged_df[['Start Date', 'End Date', 'Employee ID', 'Skill Type ID', 'Skill Name', 'Expertise', 'Experience']]

output_excel_path = 'data/new_skills_data_for_prima.xlsx'
final_df.to_excel(output_excel_path, index=False, sheet_name='Mapped Data')

print(f"Excel workbook created: {output_excel_path}")