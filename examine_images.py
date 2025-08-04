import pandas as pd
import re

def examine_image_data():
    """Examine image URLs and data in the faire_products.xlsx file"""
    
    try:
        # Load the Faire products file
        print("Loading Faire products file...")
        faire_df = pd.read_excel('data/faire_products.xlsx', sheet_name='Products')
        
        # Get data from row 4 onwards (skip header rows)
        data_df = faire_df.iloc[3:].copy()
        
        print(f"Total products: {len(data_df)}")
        print("\n" + "="*60)
        print("IMAGE COLUMN ANALYSIS")
        print("="*60)
        
        # Check for image-related columns
        image_columns = []
        for col in data_df.columns:
            if any(keyword in col.lower() for keyword in ['image', 'photo', 'picture', 'url']):
                image_columns.append(col)
        
        if image_columns:
            print(f"Found {len(image_columns)} image-related columns:")
            for col in image_columns:
                print(f"  - {col}")
            
            print("\n" + "-"*40)
            print("SAMPLE IMAGE DATA")
            print("-"*40)
            
            for col in image_columns:
                print(f"\nColumn: {col}")
                print(f"Non-null values: {data_df[col].notna().sum()}")
                
                # Show sample values
                sample_values = data_df[col].dropna().head(3)
                for i, value in enumerate(sample_values, 1):
                    print(f"  Sample {i}: {str(value)[:100]}{'...' if len(str(value)) > 100 else ''}")
                
                # Analyze URL patterns
                if sample_values.any():
                    first_value = str(sample_values.iloc[0])
                    if 'http' in first_value:
                        print(f"  URL pattern detected")
                        # Check for multiple URLs
                        if ' ' in first_value or '\n' in first_value:
                            print(f"  Multiple URLs detected (space/newline separated)")
                        else:
                            print(f"  Single URL per cell")
                    else:
                        print(f"  No URL pattern detected")
        else:
            print("No image-related columns found")
        
        print("\n" + "="*60)
        print("SKU ANALYSIS")
        print("="*60)
        
        # Analyze SKU patterns to understand product categories
        if 'SKU' in data_df.columns:
            sku_data = data_df['SKU'].dropna()
            print(f"Total SKUs: {len(sku_data)}")
            
            # Extract prefixes
            prefixes = {}
            for sku in sku_data:
                if pd.notna(sku):
                    sku_str = str(sku).strip()
                    # Extract prefix (first 3-6 characters)
                    prefix = sku_str[:6] if len(sku_str) >= 6 else sku_str[:3]
                    prefixes[prefix] = prefixes.get(prefix, 0) + 1
            
            # Show top prefixes
            print("\nTop SKU prefixes:")
            sorted_prefixes = sorted(prefixes.items(), key=lambda x: x[1], reverse=True)
            for prefix, count in sorted_prefixes[:10]:
                print(f"  {prefix}: {count} products")
        
        print("\n" + "="*60)
        print("SAMPLE PRODUCTS WITH IMAGES")
        print("="*60)
        
        # Show a few products that have image data
        sample_products = data_df.head(5)
        
        for idx, product in sample_products.iterrows():
            print(f"\nProduct {idx}:")
            if 'Product Name (English)' in product:
                print(f"  Name: {product['Product Name (English)']}")
            if 'SKU' in product:
                print(f"  SKU: {product['SKU']}")
            
            # Check for image data
            image_found = False
            for col in image_columns:
                if pd.notna(product[col]) and str(product[col]).strip():
                    print(f"  {col}: {str(product[col])[:80]}{'...' if len(str(product[col])) > 80 else ''}")
                    image_found = True
            
            if not image_found:
                print("  No image data found")
        
    except Exception as e:
        print(f"Error examining image data: {e}")

if __name__ == "__main__":
    examine_image_data() 