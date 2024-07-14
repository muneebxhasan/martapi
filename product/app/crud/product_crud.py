from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.productModel import Product, ProductImageRead, ProductOptionRead, ProductRead, ProductUpdate, ProductRating ,ProductOption ,ProductImage ,ProductOptionCreate,ProductCreate
from app.core.dp_kafka import Producer
import json
# from app import stock_pb2

def add_new_product(product_data: ProductCreate, session: Session) -> Product:
    try:
        # Convert Pydantic ProductCreate to SQLAlchemy Product
        db_product = Product(
            name=product_data.name,
            description=product_data.description,
            brand=product_data.brand,
            category=product_data.category
        )
        
        # Add options and images to the product
        for option_data in product_data.options:
            db_option = ProductOption(
                product_id=option_data.product_id,
                expiry=option_data.expiry,
                weight=option_data.weight,
                price=option_data.price,
                colour=option_data.colour,
                size=option_data.size
            )
            for image_data in option_data.images:
                db_image = ProductImage(
                    product_option_id=image_data.product_option_id,
                    url=image_data.url
                )
                db_option.images.append(db_image)
            db_product.options.append(db_option)

        print("Adding Product to Database")
        session.add(db_product)
        session.commit()
        session.refresh(db_product)
        return db_product
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Failed to add product to database") from e

def get_all_products(session: Session) -> list[Product]:
    products = session.exec(select(Product)).all()
    products = [product for product in products]
    return products

def get_product_by_id(product_id: int, session: Session) -> ProductRead:
    product = session.exec(
        select(Product).where(Product.id == product_id)
    ).one_or_none()
    
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    # Convert the retrieved Product to ProductRead
    product_read = ProductRead(
        name=product.name,
        description=product.description,
        brand=product.brand,
        category=product.category,
        options=[
            ProductOptionRead(
                product_id=option.product_id,
                expiry=option.expiry,
                weight=option.weight,
                price=option.price,
                colour=option.colour,
                size=option.size,
            
                images=[
                    ProductImageRead(
                        product_option_id=image.product_option_id,
                        url=image.url
                    ) for image in option.images
                ]
            ) for option in product.options
        ]
    )
    
    return product_read

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

async def add_product_option(productv: ProductOptionCreate ,session:Session,producer:Producer):
    product = session.exec(select(Product).where(Product.id == productv.product_id)).one_or_none()
    if not product:
            raise HTTPException(status_code=404, detail="Product not found!!!")
    
    stock = {
        "product_id": productv.product_id,
        "option_id": productv.stock,
        "quantity": productv.stock,
    }
    # item_dict = {field: getattr(item, field) for field in item.dict()} 
    stock = json.dumps(stock).encode("utf-8")

    await producer.send_and_wait("product_stock",stock)
    # new_p = productv.model_dump(exclude_unset=True)
    # new_p = ProductOption(**new_p)
    new_p = ProductOption.model_validate(productv)
    product.options.append(new_p)
    session.commit()
    session.refresh(new_p)

    return new_p

def get_all_option(product_id:int,session:Session):
    v = session.exec(select(ProductOption).where(ProductOption.product_id == product_id)).all()
    return v

def get_option_by_id(option_id:int,session:Session):
    option = session.exec(select(ProductOption).where(ProductOption.id == option_id)).one_or_none()
    if option is None:
        raise HTTPException(status_code=404, detail="Option not found")
    return option

def update_option_by_id(option_id: int, to_update_option_data:ProductOption, session: Session):
    # Step 1: Get the Option by ID
    option = session.exec(select(ProductOption).where(ProductOption.id == option_id)).one_or_none()
    if option is None:
        raise HTTPException(status_code=404, detail="Option not found")
    # Step 2: Update the Option
    hero_data = to_update_option_data.model_dump(exclude_unset=True)
    option.sqlmodel_update(hero_data)
    session.add(option)
    session.commit()
    return option

def delete_option_by_id(option_id: int, session: Session):
    # Step 1: Get the Option by ID
    option = session.exec(select(ProductOption).where(ProductOption.id == option_id)).one_or_none()
    if option is None:
        raise HTTPException(status_code=404, detail="Option not found")
    # Step 2: Delete the Option
    session.delete(option)
    session.commit()
    return {"message": "Option Deleted Successfully"}

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

def get_all_review_of_product(product_id:int,session:Session)->list[ProductRating]:
    reviews = session.exec(select(ProductRating).where(ProductRating.product_id == product_id)).all()
    reviews = [review for review in reviews]
    return reviews

def get_all_review_by_user(user_id:int,session:Session)->list[ProductRating]:
    reviews = session.exec(select(ProductRating).where(ProductRating.user_id == user_id)).all()
    reviews = [review for review in reviews]
    return reviews  

def get_user_review(product_id:int,user_id:int,session:Session):
    
    review = session.exec(select(ProductRating).where(ProductRating.product_id == product_id,ProductRating.user_id == user_id)).all()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return review   

def delete_review_by_id(review_id: int, session: Session):
    # Step 1: Get the Review by ID
    review = session.exec(select(ProductRating).where(ProductRating.id == review_id)).one_or_none()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    # Step 2: Delete the Review
    session.delete(review)
    session.commit()
    return {"message": "Review Deleted Successfully"}

def delete_review_by_user(user_id:int,session:Session):
    reviews = session.exec(select(ProductRating).where(ProductRating.user_id == user_id)).all()
    if not reviews:
        raise HTTPException(status_code=404, detail="User has no reviews")
    for review in reviews:
        session.delete(review)
    session.commit()
    return {"message": "All Reviews Deleted Successfully"}

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

def update_Image_by_id(image_id: int, to_update_image_data:ProductImage, session: Session):
    # Step 1: Get the Image by ID
    image = session.exec(select(ProductImage).where(ProductImage.id == image_id)).one_or_none()
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    # Step 2: Update the Image
    hero_data = to_update_image_data.model_dump(exclude_unset=True)
    image.sqlmodel_update(hero_data)
    session.add(image)
    session.commit()
    return image

def delete_Image_by_id(image_id: int, session: Session):
    # Step 1: Get the Image by ID
    image = session.exec(select(ProductImage).where(ProductImage.id == image_id)).one_or_none()
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    # Step 2: Delete the Image
    session.delete(image)
    session.commit()
    return {"message": "Image Deleted Successfully"}


    