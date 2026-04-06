import streamlit as st
from engine import CacheSimulator # This connects your frontend to your backend!

# 1. Page Setup
st.set_page_config(page_title="Cache Simulator", layout="wide")
st.title("🖥️ CPU Cache Performance Analyzer")
# st.markdown("Developed by: Aditya Parmale (Roll: 24108B0043)")
st.markdown("---")

# 2. Sidebar Controls (Hardware Configuration)
st.sidebar.header("⚙️ Hardware Configuration")

cache_size = st.sidebar.select_slider(
    "Cache Size (Bytes)", 
    options=[1024, 2048, 4096, 8192, 16384, 32768, 65536], 
    value=4096
)

block_size = st.sidebar.select_slider(
    "Block Size (Bytes)", 
    options=[16, 32, 64, 128], 
    value=32
)

associativity = st.sidebar.select_slider(
    "Associativity (Ways)", 
    options=[1, 2, 4, 8, 16], 
    value=4
)
st.sidebar.info("Note: 1-Way Associativity is 'Direct-Mapped'.")

# 3. Main Area (File Upload)
st.subheader("1. Upload Memory Trace")
uploaded_file = st.file_uploader("Upload a .txt file with hex addresses (e.g., 0x1A2B)", type=["txt"])

# 4. The Execution Button
if st.button("🚀 Run Simulation"):
    if uploaded_file is not None:
        # Create a new engine using the slider inputs
        sim = CacheSimulator(cache_size, block_size, associativity)
        
        # Read the uploaded file line by line
        content = uploaded_file.getvalue().decode("utf-8").splitlines()
        
        # Feed every address into your engine
        for line in content:
            clean_addr = line.strip()
            if clean_addr: # Make sure it's not a blank line
                try:
                    sim.access_memory(clean_addr)
                except ValueError:
                    pass # Ignore lines that aren't valid numbers
        
        # 5. Display the Results
        stats = sim.get_stats()
        
        st.markdown("---")
        st.subheader("📊 Simulation Results")
        
        # Create columns for a nice scoreboard layout
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Accesses", f"{stats['Total Accesses']:,}")
        col2.metric("Cache Hits", f"{stats['Hits']:,}")
        col3.metric("Cache Misses", f"{stats['Misses']:,}")
        
        col4, col5 = st.columns(2)
        col4.metric("Hit Rate (%)", f"{stats['Hit Rate (%)']}%")
        col5.metric("Miss Rate (%)", f"{stats['Miss Rate (%)']}%")
        
    else:
        st.warning("⚠️ Please upload a memory trace .txt file first.")