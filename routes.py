from flask import render_template, Flask
from waitress import serve
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from Parser import parser, marketparser
from datetime import date
from newscraper import marketscrape
import pandas
import os

#Used to verify that the current date flea market file exists; if it doesn't, the program will run the marketscraper and then launch the web app.
today = date.today()
filename = os.path.isfile(f'{today}.csv')
if filename:
    pass
else:
    marketscrape()

app = Flask(__name__)

#generated using os.urandom(12).hex()
app.config['SECRET_KEY'] = '0e6354d75ada225d2d9c99ce'

class ItemForm(FlaskForm):
    item = StringField('Barter Item', [DataRequired()])
    submit = SubmitField('Submit')

@app.route('/' , methods=['GET','POST'])
def main():
    form = ItemForm()
    if form.validate_on_submit():
        barteritem = parser(form.item.data)
        marketitem = marketparser(form.item.data)
        #the two parsers can pass a string as output if there are no matches, these tryexcepts are used to solve the error of passing a string to .to_html when there is a string output.
        try:
            barter = barteritem.to_html(classes='barteritems', index=False)
        except:
            barter = barteritem
        try: 
            market = marketitem.to_html(classes='marketitems', index=False)
        except:
            market = marketitem
        return render_template('main.html', form=form, 
                                barteritem=barter, 
                                marketitem=market,
                                markettitle = 'Flea Market Prices',
                                bartertitle = 'Barters Available')
    return render_template('main.html', form=form)
                
if __name__ == '__main__':
    serve(app, host='127.0.0.1', port=5000)