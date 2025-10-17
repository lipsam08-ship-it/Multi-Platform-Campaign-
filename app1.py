import streamlit as st
import pandas as pd
import json
import datetime
from typing import List, Dict

# Page configuration
st.set_page_config(
    page_title="Multi-Platform Campaign Builder",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .platform-card {
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        background-color: #f0f2f6;
        margin-bottom: 1rem;
    }
    .campaign-phase {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

class CampaignBuilder:
    def __init__(self):
        self.platforms = ["Instagram", "TikTok", "Email", "Twitter", "LinkedIn", "Facebook"]
        self.campaign_phases = ["Awareness", "Consideration", "Conversion", "Retention"]
        
    def generate_prompt_sequence(self, campaign_data: Dict) -> List[Dict]:
        """Generate sequential prompts based on campaign parameters"""
        prompts = []
        
        # Safely get values with defaults to prevent KeyError
        product_name = campaign_data.get('product_name', 'Your Product')
        target_audience = campaign_data.get('target_audience', 'your target audience')
        key_message = campaign_data.get('key_message', 'your key message')
        selected_platforms = campaign_data.get('selected_platforms', ['Instagram', 'TikTok'])
        campaign_phases = campaign_data.get('campaign_phases', ['Awareness'])

        # Phase 1: Foundation
        prompts.append({
            "phase": "Foundation",
            "platform": "All",
            "prompt": f"""Act as a senior marketing strategist. Create a multi-platform campaign for:
            
Product: {product_name}
Target Audience: {target_audience}
Key Message: {key_message}
Platforms: {', '.join(selected_platforms)}

Propose a weekly strategy with specific goals for each platform."""
        })
        
        # Phase 2: Platform-specific content
        for platform in selected_platforms:
            prompts.append({
                "phase": "Content Creation",
                "platform": platform,
                "prompt": f"""For {platform}, generate 3-5 content ideas for the {campaign_phases[0] if campaign_phases else 'Awareness'} phase targeting {target_audience}. Focus on:
- Platform-best practices for {platform}
- Content format recommendations
- Hashtag strategy
- Engagement tactics"""
            })
        
        # Phase 3: Asset creation
        prompts.append({
            "phase": "Asset Development",
            "platform": "All",
            "prompt": f"""Create specific copy and content guidelines for:
Product: {product_name}

Include:
- 5 email subject lines
- 3 Instagram carousel concepts
- 2 TikTok script outlines
- Social media post templates"""
        })
        
        return prompts

def main():
    st.markdown('<div class="main-header">🚀 Multi-Platform Campaign Builder</div>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'campaign_data' not in st.session_state:
        st.session_state.campaign_data = {}
    if 'prompts' not in st.session_state:
        st.session_state.prompts = []
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0
    
    builder = CampaignBuilder()
    
    # Sidebar for navigation
    with st.sidebar:
        st.header("Campaign Builder Steps")
        steps = ["Campaign Foundation", "Platform Selection", "Content Strategy", "Prompt Generation", "Execution Plan"]
        
        for i, step in enumerate(steps):
            if st.button(step, key=f"step_{i}", use_container_width=True):
                st.session_state.current_step = i
        
        st.markdown("---")
        st.header("Quick Actions")
        if st.button("Reset Campaign", type="secondary"):
            st.session_state.campaign_data = {}
            st.session_state.prompts = []
            st.session_state.current_step = 0
            st.rerun()
    
    # Step 1: Campaign Foundation
    if st.session_state.current_step == 0:
        st.header("🎯 Campaign Foundation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.campaign_data['product_name'] = st.text_input(
                "Product/Service Name",
                placeholder="EcoVibe Reusable Bottles"
            )
            
            st.session_state.campaign_data['target_audience'] = st.text_area(
                "Target Audience",
                placeholder="Eco-conscious millennials and Gen Z, aged 18-30, interested in sustainability..."
            )
            
            st.session_state.campaign_data['campaign_duration'] = st.selectbox(
                "Campaign Duration",
                ["2 weeks", "4 weeks", "6 weeks", "8 weeks"]
            )
        
        with col2:
            st.session_state.campaign_data['key_message'] = st.text_area(
                "Key Message",
                placeholder="Stylish sustainability for the modern eco-warrior..."
            )
            
            st.session_state.campaign_data['campaign_goal'] = st.selectbox(
                "Primary Campaign Goal",
                ["Brand Awareness", "Lead Generation", "Product Launch", "Engagement", "Sales Conversion"]
            )
            
            st.session_state.campaign_data['budget_tier'] = st.selectbox(
                "Budget Tier",
                ["Bootstrapped", "Moderate", "Amplified", "Enterprise"]
            )
        
        if st.button("Save Foundation & Continue", type="primary"):
            st.session_state.current_step = 1
            st.rerun()
    
    # Step 2: Platform Selection
    elif st.session_state.current_step == 1:
        st.header("📱 Platform Selection")
        
        st.subheader("Choose Your Platforms")
        selected_platforms = []
        
        cols = st.columns(3)
        for i, platform in enumerate(builder.platforms):
            with cols[i % 3]:
                if st.checkbox(platform, key=f"platform_{platform}"):
                    selected_platforms.append(platform)
        
        st.session_state.campaign_data['selected_platforms'] = selected_platforms
        
        if selected_platforms:
            st.subheader("Platform Strategy Overview")
            for platform in selected_platforms:
                with st.expander(f"{platform} Strategy"):
                    st.text_area(
                        f"Specific goals for {platform}",
                        placeholder=f"What do you want to achieve on {platform}?",
                        key=f"goal_{platform}"
                    )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", use_container_width=True):
                st.session_state.current_step = 0
                st.rerun()
        with col2:
            if st.button("Continue to Content Strategy →", type="primary", use_container_width=True):
                st.session_state.current_step = 2
                st.rerun()
    
    # Step 3: Content Strategy
    elif st.session_state.current_step == 2:
        st.header("📝 Content Strategy")
        
        st.subheader("Campaign Phases")
        selected_phases = st.multiselect(
            "Select campaign phases:",
            builder.campaign_phases,
            default=builder.campaign_phases
        )
        
        st.session_state.campaign_data['campaign_phases'] = selected_phases
        
        if selected_phases:
            for phase in selected_phases:
                with st.expander(f"Phase: {phase}", expanded=True):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.text_input(
                            f"{phase} Goal",
                            placeholder=f"Primary objective for {phase} phase",
                            key=f"goal_{phase}"
                        )
                        
                        st.text_area(
                            f"{phase} Key Messages",
                            placeholder="Main talking points...",
                            key=f"messages_{phase}"
                        )
                    
                    with col2:
                        st.text_area(
                            f"{phase} Call-to-Action",
                            placeholder="What should users do?",
                            key=f"cta_{phase}"
                        )
                        
                        st.multiselect(
                            f"{phase} Content Types",
                            ["Video", "Images", "Carousels", "Stories", "Blog Posts", "Emails"],
                            key=f"types_{phase}"
                        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", use_container_width=True):
                st.session_state.current_step = 1
                st.rerun()
        with col2:
            if st.button("Generate Prompts →", type="primary", use_container_width=True):
                st.session_state.current_step = 3
                st.rerun()
    
    # Step 4: Prompt Generation
    elif st.session_state.current_step == 3:
        st.header("🤖 Sequential Prompt Generation")
        
        if not st.session_state.prompts:
            st.session_state.prompts = builder.generate_prompt_sequence(st.session_state.campaign_data)
        
        st.success(f"Generated {len(st.session_state.prompts)} sequential prompts for your campaign!")
        
        # Display prompts in sequence
        for i, prompt_data in enumerate(st.session_state.prompts):
            with st.container():
                st.markdown(f"""
                <div class="campaign-phase">
                    <h4>Step {i+1}: {prompt_data['phase']} - {prompt_data['platform']}</h4>
                </div>
                """, unsafe_allow_html=True)
                
                st.text_area(
                    f"Prompt {i+1}",
                    value=prompt_data['prompt'],
                    height=150,
                    key=f"prompt_{i}"
                )
                
                col1, col2 = st.columns([3, 1])
                with col2:
                    if st.button("Copy Prompt", key=f"copy_{i}"):
                        st.code(prompt_data['prompt'], language=None)
                        st.success("Prompt copied to clipboard!")
        
        # Execution plan generation
        st.subheader("🎯 Campaign Execution Plan")
        
        if st.button("Generate Campaign Timeline", type="primary"):
            timeline_data = []
            start_date = datetime.date.today()
            
            for i, phase in enumerate(st.session_state.campaign_data.get('campaign_phases', [])):
                for j, platform in enumerate(st.session_state.campaign_data.get('selected_platforms', [])):
                    timeline_data.append({
                        "Week": f"Week {i+1}",
                        "Phase": phase,
                        "Platform": platform,
                        "Task": f"Create {platform} content for {phase}",
                        "Status": "Planned"
                    })
            
            timeline_df = pd.DataFrame(timeline_data)
            st.dataframe(timeline_df, use_container_width=True)
            
            # Download option
            csv = timeline_df.to_csv(index=False)
            st.download_button(
                label="Download Timeline as CSV",
                data=csv,
                file_name="campaign_timeline.csv",
                mime="text/csv"
            )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", use_container_width=True):
                st.session_state.current_step = 2
                st.rerun()
        with col2:
            if st.button("View Final Plan →", type="primary", use_container_width=True):
                st.session_state.current_step = 4
                st.rerun()
    
    # Step 5: Final Plan
    elif st.session_state.current_step == 4:
        st.header("✅ Campaign Execution Plan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Campaign Summary")
            st.json(st.session_state.campaign_data)
            
            st.subheader("Generated Prompts")
            st.info(f"Total prompts generated: {len(st.session_state.prompts)}")
            
            for i, prompt in enumerate(st.session_state.prompts):
                with st.expander(f"Prompt {i+1}: {prompt['phase']}"):
                    st.write(prompt['prompt'])
        
        with col2:
            st.subheader("Quick Start Guide")
            
            st.markdown("""
            1. **Start with Foundation Prompt** - Get overall strategy
            2. **Move to Platform-specific Prompts** - Generate tailored content
            3. **Use Asset Development Prompts** - Create actual copy and visuals
            4. **Execute in Sequence** - Follow the generated timeline
            """)
            
            st.subheader("Next Steps")
            st.markdown("""
            - Copy prompts to your preferred AI tool
            - Refine outputs based on your brand voice
            - Set up your content calendar
            - Begin execution according to timeline
            """)
            
            # Export campaign data
            if st.button("Export Campaign Plan", type="primary"):
                campaign_export = {
                    "campaign_data": st.session_state.campaign_data,
                    "prompts": st.session_state.prompts,
                    "generated_at": str(datetime.datetime.now())
                }
                
                st.download_button(
                    label="Download JSON Export",
                    data=json.dumps(campaign_export, indent=2),
                    file_name="campaign_plan.json",
                    mime="application/json"
                )
        
        if st.button("Start New Campaign", type="secondary"):
            st.session_state.campaign_data = {}
            st.session_state.prompts = []
            st.session_state.current_step = 0
            st.rerun()

if __name__ == "__main__":
    main()
