import pandas as pd      

def load_data():
    """Loads college data from a CSV file (replace with your actual data source).

    Returns:
        pd.DataFrame: The loaded college data.
    """

    try:
        df = pd.read_excel("APEAPCET_Cleaned_data.xlsx")  # Replace with your file path
        return df
    except FileNotFoundError:
        return None
    
def filter_colleges(df, rank, districts, category,branches):
   
    filtered_df = df.copy() 

    filtered_df = filtered_df[filtered_df[category] >= rank]

   
    if districts:
        filtered_df = filtered_df[filtered_df['DIST'].isin(districts)]

    if branches:
        filtered_df = filtered_df[filtered_df['branch_code'].isin(branches)]

    filtered_df['COLLFEE'] = filtered_df['COLLFEE'].apply(lambda x: f"₹{x:,.2f}")

    filtered_df = filtered_df.sort_values(by="inst_name")
    filtered_df['S.No'] = range(1, len(filtered_df) + 1)
    selected_columns = ['S.No'] + ["inst_code", "inst_name", "INST_REG","DIST" ,"PLACE", "AFFLIA\n.UNIV","branch_code",category, "COLLFEE"]
    filtered_df = filtered_df[selected_columns]
    
    new_col_names = {"inst_code": "Institution Code", "inst_name": "Institution Name", "branch_code": "Branch Code","COLLFEE": "College Fee", category : "Last Year Cutoff" }
    filtered_df = filtered_df.rename(columns= new_col_names)
    


    
    return filtered_df



# if __name__=="__main__":
#     data = load_data()
#     columns = data.columns
#     category = list(columns[9:27])
#     print(category)