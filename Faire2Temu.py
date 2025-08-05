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
    
    CATEGORY SPLITTING:
    This script now supports splitting products into multiple categories based on SKU prefixes.
    
    To add new categories, modify the CATEGORY_CONFIGS dictionary below or use the
    add_category_config() function before calling copy_mapped_data().
    
    Example of adding a new category:
        add_category_config('hats', ['CAP', 'HAT'], 'output/temu_template_hats.xlsx', 'Hats and Caps')
        copy_mapped_data()
    
    The 'other' category is always the catch-all for products not matching any specific prefixes.
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
    # CATEGORY ASSIGNMENT (MODULAR)
    # ============================================================================
    # Category assignment is now handled by the separate category_assigner.py module.
    # This provides enhanced category logic with support for image data analysis.
    # Import the category assigner
    from category_assigner import CategoryAssigner
    
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
    # HELPER FUNCTIONS
    # ============================================================================
    
    def add_category_config(category_name, prefixes, output_file, description):
        """
        Helper function to add new category configurations.
        This can be called before running the main function to add new categories.
        
        Example:
            add_category_config('hats', ['CAP', 'HAT'], 'output/temu_template_hats.xlsx', 'Hats and Caps')
        """
        global CATEGORY_CONFIGS
        if 'CATEGORY_CONFIGS' not in globals():
            CATEGORY_CONFIGS = {}
        
        CATEGORY_CONFIGS[category_name] = {
            'prefixes': prefixes,
            'output_file': output_file,
            'description': description
        }
        print(f"Added category: {category_name} with prefixes {prefixes}")
    
    def determine_category_code(product_name, image_data=None, default_category='29153'):
        """
        Determine the category code based on product name and image data.
        Returns the category code for the first matching condition, or default if no match.
        
        Args:
            product_name: The product name to analyze
            image_data: Optional image data (URLs, descriptions) to analyze
            default_category: Default category if no match is found
            
        Returns:
            str: The category code for the product
        """
        # Use the modular category assigner
        category_assigner = CategoryAssigner()
        return category_assigner.determine_category(product_name, image_data)
    
    # ============================================================================
    # PROCESSING FUNCTION FOR EACH CATEGORY
    # ============================================================================
    
    def process_product_category(product_data, template_file, output_file, category_name):
        """Process a specific category of products and save to output file"""
        
        print(f"Processing {category_name} category ({len(product_data)} products)...")
        
        # Copy the template file to output
        shutil.copy2(template_file, output_file)
        
        # Load the copied workbook and modify it
        workbook = load_workbook(output_file)
        template_sheet = workbook['Template']
        
        # Convert product_data back to DataFrame for easier processing
        category_df = pd.DataFrame(product_data)
        
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
        
        # Process each mapping
        for faire_col, temu_col in COLUMN_MAPPINGS.items():
            if faire_col in category_df.columns:
                print(f"  Mapping: {faire_col} -> {temu_col}")
                
                # Get source data
                source_data = category_df[faire_col].tolist()
                
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
        
        # Conditional logic for Variation Theme and Color assignment
        print("Processing conditional Variation Theme logic...")
        if variation_theme_col_idx is not None:
            # Get the Contribution Goods data to detect duplicates
            contribution_goods_data = []
            if 'SKU' in category_df.columns:
                # Transform SKU to Contribution Goods for comparison
                sku_data = category_df['SKU'].tolist()
                contribution_goods_data = [transform_sku_to_goods(sku) for sku in sku_data]
            
            # Find the Color column
            color_col_idx = None
            for col_idx, cell in enumerate(template_sheet[2], 1):
                if str(cell.value) == 'Color':
                    color_col_idx = col_idx
                    break
            
            # Get the Color data that was mapped
            color_data = []
            if 'Option 1 Value' in category_df.columns:
                color_data = category_df['Option 1 Value'].tolist()
            
            if color_col_idx is not None and contribution_goods_data and color_data:
                # Count occurrences of each Contribution Goods value
                goods_count = {}
                for goods in contribution_goods_data:
                    goods_count[goods] = goods_count.get(goods, 0) + 1
                
                # Process each row for conditional logic
                goods_occurrence = {}  # Track occurrence count for each goods value
                
                for row_idx, (color_value, goods_value) in enumerate(zip(color_data, contribution_goods_data), 5):
                    if pd.isna(color_value) or str(color_value).strip() == '':
                        # No color value - determine if this is part of a multi-variant product
                        if goods_count.get(goods_value, 0) > 1:
                            # Multiple variants exist - assign sequential color
                            goods_occurrence[goods_value] = goods_occurrence.get(goods_value, 0) + 1
                            color_number = goods_occurrence[goods_value]
                            template_sheet.cell(row=row_idx, column=variation_theme_col_idx, value='Color')
                            template_sheet.cell(row=row_idx, column=color_col_idx, value=f'Color {color_number}')
                        else:
                            # Single variant - use 'One Color'
                            template_sheet.cell(row=row_idx, column=variation_theme_col_idx, value='Color')
                            template_sheet.cell(row=row_idx, column=color_col_idx, value='One Color')
                    else:
                        # Has color value - Variation Theme stays as 'Color' (already set by mapping)
                        # Color value is already set by the mapping
                        pass
                
                print(f"  Applied conditional logic to {len(color_data)} rows")
                print(f"  - Rows with color: Set Variation Theme = 'Color' (existing value)")
                print(f"  - Rows without color: Set Variation Theme = 'Color'")
                print(f"    - Multi-variant products: Sequential 'Color 1', 'Color 2', etc.")
                print(f"    - Single products: 'One Color'")
            else:
                print("  Warning: Could not find Color column or Contribution Goods data")
        else:
            print("  Warning: Could not find Variation Theme column for conditional logic")
        
        # Calculate pricing strategy
        if base_price_col_indices and list_price_col_indices:
            print("Calculating pricing strategy (1x and 1.25x Faire price, floored to X.99)...")
            num_data_rows = len(category_df)
            
            # Get the original Faire price data
            faire_price_col = 'USD Unit Retail Price'
            faire_prices = category_df[faire_price_col].tolist()
            
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
        
        # Special handling for Contribution Goods (transformed from SKU)
        print("Processing Contribution Goods transformation...")
        if 'SKU' in category_df.columns:
            # Get SKU data
            sku_data = category_df['SKU'].tolist()
            
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
        
        # Special handling for Image URLs
        print("Processing Image URLs...")
        if 'Option Image' in category_df.columns or 'Product Images' in category_df.columns:
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
            
            for row_idx, (_, row_data) in enumerate(category_df.iterrows(), 5):
                # Determine which image source to use
                image_urls = []
                
                # First try Option Image
                if 'Option Image' in category_df.columns and pd.notna(row_data['Option Image']):
                    image_urls = [str(row_data['Option Image']).strip()]
                    option_image_count += 1
                # Fallback to Product Images
                elif 'Product Images' in category_df.columns and pd.notna(row_data['Product Images']):
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
            
            print(f"  Processed image URLs for {len(category_df)} rows")
            print(f"    - Used Option Image: {option_image_count} rows")
            print(f"    - Used Product Images: {product_images_count} rows")
            print(f"    - No image data: {no_image_count} rows")
        else:
            print("  Warning: No image columns found in Faire file")
        
        # Process fixed column values with conditional category assignment
        print("Processing fixed column values with conditional category assignment...")
        
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
            
            # Get the number of data rows
            num_data_rows = len(category_df)
            
            # Special handling for Category column with enhanced assignment
            if temu_col == 'Category':
                print("    Applying enhanced category assignment...")
                category_assignments = {}
                
                # Get product names and image data for category assignment
                product_names = []
                image_data = []
                if 'Product Name (English)' in category_df.columns:
                    product_names = category_df['Product Name (English)'].tolist()
                if 'Product Images' in category_df.columns:
                    image_data = category_df['Product Images'].tolist()
                
                # Process each row with enhanced category assignment
                for row_idx in range(5, 5 + num_data_rows):
                    product_name = product_names[row_idx - 5] if row_idx - 5 < len(product_names) else ''
                    img_data = image_data[row_idx - 5] if row_idx - 5 < len(image_data) else None
                    
                    # Use the enhanced category assigner
                    category_code = category_assigner.determine_category(product_name, img_data)
                    
                    # Track category assignments for reporting
                    if category_code not in category_assignments:
                        category_assignments[category_code] = 0
                    category_assignments[category_code] += 1
                    
                    template_sheet.cell(row=row_idx, column=temu_col_idx, value=category_code)
                
                # Report category assignments with descriptions
                print(f"    Category assignments:")
                for category_code, count in category_assignments.items():
                    category_info = category_assigner.get_category_info(category_code)
                    description = category_info['description'] if category_info else 'Unknown'
                    print(f"      {category_code} ({description}): {count} products")
            else:
                # Write fixed value to all data rows for non-category columns
                for row_idx in range(5, 5 + num_data_rows):
                    template_sheet.cell(row=row_idx, column=temu_col_idx, value=fixed_value)
            
            print(f"    Set values for {num_data_rows} rows")
        
        # Save the workbook
        workbook.save(output_file)
        workbook.close()
        
        print(f"Completed processing {category_name} category ({len(category_df)} products)")
    
    # ============================================================================
    # MAIN PROCESSING FUNCTION
    # ============================================================================
    
    try:
        # File paths
        faire_file = 'data/faire_products.xlsx'
        temu_template_file = 'data/temu_template.xlsx'
        
        # Define category configurations
        CATEGORY_CONFIGS = {
            'handbags': {
                'prefixes': ['HBG', 'HW', 'HM', 'HL'],
                'output_file': 'output/temu_template_handbags.xlsx',
                'description': 'Handbags, Wallets, Cosmetic Bags, Travel Bags'
            },
            'other': {
                'prefixes': [],  # Empty means catch-all for anything not in other categories
                'output_file': 'output/temu_template_other.xlsx',
                'description': 'All other products (hats, accessories, etc.)'
            }
            # Future categories can be added here:
            # 'hats': {
            #     'prefixes': ['CAP', 'HAT'],
            #     'output_file': 'output/temu_template_hats.xlsx',
            #     'description': 'Hats and Caps'
            # },
            # 'accessories': {
            #     'prefixes': ['TO-', 'ACC'],
            #     'output_file': 'output/temu_template_accessories.xlsx',
            #     'description': 'Accessories and Straps'
            # }
        }
        
        print("Starting enhanced mapping tool...")
        print(f"Mapping {len(COLUMN_MAPPINGS)} columns")
        print(f"Setting {len(FIXED_COLUMN_VALUES)} fixed values")
        print(f"Categories: {list(CATEGORY_CONFIGS.keys())}")
        
        # Initialize category assigner
        category_assigner = CategoryAssigner()
        print(f"Enhanced category rules: {len(category_assigner.category_rules)} categories available")
        
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
        
        # Step 4: Split data into categories
        print("Splitting data into categories...")
        
        # Get data from row 4 onwards (skip header rows)
        data_df = faire_df.iloc[3:].copy()
        
        # Initialize category data containers
        category_data = {category: [] for category in CATEGORY_CONFIGS.keys()}
        
        # Split data based on SKU prefixes
        for idx, row in data_df.iterrows():
            sku = str(row['SKU']) if pd.notna(row['SKU']) else ''
            assigned_category = None
            
            # Check each category's prefixes (except 'other' which is catch-all)
            for category, config in CATEGORY_CONFIGS.items():
                if category == 'other':
                    continue  # Skip 'other' for now, it's the catch-all
                
                if any(sku.startswith(prefix) for prefix in config['prefixes']):
                    assigned_category = category
                    break
            
            # If no specific category found, assign to 'other'
            if assigned_category is None:
                assigned_category = 'other'
            
            category_data[assigned_category].append(row)
        
        # Print category breakdown
        print("Category breakdown:")
        for category, data in category_data.items():
            config = CATEGORY_CONFIGS[category]
            print(f"  {category.title()}: {len(data)} products ({config['description']})")
        
        # Process each category
        for category, data in category_data.items():
            if len(data) > 0:  # Only process categories with data
                config = CATEGORY_CONFIGS[category]
                print(f"\nProcessing {category} products...")
                process_product_category(data, temu_template_file, config['output_file'], category)
        
        print(f"\nSuccess! Output files saved to:")
        for category, config in CATEGORY_CONFIGS.items():
            if len(category_data[category]) > 0:
                print(f"  {category.title()}: {config['output_file']}")
        
        return  # Exit early since we're now using separate function
        
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
