"""
Category Assignment Module for Faire2Temu

This module handles the intelligent assignment of Temu category codes based on
product names and image data. It uses keyword matching to automatically categorize
products into the appropriate Temu categories.

Usage:
    from category_assigner import CategoryAssigner
    
    assigner = CategoryAssigner()
    category_code = assigner.determine_category(product_name, image_data)
"""

import re
from typing import Optional, List, Dict, Any

class CategoryAssigner:
    """
    Handles intelligent category assignment based on product names and image data.
    
    This class contains all the category assignment logic and rules for mapping
    products to appropriate Temu category codes based on keyword analysis.
    """
    
    def __init__(self):
        """Initialize the category assigner with all category rules."""
        self.category_rules = self._load_category_rules()
        self.default_category = '29153'  # Default category for unmatched products
    
    def determine_category(self, product_name: str, image_data: Optional[str] = None) -> str:
        """
        Determine the appropriate category code based on product name and image data.
        
        Args:
            product_name: The product name to analyze
            image_data: Optional image data (URLs, descriptions) to analyze
            
        Returns:
            str: The category code for the product
        """
        if not product_name:
            return self.default_category
        
        # Normalize product name for case-insensitive matching
        normalized_name = str(product_name).lower()
        
        # Check each category rule in order (first match wins)
        for rule in self.category_rules:
            if self._matches_rule(normalized_name, image_data, rule):
                return rule['category_code']
        
        return self.default_category
    
    def _matches_rule(self, product_name: str, image_data: Optional[str], rule: Dict[str, Any]) -> bool:
        """
        Check if a product matches a specific category rule.
        
        Args:
            product_name: Normalized product name
            image_data: Optional image data
            rule: Category rule dictionary
            
        Returns:
            bool: True if product matches the rule
        """
        # Get the condition function from the rule
        condition_func = rule['condition']
        
        # Call the condition function with product name and image data
        return condition_func(product_name, image_data)
    
    def _load_category_rules(self) -> List[Dict[str, Any]]:
        """
        Load all category assignment rules.
        
        Returns:
            List of category rule dictionaries
        """
        return [
            # Pet Supplies / Small Animals / Carriers
            {
                'category_code': '2062',
                'description': 'Pet Supplies / Small Animals / Carriers',
                'condition': lambda name, img: (
                    any(word in name for word in ['pet', 'animal', 'dog', 'cat', 'bird', 'hamster', 'rabbit', 'guinea', 'ferret']) and
                    any(word in name for word in ['carrier', 'crate', 'kennel', 'bag', 'cage', 'transport'])
                )
            },
            
            # Home & Kitchen / Kitchen & Dining / Kitchen Utensils & Gadgets
            {
                'category_code': '9923',
                'description': 'Home & Kitchen / Kitchen & Dining / Kitchen Utensils & Gadgets',
                'condition': lambda name, img: (
                    any(word in name for word in ['kitchen', 'cooking', 'baking', 'dining', 'food', 'chef']) and
                    any(word in name for word in ['utensil', 'gadget', 'tool', 'set', 'spatula', 'whisk', 'opener', 'strainer', 'grater'])
                )
            },
            
            # Home & Kitchen / Bath / Towels / Beach Towels
            {
                'category_code': '11809',
                'description': 'Home & Kitchen / Bath / Towels / Beach Towels',
                'condition': lambda name, img: (
                    any(word in name for word in ['bath', 'bathroom', 'shower', 'beach', 'pool', 'spa']) and
                    any(word in name for word in ['towel', 'wrap', 'robe', 'bath towel', 'beach towel'])
                )
            },
            
            # Beauty & Personal Care / Foot, Hand & Nail Care / Tools & Accessories
            {
                'category_code': '19843',
                'description': 'Beauty & Personal Care / Foot, Hand & Nail Care / Tools & Accessories',
                'condition': lambda name, img: (
                    any(word in name for word in ['nail', 'foot', 'hand', 'spa', 'pedicure', 'manicure', 'beauty']) and
                    any(word in name for word in ['tool', 'accessory', 'slipper', 'file', 'clipper', 'brush', 'polish'])
                )
            },
            
            # Cell Phones & Accessories / Cases, Holsters & Sleeves
            {
                'category_code': '24380',
                'description': 'Cell Phones & Accessories / Cases, Holsters & Sleeves',
                'condition': lambda name, img: (
                    any(word in name for word in ['phone', 'cell', 'smartphone', 'mobile', 'iphone', 'android']) and
                    any(word in name for word in ['case', 'holster', 'sleeve', 'crossbody', 'lanyard', 'cover', 'protector'])
                )
            },
            
            # Clothing, Shoes & Jewelry / Women / Accessories / Belts
            {
                'category_code': '29264',
                'description': 'Clothing, Shoes & Jewelry / Women / Accessories / Belts',
                'condition': lambda name, img: (
                    any(word in name for word in ['women', 'female', 'ladies', 'woman']) and
                    any(word in name for word in ['belt', 'waistband', 'strap', 'leather belt'])
                )
            },
            
            # Clothing, Shoes & Jewelry / Women / Accessories / Scarves & Wraps
            {
                'category_code': '29290',
                'description': 'Clothing, Shoes & Jewelry / Women / Accessories / Scarves & Wraps',
                'condition': lambda name, img: (
                    any(word in name for word in ['women', 'female', 'ladies', 'woman']) and
                    any(word in name for word in ['scarf', 'wrap', 'shawl', 'stole', 'neck scarf'])
                )
            },
            
            # Clothing, Shoes & Jewelry / Women / Accessories / Sunglasses & Eyewear
            {
                'category_code': '29312',
                'description': 'Clothing, Shoes & Jewelry / Women / Accessories / Sunglasses & Eyewear',
                'condition': lambda name, img: (
                    any(word in name for word in ['eyeglass', 'glasses', 'sunglasses', 'sunglass', 'eye', 'vision']) and
                    any(word in name for word in ['case', 'holder', 'container', 'protector'])
                )
            },
            
            # Clothing, Shoes & Jewelry / Women / Accessories / Wallets
            {
                'category_code': '29324',
                'description': 'Clothing, Shoes & Jewelry / Women / Accessories / Wallets',
                'condition': lambda name, img: (
                    any(word in name for word in ['women', 'female', 'ladies', 'woman']) and
                    any(word in name for word in ['wallet', 'card case', 'money organizer', 'purse', 'coin pouch', 'billfold'])
                )
            },
            
            # Clothing, Shoes & Jewelry / Women / Jewelry / Brooches & Pins
            {
                'category_code': '29522',
                'description': 'Clothing, Shoes & Jewelry / Women / Jewelry / Brooches & Pins',
                'condition': lambda name, img: (
                    any(word in name for word in ['women', 'female', 'ladies', 'woman']) and
                    any(word in name for word in ['brooch', 'pin', 'badge', 'lapel', 'decorative pin'])
                )
            },
            
            # Clothing, Shoes & Jewelry / Women / Jewelry / Necklaces
            {
                'category_code': '29542',
                'description': 'Clothing, Shoes & Jewelry / Women / Jewelry / Necklaces',
                'condition': lambda name, img: (
                    any(word in name for word in ['women', 'female', 'ladies', 'woman']) and
                    any(word in name for word in ['necklace', 'pendant', 'choker', 'chain', 'jewelry'])
                )
            },
            
            # Clothing, Shoes & Jewelry / Luggage & Travel Gear / Cosmetic Cases
            {
                'category_code': '30988',
                'description': 'Clothing, Shoes & Jewelry / Luggage & Travel Gear / Cosmetic Cases',
                'condition': lambda name, img: (
                    any(word in name for word in ['cosmetic', 'make-up', 'makeup', 'beauty']) and
                    any(word in name for word in ['case', 'bag', 'holder', 'organizer', 'travel'])
                )
            },
            
            # Sports & Outdoors / Sports / Leisure Sports / Pickleball / Paddles
            {
                'category_code': '36256',
                'description': 'Sports & Outdoors / Sports / Leisure Sports / Pickleball / Paddles',
                'condition': lambda name, img: (
                    any(word in name for word in ['sport', 'outdoor', 'game', 'pickleball', 'tennis', 'badminton', 'paddle']) and
                    any(word in name for word in ['paddle', 'racket', 'ball', 'set', 'equipment'])
                )
            },
            
            # Arts, Crafts & Sewing / Organization / Pen, Pencil & Marker Cases
            {
                'category_code': '39969',
                'description': 'Arts, Crafts & Sewing / Organization / Pen, Pencil & Marker Cases',
                'condition': lambda name, img: (
                    any(word in name for word in ['art', 'craft', 'sewing', 'school', 'office', 'stationery']) and
                    any(word in name for word in ['pen', 'pencil', 'marker', 'case', 'pouch', 'holder', 'organizer'])
                )
            },
            
            # Books / Children's Books / Education & Reference / Journal Writing
            {
                'category_code': '46208',
                'description': 'Books / Children\'s Books / Education & Reference / Journal Writing',
                'condition': lambda name, img: (
                    any(word in name for word in ['book', 'children', 'kids', 'education', 'reference', 'reading', 'writing', 'journal', 'diary', 'notebook'])
                )
            },
            
            # Original simple rules (keep for backward compatibility)
            {
                'category_code': '29163',
                'description': 'Tote bags and totes',
                'condition': lambda name, img: 'tote' in name
            },
            {
                'category_code': '29164',
                'description': 'Backpacks',
                'condition': lambda name, img: 'backpack' in name
            },
            {
                'category_code': '29165',
                'description': 'Wallets',
                'condition': lambda name, img: 'wallet' in name
            },
        ]
    
    def get_category_info(self, category_code: str) -> Optional[Dict[str, str]]:
        """
        Get information about a specific category code.
        
        Args:
            category_code: The category code to look up
            
        Returns:
            Dictionary with category information or None if not found
        """
        for rule in self.category_rules:
            if rule['category_code'] == category_code:
                return {
                    'code': rule['category_code'],
                    'description': rule['description']
                }
        return None
    
    def get_all_categories(self) -> List[Dict[str, str]]:
        """
        Get a list of all available categories.
        
        Returns:
            List of dictionaries with category codes and descriptions
        """
        return [
            {
                'code': rule['category_code'],
                'description': rule['description']
            }
            for rule in self.category_rules
        ]

# Example usage and testing
if __name__ == "__main__":
    # Test the category assigner
    assigner = CategoryAssigner()
    
    # Test cases
    test_cases = [
        ("Women's Leather Belt", "29264"),
        ("Pet Carrier for Dogs", "2062"),
        ("Kitchen Utensil Set", "9923"),
        ("Beach Towel", "11809"),
        ("Nail Art Tools", "19843"),
        ("iPhone Case", "24380"),
        ("Women's Scarf", "29290"),
        ("Eyeglass Case", "29312"),
        ("Women's Wallet", "29324"),
        ("Women's Brooch", "29522"),
        ("Women's Necklace", "29542"),
        ("Cosmetic Case", "30988"),
        ("Pickleball Paddle", "36256"),
        ("Pen Case", "39969"),
        ("Children's Book", "46208"),
        ("Tote Bag", "29163"),
        ("Backpack", "29164"),
        ("Wallet", "29165"),
        ("Random Product", "29153"),  # Default
    ]
    
    print("Testing Category Assigner:")
    print("=" * 50)
    
    for product_name, expected_category in test_cases:
        actual_category = assigner.determine_category(product_name)
        status = "✅" if actual_category == expected_category else "❌"
        print(f"{status} {product_name} -> {actual_category} (expected: {expected_category})")
    
    print(f"\nDefault category: {assigner.default_category}")
    print(f"Total categories: {len(assigner.category_rules)}") 