from config import GeminiConfig
import json

class MarketingCopyGenerator:
    def __init__(self):
        self.config = GeminiConfig()
        self.model = self.config.get_generative_model()
    
    def generate_marketing_copy(self, product_info, campaign_type="email"):
        """
        Generate marketing copy for various campaign types.
        
        Args:
            product_info (dict): Product details
            campaign_type (str): 'email', 'social', 'landing_page', 'ad_copy'
        """
        
        # Template for different campaign types
        templates = {
            "email": {
                "structure": "Subject line, greeting, value proposition, features, call-to-action",
                "tone": "professional but engaging",
                "length": "150-200 words"
            },
            "social": {
                "structure": "Hook, value proposition, call-to-action, hashtags",
                "tone": "casual and energetic",
                "length": "50-100 words"
            },
            "landing_page": {
                "structure": "Headline, subheadline, benefits, features, testimonial placeholder, CTA",
                "tone": "confident and persuasive",
                "length": "300-400 words"
            },
            "ad_copy": {
                "structure": "Headline, description, call-to-action",
                "tone": "direct and compelling",
                "length": "25-50 words"
            }
        }
        
        template = templates.get(campaign_type, templates["email"])
        
        prompt = f"""
        You are a senior marketing copywriter creating {campaign_type} copy for a business product.
        
        Product Information:
        - Name: {product_info.get('name', 'N/A')}
        - Category: {product_info.get('category', 'N/A')}
        - Key Features: {', '.join(product_info.get('features', []))}
        - Target Audience: {product_info.get('target_audience', 'N/A')}
        - Unique Value Proposition: {product_info.get('value_proposition', 'N/A')}
        - Price Point: {product_info.get('price_point', 'N/A')}
        
        Requirements:
        - Structure: {template['structure']}
        - Tone: {template['tone']}
        - Length: {template['length']}
        - Include emotional triggers and urgency where appropriate
        - Focus on benefits, not just features
        - Use power words and active voice
        
        Generate compelling copy that drives action.
        """
        
        response = self.model.generate_content(prompt)
        return response.text

# Example usage
if __name__ == "__main__":
    generator = MarketingCopyGenerator()
    
    product_info = {
        "name": "DataFlow Pro",
        "category": "Business Analytics Software",
        "features": [
            "Real-time data visualization",
            "Automated report generation",
            "Advanced predictive analytics",
            "Cloud-based collaboration"
        ],
        "target_audience": "Data analysts and business intelligence teams",
        "value_proposition": "Transform raw data into actionable insights 10x faster",
        "price_point": "Enterprise-level pricing with ROI guarantee"
    }
    
    # Generate different types of marketing copy
    for campaign_type in ["email", "social", "landing_page", "ad_copy"]:
        print(f"\n--- {campaign_type.upper()} COPY ---")
        copy = generator.generate_marketing_copy(product_info, campaign_type)
        print(copy)
        print("-" * 50)