import pandas as pd
from datetime import datetime
import re
from config import GeminiConfig

class BusinessDocumentAnalyzer:
    def __init__(self):
        self.config = GeminiConfig()
        self.model = self.config.get_generative_model()
    
    def analyze_document(self, document_text, analysis_type="comprehensive"):
        """
        Analyze business documents with various focus areas.
        
        Args:
            document_text (str): The document content
            analysis_type (str): 'comprehensive', 'financial', 'strategic', 'operational'
        """
        
        analysis_templates = {
            "comprehensive": {
                "focus": "overall business impact, key decisions, action items",
                "format": "executive summary, key findings, recommendations, next steps"
            },
            "financial": {
                "focus": "revenue, costs, profitability, financial risks and opportunities",
                "format": "financial highlights, trend analysis, budget implications"
            },
            "strategic": {
                "focus": "competitive position, market opportunities, strategic initiatives",
                "format": "strategic insights, competitive analysis, strategic recommendations"
            },
            "operational": {
                "focus": "process efficiency, resource allocation, operational challenges",
                "format": "operational summary, efficiency metrics, improvement opportunities"
            }
        }
        
        template = analysis_templates.get(analysis_type, analysis_templates["comprehensive"])
        
        prompt = f"""
        You are a senior business analyst reviewing an important business document.
        
        Analysis Focus: {template['focus']}
        
        Document Content:
        {document_text}
        
        Provide analysis in the following format:
        {template['format']}
        
        Requirements:
        - Extract quantitative data where available
        - Identify key business implications
        - Highlight urgent items requiring immediate attention
        - Provide specific, actionable recommendations
        - Use business terminology appropriate for executive audience
        
        Keep the analysis concise but comprehensive.
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def extract_action_items(self, document_text):
        """Extract specific action items from business documents."""
        
        prompt = f"""
        Extract all action items, decisions, and next steps from this business document.
        
        Document:
        {document_text}
        
        For each item, provide:
        1. Action Item: [specific task]
        2. Owner: [person/team responsible if mentioned]
        3. Deadline: [if mentioned]
        4. Priority: [High/Medium/Low based on context]
        
        Format as a numbered list. If no clear action items exist, state "No specific action items identified."
        """
        
        response = self.model.generate_content(prompt)
        return response.text

# Example usage
if __name__ == "__main__":
    analyzer = BusinessDocumentAnalyzer()
    
    # Sample business document
    sample_report = """
    Q3 2025 Business Review Meeting Minutes
    Date: July 15, 2025
    Attendees: Sarah Chen (CEO), Mike Rodriguez (CFO), Lisa Wang (CTO), John Davis (VP Sales)
    
    Key Discussion Points:
    
    1. Financial Performance:
    - Q3 revenue reached $2.3M, representing 18% growth over Q2
    - Operating expenses increased by 12% due to new hires in engineering
    - Net profit margin decreased from 22% to 19%
    - Mike to provide detailed cost analysis by July 25th
    
    2. Product Development:
    - New AI feature beta testing shows 35% improvement in user engagement
    - Technical debt in legacy system causing 15% performance degradation
    - Lisa recommended allocating $200K for system modernization
    - Board approval needed for additional engineering budget
    
    3. Sales Performance:
    - 47 new enterprise clients acquired in Q3
    - Average deal size increased from $15K to $22K
    - Customer churn rate at 3.2%, down from 4.1% in Q2
    - John to implement new customer success program by August 15th
    
    4. Strategic Initiatives:
    - Partnership with TechCorp progressing well, contract signing expected by month-end
    - Expansion into European market delayed due to regulatory compliance requirements
    - Competitor analysis reveals need for mobile app development
    
    Next Meeting: August 15, 2025
    """
    
    # Comprehensive analysis
    print("=== COMPREHENSIVE ANALYSIS ===")
    comprehensive = analyzer.analyze_document(sample_report, "comprehensive")
    print(comprehensive)
    
    print("\n=== FINANCIAL ANALYSIS ===")
    financial = analyzer.analyze_document(sample_report, "financial")
    print(financial)
    
    print("\n=== ACTION ITEMS ===")
    actions = analyzer.extract_action_items(sample_report)
    print(actions)
