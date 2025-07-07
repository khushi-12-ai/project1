import streamlit as st
import pandas as pd
#import plotly.graph_objects as go
#from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Energy Consumption Calculator",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .result-container {
        background: linear-gradient(135deg, #f093fb, #f5576c);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-top: 2rem;
    }
    
    .energy-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    
    .stSelectbox > div > div {
        background-color: white;
        border-radius: 10px;
    }
    
    .stTextInput > div > div {
        background-color: white;
        border-radius: 10px;
    }
    
    .stNumberInput > div > div {
        background-color: white;
        border-radius: 10px;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        width: 100%;
        margin-top: 1rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# App header
st.markdown('<h1 class="main-header">⚡ Energy Calculator</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Calculate your home\'s energy consumption</p>', unsafe_allow_html=True)

# Create columns for better layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 👤 Personal Information")
    name = st.text_input("Your Name", placeholder="Enter your name")
    age = st.number_input("Your Age", min_value=1, max_value=120, step=1)
    
with col2:
    st.markdown("### 📍 Location Information")
    city = st.text_input("Your City", placeholder="Enter your city")
    area = st.text_input("Area Name", placeholder="Enter your area")

# Housing information
st.markdown("### 🏠 Housing Information")
col3, col4 = st.columns([1, 1])

with col3:
    housing_type = st.selectbox(
        "Housing Type",
        ["Select Type", "Flat", "Tenament"],
        format_func=lambda x: f"🏠 {x}" if x != "Select Type" else x
    )

with col4:
    facility = st.selectbox(
        "Home Size",
        ["Select Size", "1BHK", "2BHK", "3BHK"],
        format_func=lambda x: f"🏡 {x}" if x != "Select Size" else x
    )

# Appliances section
st.markdown("### 🔌 Appliances")
col5, col6, col7 = st.columns([1, 1, 1])

with col5:
    ac = st.checkbox("❄️ Air Conditioner")
    
with col6:
    fridge = st.checkbox("🧊 Refrigerator")
    
with col7:
    washing_machine = st.checkbox("🌊 Washing Machine")

# Calculate button
if st.button("⚡ Calculate Energy Consumption"):
    # Validation
    if not all([name, age, city, area]) or housing_type == "Select Type" or facility == "Select Size":
        st.error("Please fill in all required fields!")
    else:
        # Calculate energy consumption
        cal_energy = 0
        
        # Base energy calculation based on BHK
        if facility == "1BHK":
            cal_energy += 2 * 0.4 + 2 * 0.8  # 2.4
        elif facility == "2BHK":
            cal_energy += 3 * 0.4 + 3 * 0.8  # 3.6
        elif facility == "3BHK":
            cal_energy += 4 * 0.4 + 4 * 0.8  # 4.8
        
        # Add appliance energy
        appliance_energy = 0
        appliances_used = []
        
        if ac:
            appliance_energy += 3
            appliances_used.append("Air Conditioner")
        if fridge:
            appliance_energy += 3
            appliances_used.append("Refrigerator")
        if washing_machine:
            appliance_energy += 3
            appliances_used.append("Washing Machine")
        
        cal_energy += appliance_energy
        
        # Display results
        st.markdown(f"""
        <div class="result-container">
            <div style="font-size: 2rem; margin-bottom: 1rem;">🔋</div>
            <div><strong>Hello {name}!</strong></div>
            <div>Your estimated energy consumption is</div>
            <div class="energy-value">{cal_energy:.1f} kWh</div>
            <div style="font-size: 0.9rem;">Based on your {facility} {housing_type.lower()} in {city}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Energy breakdown chart
        st.markdown("### 📊 Energy Breakdown")
        
        # Create data for visualization
        base_energy = cal_energy - appliance_energy
        
        fig = go.Figure()
        
        # Add base energy
        fig.add_trace(go.Bar(
            name='Base Energy (Lighting & Basic)',
            x=['Energy Consumption'],
            y=[base_energy],
            marker_color='#667eea',
            text=f'{base_energy:.1f} kWh',
            textposition='inside'
        ))
        
        # Add appliance energy
        if appliance_energy > 0:
            fig.add_trace(go.Bar(
                name='Appliances',
                x=['Energy Consumption'],
                y=[appliance_energy],
                marker_color='#f093fb',
                text=f'{appliance_energy:.1f} kWh',
                textposition='inside'
            ))
        
        fig.update_layout(
            title='Energy Consumption Breakdown',
            xaxis_title='Category',
            yaxis_title='Energy (kWh)',
            barmode='stack',
            height=400,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed breakdown
        st.markdown("### 📋 Detailed Breakdown")
        
        breakdown_data = {
            'Category': ['Base Energy (Lighting & Basic)', 'Appliances', 'Total'],
            'Energy (kWh)': [base_energy, appliance_energy, cal_energy],
            'Percentage': [
                f"{(base_energy/cal_energy)*100:.1f}%",
                f"{(appliance_energy/cal_energy)*100:.1f}%",
                "100.0%"
            ]
        }
        
        df = pd.DataFrame(breakdown_data)
        st.dataframe(df, use_container_width=True)
        
        # Energy saving tips
        st.markdown("### 💡 Energy Saving Tips")
        
        tips = [
            "🔆 Use LED bulbs instead of incandescent bulbs",
            "🌡️ Set AC temperature to 24°C or higher",
            "🔌 Unplug electronic devices when not in use",
            "🪟 Use natural light during the day",
            "🧊 Keep refrigerator at optimal temperature (3-4°C)",
            "👔 Use cold water for washing clothes when possible"
        ]
        
        for tip in tips:
            st.markdown(f"- {tip}")
        
        # Summary card
        st.markdown("### 📈 Summary")
        col8, col9, col10 = st.columns([1, 1, 1])
        
        with col8:
            st.metric("Total Energy", f"{cal_energy:.1f} kWh")
        
        with col9:
            st.metric("Base Energy", f"{base_energy:.1f} kWh")
        
        with col10:
            st.metric("Appliance Energy", f"{appliance_energy:.1f} kWh")
        
        # Appliances used
        if appliances_used:
            st.markdown("### 🔌 Appliances Included")
            for appliance in appliances_used:
                st.markdown(f"✅ {appliance}")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; font-size: 0.9rem;'>"
    "💡 Energy Calculator - Calculate your home's energy consumption efficiently"
    "</div>",
    unsafe_allow_html=True
)

# Sidebar information
with st.sidebar:
    st.markdown("### ℹ️ About")
    st.markdown("""
    This Energy Calculator helps you estimate your home's energy consumption based on:
    
    - **Home Size**: 1BHK, 2BHK, or 3BHK
    - **Appliances**: AC, Refrigerator, Washing Machine
    - **Base Energy**: Lighting and basic electrical needs
    
    The calculation uses standard energy consumption rates for different home sizes and appliances.
    """)
    
    st.markdown("### 🔧 How to Use")
    st.markdown("""
    1. Fill in your personal information
    2. Select your housing type and size
    3. Check the appliances you use
    4. Click 'Calculate Energy Consumption'
    5. View your results and energy breakdown
    """)
    
    st.markdown("### 📊 Energy Units")
    st.markdown("""
    - **kWh**: Kilowatt-hour (unit of energy)
    - **Base Energy**: 0.4 kWh per room (lighting) + 0.8 kWh per room (basic appliances)
    - **Major Appliances**: 3 kWh each (AC, Fridge, Washing Machine)
    """)
