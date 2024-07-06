from fastapi import HTTPException, APIRouter
from app.crud import product_crud # type: ignore
from app.api.dep import DB_session 
from app.models.productModel import Product, ProductRating, ProductUpdate, ProductList ,ProductOption,ProductBase,ProductImage

router = APIRouter()

@router.get("/all", response_model=ProductList)
def get_all_products(session: DB_session):
    return {"products": product_crud.get_all_products(session)}

@router.get("/{product_id}", response_model=Product)
def get_product_by_id(product_id: int, session:DB_session):
    try:
        return product_crud.get_product_by_id(product_id, session)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e


@router.post("/add", response_model=ProductBase)
def add_new_product(product: Product, session:DB_session ):
    try:
        return product_crud.add_new_product(product,session)
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


@router.put("/update/{product_id}", response_model=ProductUpdate)
def update_product_by_id(product_id: int, to_update_product_data: ProductUpdate, session:DB_session):
    try:
        return product_crud.update_product_by_id(product_id, to_update_product_data, session)
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


@router.post("/variation/", response_model=ProductOption)
def add_review_to_product( product_v:ProductOption, session:DB_session):
    try:
       product =  product_crud.add_product_variation(product_v, session)
       return product
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e


@router.get("/variation/{product_id}")
def get_all_product_variation(product_id:int,session:DB_session):
    try:
        return product_crud.get_all_variation(product_id,session)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e
