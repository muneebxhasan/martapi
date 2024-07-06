from typing import Optional
from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.productModel import Product, ProductUpdate, ProductRating ,ProductOption ,ProductImage
from app.core.dp_kafka import Producer


def add_new_product(product_data: Product, session: Session):
    
    
    try:
        print("Adding Product to Database")
        session.add(product_data)
        session.commit()
        session.refresh(product_data)
        return product_data
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to add product to database") from e

def get_all_products(session: Session) -> list[Product]:
    products = session.exec(select(Product)).all()
    products = [product for product in products]
    return products

def get_product_by_id(product_id: int, session: Session):
    product = session.exec(select(Product).where(Product.id == product_id)).one_or_none()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

def update_product_by_id(product_id: int, to_update_product_data:ProductUpdate, session: Session):
    # Step 1: Get the Product by ID
    product = session.exec(select(Product).where(Product.id == product_id)).one_or_none()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    # Step 2: Update the Product
    hero_data = to_update_product_data.model_dump(exclude_unset=True)
    product.sqlmodel_update(hero_data)
    session.add(product)
    session.commit()
    return product

def delete_product_by_id(product_id: int, session: Session):
    # Step 1: Get the Product by ID
    product = session.exec(select(Product).where(Product.id == product_id)).one_or_none()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    # Step 2: Delete the Product
    session.delete(product)
    session.commit()
    return {"message": "Product Deleted Successfully"}



def add_product_review( productrating:ProductRating, session: Session):
        # Step 1: Get the Product by ID
        product = session.exec(select(Product).where(Product.id == productrating.product_id)).one_or_none()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found!!!")
        
        # Step 2: Create a new review
        new_review = ProductRating.model_validate(productrating)
        # print(new_review)
        # Step 3: Add the review to the product
        product.ratings.append(new_review)
        print("debugging product")
        # Step 4: Commit the changes
        session.commit()
        session.refresh(new_review)
        
        return new_review

def add_product_Image( product_i:ProductImage, session: Session):
        # Step 1: Get the Product by ID
        product = session.exec(select(Product).where(Product.id == product_i.product_id)).one_or_none()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found!!!")
        
        # Step 2: Create a new Image
        new_review = ProductImage.model_validate(product_i)
        # print(new_review)
        # Step 3: Add the Image to the product
        product.images.append(new_review)
        print("debugging product")
        # Step 4: Commit the changes
        session.commit()
        session.refresh(new_review)
        
        return new_review

def get_all_Image(product_id:int,session:Session):
    v = session.exec(select(ProductImage).where(ProductImage.product_id == product_id)).all()
    return v

def add_product_variation(productv: ProductOption ,session:Session):
    product = session.exec(select(Product).where(Product.id == productv.product_id)).one_or_none()
    if not product:
            raise HTTPException(status_code=404, detail="Product not found!!!")
    
    new_v = ProductOption.model_validate(productv)

    product.variation.append(new_v)
    session.commit()
    session.refresh(new_v)

    return new_v

def get_all_variation(product_id:int,session:Session):
    v = session.exec(select(ProductOption).where(ProductOption.product_id == product_id)).all()
    return v