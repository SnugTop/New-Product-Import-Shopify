import csv
import shopify
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('api_info.env')

# Retrieve variables from the environment
api_key = os.getenv('SHOPIFY_API_KEY')
api_secret = os.getenv('SHOPIFY_API_SECRET')
admin_access_token = os.getenv('SHOPIFY_ACCESS_TOKEN_ADMIN')
store_access_token = os.getenv('SHOPIFY_ACCESS_TOKEN_STORE')
shop_name = os.getenv('SHOPIFY_SHOP_NAME')

# Validate that all necessary environment variables are present
if not all([api_key, api_secret, admin_access_token, store_access_token, shop_name]):
    raise EnvironmentError("One or more environment variables are missing. Please check your .env file.")

# Set up Shopify API session
shop_url = f"https://{shop_name}"
api_version = "2023-10"

# Create a new session and activate it
session = shopify.Session(shop_url, api_version, admin_access_token)
shopify.ShopifyResource.activate_session(session)

# Open and read the CSV file
with open('test_products.csv', newline='') as csvfile:  # Change this to the name of your CSV file
 reader = csv.DictReader(csvfile)
 for row in reader:
    try:
        # Create a new product
        new_product = shopify.Product()
        new_product.title = row['Title']
        new_product.body_html = row['Description']
        new_product.vendor = row['Vendor']
        new_product.product_type = row['Type']
        new_product.status = "draft"  # Set product status to draft

        # Create a new variant
        variant = shopify.Variant()
        variant.price = str(row['Price'])
        variant.sku = row['SKU']
        variant.inventory_quantity = int(row['Inventory'])
        variant.inventory_management = 'shopify'  # Enable inventory tracking

        # Assign the variant to the product
        new_product.variants = [variant]

        # Save the product to Shopify
        success = new_product.save()
        if success:
            print(f"Product '{row['Title']}' added successfully.")
        else:
            print(f"Failed to save product '{row['Title']}': {new_product.errors.full_messages()}")
    except Exception as e:
        print(f"An error occurred while processing product '{row['Title']}': {e}")
# Clear the session after the script finishes
shopify.ShopifyResource.clear_session()
