from fastapi import FastAPI, Path, Query, HTTPException, status
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# get endpoint examples
@app.get("/")
def home():
    return {"Data":"Test"}


@app.get("/about")
def about():
    return {
        "Name": "Aman",
        "Age": 27,
        "City": "Bangalore"
        }


# creating an inventory

inventory={
    1:{
        "name":"mobile",
        "price":50000,
        "brand":"samsung",
        "count":5
    },
    2:{
        "name":"mobile",
        "price":20000,
        "brand":"motorola",
        "count":15
    },
    3:{
        "name":"laptop",
        "price":90000,
        "brand":"apple",
        "count":12
    },
    4:{
        "name":"laptop",
        "price":70000,
        "brand":"lenovo",
        "count":5
    },
    5:{
        "name":"mobile",
        "price":40000,
        "brand":"apple",
        "count":58
    }
}

# getting an item by using their id

@app.get("/get-item-by-id/{id}")
def getItemById(id:int):
    return {"Item": inventory.get(id)}


# Since FastAPI provides us with automatic documentation, we can utilize it more.
# To do this, we can use Path, which is used with path parameters to provide more information

@app.get("/get-item-by-name/{name}")
def getItemByName(name:str = Path(description="The name of the item user is searching for")):
    results = {k: v for k, v in inventory.items() if v["name"].lower() == name.lower()}
    return {"items": results}


# Lets see query parameters
@app.get("/get-item-by-brand")
def getItemByBrand(brand: str): #automatically understands that this is a query parameter
    results = {k: v for k,v in inventory.items() if v["brand"].lower() == brand.lower()}
    return {"items": results}

# Optional query parameter (give default value)
@app.get("/get-item-by-brand-optional-queryparam")
def getItemByBrand(brand: str = None): #Makes the query param as optional
    results = {k: v for k,v in inventory.items() if v["brand"].lower() == brand.lower()}
    return {"items": results}

@app.get("/get-item-by-name-and-inventory-more-than")
def getItemByNameAndInventoryMoreThan(name: str, count: int = None):
    if count is not None:
        results = {k: v for k,v in inventory.items() 
                if (v["name"].lower() == name.lower() and v["count"] > count)}
    else:
        results = {k: v for k,v in inventory.items() 
                if (v["name"].lower() == name.lower())}
    return {"items" : results}

# Path parameters and Query parameters together:
@app.get("/get-item-by-name-and-price-range/{name}")
def getItemByNameAndPriceRange(name:str, priceMin:int=0, priceMax:int=None):
    if priceMax is not None:
        results = {k:v for k,v in inventory.items()
                   if(v["name"].lower() == name.lower() and v["price"] > priceMin and v["price"] < priceMax)}
    else:
        results = {k:v for k,v in inventory.items()
                   if(v["name"].lower() == name.lower() and v["price"] > priceMin)}
    return {"items" : results}


# Using Request Body
# For this, we need to have the class that the request body will follow the structure of
# we also need pydantic import for this as basemodel

#The optional is also imported from typing, that can be used at multiple places
# creating the class first
class Item(BaseModel):
    name:str
    price:float
    brand:Optional[str] = None
    count: int

@app.post("/create-item/{item_id}")
def createItem(item_id: int, item: Item): # FastAPI automatically understands that since its a post request it will have a request body
    if item_id in inventory:
        # return {"Error": "item id already exists"}
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST) # this uses the HTTPException and status
    # inventory[item_id] = {"name":item.name, "brand":item.brand, "price":item.price, "count":item.count}
    inventory[item_id] = item; # this also works as the above line.
    return inventory[item_id]

# updating an item

@app.put("/update-item/{id}")
def updateItem(id:int, item:Item):
    if id not in inventory:
        # return {"Error": "Id is not present in the inventory"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # inventory[id] = item
    inventory[id].update(item) #another way of updating, above line of code also works
    return inventory[id]

# We can work with Item class above as well, BUT that would lead the user to provide values for all variables
# So we can create a DTO for UpdateItem

class UpdateItemDTO(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = 0
    brand: Optional[str] = None
    count: Optional[int] = 0

@app.put("/update-item-with-dto/{id}")
def updateItemWithDTO(id:int, item:UpdateItemDTO):
    if id not in inventory:
        return {"Error": "Id is not present in the inventory"}
    # inventory[id] = item
    update_data = item.model_dump(exclude_unset=True) # This lets the values that already exist as it is.
    inventory[id].update(update_data) #another way of updating, above line of code also works
    return inventory[id]


# Deleting an item
@app.delete("/delete-item")
def deleteItem(id:int = Query(...,description="The id of the item to be deleted")):
    if id not in inventory:
        # return {"Error" : "id does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    del inventory[id]
    return {"Success" : "Item deleted"}