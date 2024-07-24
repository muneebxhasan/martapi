from fastapi import HTTPException, APIRouter
from app.crud import product_crud # type: ignore
from app.api.dep import DB_session 
from app.models.productModel import ProductRead
router = APIRouter()


@router.get("/all")
def get_all_products(db: DB_session):
    products=product_crud.get_all_products(db)
    print(products)
    return products



@router.get("/{product_id}", response_model=ProductRead)
def get_product_by_id(product_id: int, db:DB_session):
    try:
        return product_crud.get_product_by_id(product_id, db)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e




