# Business NLP System with Gemini API

A comprehensive Natural Language Processing system designed for business applications, powered by Google's Gemini API. This system provides intelligent document analysis, marketing copy generation, sentiment analysis, competitive intelligence, and knowledge management capabilities.

## 🌟 Features

- **📝 Marketing Copy Generation** - Create compelling email campaigns, social media posts, landing pages, and advertisements
- **📄 Document Analysis** - Extract insights, action items, and strategic recommendations from business documents
- **😊 Sentiment Analysis** - Analyze customer feedback and social media sentiment for business intelligence
- **🧠 Knowledge Base Q&A** - Build and query intelligent knowledge bases with semantic search
- **📊 Business Report Generation** - Generate comprehensive reports from metrics and data
- **🔍 Competitive Intelligence** - Analyze competitor information and market trends
- **🤖 Interactive Chatbot** - Unified interface combining all NLP capabilities

## 📋 Prerequisites

- Python 3.8 or higher
- Google Cloud account with Gemini API access
- Gemini API key

## 🚀 Quick Setup

### 1. Clone and Install Dependencies

```bash
# Install required packages
pip install google-generativeai pandas numpy scikit-learn python-dotenv requests
```

### 2. Environment Configuration

Create a `.env` file in the project root directory:


Add your Gemini API key to the `.env` file:

```env
# .env file
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Get Your Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Generate an API key
4. Copy the key to your `.env` file

## 📁 Project Structure

```
business-nlp-system/
├── config.py                           # Gemini API configuration
├── intelligent_business_chatbot.py     # Main interactive chatbot
├── business_document_analyzer.py       # Document analysis module
├── competitive_intelligence_analyzer.py # Competitor analysis module
├── customer_sentiment_analyzer.py      # Sentiment analysis module
├── intelligent_knowledge_base.py       # Knowledge base management
├── marketing_copy_generator.py         # Marketing copy generation
├── .env                                # Environment variables
└── README.md                          # This file
```

## 🏃‍♂️ Running the Applications

### 1. Test Configuration

Verify your API key and configuration:

```bash
python config.py
```

**Expected Output:**
```
✅ Gemini API configured successfully!
Test response: Hello! I'm ready to assist you with professional business communication and analysis.
```

### 2. Interactive Business Chatbot (Recommended)

Launch the main interactive interface:

```bash
python intelligent_business_chatbot.py
```

**Features Available:**
- Marketing copy generation
- Document analysis
- Sentiment analysis
- Knowledge base Q&A
- Business report generation
- Competitive intelligence
- General business assistant

### 3. Individual Modules

Run specific modules independently:

#### Marketing Copy Generator
```bash
python marketing_copy_generator.py
```

#### Document Analyzer
```bash
python business_document_analyzer.py
```

#### Sentiment Analyzer
```bash
python customer_sentiment_analyzer.py
```

#### Competitive Intelligence
```bash
python competitive_intelligence_analyzer.py
```

#### Knowledge Base
```bash
python intelligent_knowledge_base.py
```

## 📖 Usage Examples

### Marketing Copy Generation

```python
from marketing_copy_generator import MarketingCopyGenerator

generator = MarketingCopyGenerator()

product_info = {
    "name": "ProjectFlow Pro",
    "category": "Project Management Software",
    "features": ["Real-time collaboration", "Advanced analytics", "Mobile app"],
    "target_audience": "Project managers and teams",
    "value_proposition": "Increase team productivity by 40%",
    "price_point": "Affordable enterprise pricing"
}

# Generate email copy
email_copy = generator.generate_marketing_copy(product_info, "email")
print(email_copy)
```

### Document Analysis

```python
from business_document_analyzer import BusinessDocumentAnalyzer

analyzer = BusinessDocumentAnalyzer()

document = """
Q3 Business Review: Revenue increased 25% to $2.1M. 
Customer acquisition cost decreased 15%. 
Next steps: expand marketing budget, hire 2 engineers.
"""

# Comprehensive analysis
analysis = analyzer.analyze_document(document, "comprehensive")
print(analysis)

# Extract action items
actions = analyzer.extract_action_items(document)
print(actions)
```

### Sentiment Analysis

```python
from customer_sentiment_analyzer import CustomerSentimentAnalyzer

analyzer = CustomerSentimentAnalyzer()

feedback = [
    "Love the new features! Great customer service.",
    "App crashes frequently, very frustrating.",
    "Good product but pricing is too high."
]

# Batch sentiment analysis
analysis = analyzer.batch_sentiment_analysis(feedback)
print(analysis)
```

### Knowledge Base Q&A

```python
from intelligent_knowledge_base import IntelligentKnowledgeBase

kb = IntelligentKnowledgeBase()

# Add documents
documents = [
    {
        'id': 'HR-001',
        'title': 'Remote Work Policy',
        'content': 'Employees can work remotely up to 3 days per week...',
        'category': 'HR Policy'
    }
]

kb.add_documents(documents)

# Query the knowledge base
answer = kb.generate_answer("How many days can I work from home?")
print(answer['answer'])
```

## ⚙️ Configuration Options

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Your Gemini API key | Yes |

### Model Configuration

The system uses:
- **Generative Model**: `gemini-2.0-flash`
- **Embedding Model**: `models/text-embedding-004`

To change models, edit `config.py`:

```python
# In config.py
self.generative_model = genai.GenerativeModel('gemini-2.5-pro')  # Alternative model
```

## 🛠️ Troubleshooting

### Common Issues

1. **API Key Error**
   ```
   ValueError: GEMINI_API_KEY not found in environment variables
   ```
   **Solution:** Ensure your `.env` file contains the correct API key

2. **Import Errors**
   ```
   ModuleNotFoundError: No module named 'google.generativeai'
   ```
   **Solution:** Install missing dependencies:
   ```bash
   pip install google-generativeai
   ```

3. **Rate Limiting**
   ```
   API rate limit exceeded
   ```
   **Solution:** Add delays between API calls or upgrade your API plan

### Debug Mode

Enable detailed logging by adding to your scripts:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📊 Performance Tips

1. **Batch Processing**: Use batch operations for multiple documents
2. **Caching**: The system caches embeddings to improve performance
3. **Context Length**: Keep document inputs under 30K tokens for optimal performance
4. **API Limits**: Be mindful of API rate limits for production use

## 🔒 Security Best Practices

1. **API Key Security**:
   - Never commit `.env` files to version control
   - Use environment variables in production
   - Rotate API keys regularly

2. **Data Privacy**:
   - Don't send sensitive data to the API
   - Implement data sanitization for customer information
   - Consider on-premises solutions for sensitive documents
