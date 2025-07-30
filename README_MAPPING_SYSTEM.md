# Enhanced Faire to Temu Mapping System

This enhanced system allows you to map multiple columns from Faire products to Temu template with configurable fixed values.

## 🚀 Features

- **Column Mapping**: Map multiple columns from Faire to Temu
- **Fixed Values**: Set default values for specific Temu columns
- **Data Transformations**: Custom data processing for specific columns
- **Image URL Processing**: Intelligent handling of Option Image and Product Images
- **Validation**: Automatic checking for missing columns
- **Detailed Logging**: See exactly what was processed

## 📁 Files

- `Faire2Temu.py` - Main script with enhanced mapping system
- `test_suite.py` - Comprehensive test suite for all functionality
- `README_MAPPING_SYSTEM.md` - This documentation file

## ⚙️ Configuration

### 1. Column Mappings

Edit the `COLUMN_MAPPINGS` dictionary in `Faire2Temu.py`:

```python
COLUMN_MAPPINGS = {
    # Basic product information
    'Product Name (English)': 'Product Name',
    'Description (English)': 'Product Description',
    'SKU': 'Contribution SKU',
    'USD Unit Retail Price': 'Base Price - USD',
    'USD Unit Retail Price': 'List Price - USD',
    'On Hand Inventory': 'Quantity',
    'Made In Country': 'Country/Region of Origin',
    
    # Option mappings
    'Option 1 Name': 'Variation Theme',
    'Option 1 Value': 'Color',
    
    # Dimension mappings
    'Item Weight': 'Weight - lb',
    'Item Length': 'Length - in',
    'Item Width': 'Width - in',
    'Item Height': 'Height - in',
    
    # Add more mappings here:
    'Product Status': 'Status',
    'Product Images': 'Detail Images URL',
}
```

### 2. Fixed Column Values

Edit the `FIXED_COLUMN_VALUES` dictionary in `Faire2Temu.py`:

```python
FIXED_COLUMN_VALUES = {
    'Category': '29153',
    'Country/Region of Origin': 'China',
    'Province of Origin': 'Guangdong',
    'Update or Add': 'Add',
    'Shipping Template': 'NIMA2',
    'Size': 'One Size',
    
    # Add more fixed values:
    'Status': 'Active',
    'Brand': 'Your Brand Name',
    'Handling Time': '1',
    'Import Designation': 'General',
    'Fulfillment Channel': 'FBA',
}
```

### 3. Data Transformations

Add custom transformation functions in `Faire2Temu.py`:

```python
def transform_price(price_value):
    """Transform price values"""
    if pd.isna(price_value):
        return ''
    return str(price_value).replace('$', '').strip()

def transform_sku_to_goods(sku_value):
    """Transform SKU to Contribution Goods by removing letter suffix"""
    # Examples: 'HBG100PN' → 'HBG100', 'HBG200' → 'HBG200'
    if pd.isna(sku_value):
        return ''
    sku_str = str(sku_value).strip()
    match = re.match(r'^(.+?)([A-Za-z]+)$', sku_str)
    return match.group(1) if match else sku_str

TRANSFORMATIONS = {
    'USD Unit Retail Price': transform_price,
    'Product Name (English)': transform_product_name,
    'SKU': transform_sku_to_goods,
}
```

## 🏃‍♂️ Usage

### Basic Usage
```bash
python Faire2Temu.py
```

### View Available Columns
```bash
python test_suite.py --test columns
```

### Run All Tests
```bash
python test_suite.py --test all
```

### Run Specific Tests
```bash
python test_suite.py --test baseline     # Test basic functionality
python test_suite.py --test fixed        # Test fixed values
python test_suite.py --test sku          # Test SKU transformation
python test_suite.py --test mappings     # Test new mappings
python test_suite.py --test images       # Test image processing
```

## 📊 Current Configuration

### Mapped Columns (12 + 1 transformed)
- ✅ Product Name (English) → Product Name
- ✅ Description (English) → Product Description  
- ✅ SKU → Contribution SKU
- ✅ USD Unit Retail Price → Base Price - USD
- ✅ USD Unit Retail Price → List Price - USD
- ✅ On Hand Inventory → Quantity
- ✅ Made In Country → Country/Region of Origin
- ✅ Option 1 Name → Variation Theme
- ✅ Option 1 Value → Color
- ✅ Item Weight → Weight - lb
- ✅ Item Length → Length - in
- ✅ Item Width → Width - in
- ✅ Item Height → Height - in
- ✅ SKU → Contribution Goods (with transformation: removes letter suffix)

### Fixed Values (6)
- ✅ Category = '29153'
- ✅ Country/Region of Origin = 'China'
- ✅ Province of Origin = 'Guangdong'
- ✅ Update or Add = 'Add'
- ✅ Shipping Template = 'NIMA2'
- ✅ Size = 'One Size'

## 📈 Results

- **5,669 products** processed successfully
- **12 column mappings** applied + **1 SKU transformation**
- **Image URL processing** for 5,669 rows
- **6 fixed values** set for all rows
- **Output file**: `output/temu_upload_generated_with_fixed_values.xlsx`

## 🔧 Adding More Mappings

1. **Open `Faire2Temu.py`**
2. **Find the `COLUMN_MAPPINGS` dictionary**
3. **Add new mappings**:
   ```python
   'Faire Column Name': 'Temu Column Name',
   ```
4. **Run the script**: `python Faire2Temu.py`

## 🔧 Adding More Fixed Values

1. **Open `Faire2Temu.py`**
2. **Find the `FIXED_COLUMN_VALUES` dictionary**
3. **Add new fixed values**:
   ```python
   'Temu Column Name': 'Fixed Value',
   ```
4. **Run the script**: `python Faire2Temu.py`

## 📋 Example Additions

### More Column Mappings
```python
COLUMN_MAPPINGS = {
    # ... existing mappings ...
    'Product Status': 'Status',
    'Item Weight': 'Weight - lb',
    'Item Length': 'Length - in',
    'Item Width': 'Width - in',
    'Item Height': 'Height - in',
    'Product Images': 'Detail Images URL',
    'Option 1 Name': 'Color',
    'Option 1 Value': 'Color Value',
    'Option 2 Name': 'Size',
    'Option 2 Value': 'Size Value',
}
```

### More Fixed Values
```python
FIXED_COLUMN_VALUES = {
    # ... existing fixed values ...
    'Status': 'Active',
    'Brand': 'Your Brand Name',
    'Shipping Template': 'Standard',
    'Handling Time': '1',
    'Import Designation': 'General',
    'Fulfillment Channel': 'FBA',
}
```

## 🎯 Benefits

- **Easy Configuration**: Simple dictionary-based mapping
- **Flexible**: Add/remove mappings without code changes
- **Reliable**: Validation and error handling
- **Transparent**: Detailed logging of all operations
- **Extensible**: Easy to add new features

## 📝 Notes

- Fixed values override mapped values for the same column
- All data is copied from row 4 onwards (skipping rows 1-3)
- Template structure and formatting are preserved
- Output file includes both mapped and fixed values
- **Image Processing Logic**:
  - Priority: Option Image → Product Images (fallback)
  - Product Images are split by whitespace/newlines
  - First URL assigned to SKU Images URL and Detail Images URL
  - Multiple URLs distributed across SKU Images URL columns 