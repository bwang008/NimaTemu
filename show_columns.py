import pandas as pd

def show_columns_for_mapping():
    """Display all available columns from both files for easy mapping reference."""
    
    try:
        # Load both files
        faire_df = pd.read_excel('data/faire_products.xlsx', sheet_name='Products')
        temu_df = pd.read_excel('data/temu_template.xlsx', sheet_name='Template', header=1)
        
        print("COLUMN MAPPING REFERENCE")
        print("=" * 80)
        print()
        
        print("FAIRE COLUMNS (data/faire_products.xlsx):")
        print("-" * 50)
        for i, col in enumerate(faire_df.columns, 1):
            print(f"{i:2d}. {col}")
        
        print(f"\nTotal Faire columns: {len(faire_df.columns)}")
        print()
        
        print("TEMU COLUMNS (data/temu_template.xlsx):")
        print("-" * 50)
        for i, col in enumerate(temu_df.columns, 1):
            print(f"{i:2d}. {col}")
        
        print(f"\nTotal Temu columns: {len(temu_df.columns)}")
        print()
        
        print("SUGGESTED MAPPINGS:")
        print("-" * 50)
        print("# Basic product information")
        print("'Product Name (English)': 'Product Name',")
        print("'Description (English)': 'Product Description',")
        print("'Product Token': 'Contribution Goods',")
        print("'SKU': 'Contribution SKU',")
        print("'USD Unit Retail Price': 'Base Price - USD',")
        print("'On Hand Inventory': 'Quantity',")
        print("'Made In Country': 'Country/Region of Origin',")
        print()
        print("# Optional mappings you might want to add:")
        print("'Product Status': 'Status',")
        print("'Item Weight': 'Weight - lb',")
        print("'Item Length': 'Length - in',")
        print("'Item Width': 'Width - in',")
        print("'Item Height': 'Height - in',")
        print("'Product Images': 'Detail Images URL',")
        print("'Option 1 Name': 'Color',")
        print("'Option 1 Value': 'Color Value',")
        print("'Option 2 Name': 'Size',")
        print("'Option 2 Value': 'Size Value',")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    show_columns_for_mapping() 