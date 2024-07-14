from fastapi import HTTPException, APIRouter
from app.crud import product_crud # type: ignore
from app.api.dep import DB_session 
from app.models.productModel import Product, ProductRating, ProductRead, ProductUpdate, ProductList ,ProductOption,ProductBase,ProductImage,ProductOptionCreate,ProductCreate
from app.core.dp_kafka import Producer
router = APIRouter()

@router.post("/add", response_model=ProductBase)
def add_new_product(product: ProductCreate,session:DB_session ):
    # try:
        return product_crud.add_new_product(product,session)
    # except HTTPException as http_err:
    #     raise http_err
    # except Exception as e:
    #    return e

@router.get("/all", response_model=ProductList)
def get_all_products(session: DB_session):
    return {"products": product_crud.get_all_products(session)}

@router.get("/{product_id}", response_model=ProductRead)
def get_product_by_id(product_id: int, session:DB_session):
    try:
        return product_crud.get_product_by_id(product_id, session)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e

@router.put("/update/{product_id}", response_model=ProductUpdate)
def update_product_by_id(product_id: int, to_update_product_data: ProductUpdate, session:DB_session):
    try:
        return product_crud.update_product_by_id(product_id, to_update_product_data, session)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e

@router.delete("/delete/{product_id}", response_model=dict)
def delete_product_by_id(product_id: int, session:DB_session):
    try:
        product_crud.delete_product_by_id(product_id, session)
        return {"detail": "Product deleted"}
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e

@router.post("/option/", response_model=ProductOption)
async def add_product_option( product_v:ProductOptionCreate,session:DB_session,producer:Producer):
    try:
       product = await product_crud.add_product_option(product_v,session,producer)
       return product
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e

@router.get("/option/{product_id}")
def get_all_product_option(product_id:int,session:DB_session):
    try:
        return product_crud.get_all_option(product_id,session)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e

@router.get("/option/{option_id}")
def get_option_by_id(option_id:int,session:DB_session):
    try:
        return product_crud.get_option_by_id(option_id,session)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e

@router.put("/option/{option_id}", response_model=ProductOption)
def update_option_by_id(option_id:int, product_data:ProductOption, session:DB_session):
    try:
        return product_crud.update_option_by_id(option_id,product_data,session)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e

@router.delete("/option/{option_id}")
def delete_option_by_id(option_id:int,session:DB_session):
    try:
        return product_crud.delete_option_by_id(option_id,session)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e

@router.post("/review/{product_id}", response_model=ProductRating)
def add_review_product( productrating:ProductRating, session:DB_session):
    try:
        return product_crud.add_product_review(productrating, session)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e

@router.get("/review/product/{product_id}")
def get_all_product_review(product_id:int,session:DB_session):
    try:
        return product_crud.get_all_review_of_product(product_id,session)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e
    
@router.get("/reviews/user/{user_id}")
def get_all_user_review(user_id:int,session:DB_session):
    try:
        return product_crud.get_all_review_by_user(user_id,session)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e    

@router.get("/review/product/{product_id}/user/{user_id}")
def get_user_review(product_id:int,user_id:int,session:DB_session):
    try:
        return product_crud.get_user_review(product_id,user_id,session)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e

@router.delete("/review/{review_id}")
def delete_review(review_id:int,session:DB_session):
    try:
        return product_crud.delete_review_by_id(review_id,session)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e

@router.delete("/review/user/{user_id}")
def delete_user_review(user_id:int,session:DB_session):
    try:
        return product_crud.delete_review_by_user(user_id,session)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e

@router.post("/image/", response_model=ProductImage)
def add_Image_to_product( product_v:ProductImage, session:DB_session):
    try:
       product =  product_crud.add_product_Image(product_v, session)
       return product
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e

@router.get("/image/{product_id}")
def get_all_product_Image(product_id:int,session:DB_session):
    try:
        return product_crud.get_all_Image(product_id,session)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e

@router.put("/image/{image_id}", response_model=ProductImage)
def update_Image_by_id(image_id:int, product_data:ProductImage, session:DB_session):
    try:
        return product_crud.update_Image_by_id(image_id,product_data,session)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e

@router.delete("/image/{image_id}")
def delete_Image(image_id:int,session:DB_session):
    try:
        return product_crud.delete_Image_by_id(image_id,session)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e

