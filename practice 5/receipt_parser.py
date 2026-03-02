import re

def parse_receipt(text):
    #Extract prices
    prices = re.findall(r"\d+\.\d{2}", text)

    #Extract product names 
    products = re.findall(r"[A-Za-z]+(?=\s+\d+\.\d{2})", text)

    #Calculate total amount (sum of prices)
    total = sum(float(p) for p in prices)

    #Extract date and time
    date_match = re.search(r"\d{4}-\d{2}-\d{2}", text)
    date = date_match.group() if date_match else None

    #Extract payment method
    payment_match = re.search(r"Cash|Card", text)
    payment = payment_match.group() if payment_match else None

    return {
        "products": products,
        "prices": prices,
        "total": total,
        "date": date,
        "payment": payment
    }


with open("sample_receipt.txt", "r") as f:
    text = f.read()

result = parse_receipt(text)

print(result)