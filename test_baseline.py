import pandas as pd

def test_baseline_output():
    """Test the baseline tool output to verify data was copied correctly."""
    
    try:
        # Load the original Faire file to get source data
        faire_df = pd.read_excel('data/faire_products.xlsx', sheet_name='Products')
        product_name_col = None
        for col in faire_df.columns:
            if 'Product Name (English)' in str(col):
                product_name_col = col
                break
        
        # Get first 5 product names from source (row 4 onwards, skip rows 1-3)
        source_names = faire_df.iloc[3:8][product_name_col].dropna().tolist()
        
        # Load the output file to get destination data
        output_df = pd.read_excel('output/temu_upload_generated.xlsx', sheet_name='Template', header=1)
        
        # Find the Product Name column in output
        output_product_name_col = None
        for col in output_df.columns:
            if 'Product Name' in str(col):
                output_product_name_col = col
                break
        
        # Get first 5 product names from output
        output_names = output_df.iloc[0:5][output_product_name_col].dropna().tolist()
        
        print("Baseline Tool Test Results:")
        print("=" * 50)
        print(f"Source file: data/faire_products.xlsx")
        print(f"Output file: output/temu_upload_generated.xlsx")
        print(f"Total source products: {len(faire_df.iloc[3:][product_name_col].dropna())}")
        print(f"Total output products: {len(output_df[output_product_name_col].dropna())}")
        print()
        print("First 5 product names comparison:")
        print("-" * 30)
        
        for i, (source, output) in enumerate(zip(source_names, output_names)):
            print(f"Row {i+1}:")
            print(f"  Source: {source}")
            print(f"  Output: {output}")
            print(f"  Match: {'✓' if source == output else '✗'}")
            print()
        
        # Check if all names match
        all_match = source_names == output_names
        print(f"All names match: {'✓' if all_match else '✗'}")
        
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    test_baseline_output() 