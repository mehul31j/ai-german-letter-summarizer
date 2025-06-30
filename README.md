# AI German Document Summarizer

A Streamlit application that uses OCR and AI to extract, summarize, and analyze documents (letters, invoices, contracts).

## Features

- **Document Processing**
  - Upload images or PDFs
  - OCR text extraction with language selection
  - Smart document classification (invoice, contract, letter)

- **Smart Analysis**
  - Document type detection
  - Interactive timeline of important dates
  - Contact information extraction
  - English summaries and key points

- **User Interface**
  - Configurable settings
  - Interactive timeline visualization
  - Contact cards with clickable links
  - Responsive design

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-letter-summarizer.git
cd ai-letter-summarizer
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the project root and add your DeepSeek API key:
```
DEEPSEEK_API_KEY=your_api_key_here
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8504`

3. Upload a German document (image or PDF)

4. Select the document language

5. Click "Analyze Document" to get:
   - Document classification
   - Timeline of important dates
   - Contact information
   - English summary
   - Key points

## Requirements

- Python 3.8+
- Tesseract OCR
- DeepSeek API key

## Project Structure

```
ai-letter-summarizer/
├── app.py                 # Main Streamlit application
├── ocr_utils.py          # OCR text extraction functions
├── summarizer.py         # Text summarization and analysis
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not in repo)
├── sample_docs/          # Sample documents for testing
└── README.md            # Project documentation
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
