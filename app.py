import streamlit as st
import re
from datetime import datetime
import plotly.express as px
from ocr_utils import extract_text, get_available_languages, LANGUAGE_MAPPING
from summarizer import summarize_text, extract_key_points

# Initialize session state for configurations
if 'max_summary_length' not in st.session_state:
    st.session_state.max_summary_length = 150
if 'max_key_points' not in st.session_state:
    st.session_state.max_key_points = 5

def extract_dates(text):
    """Extract dates from text using various formats."""
    # German date patterns
    date_patterns = [
        r'\d{1,2}\.\s*(?:Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)\s*\d{4}',
        r'\d{1,2}\.\d{1,2}\.\d{4}',
        r'\d{4}-\d{2}-\d{2}'
    ]
    
    dates = []
    for pattern in date_patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            date_str = match.group()
            try:
                # Convert to datetime object
                if any(month in date_str for month in ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']):
                    # German month names
                    month_map = {
                        'Januar': '01', 'Februar': '02', 'März': '03', 'April': '04',
                        'Mai': '05', 'Juni': '06', 'Juli': '07', 'August': '08',
                        'September': '09', 'Oktober': '10', 'November': '11', 'Dezember': '12'
                    }
                    parts = date_str.split()
                    day = parts[0].strip('.')
                    month = month_map[parts[1]]
                    year = parts[2]
                    date_str = f"{year}-{month}-{day.zfill(2)}"
                elif '.' in date_str:
                    # DD.MM.YYYY format
                    day, month, year = date_str.split('.')
                    date_str = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                
                # Get context (50 characters before and after the date)
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end].strip()
                
                # Clean up context
                context = re.sub(r'\s+', ' ', context)  # Remove extra whitespace
                
                dates.append({
                    'date': date_obj,
                    'text': date_str,
                    'context': context
                })
            except ValueError:
                continue
    
    # Sort dates chronologically
    dates.sort(key=lambda x: x['date'])
    return dates

def extract_contact_info(text):
    """Extract contact information from text."""
    # Email pattern
    email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    # Phone pattern (German format) - improved regex
    phone_pattern = r'(\+49|0)\s*\d{2,4}\s*\d{2,4}\s*\d{2,4}'
    # IBAN pattern
    iban_pattern = r'[A-Z]{2}\s?\d{2}\s?(\d{4}\s?){2,4}\d{2,4}'
    # Name pattern (after "Sehr geehrte" or "Mit freundlichen Grüßen")
    name_pattern = r'(?:Sehr geehrte|Mit freundlichen Grüßen)[\s,]+([A-Za-zäöüßÄÖÜ\s]+)'
    
    # Clean up phone numbers
    phones = []
    for match in re.finditer(phone_pattern, text):
        phone = match.group()
        # Remove spaces and format for tel: link
        phone = re.sub(r'\s+', '', phone)
        phones.append(phone)
    
    contacts = {
        'emails': re.findall(email_pattern, text),
        'phones': phones,
        'ibans': re.findall(iban_pattern, text),
        'names': re.findall(name_pattern, text)
    }
    return contacts

def classify_document(text):
    """Classify document type based on content and extract specific fields."""
    text_lower = text.lower()
    doc_info = {'type': 'unknown', 'fields': {}}
    
    # Check for invoice indicators
    invoice_indicators = ['rechnung', 'invoice', 'betrag', 'summe', '€', 'eur']
    if any(indicator in text_lower for indicator in invoice_indicators):
        doc_info['type'] = 'invoice'
        # Extract invoice amount
        amount_match = re.search(r'(\d+[.,]\d+)\s*€', text)
        if amount_match:
            doc_info['fields']['amount'] = amount_match.group(1)
        # Extract invoice number
        inv_match = re.search(r'Rechnung\s*(?:Nr\.?|Nummer)?\s*([A-Z0-9-]+)', text, re.IGNORECASE)
        if inv_match:
            doc_info['fields']['invoice_number'] = inv_match.group(1)
    
    # Check for contract indicators
    contract_indicators = ['vertrag', 'agreement', 'vereinbarung', 'contract']
    if any(indicator in text_lower for indicator in contract_indicators):
        doc_info['type'] = 'contract'
        # Extract contract duration
        duration_match = re.search(r'Laufzeit\s*:\s*(\d+)\s*(?:Monate|Jahre)', text, re.IGNORECASE)
        if duration_match:
            doc_info['fields']['duration'] = duration_match.group(1)
    
    # Check for letter indicators
    letter_indicators = ['brief', 'letter', 'sehr geehrte', 'mit freundlichen grüßen']
    if any(indicator in text_lower for indicator in letter_indicators):
        doc_info['type'] = 'letter'
    
    return doc_info

def create_timeline(dates):
    """Create an interactive timeline visualization."""
    if not dates:
        return None
    
    # Prepare data for timeline
    timeline_data = []
    for date_info in dates:
        timeline_data.append({
            'Date': date_info['date'],
            'Event': date_info['context'],
            'Formatted Date': date_info['text']
        })
    
    # Create timeline using plotly
    fig = px.timeline(
        timeline_data,
        x_start='Date',
        x_end='Date',
        y='Event',
        title='Document Timeline',
        labels={'Date': 'Date', 'Event': 'Event'},
        hover_data=['Formatted Date']
    )
    
    # Customize the timeline
    fig.update_layout(
        showlegend=False,
        height=300,
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis=dict(
            title='Date',
            tickformat='%d %b %Y'
        ),
        yaxis=dict(
            title='Event',
            automargin=True
        )
    )
    
    return fig

st.title("🇩🇪 AI Letter & Contract Summarizer")
st.caption("Upload German documents to extract, summarize, and analyze their content")

# Sidebar configurations
with st.sidebar:
    st.header("⚙️ Settings")
    st.session_state.max_summary_length = st.slider(
        "Maximum Summary Length",
        min_value=100,
        max_value=300,
        value=st.session_state.max_summary_length,
        help="Maximum number of characters in the summary"
    )
    st.session_state.max_key_points = st.slider(
        "Maximum Key Points",
        min_value=3,
        max_value=10,
        value=st.session_state.max_key_points,
        help="Maximum number of key points to extract"
    )

# Language selection
available_langs = get_available_languages()
lang_options = {v: k for k, v in LANGUAGE_MAPPING.items() if v in available_langs}
selected_lang = st.selectbox(
    "Select Document Language",
    options=list(lang_options.keys()),
    format_func=lambda x: f"{x.upper()} ({lang_options[x]})",
    index=0
)

# File upload
uploaded_file = st.file_uploader(
    "Upload a letter (image/pdf)", 
    type=["png", "jpg", "jpeg", "pdf"],
    help="Supported formats: PNG, JPG, JPEG, PDF"
)

if uploaded_file:
    try:
        # Display the uploaded document
        if uploaded_file.type == "application/pdf":
            st.write("📄 PDF Document")
        else:
            st.image(uploaded_file, caption="Uploaded Document", use_column_width=True)
        
        # Extract text with selected language
        with st.spinner("🔍 Extracting text from document..."):
            extracted_text = extract_text(uploaded_file, lang=lang_options[selected_lang])
            
            if not extracted_text.strip():
                st.warning("⚠️ No text could be extracted from the document. Please ensure the image is clear and contains text.")
            else:
                # Show original text
                st.subheader("📄 Original Text")
                with st.expander("Show extracted text", expanded=True):
                    st.text(extracted_text)

                # Document Classification and Specific Fields
                doc_info = classify_document(extracted_text)
                st.info(f"📋 Document Type: {doc_info['type'].upper()}")
                
                # Display specific fields based on document type
                if doc_info['fields']:
                    with st.expander("📊 Document Details", expanded=True):
                        for field, value in doc_info['fields'].items():
                            st.write(f"**{field.replace('_', ' ').title()}:** {value}")

                # Timeline View
                dates = extract_dates(extracted_text)
                if dates:
                    st.subheader("📅 Document Timeline")
                    timeline_fig = create_timeline(dates)
                    if timeline_fig:
                        st.plotly_chart(timeline_fig, use_container_width=True)
                    
                    # Highlight upcoming deadlines
                    today = datetime.now()
                    upcoming_dates = [d for d in dates if d['date'] > today]
                    if upcoming_dates:
                        st.warning("⚠️ Upcoming Deadlines:")
                        for date in upcoming_dates:
                            st.write(f"- {date['text']}: {date['context']}")

                # Contact Information
                contacts = extract_contact_info(extracted_text)
                if any(contacts.values()):
                    with st.expander("📇 Contact Information", expanded=True):
                        # Create contact card
                        if contacts['names']:
                            st.write("👤 **Sender/Recipient:**")
                            for name in contacts['names']:
                                st.write(name.strip())
                        
                        if contacts['emails']:
                            st.write("📧 **Emails:**")
                            for email in contacts['emails']:
                                st.markdown(f"[{email}](mailto:{email})")
                        
                        if contacts['phones']:
                            st.write("📱 **Phone Numbers:**")
                            for phone in contacts['phones']:
                                st.markdown(f"[{phone}](tel:{phone})")
                        
                        if contacts['ibans']:
                            st.write("💳 **IBAN Numbers:**")
                            for iban in contacts['ibans']:
                                st.code(iban)

                if st.button("🧠 Analyze Document", type="primary"):
                    try:
                        with st.spinner("🤖 AI is analyzing your document..."):
                            # Create columns for summary and key points
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.subheader("📝 Summary")
                                summary = summarize_text(
                                    extracted_text, 
                                    max_length=st.session_state.max_summary_length
                                )
                                if summary.startswith("⚠️"):
                                    st.error(summary)
                                else:
                                    st.success(summary)
                            
                            with col2:
                                st.subheader("📌 Key Points")
                                key_points = extract_key_points(
                                    extracted_text,
                                    max_points=st.session_state.max_key_points
                                )
                                if key_points and key_points[0].startswith("⚠️"):
                                    st.error(key_points[0])
                                else:
                                    for point in key_points:
                                        st.markdown(point)
                                        
                    except Exception as e:
                        st.error(f"❌ Error during analysis: {str(e)}")
                        st.info("Please try again or contact support if the issue persists.")
                        
    except Exception as e:
        st.error(f"❌ Error processing document: {str(e)}")
        st.info("Please ensure your document is in a supported format and try again.")

else:
    # Show instructions when no file is uploaded
    st.info("👆 Upload a document to get started!")
    st.markdown("""
    ### How it works:
    1. Upload your German document (image or PDF)
    2. The system will extract the text using OCR
    3. AI will analyze the content and provide:
        - Document type classification and specific fields
        - Interactive timeline of important dates
        - Contact information extraction
        - A concise summary in English
        - Key points and important details
    """)
