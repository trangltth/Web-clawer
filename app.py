from flask import Flask, render_template, render_template_string
import json
from object_data import product, category
import psycopg2
import app
import pandas as pd
from flask_menu import Menu, register_menu


conn = psycopg2.connect("dbname=postgres port=5433 user=postgres")
data_category = category.category().get_parent_category(conn)
app = Flask(__name__, template_folder="templates")
Menu(app=app)

@app.route('/')
@app.route('/home')
def index():
    data_product = product.product().get_all_product_by_category(data_category[0][0],conn)
    return render_template('index.html', products = data_product, categories = data_category)

@app.route('/product/<int:category_id>', methods=['GET','POST'])
def get_product(category_id):
    data_product = product.product().get_all_product_by_category((category_id,),conn)
    return render_template('index.html', products = data_product, categories = data_category)

@app.route('/categories/<int:category_id>', methods=['GET'])
def get_child_category(category_id):
    data_product = product.product().get_all_product_by_category((category_id,), conn)
    child_categories = category.category().get_child_category((category_id,), conn)    
    return render_template('index.html', parent_id = category_id, products = data_product, categories = data_category, child_categories = child_categories)

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 