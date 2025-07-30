import pandas as pd

def check_product_token():
    """Check what data is in the Product Token column from Faire file."""
    
    try:
        # Load Faire products file
        faire_df = pd.read_excel('data/faire_products.xlsx', sheet_name='Products')
        
        print("PRODUCT TOKEN ANALYSIS")
        print("=" * 50)
        
        # Check if Product Token column exists
        if 'Product Token' in faire_df.columns:
            print(f"✓ Found 'Product Token' column")
            
            # Get data from row 4 onwards (skip rows 1-3)
            product_tokens = faire_df.iloc[3:]['Product Token'].dropna()
            
            print(f"\nTotal Product Token values: {len(product_tokens)}")
            print(f"Unique Product Token values: {len(product_tokens.unique())}")
            
            print(f"\nFirst 10 Product Token values:")
            print("-" * 30)
            for i, token in enumerate(product_tokens.head(10), 1):
                print(f"{i:2d}. {token}")
            
            print(f"\nSample of unique Product Tokens:")
            print("-" * 30)
            unique_tokens = product_tokens.unique()
            for i, token in enumerate(unique_tokens[:10], 1):
                print(f"{i:2d}. {token}")
            
            # Check if these are being mapped to Contribution Goods
            print(f"\nMAPPING INFORMATION:")
            print("-" * 30)
            print("'Product Token' from Faire → 'Contribution Goods' in Temu")
            print("This mapping is defined in COLUMN_MAPPINGS:")
            print("'Product Token': 'Contribution Goods',")
            
        else:
            print("✗ 'Product Token' column not found in Faire file")
            print("Available columns:")
            for col in faire_df.columns:
                if 'token' in col.lower() or 'product' in col.lower():
                    print(f"  - {col}")
                    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_product_token() 