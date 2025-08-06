# Faire2Temu - Enhanced Product Mapping System

A comprehensive tool for mapping Faire product data to Temu's upload format with intelligent category assignment and modular architecture.

## 🏗️ **System Architecture**

The system is now organized into modular components for better maintainability and extensibility:

```
Faire2Temu/
├── Faire2Temu.py              # Main orchestrator (717 lines)
├── category_assigner.py        # Enhanced category logic (300+ lines)
├── Faire2TemuApp.py           # Web interface (400+ lines)
├── start_web_app.bat          # Easy startup script
├── data/
│   ├── faire_products.xlsx     # Source Faire data
│   └── temu_template.xlsx      # Temu template
├── output/
│   ├── temu_template_handbags.xlsx      # New product uploads
│   ├── temu_template_other.xlsx         # New product uploads
│   ├── temu_template_handbags_update.xlsx # Product updates
│   └── temu_template_other_update.xlsx    # Product updates
└── README_MAPPING_SYSTEM.md   # This documentation
```

## 📋 **Module Overview**

### **1. Faire2Temu.py (Main Orchestrator)**
- **Purpose**: Coordinates the entire mapping process
- **Responsibilities**:
  - Data loading and validation
  - Column mapping and transformation
  - File processing and Excel manipulation
  - Pricing calculations
  - Category splitting by SKU prefixes
- **Size**: 717 lines, 33KB
- **Key Functions**:
  - `copy_mapped_data()`: Main processing function
  - `process_product_category()`: Handles individual categories
  - `transform_*()`: Data transformation functions

### **2. category_assigner.py (Enhanced Category Logic)**
- **Purpose**: Intelligent category assignment based on product names and image data
- **Responsibilities**:
  - Keyword-based category matching
  - Support for 18+ category types
  - Image data analysis (future enhancement)
  - Category information lookup
- **Size**: 300+ lines
- **Key Features**:
  - 18 different category rules with AND/OR logic
  - Case-insensitive keyword matching
  - Priority-based matching (first match wins)
  - Extensible rule system

### **3. Faire2TemuApp.py (Web Interface)**
- **Purpose**: User-friendly web interface for non-technical users
- **Responsibilities**:
  - File upload and processing
  - Real-time progress tracking
  - Category testing and analysis
  - System status monitoring
- **Size**: 400+ lines
- **Key Features**:
  - Drag-and-drop file upload
  - Progress bars and status updates
  - Interactive category testing
  - Download buttons for generated files
  - Comprehensive help and documentation

## 🔧 **How It Works**

### **Data Flow:**
1. **Load Data**: Read Faire products and Temu template
2. **Split by Category**: Group products by SKU prefixes (handbags vs other)
3. **Process Each Category**: Apply mappings and transformations
4. **Assign Categories**: Use intelligent category assignment
5. **Generate Files**: Create upload-ready Excel files

### **Category Assignment Process:**
```
Product Name → category_assigner.py → Category Code
"Women's Leather Belt" → Rule Matching → "29264"
"Pet Carrier for Dogs" → Rule Matching → "2062"
"Kitchen Utensil Set" → Rule Matching → "9923"
```

### **Available Categories:**
- **2062**: Pet Supplies / Small Animals / Carriers
- **9923**: Home & Kitchen / Kitchen Utensils & Gadgets
- **11809**: Home & Kitchen / Bath / Towels
- **19843**: Beauty & Personal Care / Nail Tools
- **24380**: Cell Phones & Accessories / Cases
- **29264**: Women / Accessories / Belts
- **29290**: Women / Accessories / Scarves
- **29312**: Women / Accessories / Eyewear Cases
- **29324**: Women / Accessories / Wallets
- **29522**: Women / Jewelry / Brooches
- **29542**: Women / Jewelry / Necklaces
- **30988**: Luggage & Travel / Cosmetic Cases
- **36256**: Sports & Outdoors / Pickleball
- **39969**: Arts & Crafts / Pen Cases
- **46208**: Books / Children's Books
- **29163**: Tote Bags (legacy)
- **29164**: Backpacks (legacy)
- **29165**: Wallets (legacy)

## 🚀 **Usage**

### **Web Interface (Recommended for Non-Technical Users):**
```bash
# Option 1: Double-click the batch file
start_web_app.bat

# Option 2: Run directly with streamlit
streamlit run Faire2TemuApp.py
```

### **Command Line Usage (For Technical Users):**
```bash
# Default: Filter products with stock > 0
python Faire2Temu.py

# Stock filtering options
python Faire2Temu.py --filter-stock     # Enable stock filtering (default)
python Faire2Temu.py --no-filter-stock  # Disable stock filtering (process all products)
python Faire2Temu.py -f                 # Short form: enable stock filtering
python Faire2Temu.py -F                 # Short form: disable stock filtering
python Faire2Temu.py --help             # Show all options
```

### **Testing Category Logic:**
```bash
python category_assigner.py
```

### **Web Interface Features:**
- 🖥️ **Home Dashboard**: System status and recent activity
- 📤 **Upload & Process**: Drag-and-drop file upload with progress tracking
- 📊 **Category Analysis**: Test category assignment and view all available categories
- ⚙️ **Settings**: System information and file path verification
- 📖 **Help**: Comprehensive documentation and troubleshooting guide

### **Command Line Expected Output:**
```
Starting enhanced mapping tool...
Mapping 8 columns
Setting 6 fixed values
Categories: ['handbags', 'other']
Enhanced category rules: 18 categories available

Loading Faire products file...
Loading Temu template...
Validating column mappings...

Category breakdown:
  Handbags: 150 products (Handbags, Wallets, Cosmetic Bags, Travel Bags)
  Other: 75 products (All other products)

Processing handbags products...
  Mapping: Product Name (English) -> Product Name
  Mapping: Description (English) -> Product Description
  ...
  Applying enhanced category assignment...
  Category assignments:
    29264 (Women / Accessories / Belts): 25 products
    29324 (Women / Accessories / Wallets): 30 products
    29153 (Default): 95 products

Success! Output files saved to:
  Handbags: output/temu_template_handbags.xlsx
  Other: output/temu_template_other.xlsx
```

## 📁 **File Types Generated**

### **New Product Upload Files:**
- `temu_template_handbags.xlsx`: Handbags, wallets, cosmetic bags
- `temu_template_other.xlsx`: All other products

### **Product Update Files:**
- `temu_template_handbags_update.xlsx`: Update version (no pricing/quantity)
- `temu_template_other_update.xlsx`: Update version (no pricing/quantity)

## 🔧 **Configuration**

### **Stock Filtering:**
The script now includes optional stock filtering to only process products with inventory > 0:

- **Default behavior**: Only processes products with stock > 0
- **Disable filtering**: Use `--no-filter-stock` to process all products
- **Filtering statistics**: Shows total products, in-stock count, and filtered count

**Example output with filtering:**
```
Stock filtering: ENABLED
Filtering products with stock > 0...
  Total products: 5669
  Products with stock > 0: 5251
  Products filtered out: 418
```

**Example output without filtering:**
```
Stock filtering: DISABLED
Stock filtering disabled - processing all products
```

### **Column Mappings** (in Faire2Temu.py):
```python
COLUMN_MAPPINGS = {
    'Product Name (English)': 'Product Name',
    'Description (English)': 'Product Description',
    'SKU': 'Contribution SKU',
    'On Hand Inventory': 'Quantity',
    # ... more mappings
}
```

### **Fixed Values** (in Faire2Temu.py):
```python
FIXED_COLUMN_VALUES = {
    'Category': '29153',  # Default, overridden by category assigner
    'Country/Region of Origin': 'Mainland China',
    'Province of Origin': 'Guangdong',
    'Update or Add': 'Add',
    'Shipping Template': 'NIMA2',
}
```

### **Category Rules** (in category_assigner.py):
```python
{
    'category_code': '29264',
    'description': 'Women / Accessories / Belts',
    'condition': lambda name, img: (
        any(word in name for word in ['women', 'female', 'ladies']) and
        any(word in name for word in ['belt', 'waistband', 'strap'])
    )
}
```

## 🧪 **Testing**

### **Category Logic Testing:**
```bash
python category_assigner.py
```
Expected output:
```
Testing Category Assigner:
==================================================
✅ Women's Leather Belt -> 29264 (expected: 29264)
✅ Pet Carrier for Dogs -> 2062 (expected: 2062)
✅ Kitchen Utensil Set -> 9923 (expected: 9923)
...
```

### **Integration Testing:**
```bash
python Faire2Temu.py
```

## 🔄 **Update Process**

To create update files (for existing products):
1. Run `Faire2Temu.py` to generate base files
2. Run `create_update_files.py` to create `_update.xlsx` versions
3. Update files have:
   - "Update" instead of "Add"
   - Blank Quantity columns
   - Blank Base Price columns
   - Blank List Price columns

## 📈 **Benefits of Modular Architecture**

### **Maintainability:**
- ✅ Category logic isolated in separate module
- ✅ Easy to add new category rules
- ✅ Clear separation of concerns
- ✅ Reduced complexity in main file

### **Extensibility:**
- ✅ Easy to add new category types
- ✅ Support for image data analysis
- ✅ Configurable keyword matching
- ✅ Priority-based rule system

### **Testing:**
- ✅ Each module can be tested independently
- ✅ Category logic has built-in test cases
- ✅ Clear input/output interfaces

### **Documentation:**
- ✅ Self-documenting code structure
- ✅ Clear module responsibilities
- ✅ Comprehensive README

## 🛠️ **Troubleshooting**

### **Common Issues:**

1. **Missing Files:**
   ```
   Error: Could not find a file. Please check your file paths.
   ```
   - Ensure `data/faire_products.xlsx` exists
   - Ensure `data/temu_template.xlsx` exists

2. **Category Assignment Issues:**
   - Check category rules in `category_assigner.py`
   - Test with `python category_assigner.py`
   - Verify product names contain expected keywords

3. **Excel Processing Errors:**
   - Ensure Excel files are not open in other applications
   - Check file permissions
   - Verify template structure matches expected format

### **Debugging:**
- Enable verbose output in `Faire2Temu.py`
- Test individual modules separately
- Check category assignments in output logs

## 🔮 **Future Enhancements**

### **Planned Features:**
- Image data analysis for category assignment
- Machine learning-based category prediction
- Support for more Temu categories
- Batch processing for large datasets
- Web interface for configuration

### **Extensibility Points:**
- Add new category rules in `category_assigner.py`
- Modify column mappings in `Faire2Temu.py`
- Add new transformation functions
- Create additional output formats

---

**Last Updated**: December 2024
**Version**: 2.0 (Modular Architecture)
**Maintainer**: NimaTemu Development Team 