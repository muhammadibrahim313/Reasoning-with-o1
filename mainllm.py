import sys
import os
from dotenv import load_dotenv
from file_detector import process_file
from llmsetup import setup_cerebras_client, setup_openai_client, summarize_with_llama, analyze_with_openai

# Load environment variables from .env file
load_dotenv()

def main():
    if len(sys.argv) < 2:
        print("Usage: python mainllm.py <directory_path>")
        sys.exit(1)

    directory_path = sys.argv[1]

    if not os.path.isdir(directory_path):
        print(f"The specified path {directory_path} is not a directory.")
        sys.exit(1)

    # Setup LLM clients
    cerebras_client = setup_cerebras_client()
    openai_client = setup_openai_client()

    summaries = []

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            try:
                print(f"\nProcessing {filename}...")
                extracted_text = process_file(file_path)
                
                # Summarize with LLaMA 3.1 70B
                summary = summarize_with_llama(cerebras_client, extracted_text)
                summaries.append(f"Summary of {filename}:\n{summary}")
                
                print(f"Processed and summarized {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

    if summaries:
        final_report = analyze_with_openai(openai_client, summaries)
        
        # Save the final report
        report_path = os.path.join(os.path.dirname(__file__), "liability_analysis_report.txt")
        with open(report_path, "w", encoding="utf-8") as report_file:
            report_file.write(final_report)
        
        print(f"\nLiability analysis report has been saved to: {report_path}")
    else:
        print("No files were successfully processed and summarized.")

if __name__ == "__main__":
    main()