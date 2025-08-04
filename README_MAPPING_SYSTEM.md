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

## 👜 Bag/Handbag Product Prefixes

Based on analysis of the Faire products file, the following SKU prefixes are associated with bag/handbag products:

### Major Bag Prefixes (100+ products):
- **HBG104**: 1,385 products - Handbags, Crossbody Bags
- **HBG103**: 550 products - Tote Handbags  
- **HBG105**: 481 products - Clutch Handbags

### Hat/Cap Prefixes (50+ products):
- **CAP006**: 144 products - Baseball Caps, Fedora Hats
- **CAP005**: 60 products - Baseball Caps, Fedora Hats

### Bag Strap/Accessory Prefixes:
- **TO-407**: 63 products - Chain Belt Accessories
- **TO-406**: 53 products - Handbag Straps
- **TO-405**: 49 products - Handbag Straps

### Wallet/Purse Prefixes:
- **HW0080**: 31 products - Fashion Wallets
- **HW0083**: 20 products - Coin Purses
- **HW0084**: 20 products - Coin Purses
- **HW0076**: 18 products - Wristlet Wallets
- **HW0085**: 17 products - Small Wallets
- **HW0074**: 11 products - Ladies Wallets
- **HW0082**: 11 products - Zip Around Wallets

### Cosmetic Bag Prefixes:
- **HM0059**: 31 products - Cosmetic Pouches
- **HM0054**: 20 products - Cosmetic Bags
- **HM0056**: 17 products - Wristlet Handbags
- **HM0052**: 15 products - Travel Cosmetic Pouches
- **HM0060**: 13 products - Cosmetic Bag Sets

### Travel/Duffle Bag Prefixes:
- **HL0042**: 20 products - Duffle Bags, Weekender Bags
- **HL0049**: 14 products - Duffle Bags
- **HL0050**: 12 products - Shopping Cart Bags
- **HL0043**: 8 products - Duffle Bags
- **HL0044**: 8 products - Duffle Bags

### Card Holder Prefixes:
- **GCH148**: 18 products - Card Holders
- **GCH147**: 8 products - Card Holders

### Coin Purse Prefixes:
- **HD0038**: 17 products - Coin Bags
- **HD0055**: 10 products - Beaded Coin Purses
- **HD0056**: 10 products - Beaded Coin Purses
- **HD0039**: 10 products - Coin Purses
- **HD0051**: 10 products - Beaded Coin Purses
- **HD0054**: 10 products - Beaded Coin Purses
- **HD0053**: 10 products - Beaded Coin Purses
- **HD0049**: 10 products - Beaded Coin Purses
- **HD0050**: 10 products - Beaded Coin Purses

### Crossbody Bag Prefixes:
- **HX0036**: 10 products - Cross Body Bags

### Fanny Pack Prefixes:
- **BT0188**: 10 products - Fanny Packs
- **BT0198**: 9 products - Waist Handbags

### Wristlet Prefixes:
- **GK1774**: 12 products - Wristlet Coin Purses
- **GK2124**: 9 products - Wristlet Card Holders

### Total Summary:
- **198 bag-related prefixes** identified
- **716 other prefixes** (non-bag products)
- **914 total unique SKU prefixes** in the dataset

This information can be used for filtering products by category or for targeted processing of specific product types.

## 🎯 Flexible Category System

The script now supports automatic splitting of products into multiple categories based on SKU prefixes. This allows you to create separate upload files for different product types.

### Current Categories:
- **handbags**: HBG, HW, HM, HL prefixes (2,870 products)
- **other**: Catch-all for remaining products (2,799 products)

### Adding New Categories:

#### Method 1: Modify CATEGORY_CONFIGS in the script
```python
CATEGORY_CONFIGS = {
    'handbags': {
        'prefixes': ['HBG', 'HW', 'HM', 'HL'],
        'output_file': 'output/temu_template_handbags.xlsx',
        'description': 'Handbags, Wallets, Cosmetic Bags, Travel Bags'
    },
    'hats': {
        'prefixes': ['CAP', 'HAT'],
        'output_file': 'output/temu_template_hats.xlsx',
        'description': 'Hats and Caps'
    },
    'accessories': {
        'prefixes': ['TO-', 'ACC'],
        'output_file': 'output/temu_template_accessories.xlsx',
        'description': 'Accessories and Straps'
    },
    'other': {
        'prefixes': [],  # Empty = catch-all
        'output_file': 'output/temu_template_other.xlsx',
        'description': 'All other products'
    }
}
```

#### Method 2: Use the helper function
```python
from Faire2Temu import add_category_config, copy_mapped_data

# Add new categories
add_category_config('hats', ['CAP', 'HAT'], 'output/temu_template_hats.xlsx', 'Hats and Caps')
add_category_config('accessories', ['TO-', 'ACC'], 'output/temu_template_accessories.xlsx', 'Accessories')

# Run processing
copy_mapped_data()
```

### Benefits:
- **Automatic categorization** based on SKU prefixes
- **Separate processing** for each category with full functionality
- **Easy to extend** - just add new category configurations
- **Clean separation** - no overlap between files
- **Maintains all features** - color assignment, pricing, image processing, etc.

### Example Output:
```
Category breakdown:
  Handbags: 2870 products (Handbags, Wallets, Cosmetic Bags, Travel Bags)
  Hats: 204 products (Hats, Caps, and Headwear)
  Accessories: 156 products (Accessories, Straps, and Small Items)
  Other: 2439 products (All other products)

Success! Output files saved to:
  Handbags: output/temu_template_handbags.xlsx
  Hats: output/temu_template_hats.xlsx
  Accessories: output/temu_template_accessories.xlsx
  Other: output/temu_template_other.xlsx
``` 