import requests
import json
from datetime import datetime
import re
from config import GeminiConfig

class CompetitiveIntelligenceAnalyzer:
    def __init__(self):
        self.config = GeminiConfig()
        self.model = self.config.get_generative_model()
        self.intelligence_data = []
    
    def analyze_competitor_content(self, content_items):
        """Analyze competitor-related content for strategic insights."""
        
        # Combine all content for analysis
        combined_content = ""
        for item in content_items:
            combined_content += f"""
            Source: {item.get('source', 'Unknown')}
            Title: {item.get('title', 'N/A')}
            Date: {item.get('date', 'N/A')}
            Content: {item.get('content', 'N/A')}
            
            ---
            """
        
        analysis_prompt = f"""
        Analyze the following competitive intelligence for strategic business insights:
        
        {combined_content}
        
        Provide analysis in these categories:
        
        1. COMPETITIVE THREATS
        - New product launches or features
        - Market expansion moves
        - Technology advantages
        - Pricing strategies
        
        2. MARKET OPPORTUNITIES
        - Gaps in competitor offerings
        - Customer pain points mentioned
        - Market segments being neglected
        - Potential partnership opportunities
        
        3. STRATEGIC RECOMMENDATIONS
        - Immediate response actions needed
        - Long-term strategic adjustments
        - Product development priorities
        - Market positioning changes
        
        4. FINANCIAL INTELLIGENCE
        - Funding announcements
        - Revenue indicators
        - Investment priorities
        - Cost structure insights
        
        5. CUSTOMER INTELLIGENCE
        - Customer satisfaction trends
        - Feature requests and complaints
        - User behavior patterns
        - Churn indicators
        
        Focus on actionable insights that can inform business decisions.
        Highlight urgent items requiring immediate attention.
        """
        
        response = self.model.generate_content(analysis_prompt)
        return response.text
    
    def extract_key_insights(self, analysis_text):
        """Extract key insights and action items from competitive analysis."""
        
        insights_prompt = f"""
        Extract the most critical insights from this competitive analysis:
        
        {analysis_text}
        
        Provide:
        1. Top 3 Strategic Threats (most urgent competitive risks)
        2. Top 3 Market Opportunities (best chances to gain advantage)
        3. Immediate Action Items (next 30 days)
        4. Strategic Initiatives (next 90 days)
        5. Monitoring Priorities (what to watch closely)
        
        Format each item as:
        - Insight/Action: [specific description]
        - Business Impact: [potential effect on business]
        - Urgency: [High/Medium/Low]
        - Resources Needed: [what's required to act]
        """
        
        response = self.model.generate_content(insights_prompt)
        return response.text
    
    def generate_competitive_report(self, intelligence_items, report_focus="comprehensive"):
        """Generate a comprehensive competitive intelligence report."""
        
        # Analyze the intelligence
        analysis = self.analyze_competitor_content(intelligence_items)
        
        # Extract key insights
        insights = self.extract_key_insights(analysis)
        
        # Generate executive summary
        summary_prompt = f"""
        Create an executive summary of this competitive intelligence analysis:
        
        {analysis}
        
        The executive summary should be 3-4 sentences that highlight:
        - The most significant competitive developments
        - Key strategic implications for our business
        - Recommended immediate actions
        
        Write for senior executives who need to understand the competitive landscape quickly.
        """
        
        summary = self.model.generate_content(summary_prompt)
        
        # Compile final report
        report = f"""
        # Competitive Intelligence Report
        ## Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        
        ## Executive Summary
        {summary.text}
        
        ## Detailed Analysis
        {analysis}
        
        ## Key Strategic Insights
        {insights}
        
        ## Intelligence Sources
        """
        
        for i, item in enumerate(intelligence_items, 1):
            report += f"\n{i}. {item.get('source', 'Unknown Source')} - {item.get('title', 'N/A')}"
        
        return report
    
    def track_competitor_metrics(self, competitor_name, metrics_data):
        """Track and analyze competitor performance metrics over time."""
        
        tracking_prompt = f"""
        Analyze performance metrics for competitor: {competitor_name}
        
        Metrics Data:
        {json.dumps(metrics_data, indent=2)}
        
        Provide analysis on:
        1. Performance Trends (growth/decline patterns)
        2. Competitive Positioning (how they compare to market)
        3. Strategic Implications (what this means for competition)
        4. Opportunity Assessment (areas where we can compete)
        
        Focus on specific metrics and their business implications.
        """
        
        response = self.model.generate_content(tracking_prompt)
        return response.text

# Example usage
if __name__ == "__main__":
    # Initialize competitive intelligence analyzer
    analyzer = CompetitiveIntelligenceAnalyzer()
    
    # Sample competitive intelligence data
    sample_intelligence = [
        {
            'source': 'TechCrunch',
            'title': 'RivalCorp raises $25M Series B for AI expansion',
            'date': '2025-07-15',
            'content': 'RivalCorp announced a $25M Series B funding round led by Venture Capital Partners. The company plans to use the funding to expand its AI capabilities and enter the European market. CEO Jane Smith mentioned plans to double the engineering team by year-end and launch three new AI-powered features.'
        },
        {
            'source': 'Customer Review - G2',
            'title': 'CompetitorX User Feedback',
            'date': '2025-07-10',
            'content': 'Recent user reviews show mixed feedback on CompetitorX\'s latest update. Users appreciate the new dashboard design but complain about slower performance and missing features. Several reviews mention considering switching to alternatives due to pricing increases.'
        },
        {
            'source': 'Industry Report',
            'title': 'Market Share Analysis Q2 2025',
            'date': '2025-07-01',
            'content': 'CompetitorY gained 3% market share in Q2, primarily through aggressive pricing in the SMB segment. Their customer acquisition cost decreased by 15% while maintaining a 92% customer satisfaction rate. However, enterprise clients are showing higher churn rates.'
        },
        {
            'source': 'LinkedIn Post',
            'title': 'StartupZ Product Launch',
            'date': '2025-07-12',
            'content': 'StartupZ launched their new mobile-first platform targeting millennial business owners. The platform features voice-activated controls and AI-powered automation. Early beta users report 40% time savings in daily tasks. The company is offering a 6-month free trial to attract new users.'
        }
    ]
    
    # Generate competitive intelligence report
    print("=== COMPETITIVE INTELLIGENCE ANALYSIS ===")
    
    competitive_report = analyzer.generate_competitive_report(sample_intelligence)
    print(competitive_report)
    
    # Track specific competitor metrics
    print("\n=== COMPETITOR METRICS TRACKING ===")
    
    rival_metrics = {
        'monthly_active_users': 45000,
        'customer_acquisition_cost': 120,
        'monthly_recurring_revenue': 380000,
        'churn_rate': 3.2,
        'net_promoter_score': 68,
        'average_deal_size': 2400
    }
    
    metrics_analysis = analyzer.track_competitor_metrics("RivalCorp", rival_metrics)
    print(metrics_analysis)
    
    # Save intelligence report
    with open(f"competitive_intelligence_{datetime.now().strftime('%Y%m%d_%H%M')}.md", "w") as f:
        f.write(competitive_report)
    
    print("\n✅ Competitive intelligence report generated and saved!")
