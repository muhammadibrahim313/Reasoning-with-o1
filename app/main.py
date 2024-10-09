import streamlit as st
import os
import tempfile
from file_processor import process_file
from report_generator import generate_report, save_report_as_pdf
from llm_setup import setup_cerebras_client, setup_openai_client, summarize_with_llama, analyze_with_openai
from io import BytesIO

def main():
    st.title("Document Liability Analysis")

    if 'report' not in st.session_state:
        st.session_state.report = None
    if 'pdf_buffer' not in st.session_state:
        st.session_state.pdf_buffer = None

    # File upload
    uploaded_files = st.file_uploader("Choose files", type=["pdf", "doc", "docx", "jpg", "jpeg", "png", "bmp", "tiff", "heic", "pptx", "xlsx"], accept_multiple_files=True)

    if uploaded_files:
        # Add a "Send Files" button
        if st.button("Send Files for Analysis"):
            # Set up LLM clients
            cerebras_client = setup_cerebras_client()
            openai_client = setup_openai_client()

            all_summaries = []

            progress_bar = st.progress(0)
            for i, uploaded_file in enumerate(uploaded_files):
                st.write(f"Processing: {uploaded_file.name}")
                
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name

                try:
                    # Process the file
                    extracted_text = process_file(tmp_file_path)

                    # Summarize with LLaMA
                    summary = summarize_with_llama(cerebras_client, extracted_text)
                    all_summaries.append(f"Summary of {uploaded_file.name}:\n{summary}")

                except Exception as e:
                    st.error(f"An error occurred while processing {uploaded_file.name}: {str(e)}")

                finally:
                    # Clean up the temporary file
                    os.unlink(tmp_file_path)
                
                # Update progress bar
                progress_bar.progress((i + 1) / len(uploaded_files))

            # Analyze all summaries with OpenAI
            if all_summaries:
                st.write("Generating liability analysis...")
                analysis = analyze_with_openai(openai_client, all_summaries)

                # Generate and store report
                st.session_state.report = f"# Liability Analysis Report\n\n{analysis}"
                st.markdown(st.session_state.report)

                # Generate and store PDF
                st.session_state.pdf_buffer = save_report_as_pdf(st.session_state.report)

            st.success("All files processed successfully!")

    if st.session_state.report:
        st.markdown(st.session_state.report)

    if st.session_state.pdf_buffer:
        st.download_button(
            label="Download Liability Analysis PDF",
            data=st.session_state.pdf_buffer,
            file_name="liability_analysis_report.pdf",
            mime="application/pdf"
        )

    else:
        st.write("Please upload files to analyze.")

if __name__ == "__main__":
    main()