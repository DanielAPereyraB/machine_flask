from flask import Flask,render_template, request, url_for, flash, redirect
import psycopg2
import psycopg2.extras


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

DB_HOST="localhost"
DB_NAME="Machine"
DB_USER="postgres"
DB_PASSWORD="PB12345"

conn = psycopg2.connect(dbname=DB_NAME,user=DB_USER,password=DB_PASSWORD,host=DB_HOST)
cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)



@app.route('/')
def index():
    Select = 'SELECT * FROM "Products"'
    cur.execute(Select) #execule the sql
    list_users = cur.fetchall()
    return render_template ('index.html', list_users=list_users)


@app.route('/create', methods=['GET','POST'])
def create():
    if request.method == 'POST':
        Pid = request.form['Pid']
        Pname = request.form['Pname']
        Pcode = request.form['Pcode']
        Pamount = request.form['Pamount']
        Pprice = request.form['Pprice']
        Pimg = request.form['Pimg'] 
        cur.execute('INSERT INTO "Products"(id, "Product", "Products_code", "Amount", "Price", img)VALUES (%s, %s, %s, %s, %s, %s);',(Pid,Pname,Pcode,Pamount,Pprice,Pimg))
        conn.commit()
        flash('Products Added successfully')
        return redirect(url_for('index'))

    return render_template ('create.html')

@app.route('/order',methods =['POST'])
def order():
    if request.method == 'POST':
        Pnumber= request.form['Pnumber']
        Pquantity = request.form['Pquantity']
        cur.execute('UPDATE public."Products" SET "Amount"= "Amount" - %s WHERE "Products_code"= %s;',(Pquantity,Pnumber))
        conn.commit()
        flash('Orden Added successfully')
        return redirect(url_for('index'))

@app.route('/product')
def product():
    Select = 'select * from "Products";'
    cur.execute(Select) #execule the sql
    product = cur.fetchall()
    return render_template ('product.html', product=product)


@app.route('/edit/<id>', methods=['POST','GET'])
def get_edit_product(id):
    cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM "Products" WHERE id =%s', (id))
    data = cur.fetchall()
    cur.close()
    return render_template('edit.html', pdata=data[0])

@app.route('/update/<id>', methods=['POST'])
def update_product(id):
    if request.method == 'POST': 
        Pname = request.form['Pname']
        Pcode = request.form['Pcode']
        Pamount = request.form['Pamount']
        Pprice = request.form['Pprice']
        Pimg = request.form['Pimg'] 
        cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('UPDATE public."Products" SET  "Product"=%s, "Products_code"=%s, "Amount"=%s, "Price"=%s, img=%s WHERE id = %s ;',(Pname,Pcode,Pamount,Pprice,Pimg,id))
        flash('Products Updated successfully')
        conn.commit()
        return redirect(url_for('index'))


@app.route('/delete/<id>', methods=['POST','GET'])
def delete(id):
    cur.execute('DELETE FROM public."Products" WHERE id = %s',(id))
    flash('Products Removed successfully')
    conn.commit()
    return redirect(url_for('index'))

