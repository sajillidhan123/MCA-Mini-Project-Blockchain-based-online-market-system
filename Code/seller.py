from flask import *
from database import *

seller=Blueprint('seller',__name__)

@seller.route('/sellerhome')
def sellerhome():
	return render_template('sellerhome.html')

@seller.route('/sellerviewbooking')
def sellerviewbooking():
	data={}
	sid=session['sellerid']
	q="SELECT * FROM`orderdetails` INNER JOIN `ordermaster` USING(`omaster_id`)INNER JOIN user USING (user_id) where seller_id='%s'"%(sid)
	r=select(q)
	data['bookings']=r


	if "action" in request.args:
		action=request.args['action']
		omaster_id=request.args['omaster_id']

	else:
		action=None

	if action=="deliver":
		q="update ordermaster set status='deliver' where omaster_id='%s' "%(omaster_id)
		r=update(q)
		flash("Delivered successfully")
		return redirect(url_for('seller.sellerviewbooking'))

	return render_template('sellerviewbooking.html',data=data)

@seller.route('/sellerviewpayment')
def sellerviewpayment():
	omaster_id=request.args['omaster_id']
	data={}
	q="SELECT * FROM `payment` INNER JOIN `ordermaster` USING(omaster_id) INNER JOIN orderdetails USING (omaster_id)INNER JOIN products USING(product_id) INNER JOIN `user` USING(user_id) where omaster_id='%s'"%(omaster_id)
	r=select(q)
	data['payments']=r


	return render_template('sellerviewpayment.html',data=data)


@seller.route('/sellermanageproduct',methods=['get','post'])
def sellermanageproduct():
	data={}
	sid=session['sellerid']
	q="select * from seller inner join products using(seller_id) where seller_id='%s'"%(sid)
	r=select(q)
	data['pdt']=r
	sid=session['sellerid']
	if "add" in request.form:
		p=request.form['p']
		q=request.form['q']
		a=request.form['a']
		qs="insert into products values(null,'%s','%s','%s','%s')"%(sid,p,q,a)
		insert(qs)
		flash("Added successfully")

		return redirect(url_for('seller.sellermanageproduct'))
	if "action" in request.args:
		action=request.args['action']
		pid=request.args['pid']
	else:
		action=None
	if "update" in request.form:
		p=request.form['p']
		q=request.form['q']
		a=request.form['a']
		q="update products set product='%s',quantity='%s',amount='%s' where product_id='%s'"%(p,q,a,pid)
		r=update(q)
		return redirect(url_for('seller.sellermanageproduct'))
	if action=="update":
		q="select * from  products where product_id='%s'"%(pid)
		r=select(q)
		data['updatepdt']=r
	if action=="delete":
		q="delete from products where product_id='%s'"%(pid)
		delete(q)
		return redirect(url_for('seller.sellermanageproduct'))
	return render_template('sellermanageproduct.html',data=data)


@seller.route("selleraddmoneytowallet",methods=['get','post'])
def selleraddmoneytowallet():
	data={}
	login_id=session['login_id']
	q="select * from wallet where user_id='%s' and type='seller'"%(login_id)
	r=select(q)
	data['view']=r


	if 'payment' in request.form:
		wamt=request.form['wamt']
		q="select * from wallet where user_id='%s' and type='seller'"%(login_id)
		r=select(q)
		if r:
			q="update wallet set wamount=wamount+'%s' where user_id='%s'"%(wamt,login_id)
			update(q)
			flash('Added successfully')
			return redirect(url_for('seller.selleraddmoneytowallet'))
		else:

			q="insert into wallet values(null,'%s','%s','seller')"%(login_id,wamt)
			r=insert(q)
			flash('Added successfully')
			return redirect(url_for('seller.selleraddmoneytowallet'))
	return render_template('selleraddmoneytowallet.html',data=data)