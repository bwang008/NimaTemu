import pandas as pd

def analyze_columns():
    """Analyze the column structures of both Excel files to help create mappings."""
    
    try:
        # Load Faire products file
        faire_df = pd.read_excel('data/faire_products.xlsx', sheet_name='Products')
        print("FAIRE PRODUCTS COLUMNS:")
        print("=" * 50)
        for i, col in enumerate(faire_df.columns, 1):
            print(f"{i:2d}. {col}")
        print(f"\nTotal Faire columns: {len(faire_df.columns)}")
        
        print("\n" + "=" * 50)
        
        # Load Temu template file
        temu_df = pd.read_excel('data/temu_template.xlsx', sheet_name='Template', header=1)
        print("TEMU TEMPLATE COLUMNS:")
        print("=" * 50)
        for i, col in enumerate(temu_df.columns, 1):
            print(f"{i:2d}. {col}")
        print(f"\nTotal Temu columns: {len(temu_df.columns)}")
        
        # Show sample data from first few rows of each file
        print("\n" + "=" * 50)
        print("SAMPLE FAIRE DATA (first 3 rows, first 5 columns):")
        print("-" * 30)
        print(faire_df.iloc[3:6, :5].to_string())
        
        print("\n" + "=" * 50)
        print("SAMPLE TEMU DATA (first 3 rows, first 5 columns):")
        print("-" * 30)
        print(temu_df.iloc[0:3, :5].to_string())
        
    except Exception as e:
        print(f"Error analyzing columns: {e}")

if __name__ == "__main__":
    analyze_columns() 