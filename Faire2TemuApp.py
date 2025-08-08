"""
Faire2Temu Web Application

A Streamlit-based web interface for the Faire2Temu product mapping system.
This provides a user-friendly way for non-technical users to upload files
and generate Temu-compatible product files.

Usage:
    streamlit run Faire2TemuApp.py
"""

import streamlit as st
import pandas as pd
import os
import sys
from pathlib import Path
import subprocess
import tempfile
import shutil
import zipfile
import io

# Add the current directory to Python path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our custom modules
try:
    from category_assigner import CategoryAssigner
    from Faire2Temu import copy_mapped_data
except ImportError as e:
    st.error(f"Error importing modules: {e}")
    st.stop()

def main():
    """Main Streamlit application."""
    
    # Page configuration
    st.set_page_config(
        page_title="Faire2Temu - Product Mapping Tool",
        page_icon="🛍️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header
    st.title("🛍️ Faire2Temu Product Mapping Tool")
    st.markdown("Transform your Faire product data into Temu-compatible upload files")
    
    # Sidebar for navigation
    with st.sidebar:
        st.header("📋 Navigation")
        page = st.selectbox(
            "Choose a page:",
            ["🏠 Home", "📤 Upload & Process", "📊 Category Analysis", "⚙️ Settings", "📖 Help"]
        )
    
    # Page routing
    if page == "🏠 Home":
        show_home_page()
    elif page == "📤 Upload & Process":
        show_upload_page()
    elif page == "📊 Category Analysis":
        show_category_analysis_page()
    elif page == "⚙️ Settings":
        show_settings_page()
    elif page == "📖 Help":
        show_help_page()

def show_home_page():
    """Display the home page with overview and quick start."""
    
    st.header("Welcome to Faire2Temu!")
    
    # Overview
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### What is Faire2Temu?
        
        Faire2Temu is an intelligent product mapping tool that transforms your Faire product data 
        into Temu-compatible upload files. It automatically:
        
        - 📋 Maps product information to Temu's required format
        - 🏷️ Assigns appropriate categories based on product names
        - 💰 Calculates optimal pricing strategies
        - 🖼️ Processes product images and variations
        - 📦 Splits products into appropriate categories (handbags vs other)
        
        ### Quick Start
        1. Go to **📤 Upload & Process** page
        2. Upload your Faire products Excel file
        3. Click **Process Files** button
        4. Download your Temu-ready files
        """)
    
    with col2:
        st.info("""
        **System Status:**
        - ✅ Category Assigner: Ready
        - ✅ Main Processor: Ready
        - ✅ Template Files: Ready
        
        **Available Categories:** 18
        **Default Category:** 29153
        """)
    
    # Recent activity
    st.subheader("📈 Recent Activity")
    
    # Check for recent output files
    output_dir = Path("output")
    if output_dir.exists():
        recent_files = []
        for file in output_dir.glob("*.xlsx"):
            if file.stat().st_mtime > (pd.Timestamp.now() - pd.Timedelta(days=7)).timestamp():
                recent_files.append({
                    "name": file.name,
                    "size": f"{file.stat().st_size / 1024:.1f} KB",
                    "modified": pd.Timestamp.fromtimestamp(file.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
                })
        
        if recent_files:
            df = pd.DataFrame(recent_files)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No recent files found. Process some data to see activity here!")
    else:
        st.info("Output directory not found. Create some files to see activity here!")
    
    # Version timestamp
    st.markdown("---")
    st.caption("🕒 **Last Updated:** 08-08-2025 15:45:00 - Version 2.3 (Unicode Encoding Fix)")
    st.caption("📝 **Current Features:** Persistent download buttons, ZIP download, alphabetical sorting, Unicode encoding fix")

def show_upload_page():
    """Display the file upload and processing page."""
    
    st.header("📤 Upload & Process Files")
    
    # File upload section
    st.subheader("1. Upload Your Faire Products File")
    
    st.info("""
    **📋 What to Upload:**
    - Upload your **Faire products export** (Excel file from Faire)
    - The **Temu template** is already configured and will be used automatically
    - You only need to upload your product data file
    """)
    
    uploaded_file = st.file_uploader(
        "Choose your Faire products Excel file:",
        type=['xlsx', 'xls'],
        help="Upload your exported Faire products file (Excel format)"
    )
    
    if uploaded_file is not None:
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        
        # Show file info
        file_info = {
            "Name": uploaded_file.name,
            "Size": f"{uploaded_file.size / 1024:.1f} KB",
            "Type": uploaded_file.type
        }
        
        col1, col2 = st.columns(2)
        with col1:
            st.json(file_info)
        
        with col2:
            # Preview the uploaded file
            try:
                df = pd.read_excel(uploaded_file)
                st.write(f"**Preview:** {len(df)} rows, {len(df.columns)} columns")
                
                # Show sample data
                if st.checkbox("Show sample data"):
                    st.dataframe(df.head(), use_container_width=True)
                    
            except Exception as e:
                st.error(f"Error reading file: {e}")
    
    # Processing options
    st.subheader("2. Processing Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.checkbox("Generate update files", value=True, help="Create _update.xlsx files for existing products")
        st.checkbox("Show detailed processing logs", value=True, help="Display step-by-step processing information")
    
    with col2:
        st.checkbox("Auto-categorize products", value=True, help="Use intelligent category assignment")
        st.checkbox("Calculate optimal pricing", value=True, help="Apply pricing strategy (1x and 1.25x)")
    
    # Process button
    st.subheader("3. Process Files")
    
    if st.button("🚀 Process Files", type="primary", disabled=uploaded_file is None):
        if uploaded_file is not None:
            process_files(uploaded_file)
        else:
            st.error("Please upload a file first!")

def display_output_files_persistent():
    """Display output files with persistent download buttons that don't disappear."""
    
    # Initialize session state for file persistence
    if 'files_loaded' not in st.session_state:
        st.session_state.files_loaded = False
    
    if 'file_data_cache' not in st.session_state:
        st.session_state.file_data_cache = {}
    
    if 'zip_data' not in st.session_state:
        st.session_state.zip_data = None
    
    # Check for output files
    output_dir = Path("output")
    if output_dir.exists():
        files = sorted(list(output_dir.glob("*.xlsx")), key=lambda x: x.name)
        
        if files:
            # Load files into session state if not already loaded
            if not st.session_state.files_loaded:
                st.info("🔄 Loading files into session state...")
                st.session_state.files_loaded = True
                # Cache file data
                for file in files:
                    try:
                        with open(file, "rb") as f:
                            st.session_state.file_data_cache[file.name] = f.read()
                        st.success(f"✅ Cached {file.name}")
                    except Exception as e:
                        st.error(f"Error reading {file.name}: {e}")
                
                # Create ZIP data
                try:
                    st.info("🔄 Creating ZIP file...")
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                        for file in files:
                            zip_file.write(file, file.name)
                    zip_buffer.seek(0)
                    st.session_state.zip_data = zip_buffer.getvalue()
                    st.success("✅ ZIP file created")
                except Exception as e:
                    st.error(f"Error creating ZIP: {e}")
            
            # Display files section at the top
            st.subheader("📁 Generated Files")
            st.success(f"✅ Found {len(files)} files in output directory")
            
            # Download all as ZIP button
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write("**Download Options:**")
            with col2:
                if st.session_state.zip_data:
                    st.download_button(
                        label="📦 Download All as ZIP",
                        data=st.session_state.zip_data,
                        file_name="temu_output_files.zip",
                        mime="application/zip",
                        key="zip_download_main"
                    )
                else:
                    st.error("❌ ZIP data not available")
            
            # Compact file list with persistent download buttons
            st.write("**Individual Files:**")
            
            # Create a more compact display using cached data
            for i, file in enumerate(files):
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    if file.name in st.session_state.file_data_cache:
                        st.download_button(
                            label=f"📥 {file.name}",
                            data=st.session_state.file_data_cache[file.name],
                            file_name=file.name,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            key=f"download_{file.name}_{i}_{hash(file.name)}"  # Very unique key
                        )
                    else:
                        st.error(f"File data not available for {file.name}")
                
                with col2:
                    try:
                        file_size = file.stat().st_size
                        st.write(f"{file_size / 1024:.1f} KB")
                    except Exception as e:
                        st.write("Unknown")
                
                with col3:
                    try:
                        mtime = file.stat().st_mtime
                        st.write(pd.Timestamp.fromtimestamp(mtime).strftime("%m-%d %H:%M"))
                    except Exception as e:
                        st.write("Unknown")
                
                with col4:
                    st.write("✅")
            
            # Add a small separator
            st.markdown("---")
            
            # Add refresh option
            if st.button("🔄 Refresh File List", key="refresh_file_list"):
                st.session_state.files_loaded = False
                st.session_state.file_data_cache.clear()
                st.session_state.zip_data = None
                st.rerun()
            
        else:
            st.warning("⚠️ No Excel files found in output directory.")
            st.info("💡 Process some data to see generated files here!")
    else:
        st.error(f"❌ Output directory does not exist: {output_dir.absolute()}")

def ready_to_download():
    """Check if files are ready to download based on session state."""
    return st.session_state.get('files_loaded', False)

def display_output_files_separated():
    """Display output files with separated generation and download logic."""
    
    # Initialize session state
    if 'files_processed' not in st.session_state:
        st.session_state.files_processed = False
    
    if 'file_data_cache' not in st.session_state:
        st.session_state.file_data_cache = {}
    
    if 'zip_data' not in st.session_state:
        st.session_state.zip_data = None
    
    # Check for output files
    output_dir = Path("output")
    if output_dir.exists():
        files = sorted(list(output_dir.glob("*.xlsx")), key=lambda x: x.name)
        
        if files:
            # Load files into session state if not already processed
            if not st.session_state.files_processed:
                st.info("🔄 Loading files into session state...")
                st.session_state.files_processed = True
                
                # Cache file data
                for file in files:
                    try:
                        with open(file, "rb") as f:
                            st.session_state.file_data_cache[file.name] = f.read()
                        st.success(f"✅ Cached {file.name}")
                    except Exception as e:
                        st.error(f"Error reading {file.name}: {e}")
                
                # Create ZIP data
                try:
                    st.info("🔄 Creating ZIP file...")
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                        for file in files:
                            zip_file.write(file, file.name)
                    zip_buffer.seek(0)
                    st.session_state.zip_data = zip_buffer.getvalue()
                    st.success("✅ ZIP file created")
                except Exception as e:
                    st.error(f"Error creating ZIP: {e}")
            
            # Display files section at the top
            st.subheader("📁 Generated Files")
            st.success(f"✅ Found {len(files)} files in output directory")
            
            # Download all as ZIP button
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write("**Download Options:**")
            with col2:
                if st.session_state.zip_data:
                    st.download_button(
                        label="📦 Download All as ZIP",
                        data=st.session_state.zip_data,
                        file_name="temu_output_files.zip",
                        mime="application/zip",
                        key="zip_download_separated"
                    )
                else:
                    st.error("❌ ZIP data not available")
            
            # Compact file list with persistent download buttons
            st.write("**Individual Files:**")
            
            # Create a more compact display using cached data
            for i, file in enumerate(files):
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    if file.name in st.session_state.file_data_cache:
                        st.download_button(
                            label=f"📥 {file.name}",
                            data=st.session_state.file_data_cache[file.name],
                            file_name=file.name,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            key=f"download_separated_{file.name}_{i}_{hash(file.name)}"  # Very unique key
                        )
                    else:
                        st.error(f"File data not available for {file.name}")
                
                with col2:
                    try:
                        file_size = file.stat().st_size
                        st.write(f"{file_size / 1024:.1f} KB")
                    except Exception as e:
                        st.write("Unknown")
                
                with col3:
                    try:
                        mtime = file.stat().st_mtime
                        st.write(pd.Timestamp.fromtimestamp(mtime).strftime("%m-%d %H:%M"))
                    except Exception as e:
                        st.write("Unknown")
                
                with col4:
                    st.write("✅")
            
            # Add a small separator
            st.markdown("---")
            
            # Add refresh option
            if st.button("🔄 Refresh File List", key="refresh_file_list_separated"):
                st.session_state.files_processed = False
                st.session_state.file_data_cache.clear()
                st.session_state.zip_data = None
                st.rerun()
            
        else:
            st.warning("⚠️ No Excel files found in output directory.")
            st.info("💡 Process some data to see generated files here!")
    else:
        st.error(f"❌ Output directory does not exist: {output_dir.absolute()}")

def process_files(uploaded_file):
    """Process the uploaded file using the Faire2Temu system."""
    
    # Clear previous file cache when processing new files
    if 'files_processed' in st.session_state:
        st.session_state.files_processed = False
    if 'file_data_cache' in st.session_state:
        st.session_state.file_data_cache.clear()
    if 'zip_data' in st.session_state:
        st.session_state.zip_data = None
    
    # Create a progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Save uploaded file to data directory
        status_text.text("Step 1/4: Saving uploaded file...")
        progress_bar.progress(25)
        
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        temp_file_path = data_dir / "faire_products.xlsx"
        
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"✅ File saved to: {temp_file_path}")
        
        # Step 2: Check if template exists
        status_text.text("Step 2/4: Checking template file...")
        progress_bar.progress(50)
        
        template_path = data_dir / "temu_template.xlsx"
        if not template_path.exists():
            st.error("❌ Template file not found! Please ensure 'data/temu_template.xlsx' exists.")
            return
        
        st.success("✅ Template file found (using pre-configured Temu template)")
        st.info("💡 The Temu template is pre-configured and doesn't need to be uploaded each time.")
        
        # Step 3: Run the mapping process
        status_text.text("Step 3/4: Processing data...")
        progress_bar.progress(75)
        
        # Capture output from the mapping process
        with st.spinner("Processing your data..."):
            try:
                # Run the mapping process and capture output directly
                st.info("🔄 Running Faire2Temu.py script...")
                
                # Force UTF-8 encoding for the subprocess
                my_env = os.environ.copy()
                my_env["PYTHONIOENCODING"] = "utf-8"
                
                result = subprocess.run(
                    [sys.executable, "Faire2Temu.py"],
                    capture_output=True,
                    text=True,
                    encoding='utf-8',  # Explicitly set UTF-8 encoding
                    cwd=os.getcwd(),
                    env=my_env  # Pass the modified environment to the subprocess
                )
                
                
                
                # Display the output in an expandable section
                with st.expander("📋 Processing Log", expanded=True):
                    st.info(f"🔄 Script executed with return code: {result.returncode}")
                    st.info(f"📊 Output captured: {len(result.stdout.split())} lines of stdout, {len(result.stderr.split())} lines of stderr")
                    
                    # Display stdout
                    if result.stdout:
                        st.text("=== STDOUT ===")
                        for line in result.stdout.split('\n'):
                            if line.strip():
                                st.text(line.strip())
                    
                    # Display stderr
                    if result.stderr:
                        st.text("=== STDERR ===")
                        for line in result.stderr.split('\n'):
                            if line.strip():
                                st.text(line.strip())
                
                if result.returncode == 0:
                    st.success("✅ Processing completed successfully!")
                else:
                    st.error(f"❌ Processing failed with return code: {result.returncode}")
                    
            except Exception as e:
                st.error(f"❌ Error during processing: {e}")
        
        # Step 4: Show results
        status_text.text("Step 4/4: Preparing results...")
        progress_bar.progress(100)
        
        # Ensure output directory exists
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        st.success(f"✅ Output directory ready: {output_dir.absolute()}")
        
        # Display generated files at the top using separated method
        display_output_files_separated()
    
    except Exception as e:
        st.error(f"❌ Error: {e}")
    finally:
        progress_bar.empty()
        status_text.empty()

def show_category_analysis_page():
    """Display category analysis and statistics."""
    
    st.header("📊 Category Analysis")
    
    # Initialize category assigner
    try:
        category_assigner = CategoryAssigner()
        
        # Show all available categories
        st.subheader("Available Categories")
        
        categories = category_assigner.get_all_categories()
        
        # Create a DataFrame for better display
        df = pd.DataFrame(categories)
        df.columns = ["Category Code", "Description"]
        
        st.dataframe(df, use_container_width=True)
        
        # Category testing
        st.subheader("Test Category Assignment")
        
        col1, col2 = st.columns(2)
        
        with col1:
            test_product = st.text_input(
                "Enter a product name to test:",
                placeholder="e.g., Women's Leather Belt"
            )
        
        with col2:
            if st.button("🔍 Test Category"):
                if test_product:
                    category_code = category_assigner.determine_category(test_product)
                    category_info = category_assigner.get_category_info(category_code)
                    
                    if category_info:
                        st.success(f"**Assigned Category:** {category_code}")
                        st.info(f"**Description:** {category_info['description']}")
                    else:
                        st.warning(f"**Assigned Category:** {category_code} (Unknown)")
                else:
                    st.error("Please enter a product name to test")
        
        # Batch testing
        st.subheader("Batch Category Testing")
        
        sample_products = st.text_area(
            "Enter multiple product names (one per line):",
            height=150,
            placeholder="Women's Leather Belt\nPet Carrier for Dogs\nKitchen Utensil Set\n..."
        )
        
        if st.button("🔍 Test All Products") and sample_products:
            products = [p.strip() for p in sample_products.split('\n') if p.strip()]
            
            results = []
            for product in products:
                category_code = category_assigner.determine_category(product)
                category_info = category_assigner.get_category_info(category_code)
                description = category_info['description'] if category_info else "Unknown"
                
                results.append({
                    "Product": product,
                    "Category": category_code,
                    "Description": description
                })
            
            df_results = pd.DataFrame(results)
            st.dataframe(df_results, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error loading category assigner: {e}")

def show_settings_page():
    """Display settings and configuration options."""
    
    st.header("⚙️ Settings")
    
    st.subheader("System Information")
    
    # Get system info
    import platform
    import pandas as pd
    
    system_info = {
        "Python Version": platform.python_version(),
        "Platform": platform.platform(),
        "Pandas Version": pd.__version__,
        "Streamlit Version": st.__version__,
        "Working Directory": os.getcwd()
    }
    
    for key, value in system_info.items():
        st.text(f"{key}: {value}")
    
    # File paths
    st.subheader("File Paths")
    
    paths = {
        "Data Directory": "data/",
        "Output Directory": "output/",
        "Faire Products": "data/faire_products.xlsx",
        "Temu Template": "data/temu_template.xlsx"
    }
    
    for path_name, path in paths.items():
        path_obj = Path(path)
        if path_obj.exists():
            st.success(f"✅ {path_name}: {path}")
        else:
            st.error(f"❌ {path_name}: {path} (not found)")
    
    # Configuration
    st.subheader("Configuration")
    
    st.info("""
    **Default Settings:**
    - Default Category: 29153
    - Pricing Strategy: 1x and 1.25x Faire price
    - Shipping Template: NIMA2
    - Country of Origin: Mainland China
    - Province of Origin: Guangdong
    """)

def show_help_page():
    """Display help and documentation."""
    
    st.header("📖 Help & Documentation")
    
    st.subheader("How to Use")
    
    st.markdown("""
    ### Step-by-Step Guide
    
    1. **Prepare Your Data**
       - Export your products from Faire as an Excel file
       - Ensure the file contains required columns (Product Name, Description, SKU, etc.)
    
    2. **Upload & Process**
       - Go to the **📤 Upload & Process** page
       - Upload your Faire products Excel file
       - Click **Process Files** button
       - Wait for processing to complete
    
    3. **Download Results**
       - Download the generated Temu-compatible files
       - Use these files to upload products to Temu
    
    ### Required File Structure
    
    Your Faire products file should contain these columns:
    - Product Name (English)
    - Description (English)
    - SKU
    - On Hand Inventory
    - Made In Country
    - Option 1 Name
    - Option 1 Value
    - Item Weight
    - Item Length
    - Item Width
    - Item Height
    - Product Images (optional)
    
    ### Output Files
    
    The system generates two types of files:
    - **New Product Uploads**: For adding new products to Temu
    - **Product Updates**: For updating existing products (no pricing/quantity)
    
    ### Troubleshooting
    
    **Common Issues:**
    - **File not found errors**: Ensure all required files are in the correct directories
    - **Processing errors**: Check that your Excel file has the required columns
    - **Category assignment issues**: Verify product names contain relevant keywords
    
    **Getting Help:**
    - Check the processing log for detailed error messages
    - Use the Category Analysis page to test category assignment
    - Ensure your template file is up to date
    """)
    
    st.subheader("Contact & Support")
    
    st.info("""
    **For technical support or questions:**
    - Check the processing logs for error details
    - Verify file formats and column names
    - Test category assignment with sample products
    """)

if __name__ == "__main__":
    main() 