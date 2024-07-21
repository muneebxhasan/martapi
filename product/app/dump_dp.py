# from sqlmodel import SQLModel, Session, create_engine, select
# from typing import List, Optional
# from random import randint, choice
# from faker import Faker
# from app.models import ProductImageCreate, ProductOptionCreate, Product
# from app.core.db_eng import engine

# # Helper function to create dummy product images
# def create_product_images(option_id: int, count: int):
#     return [ProductImageCreate(product_option_id=option_id, url=f"http://example.com/image{option_id}_{i}.jpg") for i in range(count)]

# # Helper function to create dummy product options
# def create_product_options(product_id: int, count: int):
#     options = []
#     for i in range(count):
#         option_id = product_id * 10 + i
#         options.append(ProductOptionCreate(
#             product_id=product_id,
#             expiry=fake.date_this_year(),
#             weight=round(fake.random_number(digits=2, fix_len=True) / 10, 2),
#             price=round(fake.random_number(digits=3, fix_len=True) / 10, 2),
#             colour=fake.color_name(),
#             size=randint(36, 46),
#             stock=randint(0, 100),
#             images=create_product_images(option_id, randint(1, 3))
#         ))
#     return options

# # Function to create and add dummy products to the database
# def add_dummy_products(session: Session, num_products: int):
#     products = []
#     for i in range(num_products):
#         products.append(Product(
#             name=fake.product_name(),
#             description=fake.text(),
#             brand=fake.company(),
#             category=choice(["Electronics", "Clothing", "Home", "Sports", "Books"]),
#             options=create_product_options(i + 1, 3)
#         ))

#     for product in products:
#         session.add(product)
#     session.commit()

# # Use the function to add products to the database
# with Session(engine) as session:
#     add_dummy_products(session, 20)