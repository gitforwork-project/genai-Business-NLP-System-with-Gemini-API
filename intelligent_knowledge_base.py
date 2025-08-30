import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import json
from datetime import datetime
from config import GeminiConfig
import google.generativeai as genai

class IntelligentKnowledgeBase:
    def __init__(self):
        self.config = GeminiConfig()
        self.model = self.config.get_generative_model()
        self.embedding_model = self.config.get_embeddings_model()
        self.knowledge_base = pd.DataFrame()
        self.embeddings_cache = {}
    
    def add_documents(self, documents):
        """
        Add documents to the knowledge base with automatic embedding generation.
        
        Args:
            documents (list): List of dicts with 'id', 'title', 'content', 'category'
        """
        
        # Convert to DataFrame
        df = pd.DataFrame(documents)
        
        # Generate embeddings for all documents
        embeddings = genai.embed_content(
            model=self.embedding_model,
            content=df['content'].tolist(),
            task_type="RETRIEVAL_DOCUMENT"
        )['embedding']
        
        df['embeddings'] = embeddings
        df['date_added'] = datetime.now()
        
        # Add to knowledge base
        self.knowledge_base = pd.concat([self.knowledge_base, df], ignore_index=True)
        
        print(f"✅ Added {len(documents)} documents to knowledge base")
    
    def search(self, query, top_k=3, category_filter=None):
        """
        Semantic search with optional category filtering.
        
        Args:
            query (str): Search query
            top_k (int): Number of results to return
            category_filter (str): Optional category filter
        """
        
        if self.knowledge_base.empty:
            return "Knowledge base is empty. Please add documents first."
        
        # Generate query embedding
        query_embedding = genai.embed_content(
            model=self.embedding_model,
            content=query,
            task_type="RETRIEVAL_QUERY"
        )['embedding']
        
        # Calculate similarities
        df = self.knowledge_base.copy()
        
        # Apply category filter if specified
        if category_filter:
            df = df[df['category'].str.contains(category_filter, case=False, na=False)]
        
        if df.empty:
            return f"No documents found in category: {category_filter}"
        
        # Calculate cosine similarity
        df['similarity'] = df['embeddings'].apply(
            lambda x: np.dot(x, query_embedding)
        )
        
        # Get top results
        top_results = df.nlargest(top_k, 'similarity')
        
        return top_results[['id', 'title', 'content', 'category', 'similarity']].to_dict('records')
    
    def generate_answer(self, query, context_docs=None, max_context=3):
        """
        Generate contextual answers using retrieved documents.
        
        Args:
            query (str): User question
            context_docs (list): Pre-retrieved documents (optional)
            max_context (int): Maximum context documents to use
        """
        
        # Retrieve relevant documents if not provided
        if context_docs is None:
            context_docs = self.search(query, top_k=max_context)
        
        if not context_docs:
            return "I don't have enough information to answer this question."
        
        # Prepare context from retrieved documents
        context = ""
        for i, doc in enumerate(context_docs[:max_context]):
            context += f"Document {i+1} (ID: {doc['id']}):\n{doc['content']}\n\n"
        
        # Generate answer using context
        prompt = f"""
        You are a knowledgeable business assistant. Answer the user's question based on the provided context documents.
        
        User Question: {query}
        
        Context Documents:
        {context}
        
        Instructions:
        - Provide a clear, accurate answer based on the context
        - If the context doesn't contain enough information, say so
        - Include relevant document IDs in your response
        - Use professional business language
        - If multiple documents provide different perspectives, acknowledge this
        
        Answer:
        """
        
        response = self.model.generate_content(prompt)
        return {
            'answer': response.text,
            'sources': [doc['id'] for doc in context_docs[:max_context]],
            'confidence': min([doc['similarity'] for doc in context_docs[:max_context]])
        }

# Example usage
if __name__ == "__main__":
    # Initialize knowledge base
    kb = IntelligentKnowledgeBase()
    
    # Sample business documents
    business_docs = [
        {
            'id': 'HR-001',
            'title': 'Remote Work Policy',
            'content': 'Our company supports flexible remote work arrangements. Employees can work from home up to 3 days per week with manager approval. Core collaboration hours are 10 AM - 4 PM in your local timezone. All remote workers must maintain reliable internet connection and participate in weekly team meetings.',
            'category': 'HR Policy'
        },
        {
            'id': 'IT-001',
            'title': 'Password Security Guidelines',
            'content': 'All employees must use strong passwords with minimum 12 characters, including uppercase, lowercase, numbers, and special characters. Password rotation is required every 90 days. Two-factor authentication is mandatory for all business applications. Use the company password manager for storing credentials.',
            'category': 'IT Security'
        },
        {
            'id': 'FIN-001',
            'title': 'Expense Reporting Process',
            'content': 'Submit expense reports through the Expensify system within 30 days of incurring expenses. All receipts must be photographed and attached. Pre-approval is required for expenses over $500. Reimbursement processing typically takes 5-7 business days after approval.',
            'category': 'Finance'
        },
        {
            'id': 'HR-002',
            'title': 'Performance Review Process',
            'content': 'Annual performance reviews are conducted in Q1 of each year. Employees complete self-assessments and receive feedback from managers and peers. Goals are set collaboratively for the upcoming year. Mid-year check-ins are scheduled in July to track progress and adjust objectives.',
            'category': 'HR Policy'
        }
    ]
    
    # Add documents to knowledge base
    kb.add_documents(business_docs)
    
    # Test search functionality
    print("=== KNOWLEDGE BASE SEARCH DEMO ===")
    
    test_queries = [
        "How many days can I work from home?",
        "What are the password requirements?",
        "How do I submit expense reports?",
        "When are performance reviews conducted?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        
        # Search for relevant documents
        search_results = kb.search(query, top_k=2)
        print(f"Found {len(search_results)} relevant documents")
        
        # Generate contextual answer
        answer = kb.generate_answer(query)
        print(f"Answer: {answer['answer']}")
        print(f"Sources: {answer['sources']}")
        print("-" * 50)
