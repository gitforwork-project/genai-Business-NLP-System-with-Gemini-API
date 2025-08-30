import os
import sys
import json
from datetime import datetime
from config import GeminiConfig
from typing import Dict, List, Any
import re
from config import GeminiConfig

class IntelligentBusinessChatbot:
    def __init__(self):
        """Initialize the comprehensive business chatbot."""
        self.config = GeminiConfig()
        self.model = self.config.get_generative_model()
        self.embedding_model = self.config.get_embeddings_model()
        
        # Initialize components
        self.knowledge_base = self._initialize_knowledge_base()
        self.conversation_history = []
        self.user_context = {}
        self.session_start = datetime.now()
        
        # Available features
        self.features = {
            '1': 'Marketing Copy Generation',
            '2': 'Document Analysis & Summarization',
            '3': 'Customer Sentiment Analysis',
            '4': 'Knowledge Base Q&A',
            '5': 'Business Report Generation',
            '6': 'Competitive Intelligence',
            '7': 'General Business Assistant',
            '8': 'Export Conversation',
            '9': 'Show Statistics',
            '0': 'Exit'
        }
        
        print("🤖 Intelligent Business Chatbot Initialized!")
        print("📊 Combining NLP, Knowledge Management, and Business Intelligence")
        print("-" * 60)
    
    def _initialize_knowledge_base(self):
        """Initialize the knowledge base with sample business documents."""
        
        # Sample business knowledge base
        business_docs = [
            {
                'id': 'POLICY-001',
                'title': 'Remote Work Guidelines',
                'content': 'Employees can work remotely up to 3 days per week with manager approval. Core hours 10 AM - 4 PM local time. Weekly team meetings required. Reliable internet and secure workspace mandatory.',
                'category': 'HR Policy',
                'last_updated': '2025-07-01'
            },
            {
                'id': 'PROCESS-001',
                'title': 'Customer Onboarding Process',
                'content': 'New customer onboarding includes: welcome email within 24 hours, setup call within 48 hours, training materials delivery, 30-day check-in, and satisfaction survey. Success metrics: 90% completion rate, 4.5+ satisfaction score.',
                'category': 'Customer Success',
                'last_updated': '2025-06-15'
            },
            {
                'id': 'FINANCE-001',
                'title': 'Budget Approval Process',
                'content': 'Budget requests under $5K require department head approval. $5K-$25K needs VP approval. Over $25K requires C-level approval. All requests must include ROI analysis and 3-month impact projection.',
                'category': 'Finance',
                'last_updated': '2025-07-10'
            },
            {
                'id': 'SALES-001',
                'title': 'Lead Qualification Framework',
                'content': 'Use BANT framework: Budget (confirmed >$10K), Authority (decision maker identified), Need (pain point validated), Timeline (decision within 6 months). Score leads 1-4 on each criteria.',
                'category': 'Sales',
                'last_updated': '2025-07-05'
            }
        ]
        
        # Create embeddings for knowledge base
        kb_data = []
        for doc in business_docs:
            try:
                embedding = genai.embed_content(
                    model=self.embedding_model,
                    content=doc['content'],
                    task_type="RETRIEVAL_DOCUMENT"
                )['embedding']
                
                doc['embedding'] = embedding
                kb_data.append(doc)
                
            except Exception as e:
                print(f"Warning: Could not create embedding for {doc['id']}: {e}")
        
        return kb_data
    
    def display_menu(self):
        """Display the main menu."""
        print("\n" + "="*60)
        print("🚀 INTELLIGENT BUSINESS CHATBOT")
        print("="*60)
        print("Select a feature:")
        
        for key, value in self.features.items():
            print(f"  {key}. {value}")
        
        print("\n💡 Tip: Type 'help' anytime for guidance")
        print("-" * 60)
    
    def search_knowledge_base(self, query: str, top_k: int = 3) -> List[Dict]:
        """Search the knowledge base for relevant documents."""
        
        if not self.knowledge_base:
            return []
        
        try:
            # Generate query embedding
            query_embedding = genai.embed_content(
                model=self.embedding_model,
                content=query,
                task_type="RETRIEVAL_QUERY"
            )['embedding']
            
            # Calculate similarities
            scored_docs = []
            for doc in self.knowledge_base:
                similarity = sum(a * b for a, b in zip(doc['embedding'], query_embedding))
                scored_docs.append({**doc, 'similarity': similarity})
            
            # Sort by similarity and return top results
            scored_docs.sort(key=lambda x: x['similarity'], reverse=True)
            return scored_docs[:top_k]
            
        except Exception as e:
            print(f"Error searching knowledge base: {e}")
            return []
    
    def generate_marketing_copy(self):
        """Interactive marketing copy generation."""
        
        print("\n📝 MARKETING COPY GENERATOR")
        print("-" * 40)
        
        # Collect product information
        product_name = input("Product/Service Name: ").strip()
        if not product_name:
            print("❌ Product name is required!")
            return
        
        print("\nKey Features (press Enter after each, empty line to finish):")
        features = []
        while True:
            feature = input("  Feature: ").strip()
            if not feature:
                break
            features.append(feature)
        
        target_audience = input("Target Audience: ").strip()
        value_proposition = input("Value Proposition: ").strip()
        
        # Select copy type
        print("\nCopy Type:")
        print("1. Email Campaign")
        print("2. Social Media Post")
        print("3. Landing Page")
        print("4. Advertisement")
        
        copy_type_map = {
            '1': 'email',
            '2': 'social',
            '3': 'landing_page',
            '4': 'advertisement'
        }
        
        copy_choice = input("Select type (1-4): ").strip()
        copy_type = copy_type_map.get(copy_choice, 'email')
        
        # Generate copy
        print("\n⏳ Generating marketing copy...")
        
        prompt = f"""
        Generate compelling {copy_type} marketing copy for:
        
        Product: {product_name}
        Features: {', '.join(features) if features else 'N/A'}
        Target Audience: {target_audience or 'General audience'}
        Value Proposition: {value_proposition or 'N/A'}
        
        Requirements:
        - Professional and engaging tone
        - Clear call-to-action
        - Focus on benefits over features
        - Appropriate length for {copy_type}
        - Include emotional triggers
        
        Generate effective marketing copy:
        """
        
        try:
            response = self.model.generate_content(prompt)
            
            print("\n✅ GENERATED MARKETING COPY")
            print("=" * 50)
            print(response.text)
            print("=" * 50)
            
            # Save to conversation history
            self.conversation_history.append({
                'timestamp': datetime.now(),
                'feature': 'Marketing Copy Generation',
                'input': f"Product: {product_name}, Type: {copy_type}",
                'output': response.text
            })
            
        except Exception as e:
            print(f"❌ Error generating marketing copy: {e}")
    
    def analyze_document(self):
        """Interactive document analysis."""
        
        print("\n📄 DOCUMENT ANALYSIS")
        print("-" * 40)
        
        print("Please paste your document text (press Enter twice when finished):")
        lines = []
        empty_lines = 0
        
        while empty_lines < 2:
            line = input()
            if line.strip() == "":
                empty_lines += 1
            else:
                empty_lines = 0
            lines.append(line)
        
        document_text = '\n'.join(lines).strip()
        
        if not document_text:
            print("❌ No document text provided!")
            return
        
        print("\nAnalysis Type:")
        print("1. Executive Summary")
        print("2. Key Action Items")
        print("3. Financial Analysis")
        print("4. Strategic Insights")
        print("5. Comprehensive Analysis")
        
        analysis_choice = input("Select analysis type (1-5): ").strip()
        
        analysis_types = {
            '1': 'executive_summary',
            '2': 'action_items',
            '3': 'financial',
            '4': 'strategic',
            '5': 'comprehensive'
        }
        
        analysis_type = analysis_types.get(analysis_choice, 'comprehensive')
        
        print(f"\n⏳ Performing {analysis_type} analysis...")
        
        # Generate analysis prompt based on type
        if analysis_type == 'executive_summary':
            prompt = f"""
            Create a concise executive summary of this document:
            
            {document_text}
            
            Focus on:
            - Key decisions made
            - Important metrics or results
            - Strategic implications
            - Next steps
            
            Keep it under 150 words suitable for senior executives.
            """
        
        elif analysis_type == 'action_items':
            prompt = f"""
            Extract all action items and next steps from this document:
            
            {document_text}
            
            For each action item, identify:
            - Specific task
            - Responsible party (if mentioned)
            - Deadline (if mentioned)
            - Priority level
            
            Format as a numbered list.
            """
        
        elif analysis_type == 'financial':
            prompt = f"""
            Analyze this document for financial information and implications:
            
            {document_text}
            
            Focus on:
            - Revenue and cost metrics
            - Budget implications
            - Financial risks and opportunities
            - ROI considerations
            
            Provide specific financial insights.
            """
        
        elif analysis_type == 'strategic':
            prompt = f"""
            Analyze this document for strategic business insights:
            
            {document_text}
            
            Focus on:
            - Competitive implications
            - Market opportunities
            - Strategic risks
            - Long-term business impact
            
            Provide strategic recommendations.
            """
        
        else:  # comprehensive
            prompt = f"""
            Provide comprehensive analysis of this business document:
            
            {document_text}
            
            Include:
            1. Executive Summary
            2. Key Findings
            3. Action Items
            4. Business Implications
            5. Recommendations
            
            Structure the analysis for business stakeholders.
            """
        
        try:
            response = self.model.generate_content(prompt)
            
            print(f"\n✅ DOCUMENT ANALYSIS - {analysis_type.upper()}")
            print("=" * 60)
            print(response.text)
            print("=" * 60)
            
            # Save to conversation history
            self.conversation_history.append({
                'timestamp': datetime.now(),
                'feature': 'Document Analysis',
                'input': f"Document length: {len(document_text)} chars, Analysis: {analysis_type}",
                'output': response.text
            })
            
        except Exception as e:
            print(f"❌ Error analyzing document: {e}")
    
    def analyze_sentiment(self):
        """Interactive sentiment analysis."""
        
        print("\n😊 SENTIMENT ANALYSIS")
        print("-" * 40)
        
        print("Analysis Mode:")
        print("1. Single Customer Feedback")
        print("2. Multiple Feedback Items")
        print("3. Social Media Comments")
        
        mode_choice = input("Select mode (1-3): ").strip()
        
        if mode_choice == '1':
            feedback = input("\nEnter customer feedback: ").strip()
            if not feedback:
                print("❌ No feedback provided!")
                return
            
            print("\n⏳ Analyzing sentiment...")
            
            prompt = f"""
            Analyze the sentiment and business implications of this customer feedback:
            
            Feedback: "{feedback}"
            
            Provide:
            1. Overall Sentiment (positive/negative/neutral)
            2. Emotional Tone
            3. Specific Issues or Highlights
            4. Business Impact Assessment
            5. Recommended Response Strategy
            6. Urgency Level (low/medium/high)
            
            Format for business action.
            """
            
            try:
                response = self.model.generate_content(prompt)
                
                print("\n✅ SENTIMENT ANALYSIS RESULT")
                print("=" * 50)
                print(response.text)
                print("=" * 50)
                
            except Exception as e:
                print(f"❌ Error analyzing sentiment: {e}")
        
        elif mode_choice == '2':
            print("\nEnter multiple feedback items (press Enter twice when finished):")
            feedback_items = []
            item_num = 1
            
            while True:
                feedback = input(f"Feedback {item_num}: ").strip()
                if not feedback:
                    break
                feedback_items.append(feedback)
                item_num += 1
            
            if not feedback_items:
                print("❌ No feedback items provided!")
                return
            
            print(f"\n⏳ Analyzing {len(feedback_items)} feedback items...")
            
            combined_feedback = "\n".join([f"{i+1}. {item}" for i, item in enumerate(feedback_items)])
            
            prompt = f"""
            Analyze sentiment for multiple customer feedback items:
            
            {combined_feedback}
            
            Provide:
            1. Individual sentiment analysis for each item
            2. Overall sentiment distribution
            3. Common themes and issues
            4. Priority items requiring immediate attention
            5. Actionable insights for customer success team
            
            Format for business dashboard.
            """
            
            try:
                response = self.model.generate_content(prompt)
                
                print("\n✅ BATCH SENTIMENT ANALYSIS")
                print("=" * 50)
                print(response.text)
                print("=" * 50)
                
            except Exception as e:
                print(f"❌ Error analyzing batch sentiment: {e}")
        
        # Save to conversation history
        self.conversation_history.append({
            'timestamp': datetime.now(),
            'feature': 'Sentiment Analysis',
            'input': f"Mode: {mode_choice}, Items: {len(feedback_items) if mode_choice == '2' else 1}",
            'output': response.text if 'response' in locals() else 'Error occurred'
        })
    
    def knowledge_base_qa(self):
        """Interactive knowledge base Q&A."""
        
        print("\n🧠 KNOWLEDGE BASE Q&A")
        print("-" * 40)
        print("Ask questions about company policies, processes, or procedures...")
        
        while True:
            question = input("\n❓ Your question (or 'back' to return): ").strip()
            
            if question.lower() in ['back', 'exit', 'quit']:
                break
            
            if not question:
                print("Please enter a question.")
                continue
            
            print("⏳ Searching knowledge base...")
            
            # Search knowledge base
            relevant_docs = self.search_knowledge_base(question, top_k=3)
            
            if not relevant_docs:
                print("❌ No relevant information found in knowledge base.")
                continue
            
            # Generate contextual answer
            context = ""
            for doc in relevant_docs:
                context += f"Document: {doc['title']} (ID: {doc['id']})\n{doc['content']}\n\n"
            
            prompt = f"""
            Answer this business question using the provided knowledge base context:
            
            Question: {question}
            
            Context:
            {context}
            
            Instructions:
            - Provide a clear, accurate answer based on the context
            - Reference specific policies or procedures
            - Include document IDs for verification
            - If information is incomplete, state what additional details are needed
            
            Answer:
            """
            
            try:
                response = self.model.generate_content(prompt)
                
                print("\n✅ KNOWLEDGE BASE ANSWER")
                print("=" * 50)
                print(response.text)
                print("\n📚 Sources:")
                for doc in relevant_docs:
                    print(f"  - {doc['title']} (ID: {doc['id']}) - Relevance: {doc['similarity']:.3f}")
                print("=" * 50)
                
                # Save to conversation history
                self.conversation_history.append({
                    'timestamp': datetime.now(),
                    'feature': 'Knowledge Base Q&A',
                    'input': question,
                    'output': response.text
                })
                
            except Exception as e:
                print(f"❌ Error generating answer: {e}")
    
    def generate_business_report(self):
        """Interactive business report generation."""
        
        print("\n📊 BUSINESS REPORT GENERATOR")
        print("-" * 40)
        
        print("Report Type:")
        print("1. Sales Performance")
        print("2. Marketing Analysis")
        print("3. Customer Success")
        print("4. Financial Summary")
        print("5. Operational Metrics")
        
        report_choice = input("Select report type (1-5): ").strip()
        
        report_types = {
            '1': 'sales',
            '2': 'marketing',
            '3': 'customer_success',
            '4': 'financial',
            '5': 'operational'
        }
        
        report_type = report_types.get(report_choice, 'sales')
        
        print(f"\nGenerating {report_type} report...")
        print("Please provide key metrics (press Enter to skip any metric):")
        
        # Collect metrics based on report type
        metrics = {}
        
        if report_type == 'sales':
            metrics_prompts = [
                "Total Revenue ($): ",
                "New Customers: ",
                "Conversion Rate (%): ",
                "Average Deal Size ($): ",
                "Pipeline Value ($): ",
                "Sales Cycle (days): "
            ]
        elif report_type == 'marketing':
            metrics_prompts = [
                "Website Visitors: ",
                "Leads Generated: ",
                "Cost per Lead ($): ",
                "Email Open Rate (%): ",
                "Social Media Engagement: ",
                "Campaign ROI: "
            ]
        elif report_type == 'customer_success':
            metrics_prompts = [
                "Customer Satisfaction Score (1-5): ",
                "Net Promoter Score: ",
                "Customer Retention Rate (%): ",
                "Support Tickets Resolved: ",
                "Average Response Time (hours): ",
                "Feature Adoption Rate (%): "
            ]
        elif report_type == 'financial':
            metrics_prompts = [
                "Total Revenue ($): ",
                "Operating Expenses ($): ",
                "Net Profit Margin (%): ",
                "Cash Flow ($): ",
                "Burn Rate ($): ",
                "Budget Variance (%): "
            ]
        else:  # operational
            metrics_prompts = [
                "Team Productivity Score: ",
                "Project Completion Rate (%): ",
                "System Uptime (%): ",
                "Bug Resolution Time (hours): ",
                "Employee Satisfaction: ",
                "Process Efficiency Score: "
            ]
        
        for prompt in metrics_prompts:
            value = input(f"  {prompt}").strip()
            if value:
                metrics[prompt.replace(": ", "").replace("($)", "").replace("(%)", "")] = value
        
        if not metrics:
            print("❌ No metrics provided!")
            return
        
        print("\n⏳ Generating business report...")
        
        prompt = f"""
        Generate a comprehensive {report_type} business report using these metrics:
        
        {json.dumps(metrics, indent=2)}
        
        Structure the report with:
        1. Executive Summary (2-3 sentences)
        2. Key Performance Highlights
        3. Areas of Concern
        4. Trend Analysis (if applicable)
        5. Strategic Recommendations
        6. Action Items for Next Period
        
        Use professional business language suitable for stakeholders.
        Include specific insights and actionable recommendations.
        """
        
        try:
            response = self.model.generate_content(prompt)
            
            print(f"\n✅ {report_type.upper()} BUSINESS REPORT")
            print("=" * 60)
            print(response.text)
            print("=" * 60)
            
            # Save to conversation history
            self.conversation_history.append({
                'timestamp': datetime.now(),
                'feature': 'Business Report Generation',
                'input': f"Type: {report_type}, Metrics: {len(metrics)}",
                'output': response.text
            })
            
        except Exception as e:
            print(f"❌ Error generating report: {e}")
    
    def competitive_intelligence(self):
        """Interactive competitive intelligence analysis."""
        
        print("\n🔍 COMPETITIVE INTELLIGENCE")
        print("-" * 40)
        
        print("Intelligence Type:")
        print("1. Analyze Competitor News/Content")
        print("2. Compare Competitor Features")
        print("3. Market Positioning Analysis")
        
        intel_choice = input("Select type (1-3): ").strip()
        
        if intel_choice == '1':
            print("\nEnter competitor information (press Enter twice when finished):")
            
            competitor_info = []
            while True:
                source = input("Source (e.g., TechCrunch, LinkedIn): ").strip()
                if not source:
                    break
                
                title = input("Title/Headline: ").strip()
                content = input("Content/Summary: ").strip()
                
                if title and content:
                    competitor_info.append({
                        'source': source,
                        'title': title,
                        'content': content
                    })
            
            if not competitor_info:
                print("❌ No competitor information provided!")
                return
            
            print(f"\n⏳ Analyzing {len(competitor_info)} intelligence items...")
            
            # Combine all intelligence
            combined_intel = ""
            for item in competitor_info:
                combined_intel += f"Source: {item['source']}\nTitle: {item['title']}\nContent: {item['content']}\n\n"
            
            prompt = f"""
            Analyze this competitive intelligence for strategic insights:
            
            {combined_intel}
            
            Provide analysis on:
            1. COMPETITIVE THREATS
            - New capabilities or advantages
            - Market expansion moves
            - Strategic partnerships
            
            2. MARKET OPPORTUNITIES
            - Gaps in competitor offerings
            - Customer pain points
            - Underserved segments
            
            3. STRATEGIC RECOMMENDATIONS
            - Immediate response actions
            - Long-term strategic adjustments
            - Product development priorities
            
            4. MONITORING PRIORITIES
            - Key areas to watch
            - Metrics to track
            - Early warning signals
            
            Focus on actionable business intelligence.
            """
            
            try:
                response = self.model.generate_content(prompt)
                
                print("\n✅ COMPETITIVE INTELLIGENCE ANALYSIS")
                print("=" * 60)
                print(response.text)
                print("=" * 60)
                
                # Save to conversation history
                self.conversation_history.append({
                    'timestamp': datetime.now(),
                    'feature': 'Competitive Intelligence',
                    'input': f"Items analyzed: {len(competitor_info)}",
                    'output': response.text
                })
                
            except Exception as e:
                print(f"❌ Error analyzing competitive intelligence: {e}")
        
        elif intel_choice == '2':
            print("\nCompetitor Feature Comparison")
            
            our_product = input("Our Product/Service: ").strip()
            competitor_product = input("Competitor Product/Service: ").strip()
            
            if not our_product or not competitor_product:
                print("❌ Both product names are required!")
                return
            
            print("\nFeature comparison (press Enter twice when finished):")
            features = []
            while True:
                feature = input("Feature to compare: ").strip()
                if not feature:
                    break
                
                our_capability = input(f"Our capability for {feature}: ").strip()
                their_capability = input(f"Their capability for {feature}: ").strip()
                
                if our_capability and their_capability:
                    features.append({
                        'feature': feature,
                        'our_capability': our_capability,
                        'their_capability': their_capability
                    })
            
            if not features:
                print("❌ No features provided for comparison!")
                return
            
            print("\n⏳ Analyzing feature comparison...")
            
            features_text = ""
            for f in features:
                features_text += f"Feature: {f['feature']}\nOur capability: {f['our_capability']}\nTheir capability: {f['their_capability']}\n\n"
            
            prompt = f"""
            Compare features between our product and competitor:
            
            Our Product: {our_product}
            Competitor: {competitor_product}
            
            Feature Comparison:
            {features_text}
            
            Provide:
            1. Feature-by-feature analysis
            2. Our competitive advantages
            3. Areas where we're behind
            4. Strategic recommendations
            5. Product development priorities
            
            Focus on competitive positioning and strategy.
            """
            
            try:
                response = self.model.generate_content(prompt)
                
                print("\n✅ FEATURE COMPARISON ANALYSIS")
                print("=" * 60)
                print(response.text)
                print("=" * 60)
                
            except Exception as e:
                print(f"❌ Error analyzing feature comparison: {e}")
    
    def general_business_assistant(self):
        """General business assistant for ad-hoc queries."""
        
        print("\n🤖 GENERAL BUSINESS ASSISTANT")
        print("-" * 40)
        print("Ask me anything about business strategy, operations, or best practices!")
        print("Type 'back' to return to main menu.")
        
        while True:
            query = input("\n💼 Your business question: ").strip()
            
            if query.lower() in ['back', 'exit', 'quit']:
                break
            
            if not query:
                print("Please enter a question.")
                continue
            
            print("⏳ Thinking...")
            
            # Enhanced business context prompt
            prompt = f"""
            You are a senior business consultant and strategist. Answer this business question with expert insight:
            
            Question: {query}
            
            Provide:
            - Clear, actionable answer
            - Relevant business context
            - Best practices and frameworks
            - Potential risks and considerations
            - Next steps or recommendations
            
            Use professional business language and provide specific, implementable advice.
            """
            
            try:
                response = self.model.generate_content(prompt)
                
                print("\n✅ BUSINESS CONSULTANT RESPONSE")
                print("=" * 50)
                print(response.text)
                print("=" * 50)
                
                # Save to conversation history
                self.conversation_history.append({
                    'timestamp': datetime.now(),
                    'feature': 'General Business Assistant',
                    'input': query,
                    'output': response.text
                })
                
            except Exception as e:
                print(f"❌ Error generating response: {e}")
    
    def export_conversation(self):
        """Export conversation history to file."""
        
        print("\n💾 EXPORT CONVERSATION")
        print("-" * 40)
        
        if not self.conversation_history:
            print("❌ No conversation history to export!")
            return
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"business_chatbot_session_{timestamp}.json"
        
        # Prepare export data
        export_data = {
            'session_info': {
                'session_start': self.session_start.isoformat(),
                'export_time': datetime.now().isoformat(),
                'total_interactions': len(self.conversation_history)
            },
            'conversation_history': [
                {
                    'timestamp': item['timestamp'].isoformat(),
                    'feature': item['feature'],
                    'input': item['input'],
                    'output': item['output']
                }
                for item in self.conversation_history
            ]
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Conversation exported to: {filename}")
            print(f"📊 Total interactions: {len(self.conversation_history)}")
            
        except Exception as e:
            print(f"❌ Error exporting conversation: {e}")
    
    def show_statistics(self):
        """Show session statistics."""
        
        print("\n📈 SESSION STATISTICS")
        print("-" * 40)
        
        if not self.conversation_history:
            print("❌ No conversation history available!")
            return
        
        # Calculate statistics
        total_interactions = len(self.conversation_history)
        session_duration = datetime.now() - self.session_start
        
        # Feature usage statistics
        feature_usage = {}
        for item in self.conversation_history:
            feature = item['feature']
            feature_usage[feature] = feature_usage.get(feature, 0) + 1
        
        # Most used features
        sorted_features = sorted(feature_usage.items(), key=lambda x: x[1], reverse=True)
        
        print(f"📊 Session Started: {self.session_start.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"⏱️  Session Duration: {session_duration}")
        print(f"🔢 Total Interactions: {total_interactions}")
        print(f"📋 Knowledge Base Documents: {len(self.knowledge_base)}")
        
        print("\n🏆 FEATURE USAGE:")
        for feature, count in sorted_features:
            percentage = (count / total_interactions) * 100
            print(f"  {feature}: {count} times ({percentage:.1f}%)")
        
        print("\n📝 RECENT ACTIVITY:")
        for item in self.conversation_history[-3:]:
            print(f"  {item['timestamp'].strftime('%H:%M')} - {item['feature']}")
        
        print("-" * 40)
    
    def run(self):
        """Main chatbot loop."""
        
        print("🚀 Welcome to the Intelligent Business Chatbot!")
        print("This chatbot combines advanced NLP capabilities for business use.")
        print("Select features from the menu or type 'help' for guidance.")
        
        while True:
            try:
                self.display_menu()
                choice = input("\nSelect option (0-9): ").strip()
                
                if choice == '0':
                    print("\n👋 Thank you for using the Intelligent Business Chatbot!")
                    if self.conversation_history:
                        export_choice = input("Would you like to export your conversation? (y/n): ").strip().lower()
                        if export_choice == 'y':
                            self.export_conversation()
                    break
                
                elif choice == '1':
                    self.generate_marketing_copy()
                
                elif choice == '2':
                    self.analyze_document()
                
                elif choice == '3':
                    self.analyze_sentiment()
                
                elif choice == '4':
                    self.knowledge_base_qa()
                
                elif choice == '5':
                    self.generate_business_report()
                
                elif choice == '6':
                    self.competitive_intelligence()
                
                elif choice == '7':
                    self.general_business_assistant()
                
                elif choice == '8':
                    self.export_conversation()
                
                elif choice == '9':
                    self.show_statistics()
                
                elif choice.lower() == 'help':
                    print("\n💡 HELP GUIDE")
                    print("-" * 40)
                    print("This chatbot offers comprehensive business NLP capabilities:")
                    print("1. Marketing: Generate compelling copy for emails, social media, ads")
                    print("2. Analysis: Analyze documents, extract insights, identify action items")
                    print("3. Sentiment: Understand customer feedback and emotions")
                    print("4. Knowledge: Ask questions about company policies and procedures")
                    print("5. Reports: Generate business reports from metrics and data")
                    print("6. Intelligence: Analyze competitor information and market trends")
                    print("7. Assistant: Get expert business advice and strategic guidance")
                    print("8. Export: Save your conversation history for future reference")
                    print("9. Statistics: View session statistics and usage patterns")
                    print("\nTip: Be specific in your queries for better results!")
                
                else:
                    print("❌ Invalid option. Please select 0-9 or type 'help'.")
                
                # Pause before showing menu again
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\n👋 Session interrupted. Goodbye!")
                break
            
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")
                print("Please try again or select a different option.")
                input("Press Enter to continue...")

# Main execution
if __name__ == "__main__":
    try:
        # Initialize and run the chatbot
        chatbot = IntelligentBusinessChatbot()
        chatbot.run()
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        print("Please check your configuration and try again.")
