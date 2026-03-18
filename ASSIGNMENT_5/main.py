from fastapi import FastAPI, Query, HTTPException

app = FastAPI()

products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics"},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery"},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics"},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery"},
]

orders = []
order_counter = 1

@app.get("/")
def home():
    return {"message": "FastAPI Day 6 Assignment"}

@app.get("/products")
def get_products():
    return {"products": products}

@app.get("/products/search")
def search_products(keyword: str = Query(...)):
    result = [p for p in products if keyword.lower() in p["name"].lower()]
    if not result:
        return {"message": f"No products found for: {keyword}"}
    return {"keyword": keyword, "total_found": len(result), "products": result}

@app.get("/products/sort")
def sort_products(sort_by: str = Query("price"), order: str = Query("asc")):
    if sort_by not in ["price", "name"]:
        raise HTTPException(status_code=400, detail="sort_by must be 'price' or 'name'")
    reverse = True if order == "desc" else False
    result = sorted(products, key=lambda p: p[sort_by], reverse=reverse)
    return {"sort_by": sort_by, "order": order, "products": result}

@app.get("/products/page")
def paginate_products(page: int = Query(1, ge=1), limit: int = Query(2, ge=1)):
    start = (page - 1) * limit
    total = len(products)
    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": -(-total // limit),
        "products": products[start:start + limit]
    }

@app.get("/products/sort-by-category")
def sort_by_category():
    result = sorted(products, key=lambda p: (p["category"], p["price"]))
    return {"products": result, "total": len(result)}

@app.get("/products/browse")
def browse_products(
    keyword: str = Query(None),
    sort_by: str = Query("price"),
    order: str = Query("asc"),
    page: int = Query(1, ge=1),
    limit: int = Query(4, ge=1, le=20)
):
    result = products
    if keyword:
        result = [p for p in result if keyword.lower() in p["name"].lower()]
    if sort_by in ["price", "name"]:
        result = sorted(result, key=lambda p: p[sort_by], reverse=(order == "desc"))
    total = len(result)
    start = (page - 1) * limit
    paginated = result[start:start + limit]
    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "limit": limit,
        "total_found": total,
        "total_pages": -(-total // limit),
        "products": paginated
    }

@app.get("/products/{product_id}")
def get_product(product_id: int):
    for p in products:
        if p["id"] == product_id:
            return p
    raise HTTPException(status_code=404, detail="Product not found")

@app.post("/orders")
def create_order(customer_name: str = Query(...)):
    global order_counter
    order = {"order_id": order_counter, "customer_name": customer_name}
    orders.append(order)
    order_counter += 1
    return {"message": "Order created", "order": order}

@app.get("/orders/search")
def search_orders(customer_name: str = Query(...)):
    result = [o for o in orders if customer_name.lower() in o["customer_name"].lower()]
    if not result:
        return {"message": f"No orders found for: {customer_name}"}
    return {"customer_name": customer_name, "total_found": len(result), "orders": result}

@app.get("/orders/page")
def paginate_orders(page: int = Query(1, ge=1), limit: int = Query(3, ge=1, le=20)):
    start = (page - 1) * limit
    return {
        "page": page,
        "limit": limit,
        "total": len(orders),
        "total_pages": -(-len(orders) // limit),
        "orders": orders[start:start + limit]
    }