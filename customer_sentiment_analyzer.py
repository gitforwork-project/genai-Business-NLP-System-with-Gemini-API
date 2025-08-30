import numpy as np
from datetime import datetime
import json
from config import GeminiConfig

class CustomerSentimentAnalyzer:
    def __init__(self):
        self.config = GeminiConfig()
        self.model = self.config.get_generative_model()
    
    def analyze_sentiment(self, text, include_aspects=True):
        """
        Comprehensive sentiment analysis for customer feedback.
        
        Args:
            text (str): Customer feedback text
            include_aspects (bool): Whether to analyze specific aspects
        """
        
        base_prompt = f"""
        Analyze the sentiment of this customer feedback with business context.
        
        Customer Feedback: "{text}"
        
        Provide analysis in this JSON format:
        {{
            "overall_sentiment": "positive/negative/neutral",
            "confidence_score": 0.0-1.0,
            "emotional_tone": "specific emotion (e.g., frustrated, excited, disappointed)",
            "urgency_level": "low/medium/high",
            "business_impact": "brief description of potential business impact"
        }}
        """
        
        if include_aspects:
            base_prompt += """
            "aspect_analysis": {
                "product_quality": "sentiment",
                "customer_service": "sentiment",
                "pricing": "sentiment",
                "user_experience": "sentiment"
            },
            "key_issues": ["list of specific issues mentioned"],
            "positive_highlights": ["list of positive aspects mentioned"]
            """
        
        response = self.model.generate_content(base_prompt)
        return response.text
    
    def batch_sentiment_analysis(self, feedback_list):
        """Analyze sentiment for multiple feedback items."""
        
        # Combine feedback for batch processing
        combined_feedback = ""
        for i, feedback in enumerate(feedback_list, 1):
            combined_feedback += f"Feedback {i}: {feedback}\n\n"
        
        prompt = f"""
        Analyze sentiment for multiple customer feedback items and provide a summary.
        
        {combined_feedback}
        
        For each feedback item, provide:
        1. Feedback number
        2. Overall sentiment (positive/negative/neutral)
        3. Key concern or highlight
        4. Recommended action
        
        Then provide an overall summary:
        - Total positive/negative/neutral count
        - Most common issues
        - Urgent items requiring immediate attention
        - Overall customer satisfaction trend
        """
        
        response = self.model.generate_content(prompt)
        return response.text

# Example usage
if __name__ == "__main__":
    analyzer = CustomerSentimentAnalyzer()
    
    # Sample customer feedback
    sample_feedback = [
        "The new interface is confusing and I can't find basic features. Very frustrated with the recent update.",
        "Excellent customer service! The support team resolved my issue within 30 minutes. Highly recommend.",
        "Product works as advertised but the pricing is quite high compared to competitors. Worth considering a discount.",
        "App crashes frequently on mobile devices. This is affecting my daily workflow significantly.",
        "Love the new AI features! They've saved me hours of work. Great job on the innovation."
    ]
    
    # Analyze individual feedback
    print("=== INDIVIDUAL SENTIMENT ANALYSIS ===")
    for i, feedback in enumerate(sample_feedback[:2], 1):
        print(f"\nFeedback {i}:")
        analysis = analyzer.analyze_sentiment(feedback)
        print(analysis)
    
    # Batch analysis
    print("\n=== BATCH SENTIMENT ANALYSIS ===")
    batch_analysis = analyzer.batch_sentiment_analysis(sample_feedback)
    print(batch_analysis)
