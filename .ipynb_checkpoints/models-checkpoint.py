
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os
import csv
import sqlite3
from flask_marshmallow import Marshmallow

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'suade.db')
app.config['JWT_SECRET_KEY'] = 'super-secret'  # change this IRL
app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
app.config['MAIL_USERNAME'] = 'f3230fb2bf1a2d'
app.config['MAIL_PASSWORD'] = '825071f7c01f2e'

db = SQLAlchemy(app)
ma = Marshmallow(app)

# database models
class Order(db.Model):
    __tablename__ = 'order'
    order_id = Column(Integer, primary_key=True)
    created_at = db.Column(db.DateTime)
    vendor_id = Column(Integer)
    customer_id = Column(Integer)


class OrderLine(db.Model):
    __tablename__ = 'orderline'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer)
    product_id = Column(Integer)
    product_description = Column(String)
    product_price = Column(Float)
    product_vat_rate = Column(Float)
    discount_rate = Column(Float)
    quantity = Column(Integer)
    full_price_amount= Column(Float)
    discounted_amount= Column(Float)
    vat_amount = Column(Float)
    total_amount = Column(Float)


class Product(db.Model):
    __tablename__ = 'product'
    product_id = Column(Integer, primary_key=True)
    description = Column(String)


class Promotion(db.Model):
    __tablename__ = 'promotion'
    promotion_id = Column(Integer, primary_key=True)
    description = Column(String)


class ProductPromotion(db.Model):
    __tablename__ = 'product_promotion'
    date = db.Column(db.DateTime)
    product_id = Column(Integer, primary_key=True)
    promotion_id = Column(Integer)


class VendorCommissions(db.Model):
    __tablename__ = 'vendor_commission'
    date = db.Column(db.DateTime)
    vendor_id = Column(Integer, primary_key=True)
    rate = Column(Float)


class OrderSchema(ma.Schema):
    class Meta:
        fields = ('id', 'created_at', 'vendor_id', 'customer_id')

class OrderLineSchema(ma.Schema):
    class Meta:
        fields = ('order_id', 'product_id', 'product_description', 'product_price', 'product_vat_rate', 'discount_rate', 'quantity','full_price_amount','discounted_amount','vat_amount','total_amount')

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'description')

class PromotionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'description')

class ProductPromotionSchema(ma.Schema):
    class Meta:
        fields = ('date', 'vendor_id', 'rate')

class VendorCommissionSchema(ma.Schema):
    class Meta:
        fields = ('date', 'vendor_id', 'rate')



order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

orderline_schema = OrderLineSchema()
orderlines_schema = OrderLineSchema(many=True)

product_schema = OrderSchema()
products_schema = OrderSchema(many=True)

promotion_schema = OrderSchema()
promotions_schema = OrderSchema(many=True)

productpromotion_schema = OrderSchema()
productspromotions_schema = OrderSchema(many=True)

vendorcommission_schema = OrderSchema()
vendorcommissions = OrderSchema(many=True)
