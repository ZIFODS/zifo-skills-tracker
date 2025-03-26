import pandas as pd

file1 = "new_skills_data.csv"
file2 = "new_skills_data_onboarding.csv"

df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

merged_df = pd.concat([df1, df2])

deduplicated_df = merged_df.drop_duplicates()

deduplicated_df.to_csv('new_skills_data_merged.csv', index=False)

print("Done.")