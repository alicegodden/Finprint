import streamlit as st
import os

def load_dna_file(file):
    """Load the contents of the DNA file with error handling."""
    try:
        return file.read().decode("utf-8")
    except UnicodeDecodeError:
        try:
            return file.read().decode("ISO-8859-1")
        except Exception as e:
            st.error(f"Error reading file {file.name}: {e}")
            return None

def highlight_matches(content, pattern):
    """Highlight matches of the pattern in the content."""
    if pattern:
        highlighted_content = content.replace(pattern, f"<span style='background-color: yellow; font-weight: bold; color: black;'>{pattern}</span>")
        return highlighted_content
    return content

# Set page configuration
st.set_page_config(page_title="FinPrint", layout="wide")

# Custom CSS
st.markdown("""
    <style>
        .main {
            background-color: #f0f0f0;  /* Light gray background */
            background-image: url('fish.jpg');  /* Background image */
            background-repeat: no-repeat;
            background-size: 150px;  /* Adjust size of the zebrafish icon */
            background-position: right top;  /* Position the icon */
            padding: 2rem;
        }
        h1 {
            color: #0056b3;  /* Blue color */
        }
        h2 {
            color: #ff7f50;  /* Coral color (orange) */
        }
        .success {
            color: #28a745;  /* Green color for success messages */
        }
        .warning {
            color: #dc3545;  /* Red color for warning messages */
        }
    </style>
""", unsafe_allow_html=True)

# Title and Introduction
st.title("FinPrint")
st.markdown("""
Welcome to **FinPrint**! This application allows you to upload your DNA sequencing files and search for specific patterns. 
Simply upload your `.dna` and `.seq` files below and enter the pattern you want to find. Matches will be highlighted for your convenience. Currently
            optimised for insertion or deletions where a pattern can be recognised.
            Heterozygous chromatograms as input will be a new feature in the future!
""")

# Sidebar for user inputs
st.sidebar.header("User Inputs")
uploaded_files = st.sidebar.file_uploader("Upload DNA files (.dna or .seq)", type=["dna", "seq"], accept_multiple_files=True)
search_pattern = st.sidebar.text_input("Enter the pattern to search for:").lower()  # Convert input to lowercase

# Main area for displaying results
if uploaded_files:
    st.markdown("### Results")
    for uploaded_file in uploaded_files:
        dna_content = load_dna_file(uploaded_file)
        
        if dna_content is None:
            continue  # Skip if there's an error
        
        # Convert content to lowercase for comparison
        dna_content_lower = dna_content.lower()

        st.subheader(f"File: {uploaded_file.name}")

        # Highlight matches and display results
        if search_pattern:
            if search_pattern in dna_content_lower:
                st.markdown(highlight_matches(dna_content, search_pattern), unsafe_allow_html=True)
                st.success("It's a match!")
            else:
                st.write(dna_content)
                st.warning("No match found.")
        else:
            st.write(dna_content)  # Show file content if no search pattern is specified

# Adding spacing for better layout
st.write("\n" * 2)  # Adds extra space at the bottom of the app
