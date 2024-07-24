from fastapi import HTTPException, APIRouter
from app.crud import product_crud # type: ignore
from app.api.dep import DB_session 
from app.models.productModel import Product, ProductRating,ProductUpdate ,ProductOption,ProductImage,ProductOptionCreate,ProductCreate
from app.core.dp_kafka import Producer
router = APIRouter()


@router.post("/add",response_model=Product)
async def add_new_product(product: ProductCreate,db:DB_session,producer:Producer):
    # try:
        productt = await product_crud.add_new_product(product,db,producer)
        return productt
    # except HTTPException as http_err:
    #     raise http_err
    # except Exception as e:
    #    return e



@router.put("/update/{product_id}", response_model=ProductUpdate)
def update_product_by_id(product_id: int, to_update_product_data: ProductUpdate, db:DB_session):
    try:
        return product_crud.update_product_by_id(product_id, to_update_product_data, db)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e

@router.delete("/delete/{product_id}", response_model=dict)
def delete_product_by_id(product_id: int, db:DB_session):
    try:
        product_crud.delete_product_by_id(product_id, db)
        return {"detail": "Product deleted"}
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e

@router.post("/option/")
async def add_product_option( product_v:ProductOptionCreate,db:DB_session,producer:Producer):
    try:
       product = await product_crud.add_product_option(product_v,db,producer)
       return product
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e

@router.get("/option/{product_id}")
def get_all_product_option(product_id:int,db:DB_session):
    try:
        return product_crud.get_all_option(product_id,db)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e

@router.get("/option/{option_id}")
def get_option_by_id(option_id:int,db:DB_session):
    try:
        return product_crud.get_option_by_id(option_id,db)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e

@router.put("/option/{option_id}", response_model=ProductOption)
def update_option_by_id(option_id:int, product_data:ProductOption, db:DB_session):
    try:
        return product_crud.update_option_by_id(option_id,product_data,db)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e

@router.delete("/option/{option_id}")
def delete_option_by_id(option_id:int,db:DB_session):
    try:
        return product_crud.delete_option_by_id(option_id,db)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e

@router.post("/review/{product_id}", response_model=ProductRating)
def add_review_product( productrating:ProductRating, db:DB_session):
    try:
        return product_crud.add_product_review(productrating, db)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e

@router.get("/review/product/{product_id}")
def get_all_product_review(product_id:int,db:DB_session):
    try:
        return product_crud.get_all_review_of_product(product_id,db)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e
    
@router.get("/reviews/user/{user_id}")
def get_all_user_review(user_id:int,db:DB_session):
    try:
        return product_crud.get_all_review_by_user(user_id,db)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e    

@router.get("/review/product/{product_id}/user/{user_id}")
def get_user_review(product_id:int,user_id:int,db:DB_session):
    try:
        return product_crud.get_user_review(product_id,user_id,db)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e

@router.delete("/review/{review_id}")
def delete_review(review_id:int,db:DB_session):
    try:
        return product_crud.delete_review_by_id(review_id,db)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e

@router.delete("/review/user/{user_id}")
def delete_user_review(user_id:int,db:DB_session):
    try:
        return product_crud.delete_review_by_user(user_id,db)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e

@router.post("/image/", response_model=ProductImage)
def add_Image_to_product( product_v:ProductImage, db:DB_session):
    try:
       product =  product_crud.add_product_Image(product_v, db)
       return product
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e

@router.get("/image/{product_id}")
def get_all_product_Image(product_id:int,db:DB_session):
    try:
        return product_crud.get_all_Image(product_id,db)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e

@router.put("/image/{image_id}", response_model=ProductImage)
def update_Image_by_id(image_id:int, product_data:ProductImage, db:DB_session):
    try:
        return product_crud.update_Image_by_id(image_id,product_data,db)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e

@router.delete("/image/{image_id}")
def delete_Image(image_id:int,db:DB_session):
    try:
        return product_crud.delete_Image_by_id(image_id,db)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e

