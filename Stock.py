import pandas as pd
import streamlit as st
from datetime import datetime

def add_item(unique_key, checked_by):
    item = st.text_input("Enter last 4 digits of Barcode:", key=f"item_name{unique_key}")
    item_data = pd.DataFrame(columns=["Item", "Quantity", "Use By", "Checked By"])

    while item:
        # Ask for Quantity
        quantity = st.number_input(f"Enter the Quantity for {item}:", value=0, step=1, key=f"item_qty{unique_key}")

        # Ask for Use By date
        use_by_date = st.date_input(f"Select Use By Date for {item}:", key=f"item_date{unique_key}")

        # Create a new DataFrame with the item data
        new_data = pd.DataFrame({
            "Item": [item],
            "Quantity": [quantity],
            "Use By": [use_by_date],
            "Checked By": [checked_by]
        })

        item_data = pd.concat([item_data, new_data], ignore_index=True)

        if not st.checkbox('Do you have more of this item with a different Use By date?', key=f'add_more{unique_key}'):
            break

        unique_key += 1

    return item_data, unique_key

def main():
    st.title("Stock Take App")

    # Ask for user's name
    checked_by = st.text_input("Enter your name:", "")

    # Initialize an empty DataFrame to accumulate new data
    data = pd.DataFrame(columns=["Item", "Quantity", "Use By", "Checked By"])

    unique_key = 0
    while True:
        item_data, unique_key = add_item(unique_key, checked_by)
        data = pd.concat([data, item_data], ignore_index=True)

        if not st.checkbox('Add new Item?', key=f'add_another_item{unique_key}'):
            break

        unique_key += 1

    # Display the final DataFrame
    st.dataframe(data)

    # Provide a button to save the DataFrame as a CSV
    if st.button("Save Data"):
        # Get current date and time and format it in a file-friendly format
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Use the timestamp to create a unique filename for each CSV
        filename = f"C:/Users/liamh/OneDrive/Desktop/Stock_{timestamp}.csv"

        # Save the accumulated DataFrame to a CSV file when finished
        data.to_csv(filename, index=False)
        st.success(f"Data saved successfully! Filename: {filename}")

if __name__ == "__main__":
    main()

