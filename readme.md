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