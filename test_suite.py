import pandas as pd
import re
import sys
import argparse

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
        output_df = pd.read_excel('output/temu_upload_generated_with_fixed_values.xlsx', sheet_name='Template', header=1)
        
        # Find the Product Name column in output
        output_product_name_col = None
        for col in output_df.columns:
            if 'Product Name' in str(col):
                output_product_name_col = col
                break
        
        # Get first 5 product names from output
        output_names = output_df.iloc[0:5][output_product_name_col].dropna().tolist()
        
        print("BASELINE TOOL TEST RESULTS:")
        print("=" * 50)
        print(f"Source file: data/faire_products.xlsx")
        print(f"Output file: output/temu_upload_generated_with_fixed_values.xlsx")
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
        print(f"Baseline test failed: {e}")

def test_fixed_values():
    """Test that fixed column values were applied correctly."""
    
    try:
        # Load the output file
        output_df = pd.read_excel('output/temu_upload_generated_with_fixed_values.xlsx', sheet_name='Template', header=1)
        
        print("FIXED COLUMN VALUES TEST")
        print("=" * 50)
        
        # Check the fixed values that should have been set
        expected_fixed_values = {
            'Category': '29153',
            'Country/Region of Origin': 'Mainland China',
            'Province of Origin': 'Guangdong',
            'Update or Add': 'Add',
            'Shipping Template': 'NIMA2',
            'Size': 'One Size',
            'California Proposition 65 Warning Type': 'No Warning Applicable'
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
        
        print(f"\nTotal rows in output: {len(output_df)}")
        
    except Exception as e:
        print(f"Fixed values test failed: {e}")

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
        
        print("SKU TRANSFORMATION TEST")
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
        print(f"SKU transformation test failed: {e}")

def test_new_mappings():
    """Test that the new column mappings are working correctly."""
    
    try:
        # Load the output file
        output_df = pd.read_excel('output/temu_upload_generated_with_fixed_values.xlsx', sheet_name='Template', header=1)
        
        print("NEW COLUMN MAPPINGS TEST")
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
        
        print(f"\nTotal rows in output: {len(output_df)}")
        
    except Exception as e:
        print(f"New mappings test failed: {e}")

def test_image_processing():
    """Test that the image URL processing is working correctly."""
    
    def split_image_urls(image_urls_str):
        """
        Split image URLs that are separated by whitespace or newlines.
        Returns a list of individual URLs.
        """
        if pd.isna(image_urls_str) or str(image_urls_str).strip() == '':
            return []
        
        # Split by whitespace and newlines, then filter out empty strings
        urls = re.split(r'[\s\n]+', str(image_urls_str).strip())
        return [url.strip() for url in urls if url.strip()]
    
    try:
        # Load the output file
        output_df = pd.read_excel('output/temu_upload_generated_with_fixed_values.xlsx', sheet_name='Template', header=1)
        
        print("IMAGE URL PROCESSING TEST")
        print("=" * 50)
        
        # Find SKU Images URL columns
        sku_images_columns = []
        detail_images_columns = []
        
        for col in output_df.columns:
            if 'SKU Images URL' in str(col):
                sku_images_columns.append(col)
            elif 'Detail Images URL' in str(col):
                detail_images_columns.append(col)
        
        print(f"Found {len(sku_images_columns)} SKU Images URL columns")
        print(f"Found {len(detail_images_columns)} Detail Images URL columns")
        
        if sku_images_columns:
            print(f"\nFirst SKU Images URL column: {sku_images_columns[0]}")
            
            # Check sample data from first SKU Images URL column
            first_sku_col = sku_images_columns[0]
            sample_values = output_df[first_sku_col].dropna().head(5).tolist()
            
            print(f"\nSample values from {first_sku_col}:")
            print("-" * 40)
            for i, value in enumerate(sample_values, 1):
                print(f"{i:2d}. {value}")
            
            # Count non-empty values
            non_empty_count = len(output_df[first_sku_col].dropna())
            print(f"\nTotal non-empty values in {first_sku_col}: {non_empty_count}")
        
        # Test the URL splitting function
        print(f"\nTesting URL splitting function:")
        print("-" * 30)
        
        test_cases = [
            "https://example1.com/image1.jpg https://example2.com/image2.jpg",
            "https://example3.com/image3.jpg\nhttps://example4.com/image4.jpg",
            "https://example5.com/image5.jpg",
            "",
            None
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            result = split_image_urls(test_case)
            print(f"{i}. Input: {repr(test_case)}")
            print(f"   Output: {result}")
            print()
        
        print(f"\nTotal rows in output: {len(output_df)}")
        
    except Exception as e:
        print(f"Image processing test failed: {e}")

def show_available_columns():
    """Show available columns in both files for reference."""
    try:
        faire_df = pd.read_excel('data/faire_products.xlsx', sheet_name='Products')
        temu_df = pd.read_excel('data/temu_template.xlsx', sheet_name='Template', header=1)
        
        print("AVAILABLE COLUMNS FOR MAPPING")
        print("=" * 60)
        print("FAIRE COLUMNS:")
        for i, col in enumerate(faire_df.columns, 1):
            print(f"  {i:2d}. {col}")
        
        print(f"\nTotal Faire columns: {len(faire_df.columns)}")
        print()
        
        print("TEMU COLUMNS:")
        for i, col in enumerate(temu_df.columns, 1):
            print(f"  {i:2d}. {col}")
        
        print(f"\nTotal Temu columns: {len(temu_df.columns)}")
        
    except Exception as e:
        print(f"Error showing columns: {e}")

def run_all_tests():
    """Run all tests in sequence."""
    print("COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    print()
    
    test_functions = [
        ("Baseline Output Test", test_baseline_output),
        ("Fixed Values Test", test_fixed_values),
        ("SKU Transformation Test", test_sku_transformation),
        ("New Mappings Test", test_new_mappings),
        ("Image Processing Test", test_image_processing),
    ]
    
    for test_name, test_func in test_functions:
        print(f"\n{'='*20} {test_name} {'='*20}")
        test_func()
        print()

def main():
    parser = argparse.ArgumentParser(description='Comprehensive test suite for Faire2Temu mapping system')
    parser.add_argument('--test', choices=['baseline', 'fixed', 'sku', 'mappings', 'images', 'columns', 'all'], 
                       default='all', help='Specific test to run (default: all)')
    
    args = parser.parse_args()
    
    if args.test == 'all':
        run_all_tests()
    elif args.test == 'baseline':
        test_baseline_output()
    elif args.test == 'fixed':
        test_fixed_values()
    elif args.test == 'sku':
        test_sku_transformation()
    elif args.test == 'mappings':
        test_new_mappings()
    elif args.test == 'images':
        test_image_processing()
    elif args.test == 'columns':
        show_available_columns()

if __name__ == "__main__":
    main() 