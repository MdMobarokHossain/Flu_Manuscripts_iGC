import pandas as pd

# Load the Excel file
file_path = '/parvej/data/MEGA-H3N2.xlsx'
df = pd.read_excel(file_path)

# Display the first few rows of the dataframe to understand its structure
df.head()
# Melting the dataframe to long format
df_melted = df.melt(id_vars=[df.columns[0]], var_name='id2', value_name='Distance')

# Renaming the columns to match the requested output
df_melted.rename(columns={df_melted.columns[0]: 'id1'}, inplace=True)

# Function to determine region based on id
def determine_region(id_name):
    if id_name.startswith('Bangladesh'):
        return 'Bangladesh'
    elif id_name.startswith('EPI_ISL_'):
        return 'Vaccine'
    else:
        return 'NH'

# Applying the function to determine regions for id1 and id2
df_melted['id1_region'] = df_melted['id1'].apply(determine_region)
df_melted['id2_region'] = df_melted['id2'].apply(determine_region)

# Reordering columns to match the requested output
df_output = df_melted[['id1', 'id2', 'Distance', 'id1_region', 'id2_region']]

# Filtering out NaN distances (self-self comparisons)
df_output = df_output.dropna(subset=['Distance'])

# Resetting index for cleaner output
df_output.reset_index(drop=True, inplace=True)

# Display the transformed dataframe
df_output.head()
import matplotlib.pyplot as plt
import seaborn as sns

# Create a new column for the pair categories based on regions
def categorize_pairs(row):
    pair_set = {row['id1_region'], row['id2_region']}
    if pair_set == {'NH', 'Bangladesh'}:
        return 'NH-Bangladesh'
    elif pair_set == {'NH', 'Vaccine'}:
        return 'NH-Vaccine'
    elif pair_set == {'Bangladesh', 'Vaccine'}:
        return 'Bangladesh-Vaccine'
    else:
        return 'Other'

df_output['pair_category'] = df_output.apply(categorize_pairs, axis=1)

# Filter out the 'Other' category as it's not requested for the boxplot
df_boxplot_data = df_output[df_output['pair_category'] != 'Other']

# Plotting the boxplot
plt.figure(figsize=(10, 6))
sns.boxplot(x='pair_category', y='Distance', data=df_boxplot_data)
plt.title('Boxplot of Genetic Distance for Different Region Pairs')
plt.ylabel('Genetic Distance')
plt.xlabel('Region Pair')
plt.show()
