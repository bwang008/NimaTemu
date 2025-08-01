import pandas as pd
import shutil
from openpyxl import load_workbook
import warnings
import re

# Suppress openpyxl warnings
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

def copy_mapped_data():
    """
    Enhanced tool to copy mapped data from Faire products to Temu template.
    
    Uses a configurable mapping dictionary to copy multiple columns.
    """
    
    # ============================================================================
    # COLUMN MAPPING DICTIONARY
    # ============================================================================
    # Configure your column mappings here:
    # Key: Faire column name (from faire_products.xlsx)
    # Value: Temu column name (from temu_template.xlsx)
    
    COLUMN_MAPPINGS = {
        # Basic product information
        'Product Name (English)': 'Product Name',
        'Description (English)': 'Product Description',
        'SKU': 'Contribution SKU',
        # Note: USD Unit Retail Price is now used for pricing strategy calculation
        # 'USD Unit Retail Price': 'Base Price - USD',  # REMOVED - handled by pricing strategy
        'On Hand Inventory': 'Quantity',
        'Made In Country': 'Country/Region of Origin',
        
        # Note: Contribution Goods will be handled separately with SKU transformation
        
        # Option mappings
        'Option 1 Name': 'Variation Theme',
        'Option 1 Value': 'Color',
        
        # Price mappings
        # Note: USD Unit Retail Price is now used for pricing strategy calculation
        # 'USD Unit Retail Price': 'List Price - USD',  # REMOVED - handled by pricing strategy
        
        # Dimension mappings
        'Item Weight': 'Weight - lb',
        'Item Length': 'Length - in',
        'Item Width': 'Width - in',
        'Item Height': 'Height - in',
        
        # Optional mappings - uncomment and modify as needed
        # 'Product Status': 'Status',
        # 'Product Type': 'Category',
        # 'Product Images': 'Detail Images URL',
        # 'Option 2 Name': 'Size',
        # 'Option 2 Value': 'Size Value',
    }
    
    # ============================================================================
    # FIXED COLUMN VALUES DICTIONARY
    # ============================================================================
    # Configure fixed values for specific Temu columns here:
    # Key: Temu column name (from temu_template.xlsx)
    # Value: Fixed value to assign to all rows
    
    FIXED_COLUMN_VALUES = {
        'Category': '29153',
        'Country/Region of Origin': 'Mainland China',
        'Province of Origin': 'Guangdong',
        'Update or Add': 'Add',
        'Shipping Template': 'NIMA2',
        # Note: Size is now handled by conditional logic
        # 'Size': 'One Size',  # REMOVED - handled by conditional logic
        'California Proposition 65 Warning Type': 'No Warning Applicable',
        
        # Add more fixed values as needed:
        # 'Status': 'Active',
        # 'Brand': 'Your Brand Name',
        # 'Handling Time': '1',
        # 'Import Designation': 'General',
        # 'Fulfillment Channel': 'FBA',
    }
    
    # ============================================================================
    # DATA TRANSFORMATION FUNCTIONS (optional)
    # ============================================================================
    # Add custom transformation functions for specific columns if needed
    
    def transform_price(price_value):
        """Transform price values (remove $, convert to string, etc.)"""
        if pd.isna(price_value):
            return ''
        return str(price_value).replace('$', '').strip()
    
    def transform_product_name(name):
        """Transform product names (remove extra whitespace, etc.)"""
        if pd.isna(name):
            return ''
        return str(name).strip()
    
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
    
    # Define transformation functions for specific columns
    TRANSFORMATIONS = {
        'USD Unit Retail Price': transform_price,
        'Product Name (English)': transform_product_name,
        'Description (English)': transform_product_name,
        # Note: SKU transformation is handled separately for Contribution Goods only
        # 'SKU': transform_sku_to_goods,  # REMOVED - this was causing the bug
    }
    
    # ============================================================================
    # MAIN PROCESSING FUNCTION
    # ============================================================================
    
    try:
        # File paths
        faire_file = 'data/faire_products.xlsx'
        temu_template_file = 'data/temu_template.xlsx'
        output_file = 'output/temu_upload_generated_with_fixed_values.xlsx'
        
        print("Starting enhanced mapping tool...")
        print(f"Mapping {len(COLUMN_MAPPINGS)} columns")
        print(f"Setting {len(FIXED_COLUMN_VALUES)} fixed values")
        
        # Step 1: Load Faire products file
        print("Loading Faire products file...")
        faire_df = pd.read_excel(faire_file, sheet_name='Products')
        
        # Step 2: Load Temu template file
        print("Loading Temu template...")
        temu_df = pd.read_excel(temu_template_file, sheet_name='Template', header=1)
        
        # Step 3: Validate mappings
        print("Validating column mappings...")
        missing_faire_columns = []
        missing_temu_columns = []
        
        for faire_col, temu_col in COLUMN_MAPPINGS.items():
            if faire_col not in faire_df.columns:
                missing_faire_columns.append(faire_col)
            if temu_col not in temu_df.columns:
                missing_temu_columns.append(temu_col)
        
        if missing_faire_columns:
            print(f"Warning: Missing Faire columns: {missing_faire_columns}")
        if missing_temu_columns:
            print(f"Warning: Missing Temu columns: {missing_temu_columns}")
        
        # Step 4: Copy the template file to output
        print("Copying template file...")
        shutil.copy2(temu_template_file, output_file)
        
        # Step 5: Load the copied workbook and modify it
        workbook = load_workbook(output_file)
        template_sheet = workbook['Template']
        
        # Step 6: Process each mapping
        print("Processing column mappings...")
        
        # Find all columns named 'Quantity' in the template
        quantity_col_indices = []
        for col_idx, cell in enumerate(template_sheet[2], 1):
            if str(cell.value) == 'Quantity':
                quantity_col_indices.append(col_idx)
        
        # Find all columns named 'Base Price - USD' and 'List Price - USD'
        base_price_col_indices = []
        list_price_col_indices = []
        for col_idx, cell in enumerate(template_sheet[2], 1):
            if str(cell.value) == 'Base Price - USD':
                base_price_col_indices.append(col_idx)
            if str(cell.value) == 'List Price - USD':
                list_price_col_indices.append(col_idx)
        
        # Find Variation Theme and Size columns for conditional logic
        variation_theme_col_idx = None
        size_col_idx = None
        for col_idx, cell in enumerate(template_sheet[2], 1):
            if str(cell.value) == 'Variation Theme':
                variation_theme_col_idx = col_idx
            if str(cell.value) == 'Size':
                size_col_idx = col_idx
        
        for faire_col, temu_col in COLUMN_MAPPINGS.items():
            if faire_col in faire_df.columns and temu_col in temu_df.columns:
                print(f"  Mapping: {faire_col} -> {temu_col}")
                
                # Get source data (row 4 onwards, skip rows 1-3)
                source_data = faire_df.iloc[3:][faire_col].tolist()
                
                # Find the column index in Temu template
                temu_col_idx = None
                for col_idx, cell in enumerate(template_sheet[2], 1):  # Row 2 contains headers
                    if temu_col in str(cell.value):
                        temu_col_idx = col_idx
                        break
                
                if temu_col_idx is None:
                    print(f"    Warning: Could not find column '{temu_col}' in template")
                    continue
                
                # Apply transformation if defined
                if faire_col in TRANSFORMATIONS:
                    source_data = [TRANSFORMATIONS[faire_col](value) for value in source_data]
                    print(f"    Applied transformation: {faire_col}")
                
                # Special handling for Quantity: populate all Quantity columns
                if temu_col == 'Quantity' and quantity_col_indices:
                    for row_idx, value in enumerate(source_data, 5):
                        # Handle NaN values
                        cell_value = '' if pd.isna(value) else value
                        for q_col_idx in quantity_col_indices:
                            template_sheet.cell(row=row_idx, column=q_col_idx, value=cell_value)
                    print(f"    Copied {len(source_data)} values to all Quantity columns ({len(quantity_col_indices)})")
                    continue  # Skip the default single-column write below
                
                # Write data to template (default: single column)
                for row_idx, value in enumerate(source_data, 5):
                    # Handle NaN values
                    if pd.isna(value):
                        template_sheet.cell(row=row_idx, column=temu_col_idx, value='')
                    else:
                        template_sheet.cell(row=row_idx, column=temu_col_idx, value=value)
                
                print(f"    Copied {len(source_data)} values")
            else:
                print(f"  Skipping: {faire_col} -> {temu_col} (column not found)")
        
        # Step 6c: Conditional logic for Variation Theme and Size
        print("Processing conditional Variation Theme logic...")
        if variation_theme_col_idx is not None and size_col_idx is not None:
            # Get the Color data that was mapped
            color_data = []
            if 'Option 1 Value' in faire_df.columns:
                color_data = faire_df.iloc[3:]['Option 1 Value'].tolist()
            
            # Process each row for conditional logic
            for row_idx, color_value in enumerate(color_data, 5):
                if pd.isna(color_value) or str(color_value).strip() == '':
                    # No color value - set Variation Theme to 'Size' and Size to 'One Size'
                    template_sheet.cell(row=row_idx, column=variation_theme_col_idx, value='Size')
                    template_sheet.cell(row=row_idx, column=size_col_idx, value='One Size')
                else:
                    # Has color value - Variation Theme stays as 'Color' (already set by mapping)
                    # Size column remains empty or as set by fixed values
                    pass
            
            print(f"  Applied conditional logic to {len(color_data)} rows")
            print(f"  - Rows with color: Set Variation Theme = 'Color'")
            print(f"  - Rows without color: Set Variation Theme = 'Size', Size = 'One Size'")
        else:
            print("  Warning: Could not find Variation Theme or Size columns for conditional logic")
        
        # After all mappings, calculate pricing strategy
        if base_price_col_indices and list_price_col_indices:
            print("Calculating pricing strategy (1x and 1.25x Faire price, floored to X.99)...")
            num_data_rows = len(faire_df.iloc[3:])
            
            # Get the original Faire price data
            faire_price_col = 'USD Unit Retail Price'
            faire_prices = faire_df.iloc[3:][faire_price_col].tolist()
            
            for row_idx in range(5, 5 + num_data_rows):
                try:
                    # Get the original Faire price for this row
                    faire_price = faire_prices[row_idx - 5] if row_idx - 5 < len(faire_prices) else None
                    
                    if faire_price is not None and str(faire_price).strip() != '':
                        faire_price_float = float(str(faire_price))
                        
                        # Calculate Base Price: 1x Faire price, floored, minus 1 cent
                        base_price_raw = faire_price_float * 1
                        base_price_floored = int(base_price_raw)
                        base_price_final = base_price_floored - 0.01
                        
                        # Calculate List Price: 1.25x Faire price, floored, minus 1 cent
                        list_price_raw = faire_price_float * 1.25
                        list_price_floored = int(list_price_raw)
                        list_price_final = list_price_floored - 0.01
                        
                        # Set Base Price - USD
                        for bp_col_idx in base_price_col_indices:
                            template_sheet.cell(row=row_idx, column=bp_col_idx, value=base_price_final)
                        
                        # Set List Price - USD
                        for lp_col_idx in list_price_col_indices:
                            template_sheet.cell(row=row_idx, column=lp_col_idx, value=list_price_final)
                    else:
                        # Set empty values if no Faire price
                        for bp_col_idx in base_price_col_indices:
                            template_sheet.cell(row=row_idx, column=bp_col_idx, value='')
                        for lp_col_idx in list_price_col_indices:
                            template_sheet.cell(row=row_idx, column=lp_col_idx, value='')
                            
                except (TypeError, ValueError) as e:
                    # Set empty values on error
                    for bp_col_idx in base_price_col_indices:
                        template_sheet.cell(row=row_idx, column=bp_col_idx, value='')
                    for lp_col_idx in list_price_col_indices:
                        template_sheet.cell(row=row_idx, column=lp_col_idx, value='')
            
            print(f"  Set pricing strategy for {num_data_rows} rows")
            print(f"  Base Price: 1x Faire price, floored, minus 1 cent")
            print(f"  List Price: 1.25x Faire price, floored, minus 1 cent")
        
        # Step 6a: Special handling for Contribution Goods (transformed from SKU)
        print("Processing Contribution Goods transformation...")
        if 'SKU' in faire_df.columns:
            # Get SKU data
            sku_data = faire_df.iloc[3:]['SKU'].tolist()
            
            # Transform SKU to Contribution Goods
            contribution_goods_data = [transform_sku_to_goods(sku) for sku in sku_data]
            
            # Find Contribution Goods column in template
            goods_col_idx = None
            for col_idx, cell in enumerate(template_sheet[2], 1):  # Row 2 contains headers
                if 'Contribution Goods' in str(cell.value):
                    goods_col_idx = col_idx
                    break
            
            if goods_col_idx is not None:
                # Write transformed data to Contribution Goods column
                for row_idx, value in enumerate(contribution_goods_data, 5):
                    # Handle NaN values
                    cell_value = '' if pd.isna(value) else value
                    template_sheet.cell(row=row_idx, column=goods_col_idx, value=cell_value)
                
                print(f"  Transformed {len(contribution_goods_data)} SKUs to Contribution Goods")
                
                # Show some examples of the transformation
                print("  Sample transformations:")
                for i, (original, transformed) in enumerate(zip(sku_data[:5], contribution_goods_data[:5]), 1):
                    print(f"    {i}. '{original}' → '{transformed}'")
            else:
                print("  Warning: Could not find 'Contribution Goods' column in template")
        else:
            print("  Warning: 'SKU' column not found in Faire file")
        
        # Step 6b: Special handling for Image URLs
        print("Processing Image URLs...")
        if 'Option Image' in faire_df.columns or 'Product Images' in faire_df.columns:
            # Get data from row 4 onwards
            faire_data = faire_df.iloc[3:]
            
            # Find SKU Images URL columns in template
            sku_images_columns = []
            detail_images_columns = []
            
            for col_idx, cell in enumerate(template_sheet[2], 1):  # Row 2 contains headers
                cell_value = str(cell.value)
                if 'SKU Images URL' in cell_value:
                    sku_images_columns.append(col_idx)
                elif 'Detail Images URL' in cell_value:
                    detail_images_columns.append(col_idx)
            
            print(f"  Found {len(sku_images_columns)} SKU Images URL columns")
            print(f"  Found {len(detail_images_columns)} Detail Images URL columns")
            
            # Process each row
            option_image_count = 0
            product_images_count = 0
            no_image_count = 0
            
            for row_idx, (_, row_data) in enumerate(faire_data.iterrows(), 5):
                # Determine which image source to use
                image_urls = []
                
                # First try Option Image
                if 'Option Image' in faire_df.columns and pd.notna(row_data['Option Image']):
                    image_urls = [str(row_data['Option Image']).strip()]
                    option_image_count += 1
                # Fallback to Product Images
                elif 'Product Images' in faire_df.columns and pd.notna(row_data['Product Images']):
                    image_urls = split_image_urls(row_data['Product Images'])
                    product_images_count += 1
                else:
                    no_image_count += 1
                
                # Assign URLs to SKU Images URL columns
                if image_urls and sku_images_columns:
                    for i, url in enumerate(image_urls):
                        if i < len(sku_images_columns):
                            template_sheet.cell(row=row_idx, column=sku_images_columns[i], value=url)
                    
                    # Also assign first URL to first Detail Images URL column
                    if detail_images_columns and image_urls:
                        template_sheet.cell(row=row_idx, column=detail_images_columns[0], value=image_urls[0])
            
            print(f"  Processed image URLs for {len(faire_data)} rows")
            print(f"    - Used Option Image: {option_image_count} rows")
            print(f"    - Used Product Images: {product_images_count} rows")
            print(f"    - No image data: {no_image_count} rows")
        else:
            print("  Warning: No image columns found in Faire file")
        
        # Step 7: Process fixed column values
        print("Processing fixed column values...")
        
        for temu_col, fixed_value in FIXED_COLUMN_VALUES.items():
            print(f"  Setting fixed value: {temu_col} = '{fixed_value}'")
            
            # Find the column index in Temu template
            temu_col_idx = None
            for col_idx, cell in enumerate(template_sheet[2], 1):  # Row 2 contains headers
                if temu_col in str(cell.value):
                    temu_col_idx = col_idx
                    break
            
            if temu_col_idx is None:
                print(f"    Warning: Could not find column '{temu_col}' in template")
                continue
            
            # Get the number of data rows (same as the mapped data)
            num_data_rows = len(faire_df.iloc[3:])
            
            # Write fixed value to all data rows
            for row_idx in range(5, 5 + num_data_rows):
                template_sheet.cell(row=row_idx, column=temu_col_idx, value=fixed_value)
            
            print(f"    Set fixed value for {num_data_rows} rows")
        
        # Step 8: Save the workbook
        workbook.save(output_file)
        workbook.close()
        
        print(f"\nSuccess! Output saved to: {output_file}")
        print(f"Processed {len(COLUMN_MAPPINGS)} column mappings")
        print(f"Set {len(FIXED_COLUMN_VALUES)} fixed values")
        
        # Step 9: Show summary of what was copied
        print("\nColumn mapping summary:")
        print("-" * 40)
        for faire_col, temu_col in COLUMN_MAPPINGS.items():
            if faire_col in faire_df.columns and temu_col in temu_df.columns:
                source_count = len(faire_df.iloc[3:][faire_col].dropna())
                print(f"✓ {faire_col} -> {temu_col} ({source_count} values)")
            else:
                print(f"✗ {faire_col} -> {temu_col} (column not found)")
        
        print("\nFixed value summary:")
        print("-" * 40)
        for temu_col, fixed_value in FIXED_COLUMN_VALUES.items():
            print(f"✓ {temu_col} = '{fixed_value}' (all rows)")
        
    except FileNotFoundError as e:
        print(f"Error: Could not find a file. Please check your file paths. Details: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def show_available_columns():
    """Show available columns in both files for reference."""
    try:
        faire_df = pd.read_excel('data/faire_products.xlsx', sheet_name='Products')
        temu_df = pd.read_excel('data/temu_template.xlsx', sheet_name='Template', header=1)
        
        print("AVAILABLE COLUMNS FOR MAPPING:")
        print("=" * 60)
        print("FAIRE COLUMNS:")
        for i, col in enumerate(faire_df.columns, 1):
            print(f"  {i:2d}. {col}")
        
        print("\nTEMU COLUMNS:")
        for i, col in enumerate(temu_df.columns, 1):
            print(f"  {i:2d}. {col}")
            
    except Exception as e:
        print(f"Error showing columns: {e}")

if __name__ == "__main__":
    # Uncomment the line below to see available columns
    # show_available_columns()
    
    # Run the main mapping function
    copy_mapped_data()
