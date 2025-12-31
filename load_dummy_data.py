#!/usr/bin/env python
"""
Script to load dummy data WITHOUT images into Django database.
Run this script after setting up your Django project and migrations.
"""

import os
import sys
import json
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flipkart_clone.settings')
django.setup()

from products.models import Category, Product


def load_dummy_data():
    """Load categories and products from dummy_data.json file WITHOUT images."""
    
    json_file_path = 'dummy_data.json'
    
    if not os.path.exists(json_file_path):
        print(f"Error: {json_file_path} not found!")
        return
    
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("=" * 60)
    print("Loading Dummy Data into Database")
    print("=" * 60)
    
    # Load Categories
    print("\n📁 Loading Categories...")
    categories_created = 0
    category_map = {}
    
    for cat_data in data['categories']:
        category, created = Category.objects.get_or_create(
            name=cat_data['name']
        )
        category_map[cat_data['name']] = category
        
        if created:
            categories_created += 1
            print(f"  ✓ Created: {category.name}")
        else:
            print(f"  → Exists: {category.name}")
    
    print(f"\n✅ Categories loaded: {categories_created} new, {len(data['categories']) - categories_created} existing")
    
    # Load Products
    print("\n📦 Loading Products...")
    products_created = 0
    products_skipped = 0
    
    for prod_data in data['products']:
        category = category_map.get(prod_data['category'])
        
        if not category:
            print(f"  ⚠ Skipped: {prod_data['name']} (Category not found)")
            products_skipped += 1
            continue
        
        # Check if product already exists
        if Product.objects.filter(name=prod_data['name']).exists():
            print(f"  → Exists: {prod_data['name']}")
            continue
        
        # Create new product WITHOUT image field
        product = Product.objects.create(
            name=prod_data['name'],
            description=prod_data['description'],
            price=prod_data['price'],
            category=category
            # NO IMAGE FIELD - Let Django handle it as NULL
        )
        
        products_created += 1
        print(f"  ✓ Created: {product.name} - ₹{product.price}")
    
    print(f"\n✅ Products loaded: {products_created} new, {products_skipped} skipped")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total Categories: {Category.objects.count()}")
    print(f"Total Products: {Product.objects.count()}")
    print(f"\nNew entries added:")
    print(f"  • Categories: {categories_created}")
    print(f"  • Products: {products_created}")
    print("\n" + "=" * 60)
    print("✨ Data loading complete!")
    print("=" * 60)
    print("\n📝 NOTE: Products loaded WITHOUT images.")
    print("   Templates will show fallback icons automatically.")
    print("\n")


if __name__ == '__main__':
    try:
        load_dummy_data()
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
