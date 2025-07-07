### What is API
API or Application programming interface is like a connection between computer programs. It is an interface, offering a service to other softwares. It generally works on a request response process, where user can get intended responses based on the endpoint they hit with the correct expected reqeust.

### What is FastAPI
A python framework that allows us to build such APIs easily and optimized for high performance as it uses asynchronous servers, it also uses pydantic for validation and transformation of data internally and also uses stralette. It is intuitive, robust, short and fast to code. Because of the asynchronocity, the app can handle multiple sessions, multiple requests all at once.

#### Steps to Run
install fastapi: pip3 install fastapi
install uvicorn(server): pip3 install uvicorn 
to run the server: uvicorn working:app --reload (Doesn't work if env variables are not set)
                OR
                python -m uvicorn working:app --reload

#### Starlette: ASGI
ASGI, or Asynchronous Server Gateway Interface, is a specification for asynchronous web servers and applications in Python. It's designed to handle concurrent connections and real-time communication more efficiently 
Starlette is a lightweight ASGI framework/toolkit, which is ideal for building async web services in Python.
Starlette is not strictly tied to any particular database implementation
FastAPI itself doesn't include an Object-Relational Mapper (ORM), but it readily supports and encourages the use of ORMs for interacting with databases. FastAPI is built on top of Starlette, which doesn't enforce any specific database or ORM choice, making it flexible and adaptable to various database technologies

### Architecture of the application

Here's a clean and production-ready FastAPI boilerplate project scaffold — similar to Spring Boot's layered architecture — with:

    ✅ PostgreSQL support (via SQLAlchemy)

    ✅ Pydantic schemas (DTOs)

    ✅ CRUD-ready service/repository layers

    ✅ .env config

    ✅ Scalable layout


app/
├── api/
│   └── v1/
│       └── item_routes.py        # API endpoints
├── core/
│   └── config.py                 # App config (from .env)
├── db/
│   ├── base.py                   # Base SQLAlchemy model
│   ├── session.py                # DB session maker
│   └── init_db.py                # DB init script
├── models/
│   └── item_model.py             # SQLAlchemy models
├── repository/
│   └── item_repository.py        # DB layer
├── schemas/
│   └── item_schema.py            # Pydantic DTOs
├── services/
│   └── item_service.py           # Business logic
└── main.py                       # App entry point
.env                              # Environment variables
requirements.txt


> requirements.txt
```
fastapi
uvicorn
sqlalchemy
alembic
psycopg2-binary
slowapi
python-dotenv
pyjwt
passlib
bcrypt==4.0.1
python-multipart
email-validator
pydantic
```

> .env

```
DATABASE_URL=postgresql://postgres:password@localhost:5432/fastapi_db

```

> main.py
```
from fastapi import FastAPI
from app.api.v1.item_routes import router as item_router

app = FastAPI(title="FastAPI PostgreSQL App")

app.include_router(item_router, prefix="/items", tags=["Items"])

```

> core/config.py
```
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()

```

> db/session.py
```
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

```

> models/item_model.py
```
from sqlalchemy import Column, Integer, String
from app.db.session import Base

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Integer)

```

> schemas/item_schema.py
```
from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    price: int

class ItemOut(ItemCreate):
    id: int

    class Config:
        orm_mode = True

```

> repository/item_repository.py
```
from sqlalchemy.orm import Session
from app.models.item_model import Item
from app.schemas.item_schema import ItemCreate

def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()

def create_item(db: Session, item: ItemCreate):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

```

> services/item_service.py
```
from sqlalchemy.orm import Session
from app.repository import item_repository
from app.schemas.item_schema import ItemCreate

def fetch_item(db: Session, item_id: int):
    return item_repository.get_item(db, item_id)

def add_item(db: Session, item: ItemCreate):
    return item_repository.create_item(db, item)

```

> api/v1/item_routes.py
```
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.item_schema import ItemCreate, ItemOut
from app.services import item_service

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{item_id}", response_model=ItemOut)
def get_item(item_id: int, db: Session = Depends(get_db)):
    return item_service.fetch_item(db, item_id)

@router.post("/", response_model=ItemOut)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    return item_service.add_item(db, item)

```

> db/init_db.py (run once to create tables)
```
from app.db.session import engine
from app.models import item_model
from app.db.base import Base

def init_db():
    Base.metadata.create_all(bind=engine)

```

>> Run it via:
```
python -m app.db.init_db

```

To start the application:
🐘 Start your PostgreSQL server

🔧 Create DB: CREATE DATABASE fastapi_db;

✅ Set credentials in .env

🏁 Run: uvicorn main:app --reload