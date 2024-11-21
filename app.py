from flask import Flask, render_template, request

app = Flask(__name__)

# list 30 items - Item code, Item and rates as per quality
prod = {'101A': ['Brown rice', 50, 45.50, 41.25],
        '102B': ['Whole wheat', 30, 27.45, 21.50],
        '102C': ['Tomato sauce', 25.50, 20.25, 18.70],
        '103D': ['Mustard', 40, 39.45, 37],
        '104E': ['Barbecue sauce', 45, 43, 41.50],
        '105F': ['Red-wine vinegar', 4000, 3800, 3750],
        '106G': ['Salsa', 200, 189.50, 170],
        '107H': ['Extra virgin olive oil', 500, 478.50, 455.70],
        '108I': ['canola oil', 200, 180, 118],
        '109J': ['Hot pepper sauce', 100, 98.5, 91.25],
        '110K': ['Bananas', 60, 55, 50],
        '111L': ['Apples', 300, 250, 120],
        '112M': ['Oranges', 200, 140, 110],
        '113N': ['Mangoes', 100, 80, 50],
        '114O': ['Strawberries', 100, 90, 80],
        '115P': ['Blueberries', 95, 80, 75],
        '116Q': ['Green tea', 250, 225, 200],
        '117R': ['Sparkling water', 20, 14.50, 11],
        '118S': ['Dried apricots', 270, 250, 230],
        '119T': ['Dried figs', 100, 95, 90],
        '120U': ['Dried prunes', 90, 85, 80],
        '121V': ['Almonds', 900, 870, 850],
        '122W': ['Cashews', 1000, 950, 910],
        '123X': ['Walnuts', 800, 770, 720],
        '124Y': ['Peanuts', 400, 380, 360],
        '125Z': ['Pecans', 350, 320, 300],
        '201A': ['Pistachios', 1200, 1180, 1160],
        '202B': ['Sunflower seeds', 150, 112, 50],
        '203C': ['Sesame seeds', 120.50, 110.40, 103.45],
        '204D': ['Whole flaxseeds', 95.20, 90.45, 89.20]}

# registered customers database
customer = {'9500012345': ['Surian', 'AAA1001'],
            '9500023456': ['Nila', 'AAA1002'],
            '9712300078': ['Arivazhagan', 'AAA1003'],
            '9586233333': ['Nithin Kumar', 'AAA1004'],
            '6931245872': ['Aravind', 'AAA1005']}

# variables
TotalPrice = 0
Discount = 0
FinalPrice = 0
isRegCust = "N"
bill_list = []
BillList = []
CustomerData = []
headings = ("Item Code", "Item", "Quality", "Quantity", "Price")


# function to call index page using flask
@app.route("/")
def index():
    global TotalPrice
    global Discount
    global FinalPrice
    TotalPrice = 0
    Discount = 0
    FinalPrice = 0
    # rendering index page
    return render_template("index.html")


# function to get data from index page and redirect to the input page
@app.route("/input", methods=["POST"])
def getinfo():
    global BillList
    global CustomerData
    global isRegCust
    BillList = []

    # getting customer data
    mob = request.form['mob']
    name = request.form['name']

    # validating customer data
    if mob in customer:
        isRegCust = "Y"
    print(isRegCust)

    # storing customer data
    CustomerData = (name, mob)

    # rendering and sending data to input page
    return render_template("input.html", BillList=BillList, headings=headings)


# function to get data from the input page and redirect to output page
@app.route("/bill", methods=["POST"])
def getdata():
    global BillList
    global bill_list
    global TotalPrice
    global Discount
    global FinalPrice

    # getting input from html page
    x = []
    code = request.form['code']
    item = prod[code][0]
    quality = int(request.form['quality'])
    quantity = float(request.form['quantity'])
    add = request.form['add']

    # calculations
    s = prod[code][quality] * quantity
    TotalPrice += s

    # storing data
    x.append(code)
    x.append(item)
    x.append(quality)
    x.append(quantity)
    x.append(s)
    bill_list.append(x)
    BillList = tuple(bill_list)

    # calculating final price
    if TotalPrice < 10000:
        FinalPrice = TotalPrice
    else:
        if isRegCust == 'Y':
            FinalPrice = TotalPrice - (TotalPrice * 1.2 / 100)
            Discount = TotalPrice * 1.2 / 100
        else:
            FinalPrice = TotalPrice - (TotalPrice * 1 / 100)
            Discount = TotalPrice * 1 / 100

    # rounding off
    TotalPrice = round(TotalPrice, 2)
    Discount = round(Discount, 2)
    FinalPrice = round(FinalPrice, 2)

    # returning functions as per need
    if add == 'Y':
        # rendering and returning data to input page to add more items and display cart
        return render_template("input.html", BillList=BillList, headings=headings)
    else:
        bill_list = []
        # rendering and sending data to output page to print the invoice
        return render_template("invoice.html", CustomerData=CustomerData,
                               headings=headings, BillList=BillList, TotalPrice=TotalPrice,
                               Discount=Discount, FinalPrice=FinalPrice)


# function to restart code for new transaction
@app.route('/done', methods=['POST'])
def done():
    return index()


app.run()
