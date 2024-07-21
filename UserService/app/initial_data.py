from sqlmodel import Session
from app.core.db_eng import engine,init_db

def init():
    with Session(engine) as session:
        init_db(session)
    

def main():
    init()


if __name__ == "__main__":
    main()

