import pandas as pd
import re

def test_sku_transformation():
    """Test the SKU to Contribution Goods transformation."""
    
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
    
    try:
        # Load the output file
        output_df = pd.read_excel('output/temu_upload_generated_with_fixed_values.xlsx', sheet_name='Template', header=1)
        
        print("TESTING SKU TRANSFORMATION")
        print("=" * 50)
        
        # Check if both columns exist
        if 'Contribution SKU' in output_df.columns and 'Contribution Goods' in output_df.columns:
            print("✓ Found both Contribution SKU and Contribution Goods columns")
            
            # Get sample data
            sku_data = output_df['Contribution SKU'].dropna().head(10).tolist()
            goods_data = output_df['Contribution Goods'].dropna().head(10).tolist()
            
            print(f"\nSample SKU → Contribution Goods transformations:")
            print("-" * 50)
            
            for i, (sku, goods) in enumerate(zip(sku_data, goods_data), 1):
                print(f"{i:2d}. '{sku}' → '{goods}'")
            
            # Test the transformation function with some examples
            print(f"\nTesting transformation function:")
            print("-" * 30)
            
            test_cases = [
                'HBG100PN',
                'HBG200',
                'ABC123XY',
                'TEST456AB',
                'SIMPLE789'
            ]
            
            for test_sku in test_cases:
                result = transform_sku_to_goods(test_sku)
                print(f"'{test_sku}' → '{result}'")
            
            # Check if transformations are working correctly
            print(f"\nVerification:")
            print("-" * 20)
            
            # Check if the transformation pattern is working
            pattern_working = True
            for sku, goods in zip(sku_data[:5], goods_data[:5]):
                expected = transform_sku_to_goods(sku)
                if str(goods) != expected:
                    pattern_working = False
                    print(f"✗ Mismatch: '{sku}' should be '{expected}', got '{goods}'")
            
            if pattern_working:
                print("✓ All transformations match expected pattern")
            
            print(f"\nTotal rows processed: {len(output_df)}")
            
        else:
            print("✗ Missing required columns in output file")
            if 'Contribution SKU' not in output_df.columns:
                print("  - Contribution SKU column not found")
            if 'Contribution Goods' not in output_df.columns:
                print("  - Contribution Goods column not found")
        
    except Exception as e:
        print(f"Error testing SKU transformation: {e}")

if __name__ == "__main__":
    test_sku_transformation() 