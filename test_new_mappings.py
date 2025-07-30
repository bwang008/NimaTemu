import pandas as pd

def test_new_mappings():
    """Test that the new column mappings are working correctly."""
    
    try:
        # Load the output file
        output_df = pd.read_excel('output/temu_upload_generated_with_fixed_values.xlsx', sheet_name='Template', header=1)
        
        print("TESTING NEW COLUMN MAPPINGS")
        print("=" * 50)
        
        # Check the new mappings that should have been applied
        new_mappings = {
            'Variation Theme': 'Option 1 Name',
            'Color': 'Option 1 Value',
            'List Price - USD': 'USD Unit Retail Price',
            'Weight - lb': 'Item Weight',
            'Length - in': 'Item Length',
            'Width - in': 'Item Width',
            'Height - in': 'Item Height'
        }
        
        print("Checking new mappings in output file:")
        print("-" * 40)
        
        for temu_col, faire_col in new_mappings.items():
            if temu_col in output_df.columns:
                # Get sample data
                sample_values = output_df[temu_col].dropna().head(5).tolist()
                print(f"\n{temu_col} (from {faire_col}):")
                print(f"  Sample values: {sample_values}")
                print(f"  Total non-empty values: {len(output_df[temu_col].dropna())}")
            else:
                print(f"\n{temu_col}: Column not found in output file")
        
        # Show sample data from the output file including new columns
        print(f"\nSample data from output file (first 3 rows):")
        print("-" * 40)
        sample_columns = ['Product Name', 'Variation Theme', 'Color', 'List Price - USD', 'Weight - lb']
        available_columns = [col for col in sample_columns if col in output_df.columns]
        
        if available_columns:
            print(output_df[available_columns].head(3).to_string())
        
        print(f"\nTotal rows in output: {len(output_df)}")
        
        # Summary of all mappings
        print(f"\nALL MAPPINGS SUMMARY:")
        print("-" * 40)
        all_mappings = {
            'Product Name': 'Product Name (English)',
            'Product Description': 'Description (English)',
            'Contribution SKU': 'SKU',
            'Base Price - USD': 'USD Unit Retail Price',
            'List Price - USD': 'USD Unit Retail Price',
            'Quantity': 'On Hand Inventory',
            'Country/Region of Origin': 'Made In Country',
            'Variation Theme': 'Option 1 Name',
            'Color': 'Option 1 Value',
            'Weight - lb': 'Item Weight',
            'Length - in': 'Item Length',
            'Width - in': 'Item Width',
            'Height - in': 'Item Height'
        }
        
        for temu_col, faire_col in all_mappings.items():
            if temu_col in output_df.columns:
                non_empty_count = len(output_df[temu_col].dropna())
                print(f"✓ {temu_col} <- {faire_col} ({non_empty_count} values)")
            else:
                print(f"✗ {temu_col} <- {faire_col} (column not found)")
        
    except Exception as e:
        print(f"Error testing new mappings: {e}")

if __name__ == "__main__":
    test_new_mappings() 