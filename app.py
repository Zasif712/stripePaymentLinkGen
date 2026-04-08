from flask import Flask, request, jsonify
import stripe
import os

app = Flask(__name__)
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

@app.route('/create-payment-link', methods=['POST'])
def create_payment_link():
    data = request.json
    amount = data['amount']
    name = data['name']
    
    product = stripe.Product.create(name=f"C&P Balloons - {name}")
    price = stripe.Price.create(
        product=product.id,
        unit_amount=int(amount),
        currency="gbp"
    )
    link = stripe.PaymentLink.create(
        line_items=[{"price": price.id, "quantity": 1}]
    )
    return jsonify({"payment_url": link.url})

if __name__ == '__main__':
    app.run()