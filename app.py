import streamlit as st                  
import pandas as pd 
import io
from src.college_predictor.clg_selector import filter_colleges



def display_results(user_name, filtered_colleges,rank, selected_districts,selected_branches):
    
    st.header("Filtered Engineering Colleges Based on Your Input:")
    if user_name:
        st.write(f"Hi {user_name}, here are the engineering colleges that match your preferences:")
    else:
        st.write("Here's a list of engineering colleges that match your search criteria:")

    

    st.write(f"Based on your rank of {rank}, preferred districts of {', '.join(selected_districts)}, and desired branches of {', '.join(selected_branches)}, we found {len(filtered_colleges)} colleges that might be a good fit for you. Best of luck with your college search!! 😃👍")
    
    st.markdown("""
<span style="color:red;">Note: The list of colleges is presented in ALPHABETICAL ORDER ONLY and NOT by college ranking. Please keep this in mind.</span>
""", unsafe_allow_html=True)
    
    if filtered_colleges.empty:
        st.write("No colleges match your criteria. Please adjust your filters and try again.")
    else:
        st.dataframe(filtered_colleges)
       # Create a function to convert the DataFrame to Excel
        def to_excel(df):
            output = io.BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df.to_excel(writer, index=False, sheet_name='Filtered_Colleges')
            writer.save()
            processed_data = output.getvalue()
            return processed_data

        # Provide a download button for the Excel file
        excel_data = to_excel(filtered_colleges)
        st.download_button(label='Download Excel file',
                        data=excel_data,
                        file_name='filtered_colleges.xlsx',
                        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


def main():
    

    st.title("AP EAPCET 2024 College Selector")
    st.subheader("Based on 2022-23 Ranking Cutoff ")


    college_data = pd.read_excel("APEAPCET_Cleaned_data.xlsx") 

    if college_data is not None:
        columns = college_data.columns
    else:
        st.error("Error: College data file not found. Please ensure the file exists.")
    
    category = list(columns[9:27])
    user_name = st.session_state.get("user_name", None)
    eamcet_rank = st.number_input("Enter you Eamcet Rank", min_value=1)

    districts = sorted(college_data['DIST'].unique().tolist())
    branches = sorted(college_data['branch_code'].unique().tolist())
    category = sorted(category)


    # Multi-select widgets for districts and branches
    selected_districts = st.multiselect("Select Preferred Districts:", districts)
    selected_branches = st.multiselect("Select Preferred Branches:", branches)
    # selected_category = st.radio("Choose your Category:", category)

    selected_category = st.selectbox("Choose your Category:", category)

    # Hide selected option
    with st.empty():
        if selected_category:  # Check if an option is selected
            st.write(selected_category)  # Display the selected option (hidden)

    if st.button("Submit"):
        filtered_colleges = filter_colleges(college_data, eamcet_rank , selected_districts, selected_category, selected_branches)
        display_results(user_name,filtered_colleges, eamcet_rank, selected_districts,selected_branches)

if __name__ == "__main__":
    main()