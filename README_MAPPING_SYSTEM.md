# Enhanced Faire to Temu Mapping System

This enhanced system allows you to map multiple columns from Faire products to Temu template with configurable fixed values.

## 🚀 Features

- **Column Mapping**: Map multiple columns from Faire to Temu
- **Fixed Values**: Set default values for specific Temu columns
- **Data Transformations**: Custom data processing for specific columns
- **Validation**: Automatic checking for missing columns
- **Detailed Logging**: See exactly what was processed

## 📁 Files

- `Faire2Temu.py` - Main script with enhanced mapping system
- `show_columns.py` - Helper to view all available columns
- `test_fixed_values.py` - Test script to verify fixed values
- `mapping_example.py` - Examples of additional mappings

## ⚙️ Configuration

### 1. Column Mappings

Edit the `COLUMN_MAPPINGS` dictionary in `Faire2Temu.py`:

```python
COLUMN_MAPPINGS = {
    # Basic product information
    'Product Name (English)': 'Product Name',
    'Description (English)': 'Product Description',
    'Product Token': 'Contribution Goods',
    'SKU': 'Contribution SKU',
    'USD Unit Retail Price': 'Base Price - USD',
    'On Hand Inventory': 'Quantity',
    'Made In Country': 'Country/Region of Origin',
    
    # Add more mappings here:
    'Product Status': 'Status',
    'Item Weight': 'Weight - lb',
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
    
    # Add more fixed values:
    'Status': 'Active',
    'Brand': 'Your Brand Name',
    'Shipping Template': 'Standard',
    'Handling Time': '1',
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
python show_columns.py
```

### Test Fixed Values
```bash
python test_fixed_values.py
```

## 📊 Current Configuration

### Mapped Columns (6 + 1 transformed)
- ✅ Product Name (English) → Product Name
- ✅ Description (English) → Product Description  
- ✅ SKU → Contribution SKU
- ✅ USD Unit Retail Price → Base Price - USD
- ✅ On Hand Inventory → Quantity
- ✅ Made In Country → Country/Region of Origin
- ✅ SKU → Contribution Goods (with transformation: removes letter suffix)

### Fixed Values (3)
- ✅ Category = '29153'
- ✅ Country/Region of Origin = 'China'
- ✅ Province of Origin = 'Guangdong'

## 📈 Results

- **5,669 products** processed successfully
- **6 column mappings** applied + **1 SKU transformation**
- **3 fixed values** set for all rows
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