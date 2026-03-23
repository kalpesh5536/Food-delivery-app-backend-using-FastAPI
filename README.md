# 🍕 FastAPI Food Delivery App (QuickBite) by kalpesh

# outputs are in the follwing way

- Q1_home.png
- Q2_menu.png
- Q3_get_by_id.png
- Q4_orders.png
- Q5_summary.png
- Q6_validation_error.png
- Q7_helper function.png
- Q8_post_order.png
- Q9_with_delivery_charge.png
- Q9_pickup.png
- Q10_Menu_filter_logic.png
- Q11_add_item.png
- Q12_update_item.png
- Q13_delete_item.png
- Q14_cart_add q1.png
- Q14_cart_add_1_more_q.png
- Q14_Get_cart_total_amount.png

- Q15_checkout_with_details.png
- Q15_empty_checkout.png

- Q16_search_by_category.png
- Q16_search_by_category_case_insensitive.png
- Q16_search_by_name.png
- Q16_search_by_name_case_insensitive.png

- Q17_sort_default.png
- Q17_sort_category_desc.png

- Q18_pagination_deafult.png
- Q18_pagination_2_limit_3.png

- Q19_order_search_name.png
- Q19_order_search_sort_by.png
- Q20_browse.png

A complete backend system built using **FastAPI** as part of my internship training.
This project simulates a real-world food delivery application with menu management, cart system, order processing, and advanced API features.

---

## 🚀 Features Implemented

### 🔹 Core APIs (Day 1)

* Home route
* Get all menu items
* Get item by ID
* Orders list
* Menu summary

### 🔹 Request Handling (Day 2)

* POST order with validation
* Pydantic models
* Field constraints

### 🔹 Helper Functions (Day 3)

* `find_menu_item()`
* `calculate_bill()`
* `filter_menu_logic()`

### 🔹 CRUD Operations (Day 4)

* Add new menu item
* Update item (price, availability)
* Delete item

### 🔹 Multi-Step Workflow (Day 5)

* Cart system (add/remove items)
* Checkout process
* Order creation from cart

### 🔹 Advanced APIs (Day 6)

* Search (menu & orders)
* Sorting
* Pagination
* Combined browsing endpoint

---

## 🛠 Tech Stack

* Python
* FastAPI
* Pydantic
* Uvicorn

---

## ▶️ How to Run

```bash
# Create virtual environment
python -m venv venv

# Activate
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --reload
```

Open in browser:
👉 http://127.0.0.1:8000/docs

---

## 📸 Screenshots

All API outputs are tested using Swagger UI and stored in the `screenshots/` folder.

---

## 📂 Project Structure

```
fastapi-food-delivery-app/
│
├── main.py
├── requirements.txt
├── README.md
└── outputs/
```

---

## 🎯 Key Learnings

* API design using FastAPI
* Backend workflow building
* Data validation with Pydantic
* CRUD operations
* Real-world project structuring

---

## 🔗 Author
Kalpesh Sarsambe
