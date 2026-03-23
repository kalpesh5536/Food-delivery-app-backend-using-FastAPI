# all backend using FastAPI
# always use this to run anywhere any proj->  python -m uvicorn main:app --reload


from fastapi import FastAPI,Query, Response,status
from pydantic import BaseModel, Field
from typing import Optional

app= FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ---------------- Menu Data sample -------------------

menu=[
    
   { "id":1, "name": "pav Bhaji", "price":99,"category":"food","is_available": True},
   { "id":2, "name": "Pani puri","price":40,"category":"food", "is_available":True },
   { "id":3, "name":"chez pizza", "price":199,"category":"Pizza","is_available":True},
   {"id":4,"name":"veg Burger","price":149,"category":"Burger","is_available":True},
   {"id":5,"name":"plan pizza","price":129,"category":"Pizza","is_available":False},
   {"id":6,"name":"coke","price":49,"category":"Drink","is_available":True},
   {"id":7,"name":"ice cake","price":399,"category":"Dessert","is_available":True},
   {"id":8,"name":"cold coffee","price":89,"category":"Drink","is_available":True}
   
]

orders=[]
order_counter=1

# --------- Pydantic Model -----------------

class OrderRequest(BaseModel):
    customer_name:str=Field(..., min_length=2)
    item_id:int= Field(..., gt=0) # gt= grater than or equal to
    quantity:int =Field(..., gt=0, le=20) # le= length
    delivery_address:str=Field(..., min_length=10)
    order_type:str ="delivery"
    
class NewMenuItem(BaseModel):
    name:str=Field(..., min_length=2)
    price:int=Field(...,gt=0)
    category:str=Field(..., min_length=2)
    is_available:bool=True
    
class CheckoutRequest(BaseModel):
    customer_name:str=Field(..., min_length=2)
    delivery_address:str=Field(..., min_length=10)


# --------- Helper functions ----------------

# find Item
def find_menu_item(item_id):
    for item in menu:
        if item["id"]==item_id:
            return item
    return None

# calculate bill
def calculate_bill(price,quantity,order_type):
    total=price*quantity
    
    if order_type=="delivery":
        total+=30    # delilvery charge
    return total

# To apply filter
def filter_menu_logic(category=None, max_price=None,is_available=None):
    result=menu
    
    if category is not None:
        result=[i for i in result if i["category"]==category]
        
    if max_price is not None:
        result = [i for i in result if i["price"]<=max_price]
    
    if is_available is not None:
        result= [ i for i in result if i["is_available"]==is_available]
        
    return result


# Routes
@app.get("/")
def home():
    return{"message": "Welcome to QuickBite Food delivery by kalpesh"}

@app.get("/menu")
def get_menu():
    return {"menu":menu,"total":len(menu)}

# Menu fixed routes

@app.get("/menu/summary")
def menu_summary():
    available = [item for item in menu if item["is_available"]]
    unavailable=[item for item in menu if not item["is_available"]]
    
    categories= list({item["category"] for item in menu})
    
    return {
        "total_items": len(menu),
        "available": len(available),
        "unavailable": len(unavailable),
        "categories": categories
    }
    
    
@app.get("/menu/filter")
def filter_menu(
    category: str= Query(None),
    max_price: int = Query(None),
    is_available: bool=Query(None)
):
    result= filter_menu_logic(category,max_price,is_available)
    return {"items":result, "count": len(result)}

# SEARCH
@app.get("/menu/search")
def search(keyword: str):
    result= [
        i for i in menu
        if keyword.lower() in i["name"].lower()
        or keyword.lower() in i ["category"].lower()
    ]
    
    if not result:
        return {"message": "No items found"}
    return {"items": result, "Total": len(result)}


# Sort
@app.get("/menu/sort")
def sort_menu(sort_by : str="price", order:str= "asc"):
    
    if sort_by not in ["price","name","category"]:
        return {"error":"Invalid sort field"}
    
    reverse = True if order == "desc" else False
    sorted_menu = sorted(menu,key=lambda x: x[sort_by], reverse=reverse)
    return {"sorted": sorted_menu}

#  PAGINATION
@app.get("/menu/page")
def paginate(page:int=1, limit:int=4):
    
    start= (page-1)*limit
    data = menu[start:start+limit]
    
    total_pages=(len(menu)+ limit-1) // limit
    return {
        "page": page,
        "limit": limit,
        "total":len(menu),
        "total_pages":total_pages,
        "items":data
    }


@app.get("/menu/browse")
def browser(
    keyword: str=None,
    sort_by:str="price",
    order: str= "asc",
    page: int =1,
    limit: int =4
):
    result= menu
    if keyword:
        result= [i for i in result if keyword.lower() in i["name"].lower()]
    reverse= True if order == "desc" else False
    result= sorted(result, key=lambda x:x[sort_by],reverse=reverse)
    
    start=(page-1) * limit
    paginated= result[start:start+ limit]
    return {
        "total": len(result),
        "page": page,
        "items":paginated
    }
    

# Menu CRUD (fixed + variable)
@app.post("/menu")
def add_item(item: NewMenuItem, response:Response):
    names=[i["name"].lower() for i in menu]
    
    if item.name.lower() in names:
        response.status_code= status.HTTP_400_BAD_REQUEST
        return {"error": "Item already exists"}
    
    new_id= max(i["id"] for i in menu)+1
    
    new_item ={
        "id": new_id,
        "name":item.name,
        "price":item.price,
        "category":item.category,
        "is_available":item.is_available
    }
    menu.append(new_item)
    response.status.code= status.HTTP_201_CREATED
    return new_item


# Update
@app.put("/menu/{item_id}")
def update_item(
    item_id:int,
    price:int=Query(None),
    is_available:bool=Query(None)
):
    item= find_menu_item(item_id)
    if not item:
        return {"error":"item not found"}
    if price is not None:
        item["price"]=price
    if is_available is not None:
        item["is_available"] = is_available

    return item
  

# delete
@app.delete("/menu/{item_id}")
def delete_item(item_id: int):

    item = find_menu_item(item_id)
    if not item:
        return {"error": "Item not found"}
    menu.remove(item)
    return {"message": f"{item['name']} deleted"}



# Orders routes
@app.get("/orders")
def get_orders():
    return {"orders": orders, "total_orders": len(orders)}



@app.get("/orders/search")
def search_orders(name: str):

    result = [o for o in orders if name.lower() in o["customer_name"].lower()]
    return result

@app.get("/orders/sort")
def sort_orders(order: str = "asc"):

    reverse = True if order == "desc" else False
    return sorted(orders, key=lambda x: x["total_price"], reverse=reverse)


@app.post("/orders")
def place_order(order: OrderRequest):

    global order_counter

    item = find_menu_item(order.item_id)

    if not item:
        return {"error": "Item not found"}

    if not item["is_available"]:
        return {"error": "Item not available"}

    total = calculate_bill(item["price"], order.quantity, order.order_type)

    new_order = {
        "order_id": order_counter,
        "customer_name": order.customer_name,
        "item": item["name"],
        "quantity": order.quantity,
        "total_price": total,
        "order_type": order.order_type,
        "delivery_address":order.delivery_address
        
    }
    orders.append(new_order)
    order_counter += 1

    return new_order

    
# cart routes
cart =[]

@app.get("/cart")
def get_cart():

    total = sum(i["price"] * i["quantity"] for i in cart)

    return {"cart": cart, "total": total}

#  Add to cart
@app.post("/cart/add") 
def add_to_cart(item_id: int, quantity: int = 1):

    item = find_menu_item(item_id)

    if not item or not item["is_available"]:
        return {"error": "Item not available"}

    for c in cart:
        if c["item_id"] == item_id:
            c["quantity"] += quantity
            return {"message": "Updated quantity", "cart": cart}

    cart.append({
        "item_id": item_id,
        "name": item["name"],
        "quantity": quantity,
        "price": item["price"]
    })

    return {"cart": cart}

@app.post("/cart/checkout")
def checkout(data: CheckoutRequest):

    if not cart:
        return {"error": "Cart empty"}

    total = 0
    placed_orders = []

    for c in cart:
        bill = c["price"] * c["quantity"]
        total += bill

        placed_orders.append({
            "item": c["name"],
            "qty": c["quantity"],
            "price": bill
        })

    cart.clear()

    return {
        "orders": placed_orders,
        "grand_total": total
    }



# Q15 — REMOVE + CHECKOUT
@app.delete("/cart/{item_id}")
def remove_cart(item_id: int):

    for item in cart:
        if item["item_id"] == item_id:
            cart.remove(item)
            return {"message": "Removed"}

    return {"error": "Item not in cart"}


@app.get("/menu/{item_id}")
def get_item(item_id: int):

    for item in menu:
        if item["id"] == item_id:
            return item

    return {"error": "Item not found"}
