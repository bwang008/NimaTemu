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
        'USD Unit Retail Price': 'Base Price - USD',
        'On Hand Inventory': 'Quantity',
        'Made In Country': 'Country/Region of Origin',
        
        # Note: Contribution Goods will be handled separately with SKU transformation
        
        # Optional mappings - uncomment and modify as needed
        # 'Product Status': 'Status',
        # 'Product Type': 'Category',
        # 'Item Weight': 'Weight - lb',
        # 'Item Length': 'Length - in',
        # 'Item Width': 'Width - in',
        # 'Item Height': 'Height - in',
        # 'Product Images': 'Detail Images URL',
        # 'Option 1 Name': 'Color',  # or other appropriate Temu column
        # 'Option 1 Value': 'Color Value',
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
        'Country/Region of Origin': 'China',
        'Province of Origin': 'Guangdong',
        
        # Add more fixed values as needed:
        # 'Status': 'Active',
        # 'Brand': 'Your Brand Name',
        # 'Shipping Template': 'Standard',
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
    
    # Define transformation functions for specific columns
    TRANSFORMATIONS = {
        'USD Unit Retail Price': transform_price,
        'Product Name (English)': transform_product_name,
        'Description (English)': transform_product_name,
        'SKU': transform_sku_to_goods,  # Add transformation for SKU → Contribution Goods
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
        
        for faire_col, temu_col in COLUMN_MAPPINGS.items():
            if faire_col in faire_df.columns and temu_col in temu_df.columns:
                print(f"  Mapping: {faire_col} -> {temu_col}")
                
                # Get source data (row 4 onwards, skip rows 1-3)
                source_data = faire_df.iloc[3:][faire_col].dropna().tolist()
                
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
                
                # Write data to template
                for row_idx, value in enumerate(source_data, 3):
                    template_sheet.cell(row=row_idx, column=temu_col_idx, value=value)
                
                print(f"    Copied {len(source_data)} values")
            else:
                print(f"  Skipping: {faire_col} -> {temu_col} (column not found)")
        
        # Step 6a: Special handling for Contribution Goods (transformed from SKU)
        print("Processing Contribution Goods transformation...")
        if 'SKU' in faire_df.columns:
            # Get SKU data
            sku_data = faire_df.iloc[3:]['SKU'].dropna().tolist()
            
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
                for row_idx, value in enumerate(contribution_goods_data, 3):
                    template_sheet.cell(row=row_idx, column=goods_col_idx, value=value)
                
                print(f"  Transformed {len(contribution_goods_data)} SKUs to Contribution Goods")
                
                # Show some examples of the transformation
                print("  Sample transformations:")
                for i, (original, transformed) in enumerate(zip(sku_data[:5], contribution_goods_data[:5]), 1):
                    print(f"    {i}. '{original}' → '{transformed}'")
            else:
                print("  Warning: Could not find 'Contribution Goods' column in template")
        else:
            print("  Warning: 'SKU' column not found in Faire file")
        
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
            for row_idx in range(3, 3 + num_data_rows):
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
