
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os
import csv
import sqlite3
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_mail import Mail, Message
from datetime import datetime
from datetime import timedelta
from .models import *

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'suade.db')
app.config['JWT_SECRET_KEY'] = 'super-secret'  # change this IRL
app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
app.config['MAIL_USERNAME'] = 'f3230fb2bf1a2d'
app.config['MAIL_PASSWORD'] = '825071f7c01f2e'

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
mail = Mail(app)


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created!')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')


@app.cli.command('db_seed')
def db_seed():
    load_order_data('data/orders.csv')
    load_order_line_data('data/order_lines.csv')
    load_product('data/products.csv')
    load_promotion('data/promotions.csv')
    load_product_promotion('data/product_promotions.csv')
    load_vendor_commissions('data/commissions.csv')

    print('Database seeded!')


@app.route('/')
def hello_world():
    return 'Hello World!'


def exec_order_sql(sqlStr,sdate):
    start_date = datetime.strptime(sdate, "%d%b%Y")
    end_date = start_date + timedelta(days=1)
    start = start_date.isoformat().split('T')
    start = start[0]
    end = end_date.isoformat().split('T')
    end = end[0]
    try:
        conn = sqlite3.connect('/Users/milomia/suade/suade.db')
        sql= f"from orders inner join orderline on orders.order_id = orderline.order_id and created_at BETWEEN '{start}' and '{end}'"
        sqlStr = sqlStr + sql
        cursor=conn.execute(sqlStr)
        for row in cursor:
          print(row[0])
    except Exception  as err:
          pass
    conn.close()

    return row[0]

def exec_commission_sql(sqlStr,sdate):
    start_date = datetime.strptime(sdate, "%d%b%Y")
    end_date = start_date + timedelta(days=1)
    start = start_date.isoformat().split('T')
    start = start[0]
    end = end_date.isoformat().split('T')
    end = end[0]
    try:
        conn = sqlite3.connect('/Users/milomia/suade/suade.db')
        sql= f"  from orders inner join orderline on orders.order_id = orderline.order_id inner join vendor_commission on orders.vendor_id = vendor_commission.vendor_id and orders.created_at BETWEEN '{start}' and '{end}')"
        breakpoint()
        sqlStr = sqlStr + sql
        cursor=conn.execute(sqlStr)
        for row in cursor:
          print(row[0])
    except Exception  as err:
          pass
    conn.close()

    return row[0]


def text_get_total_items_per_day(sdate):
    sqlStr = "select sum(orderline.quantity)"
    result=exec_order_sql(sqlStr,sdate)
    return result

def text_get_customers_per_day(sdate):

    sqlStr = "select count(distinct(customer_id))"
    result = exec_order_sql(sqlStr, sdate)
    return result

def text_get_total_discount_per_day(sdate):

    sqlStr = "select sum(discounted_amount)"
    result = exec_order_sql(sqlStr, sdate)
    return result

def text_get_average_discount_rate_per_day(sdate):

    sqlStr = "select  sum(discount_rate)/count(*) "
    result = exec_order_sql(sqlStr, sdate)
    return result

def text_get_average_order_total_per_day(sdate):
    breakpoint()
    sqlStr = "select sum(total_amount)/sum(orderline.quantity) "
    result = exec_order_sql(sqlStr, sdate)
    return result

def text_get_total_amount_of_commission_per_day(sdate):
    breakpoint()
    sqlStr = "select sum(amount) from  (select  sum(total_amount)*rate as amount"
    result = exec_commission_sql(sqlStr, sdate)
    return result


def text_get_average_amount_of_commission_per_day(sdate):
    breakpoint()
    sqlStr = "select sum(amount) from (select  sum(total_amount)*rate/count(*) as amount"
    result = exec_commission_sql(sqlStr, sdate)
    return result

@app.route('/total/<string:sdate>', methods=['GET'])
def get_all(sdate:str):
    return json_get_customers_per_day(sdate),json_get_total_discount_per_day(sdate)


@app.route('/total_items/<string:sdate>', methods=['GET'])
def json_get_total_items_per_day(sdate:str):

    result = text_get_total_items_per_day(sdate)

    return jsonify(message=f'items result={result}'), 200


@app.route('/customers/<string:sdate>', methods=['GET'])
def json_get_customers_per_day(sdate:str):

    result = text_get_customers_per_day(sdate)

    return jsonify(message=f'customers={result}'), 200


@app.route('/total_discount/<string:sdate>', methods=['GET'])
def json_get_total_discount_per_day(sdate:str):

    result = text_get_total_discount_per_day(sdate)

    return jsonify(message=f'total_discount_amount={result}'), 200


@app.route('/average_discount/<string:sdate>', methods=['GET'])
def json_get_average_discount_rate_per_day(sdate:str):

    result = text_get_average_discount_rate_per_day(sdate)

    return jsonify(message=f'discount_rete_average={result}'), 200



@app.route('/average_order/<string:sdate>', methods=['GET'])
def json_get_average_order_total_per_day(sdate:str):

    result = text_get_average_order_total_per_day(sdate)

    return jsonify(message=f'order_average={result}'), 200


@app.route('/total_commission/<string:sdate>', methods=['GET'])
def json_get_total_amount_of_commission_per_day(sdate:str):

    result = text_get_total_amount_of_commission_per_day(sdate)

    return jsonify(message=f'total_commission={result}'), 200


@app.route('/average_commission/<string:sdate>', methods=['GET'])
def json_get_average_amount_of_commission_per_day(sdate:str):

    result = text_get_average_amount_of_commission_per_day(sdate)

    return jsonify(message=f'total_commission={result}'), 200

"""
@app.route('/commission_per_promotion/<string:sdate>', methods=['GET'])
def json_get_average_amount_of_commission_per_day(sdate:str):

    result = text_get_average_amount_of_commission_per_day(sdate)

    return jsonify(message=f'total_commission={result}'), 200
"""



if __name__ == '__main__':
    app.run()

def seedpath(filename):
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, filename)
    return path
