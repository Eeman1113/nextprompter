import streamlit as st
import os
import base64

def collect_js_files(path):
    js_files = []
    for root, dirs, files in os.walk(path):
        if 'node_modules' in dirs:
            dirs.remove('node_modules')  # don't visit node_modules directories
        for file in files:
            if file.endswith('.js'):
                js_files.append(os.path.join(root, file))
    return js_files

def create_output_file(selected_files, project_path, user_prompt):
    output = f"// User Prompt:\n{user_prompt}\n\n"
    for file_path in selected_files:
        relative_path = os.path.relpath(file_path, start=project_path)
        output += f"// File: {relative_path}\n"
        with open(file_path, 'r', encoding='utf-8') as js_file:
            output += js_file.read()
        output += "\n\n"
    return output

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href

st.set_page_config(page_title="Nextprompter", page_icon="📁")

st.title("次のプロンプター")
st.write("This app allows you to select a Next.js project directory, choose specific .js files (excluding node_modules), add a custom prompt, and create a formatted output file.")

# Input for project path
project_path = st.text_input("Enter the path to your Next.js project:")

if project_path:
    # Collect .js files
    js_files = collect_js_files(project_path)
    
    if not js_files:
        st.warning("No .js files found in the specified directory (excluding node_modules).")
    else:
        st.success(f"Found {len(js_files)} .js files (excluding node_modules).")
        
        # Let user select files
        selected_files = st.multiselect("Select .js files to include:", js_files)
        
        if selected_files:
            # Let user add a custom prompt
            user_prompt = st.text_area("Enter your custom prompt:", height=100)
            
            # Create output file
            output_content = create_output_file(selected_files, project_path, user_prompt)
            
            # Display preview
            st.subheader("Preview of output file:")
            st.text_area("Content", output_content, height=300)
            
            # Offer download
            if st.button("Generate Output File"):
                output_file = "nextjs_files_output.txt"
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(output_content)
                st.markdown(get_binary_file_downloader_html(output_file, 'Output File'), unsafe_allow_html=True)
                st.success("Output file generated successfully!")

st.sidebar.title("About")
st.sidebar.info(
    "This app collects .js files from a Next.js project "
    "(excluding the node_modules folder), "
    "allows you to select specific files, add a custom prompt, "
    "and generates a formatted output file with the contents of the selected files."
)
