# Import the Streamlit library
import streamlit as st

# Define the main function to create the app
def main():
    # Create a button to show the message
    if st.button("Show"):
        st.write("Hello World!")

# Run the app
if __name__ == "__main__":
    main()
