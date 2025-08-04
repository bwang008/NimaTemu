import pandas as pd
import re

def transform_sku_to_goods(sku_value):
    """
    Transform SKU to Contribution Goods by removing non-numeric suffix.
    Examples:
    - 'HBG100PN' → 'HBG100'
    - 'HBG200' → 'HBG200' (no suffix to remove)
    - 'ABC123XY' → 'ABC123'
    """
    if pd.isna(sku_value):
        return ''
    
    sku_str = str(sku_value).strip()
    
    # Use regex to find the pattern: letters/numbers followed by letters at the end
    # This will match patterns like 'HBG100PN', 'ABC123XY', etc.
    match = re.match(r'^(.+?)([A-Za-z]+)$', sku_str)
    
    if match:
        # If there's a letter suffix, remove it
        base_part = match.group(1)
        return base_part
    else:
        # If no letter suffix found, return the original SKU
        return sku_str

# Test data based on the image you showed
test_data = {
    'SKU': ['CAP00642CH', 'CAP00642MUL', 'CAP00642W', 'CS010', 'CS018'],
    'Option 1 Value': ['', '', '', 'Red', 'Blue']  # Empty for first 3, actual colors for last 2
}

# Create test DataFrame
df = pd.DataFrame(test_data)

print("Test Data:")
print(df)
print()

# Transform SKUs to Contribution Goods
contribution_goods_data = [transform_sku_to_goods(sku) for sku in df['SKU']]
print("Contribution Goods:")
for sku, goods in zip(df['SKU'], contribution_goods_data):
    print(f"  {sku} → {goods}")
print()

# Count occurrences of each Contribution Goods value
goods_count = {}
for goods in contribution_goods_data:
    goods_count[goods] = goods_count.get(goods, 0) + 1

print("Goods Count:")
for goods, count in goods_count.items():
    print(f"  {goods}: {count} occurrences")
print()

# Simulate the color assignment logic
goods_occurrence = {}  # Track occurrence count for each goods value
color_assignments = []

for i, (color_value, goods_value) in enumerate(zip(df['Option 1 Value'], contribution_goods_data)):
    if pd.isna(color_value) or str(color_value).strip() == '':
        # No color value - determine if this is part of a multi-variant product
        if goods_count.get(goods_value, 0) > 1:
            # Multiple variants exist - assign sequential color
            goods_occurrence[goods_value] = goods_occurrence.get(goods_value, 0) + 1
            color_number = goods_occurrence[goods_value]
            assigned_color = f'Color {color_number}'
        else:
            # Single variant - use 'One Color'
            assigned_color = 'One Color'
    else:
        # Has color value - keep original
        assigned_color = color_value
    
    color_assignments.append(assigned_color)
    print(f"Row {i+1}: SKU={df['SKU'][i]}, Original Color='{color_value}', Assigned Color='{assigned_color}'")

print()
print("Summary:")
print("- CAP00642 variants (CH, MUL, W) should get Color 1, Color 2, Color 3")
print("- CS010 and CS018 should keep their original colors (Red, Blue)")
print("- Any single products without colors should get 'One Color'") 