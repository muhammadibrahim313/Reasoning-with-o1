import streamlit as st
import os
import tempfile
from file_processor import process_file
from report_generator import generate_report, save_report_as_pdf
from llm_setup import setup_cerebras_client, setup_openai_client, summarize_with_llama, analyze_with_openai

def main():
    st.title("Document Liability Analysis")

    # File upload
    uploaded_files = st.file_uploader("Choose files", type=["pdf", "doc", "docx", "jpg", "jpeg", "png", "bmp", "tiff", "heic", "pptx", "xlsx"], accept_multiple_files=True)

    if uploaded_files:
        # Set up LLM clients
        cerebras_client = setup_cerebras_client()
        openai_client = setup_openai_client()

        for uploaded_file in uploaded_files:
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

                # Analyze with OpenAI
                analysis = analyze_with_openai(openai_client, [f"Summary of {uploaded_file.name}:\n{summary}"])

                # Generate and display report
                report = generate_report(uploaded_file.name, summary, analysis)
                st.markdown(report)

                # Option to save as PDF
                if st.button(f"Save {uploaded_file.name} as PDF"):
                    pdf_path = save_report_as_pdf(report)
                    st.success(f"Report saved as PDF: {pdf_path}")
                    with open(pdf_path, "rb") as pdf_file:
                        st.download_button(
                            label=f"Download {uploaded_file.name} PDF",
                            data=pdf_file,
                            file_name=f"liability_analysis_report_{uploaded_file.name}.pdf",
                            mime="application/pdf"
                        )

            except Exception as e:
                st.error(f"An error occurred while processing {uploaded_file.name}: {str(e)}")

            finally:
                # Clean up the temporary file
                os.unlink(tmp_file_path)

        st.success("All files processed successfully!")

if __name__ == "__main__":
    main()