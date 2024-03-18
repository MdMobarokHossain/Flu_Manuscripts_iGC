# Load the new Excel file with the correct format
new_excel_path = '/parvej/data/Mega_H1N1.xlsx'
data_corrected = pd.read_excel(new_excel_path)

# Display the first few rows of the dataframe to understand its structure
data_corrected.head()

# Transform the matrix into a long-format dataframe
melted_data = data_corrected.melt(id_vars=[data_corrected.columns[0]], 
                                  var_name='id2', 
                                  value_name='Distance')

# Rename the columns to match the requested format
melted_data.columns = ['id1', 'id2', 'Distance']

# Drop any rows where Distance is NaN, since we are only interested in actual comparisons
melted_data.dropna(subset=['Distance'], inplace=True)

# Define a function to determine the region based on the id
def determine_region(id_value):
    if id_value.startswith('Bangladesh_'):
        return 'Bangladesh'
    elif id_value.startswith('EPI_ISL_'):
        return 'Vaccine'
    else:
        return 'NH'

# Apply the function to create new 'id1_region' and 'id2_region' columns
melted_data['id1_region'] = melted_data['id1'].apply(determine_region)
melted_data['id2_region'] = melted_data['id2'].apply(determine_region)

# Display the transformed dataframe as requested
melted_data.reset_index(drop=True, inplace=True)
melted_data.head()

# Save the transformed dataframe to a new Excel file
output_excel_path = '/parvej/data/Transformed_MEGA_H1N1_Distances.xlsx'
melted_data.to_excel(output_excel_path, index=False)

output_excel_path
import matplotlib.pyplot as plt
import seaborn as sns

# Create a new column 'Comparison' based on the regions of id1 and id2
melted_data['Comparison'] = melted_data.apply(lambda x: f"{x['id1_region']} and {x['id2_region']}", axis=1)

# Filter out the data for comparisons of interest
filtered_data = melted_data[
    melted_data['Comparison'].isin(['NH and Bangladesh', 'NH and Vaccine', 'Bangladesh and Vaccine'])
]

# Create the boxplot
plt.figure(figsize=(10, 6))
boxplot = sns.boxplot(x='Comparison', y='Distance', data=filtered_data)
boxplot.set_title('Genetic Distance Comparisons')
boxplot.set_xlabel('Comparison Groups')
boxplot.set_ylabel('Genetic Distance')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()



