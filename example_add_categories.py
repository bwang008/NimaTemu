"""
Example script showing how to add new categories to the Faire2Temu processing.

This demonstrates the flexible category system that can handle multiple product types.
"""

from Faire2Temu import copy_mapped_data, add_category_config

def example_with_hats_category():
    """Example: Add a hats category and run the processing"""
    
    print("=== Example: Adding Hats Category ===")
    
    # Add a new category for hats
    add_category_config(
        category_name='hats',
        prefixes=['CAP', 'HAT'],  # SKU prefixes for hats
        output_file='output/temu_template_hats.xlsx',
        description='Hats, Caps, and Headwear'
    )
    
    # Add a new category for accessories
    add_category_config(
        category_name='accessories',
        prefixes=['TO-', 'ACC'],  # SKU prefixes for accessories
        output_file='output/temu_template_accessories.xlsx',
        description='Accessories, Straps, and Small Items'
    )
    
    # Run the processing with the new categories
    print("\nRunning processing with new categories...")
    copy_mapped_data()

def example_modify_existing_categories():
    """Example: Modify existing categories"""
    
    print("=== Example: Modifying Categories ===")
    
    # You can also modify the CATEGORY_CONFIGS directly in the main script
    # or use the helper function to override existing categories
    
    # Example: Split handbags into more specific categories
    add_category_config(
        category_name='wallets',
        prefixes=['HW'],  # Just wallets
        output_file='output/temu_template_wallets.xlsx',
        description='Wallets and Coin Purses'
    )
    
    add_category_config(
        category_name='handbags_only',
        prefixes=['HBG'],  # Just handbags (not wallets)
        output_file='output/temu_template_handbags_only.xlsx',
        description='Handbags Only (excluding wallets)'
    )
    
    print("\nRunning processing with modified categories...")
    copy_mapped_data()

if __name__ == "__main__":
    print("Faire2Temu Category Management Examples")
    print("=" * 50)
    
    # Uncomment one of these to see examples:
    # example_with_hats_category()
    # example_modify_existing_categories()
    
    print("\nTo run examples, uncomment the function calls above.")
    print("\nCurrent default categories:")
    print("- handbags: HBG, HW, HM, HL prefixes")
    print("- other: catch-all for everything else") 