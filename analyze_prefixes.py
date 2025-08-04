import pandas as pd
import re

def analyze_bag_prefixes():
    """Analyze Faire products to identify bag/handbag prefixes"""
    
    print("Loading Faire products file...")
    faire_df = pd.read_excel('data/faire_products.xlsx', sheet_name='Products')
    
    print(f"Total products: {len(faire_df)}")
    print(f"Columns: {list(faire_df.columns)}")
    print()
    
    # Get data from row 4 onwards (skip header rows)
    data_df = faire_df.iloc[3:].copy()
    
    # Analyze SKU prefixes
    print("=== SKU PREFIX ANALYSIS ===")
    sku_prefixes = {}
    bag_related_keywords = [
        'bag', 'handbag', 'purse', 'clutch', 'tote', 'backpack', 'wallet', 
        'crossbody', 'satchel', 'duffle', 'messenger', 'shoulder', 'hobo',
        'bucket', 'sling', 'fanny', 'belt', 'coin', 'card', 'keychain'
    ]
    
    # Get unique SKUs and their prefixes
    unique_skus = data_df['SKU'].dropna().unique()
    
    for sku in unique_skus:
        if pd.isna(sku):
            continue
            
        sku_str = str(sku).strip()
        # Extract prefix (first 3-6 characters)
        prefix = sku_str[:6] if len(sku_str) >= 6 else sku_str[:3]
        
        if prefix not in sku_prefixes:
            sku_prefixes[prefix] = {
                'count': 0,
                'examples': [],
                'product_names': [],
                'has_bag_keywords': False
            }
        
        sku_prefixes[prefix]['count'] += 1
        sku_prefixes[prefix]['examples'].append(sku_str)
        
        # Get product name for this SKU
        product_name = data_df[data_df['SKU'] == sku]['Product Name (English)'].iloc[0] if len(data_df[data_df['SKU'] == sku]) > 0 else ''
        if product_name:
            sku_prefixes[prefix]['product_names'].append(str(product_name))
    
    # Analyze each prefix for bag-related keywords
    bag_prefixes = {}
    other_prefixes = {}
    
    for prefix, info in sku_prefixes.items():
        # Check product names for bag-related keywords
        has_bag_keywords = False
        for product_name in info['product_names']:
            product_lower = str(product_name).lower()
            for keyword in bag_related_keywords:
                if keyword in product_lower:
                    has_bag_keywords = True
                    break
            if has_bag_keywords:
                break
        
        info['has_bag_keywords'] = has_bag_keywords
        
        if has_bag_keywords:
            bag_prefixes[prefix] = info
        else:
            other_prefixes[prefix] = info
    
    print("=== BAG/HANDBAG PREFIXES ===")
    print("Prefixes with bag-related keywords in product names:")
    print()
    
    # Sort by count for better readability
    sorted_bag_prefixes = sorted(bag_prefixes.items(), key=lambda x: x[1]['count'], reverse=True)
    
    for prefix, info in sorted_bag_prefixes:
        print(f"  {prefix}: {info['count']} products")
        print(f"    Examples: {info['examples'][:3]}")
        print(f"    Sample names: {info['product_names'][:2]}")
        print()
    
    print("=== SUMMARY ===")
    print(f"Total unique SKU prefixes: {len(sku_prefixes)}")
    print(f"Bag-related prefixes: {len(bag_prefixes)}")
    print(f"Other prefixes: {len(other_prefixes)}")
    
    # Save results to file
    with open('bag_prefixes_analysis.txt', 'w') as f:
        f.write("=== BAG/HANDBAG PREFIXES ANALYSIS ===\n\n")
        f.write(f"Total unique SKU prefixes: {len(sku_prefixes)}\n")
        f.write(f"Bag-related prefixes: {len(bag_prefixes)}\n")
        f.write(f"Other prefixes: {len(other_prefixes)}\n\n")
        
        f.write("=== BAG/HANDBAG PREFIXES ===\n")
        for prefix, info in sorted_bag_prefixes:
            f.write(f"{prefix}: {info['count']} products\n")
            f.write(f"  Examples: {info['examples'][:3]}\n")
            f.write(f"  Sample names: {info['product_names'][:2]}\n\n")
    
    print(f"\nDetailed results saved to: bag_prefixes_analysis.txt")
    
    return bag_prefixes, other_prefixes

if __name__ == "__main__":
    bag_prefixes, other_prefixes = analyze_bag_prefixes() 