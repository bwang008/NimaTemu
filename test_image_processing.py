import pandas as pd
import re

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
        
        print("TESTING IMAGE URL PROCESSING")
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
            sample_values = output_df[first_sku_col].dropna().head(10).tolist()
            
            print(f"\nSample values from {first_sku_col}:")
            print("-" * 40)
            for i, value in enumerate(sample_values, 1):
                print(f"{i:2d}. {value}")
            
            # Count non-empty values
            non_empty_count = len(output_df[first_sku_col].dropna())
            print(f"\nTotal non-empty values in {first_sku_col}: {non_empty_count}")
        
        if detail_images_columns:
            print(f"\nFirst Detail Images URL column: {detail_images_columns[0]}")
            
            # Check sample data from first Detail Images URL column
            first_detail_col = detail_images_columns[0]
            sample_values = output_df[first_detail_col].dropna().head(10).tolist()
            
            print(f"\nSample values from {first_detail_col}:")
            print("-" * 40)
            for i, value in enumerate(sample_values, 1):
                print(f"{i:2d}. {value}")
            
            # Count non-empty values
            non_empty_count = len(output_df[first_detail_col].dropna())
            print(f"\nTotal non-empty values in {first_detail_col}: {non_empty_count}")
        
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
        
        # Check if SKU Images URL and Detail Images URL have matching first URLs
        if sku_images_columns and detail_images_columns:
            print(f"\nVerifying first URL matching:")
            print("-" * 30)
            
            sku_col = sku_images_columns[0]
            detail_col = detail_images_columns[0]
            
            # Compare first few rows
            matches = 0
            total_checked = 0
            
            for i in range(min(10, len(output_df))):
                sku_value = output_df.iloc[i][sku_col]
                detail_value = output_df.iloc[i][detail_col]
                
                if pd.notna(sku_value) and pd.notna(detail_value):
                    total_checked += 1
                    if str(sku_value) == str(detail_value):
                        matches += 1
                        print(f"Row {i+1}: ✓ Match - {sku_value}")
                    else:
                        print(f"Row {i+1}: ✗ Mismatch - SKU: {sku_value}, Detail: {detail_value}")
            
            print(f"\nMatching summary: {matches}/{total_checked} rows have matching first URLs")
        
        print(f"\nTotal rows in output: {len(output_df)}")
        
    except Exception as e:
        print(f"Error testing image processing: {e}")

if __name__ == "__main__":
    test_image_processing() 