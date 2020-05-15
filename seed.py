from app import Order
#seed the database

import csv


def load_order_data(filename):

    headers = []

    csvfile = open(filename,"r")

    # Read in the headers/first row

    for header in csv.DictReader(csvfile, quotechar='"', delimiter=',',
                   quoting=csv.QUOTE_ALL, skipinitialspace=True):
        headers.append(header)

    for row in headers:
        order = Order()
        date = row['created_at']
        date = datetime.strptime(date,"%Y-%m-%d %H:%M:%S.%f")
        sdate = datetime.strftime(date,'%d%m%Y')
        order.order_id = row['id']
        order.created_at = date
        order.vendor_id = row['vendor_id']
        order.customer_id = row['customer_id']
        try:
            db.session.add(order)
            db.session.commit()
        except Exception  as err:
            db.session.rollback()
            print(err)

def load_order_line_data(filename):

    headers = []

    csvfile = open(filename,"r")

    # Read in the headers/first row

    for header in csv.DictReader(csvfile, quotechar='"', delimiter=',',
                   quoting=csv.QUOTE_ALL, skipinitialspace=True):
        headers.append(header)

    for row in headers:
        orderline = OrderLine()
        orderline.order_id = row['order_id']
        orderline.product_id = row['product_id']
        orderline.product_description = row['product_description']
        orderline.product_price = row['product_price']
        orderline.product_vat_rate = row['product_vat_rate']
        orderline.discount_rate = row['discount_rate']
        orderline.quantity = row['quantity']
        orderline.full_price_amount = row['full_price_amount']
        orderline.discounted_amount = row['discounted_amount']
        orderline.vat_amount = row['vat_amount']
        orderline.total_amount = row['total_amount']
        try:
            db.session.add(orderline)
            db.session.commit()
        except Exception  as err:
            db.session.rollback()
            print(err)

def load_product(filename):

    headers = []

    csvfile = open(filename,"r")

    # Read in the headers/first row

    for header in csv.DictReader(csvfile, quotechar='"', delimiter=',',
                   quoting=csv.QUOTE_ALL, skipinitialspace=True):
        headers.append(header)

    for row in headers:
        product = Product()
        product.product_id = row['id']
        product.description = row['description']
        try:
            db.session.add(product)
            db.session.commit()
        except Exception  as err:
            db.session.rollback()
            print(err)

def load_promotion(filename):

    headers = []

    csvfile = open(filename, "r")

    # Read in the headers/first row

    for header in csv.DictReader(csvfile, quotechar='"', delimiter=',',
                    quoting=csv.QUOTE_ALL, skipinitialspace=True):
        headers.append(header)

    for row in headers:
        promotion = Promotion()
        promotion.promotion_id = row['id']
        promotion.description = row['description']
        try:
            db.session.add(promotion)
            db.session.commit()
        except Exception  as err:
            db.session.rollback()
            print(err)


def load_product_promotion(filename):

    headers = []

    csvfile = open(filename, "r")

    # Read in the headers/first row

    for header in csv.DictReader(csvfile, quotechar='"', delimiter=',',
                                 quoting=csv.QUOTE_ALL, skipinitialspace=True):
        headers.append(header)

    for row in headers:
        product_promotion = ProductPromotion()
        date = row['date']
        sdate = datetime.strptime(date, '%Y-%m-%d')
        product_promotion.date = sdate
        #product_promotion.product_id = row['product_id']
        product_promotion.promotion_id = row['promotion_id']

        try:
            db.session.add(product_promotion)
            db.session.commit()
        except Exception  as err:
            db.session.rollback()
            print(err)


def load_vendor_commissions(filename):

    headers = []

    csvfile = open(filename, "r")

    # Read in the headers/first row

    for header in csv.DictReader(csvfile, quotechar='"', delimiter=',',
                                 quoting=csv.QUOTE_ALL, skipinitialspace=True):
        headers.append(header)

    for row in headers:
        vendor_commission = VendorCommissions()
        date =row['date']
        sdate = datetime.strptime(date, '%Y-%m-%d')
        vendor_commission.date = sdate
        vendor_commission.product_id = row['vendor_id']
        vendor_commission.rate = row['rate']

        try:
            db.session.add(vendor_commission)
            db.session.commit()
        except Exception  as err:
            db.session.rollback()
            print(err)
