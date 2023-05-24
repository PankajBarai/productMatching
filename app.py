import numpy as np
import pandas as pd
import random, itertools
from flask import Flask, render_template, request, redirect
from datetime import datetime
from amaze import search
from flip import search_flip

app = Flask(__name__)

app.logger.info('start')

@app.route('/', methods = ['POST','GET'])
def login():  
    # if request.method == 'POST':
    result_1 = (request.form).to_dict()['query']
    app.logger.info('########################')
    app.logger.info(result_1)
    app.logger.info(type(result_1))
    app.logger.info('########################')
    app.logger.info(len(result_1))
    app.logger.info(result_1)
    abc = search(str(result_1))
    app.logger.info('########################')
    app.logger.info(abc)
    app.logger.info('########################')
    product=abc['Product_Name']
    similar = abc['Similarity'] 
    deff = search_flip(str(result_1))
    product_flip=deff['Product_Name_flip']
    similar_flip = deff['Similarity_flip']
    # data = pd.DataFrame(result)
    app.logger.info('####  dataframe  ####')
    app.logger.info('########################')
    return render_template('index.html',count= 10 , product=product, similar = similar,product_flip=product_flip,similar_flip=similar_flip )
    # return result_1


@app.route('/about')
def about():
    return 'Under Development'


if __name__ == "__main__":
    app.run(debug=True,  port=5000)

