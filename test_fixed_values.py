import pandas as pd

def test_fixed_values():
    """Test that fixed column values were applied correctly."""
    
    try:
        # Load the output file
        output_df = pd.read_excel('output/temu_upload_generated_with_fixed_values.xlsx', sheet_name='Template', header=1)
        
        print("TESTING FIXED COLUMN VALUES")
        print("=" * 50)
        
        # Check the fixed values that should have been set
        expected_fixed_values = {
            'Category': '29153',
            'Country/Region of Origin': 'China',
            'Province of Origin': 'Guangdong'
        }
        
        print("Checking fixed values in output file:")
        print("-" * 40)
        
        for column, expected_value in expected_fixed_values.items():
            if column in output_df.columns:
                # Get the first few values to check
                actual_values = output_df[column].dropna().head(5).tolist()
                print(f"\n{column}:")
                print(f"  Expected: '{expected_value}'")
                print(f"  Actual (first 5): {actual_values}")
                
                # Check if all values match the expected value
                all_match = all(str(val) == expected_value for val in actual_values)
                print(f"  All match expected: {'✓' if all_match else '✗'}")
            else:
                print(f"\n{column}: Column not found in output file")
        
        # Show sample data from the output file
        print(f"\nSample data from output file (first 3 rows):")
        print("-" * 40)
        sample_columns = ['Product Name', 'Product Description', 'Category', 'Country/Region of Origin', 'Province of Origin']
        available_columns = [col for col in sample_columns if col in output_df.columns]
        
        if available_columns:
            print(output_df[available_columns].head(3).to_string())
        
        print(f"\nTotal rows in output: {len(output_df)}")
        
    except Exception as e:
        print(f"Error testing fixed values: {e}")

if __name__ == "__main__":
    test_fixed_values() 