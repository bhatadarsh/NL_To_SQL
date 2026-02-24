TABLES = {
    "orders": {
        "description": "Customer orders placed on the ecommerce platform",
        "columns": {
            "order_id":       {"type": "INT",       "description": "Unique order ID",           "primary_key": True,  "foreign_key": None},
            "user_id":        {"type": "INT",       "description": "References users table",    "primary_key": False, "foreign_key": "users.id"},
            "status":         {"type": "VARCHAR",   "description": "Order status",              "primary_key": False, "foreign_key": None},
            "created_at":     {"type": "TIMESTAMP", "description": "When order was created",    "primary_key": False, "foreign_key": None},
            "num_of_item":    {"type": "INT",       "description": "Number of items in order",  "primary_key": False, "foreign_key": None},
        }
    },
    "users": {
        "description": "Registered users on the platform",
        "columns": {
            "id":             {"type": "INT",       "description": "Unique user ID",            "primary_key": True,  "foreign_key": None},
            "first_name":     {"type": "VARCHAR",   "description": "First name",                "primary_key": False, "foreign_key": None},
            "last_name":      {"type": "VARCHAR",   "description": "Last name",                 "primary_key": False, "foreign_key": None},
            "email":          {"type": "VARCHAR",   "description": "Email address",             "primary_key": False, "foreign_key": None},
            "country":        {"type": "VARCHAR",   "description": "Country of residence",      "primary_key": False, "foreign_key": None},
            "city":           {"type": "VARCHAR",   "description": "City of residence",         "primary_key": False, "foreign_key": None},
            "age":            {"type": "INT",       "description": "Age of the user",           "primary_key": False, "foreign_key": None},
            "gender":         {"type": "VARCHAR",   "description": "Gender",                    "primary_key": False, "foreign_key": None},
        }
    },
    "products": {
        "description": "Product catalog",
        "columns": {
            "id":             {"type": "INT",       "description": "Unique product ID",         "primary_key": True,  "foreign_key": None},
            "name":           {"type": "VARCHAR",   "description": "Product name",              "primary_key": False, "foreign_key": None},
            "category":       {"type": "VARCHAR",   "description": "Product category",          "primary_key": False, "foreign_key": None},
            "brand":          {"type": "VARCHAR",   "description": "Brand name",                "primary_key": False, "foreign_key": None},
            "retail_price":   {"type": "DECIMAL",   "description": "Retail price in USD",       "primary_key": False, "foreign_key": None},
            "cost":           {"type": "DECIMAL",   "description": "Cost price in USD",         "primary_key": False, "foreign_key": None},
            "department":     {"type": "VARCHAR",   "description": "Men or Women department",   "primary_key": False, "foreign_key": None},
        }
    },
    "order_items": {
        "description": "Individual items within each order",
        "columns": {
            "id":             {"type": "INT",       "description": "Unique item ID",            "primary_key": True,  "foreign_key": None},
            "order_id":       {"type": "INT",       "description": "References orders table",   "primary_key": False, "foreign_key": "orders.order_id"},
            "user_id":        {"type": "INT",       "description": "References users table",    "primary_key": False, "foreign_key": "users.id"},
            "product_id":     {"type": "INT",       "description": "References products table", "primary_key": False, "foreign_key": "products.id"},
            "status":         {"type": "VARCHAR",   "description": "Item status",               "primary_key": False, "foreign_key": None},
            "sale_price":     {"type": "DECIMAL",   "description": "Actual sale price",         "primary_key": False, "foreign_key": None},
            "created_at":     {"type": "TIMESTAMP", "description": "When item was ordered",     "primary_key": False, "foreign_key": None},
        }
    },
}

VALID_TABLES = set(TABLES.keys())
VALID_COLUMNS = {table: set(info["columns"].keys()) for table, info in TABLES.items()}