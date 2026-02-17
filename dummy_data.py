from models import Product

def generate_dummy_data():
    return [
        Product(
            name="iPhone 15 Pro",
            description="Apple flagship smartphone with A17 chip",
            price=1299.99,
            quantity=25
        ),
        Product(
            name="Samsung Galaxy S24",
            description="High-end Android smartphone with AMOLED display",
            price=999.50,
            quantity=18
        ),
        Product(
            name="MacBook Air M3",
            description="Lightweight laptop powered by Apple M3 chip",
            price=1499.00,
            quantity=12
        ),
        Product(
            name="Gaming Laptop RTX 4060",
            description="High performance laptop for gaming and development",
            price=1899.99,
            quantity=6
        ),
        Product(
            name="Office Ergonomic Chair",
            description="Comfortable chair with lumbar support",
            price=249.99,
            quantity=40
        ),
        Product(
            name="Wooden Study Desk",
            description="Solid wood desk suitable for home office",
            price=399.00,
            quantity=15
        ),
        Product(
            name="Wireless Mouse",
            description="2.4GHz wireless mouse with adjustable DPI",
            price=29.99,
            quantity=120
        ),
        Product(
            name="Mechanical Keyboard",
            description="RGB backlit mechanical keyboard with blue switches",
            price=89.50,
            quantity=75
        ),
        Product(
            name="Noise Cancelling Headphones",
            description="Over-ear headphones with active noise cancellation",
            price=299.99,
            quantity=30
        ),
        Product(
            name="4K Monitor 27 inch",
            description="Ultra HD IPS monitor for productivity and gaming",
            price=549.99,
            quantity=20
        ),
        Product(
            name="USB-C Docking Station",
            description="Multi-port docking station for laptops",
            price=119.99,
            quantity=50
        ),
        Product(
            name="Smart LED Bulb",
            description="WiFi enabled smart bulb compatible with Alexa",
            price=19.99,
            quantity=200
        )
    ]