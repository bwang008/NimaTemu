"""
EXAMPLE: How to add more column mappings to Faire2Temu.py

This file shows you how to extend the COLUMN_MAPPINGS dictionary
in Faire2Temu.py to include more columns.
"""

# Example of how to add more mappings to the COLUMN_MAPPINGS dictionary in Faire2Temu.py:

EXAMPLE_MAPPINGS = {
    # Current mappings (already in the script)
    'Product Name (English)': 'Product Name',
    'Description (English)': 'Product Description',
    'Product Token': 'Contribution Goods',
    'SKU': 'Contribution SKU',
    'USD Unit Retail Price': 'Base Price - USD',
    'On Hand Inventory': 'Quantity',
    'Made In Country': 'Country/Region of Origin',
    
    # Additional mappings you can add:
    'Product Status': 'Status',
    'Product Type': 'Category',
    'Item Weight': 'Weight - lb',
    'Item Length': 'Length - in',
    'Item Width': 'Width - in',
    'Item Height': 'Height - in',
    'Product Images': 'Detail Images URL',
    
    # Option mappings for variants
    'Option 1 Name': 'Color',
    'Option 1 Value': 'Color Value',
    'Option 2 Name': 'Size',
    'Option 2 Value': 'Size Value',
    'Option 3 Name': 'Material',
    'Option 3 Value': 'Material Value',
    
    # Additional product details
    'GTIN': 'External Product ID',
    'Case Size': 'Capacity',
    'Minimum Order Quantity': 'Quantity.1',
}

# Example transformation functions you can add:
def transform_weight(weight_value):
    """Convert weight to pounds if needed"""
    if weight_value is None or str(weight_value).strip() == '':
        return ''
    # Add your weight conversion logic here
    return str(weight_value)

def transform_images(image_urls):
    """Split image URLs and handle multiple images"""
    if image_urls is None or str(image_urls).strip() == '':
        return ''
    # Split space-separated URLs
    urls = str(image_urls).split()
    return urls[0] if urls else ''  # Return first image URL

# Example TRANSFORMATIONS dictionary additions:
EXAMPLE_TRANSFORMATIONS = {
    # These would reference functions defined in Faire2Temu.py
    'USD Unit Retail Price': 'transform_price_function',  # Already defined in main script
    'Product Name (English)': 'transform_product_name_function',  # Already defined in main script
    'Description (English)': 'transform_product_name_function',  # Already defined in main script
    
    # New transformations
    'Item Weight': transform_weight,
    'Product Images': transform_images,
}

print("EXAMPLE MAPPING CONFIGURATION")
print("=" * 50)
print("To add more mappings to Faire2Temu.py:")
print()
print("1. Open Faire2Temu.py")
print("2. Find the COLUMN_MAPPINGS dictionary")
print("3. Add your new mappings following this format:")
print("   'Faire Column Name': 'Temu Column Name',")
print()
print("4. If you need data transformation, add to TRANSFORMATIONS:")
print("   'Faire Column Name': your_transform_function,")
print()
print("5. Run the script: python Faire2Temu.py") 