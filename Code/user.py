from flask import *
from database import *
import demjson
from core_blockchain import *

user=Blueprint('user',__name__)

@user.route('/userhome')
def userhome():
	return render_template('userhome.html')

@user.route('/userviewproduct',methods=['get','post'])
def userviewproduct():
	data={}
	q="select * from seller "
	r=select(q)
	data['pdt']=r
	
	if 'submit' in request.form:
		category=request.form['category']
		if category=='fashion':
			q="select * from seller where category='fashion'"
			data['pdt']=select(q)
		elif category=='sports':
			q="select * from seller where category='sports'"
			data['pdt']=select(q)
		elif category=='electronics':
			q="select * from seller where category='electronics'"
			data['pdt']=select(q)
		elif category=='beauty':
			q="select * from seller where category='beauty'"
			data['pdt']=select(q)

	return render_template('userviewproduct.html',data=data)




@user.route('/usermakepayment',methods=['get','post'])
def usermakepayment():
	data={}
	seller_id=request.args['seller_id']
	q="select login_id from login inner join  seller using(login_id) where seller_id='%s'"%(seller_id)
	res=select(q)
	slogin_id=res[0]['login_id']
	user_id=session['userid']
	oid=request.args['omaster_id']
	total=request.args['total']
	data['total']=total
	login_id=session['login_id']
	q="select * from wallet where user_id='%s'"%(login_id)
	res=select(q)
	if res:
		wamt=int(res[0]['wamount'])
	else:
		wamt=0
	if wamt<int(total):
		flash("Your wallet is low")
		return redirect(url_for('user.useraddmoneytowallet'))


	if "payment" in request.form:

		
		q="update ordermaster set status='paid' where omaster_id='%s'"%(oid)
		update(q)
		q="insert into payment values(NULL,'%s','%s',NOW())"%(oid,total)
		insert(q)
		q="update wallet set wamount=wamount-'%s' where user_id='%s' and type='user'"%(total,login_id)
		update(q)
		q="select *from wallet where user_id='%s'"%(slogin_id)
		if res:
			q="insert into wallet values(null,'%s','%s','seller')"%(slogin_id,total)
			r=insert(q)
		else:			
			q="update wallet set wamount=wamount+'%s' where user_id='%s'"%(total,slogin_id)
			update(q)

		
		q="select *,orderdetails.quantity as oq,products.quantity as pqua from orderdetails inner join products using(product_id) where omaster_id='%s'"%(oid)
		r=select(q)
		print(r)
		for i in r:
			proid=r[0]['product_id']
			oq=r[0]['oq']
			pqua=r[0]['pqua']
			q="update products set quantity=quantity-'%s' where product_id='%s'"%(oq,proid)
			update(q)
		create_block(oid, total)
		flash("Paid Successfully")
		

		return redirect(url_for('user.userviewmybookings'))
	return render_template('usermakepayment.html',data=data)

@user.route('/userviewallproduct',methods=['get','post'])
def userviewallproduct():	
	data={}
	seller_id=int(request.args['seller_id'])
	user_id=session['userid']
	q="select * from ordermaster where user_id='%s' and status='pending'"%(user_id)
	res=select(q)
	if res:
		
		print(seller_id)
		curseller_id=int(res[0]['seller_id'])
		print(curseller_id)
		if (curseller_id)!=(seller_id):
			flash('You Can Buy Products Only from a Single Seller')
			return redirect(url_for('user.userviewproduct'))
	q="select * from products where seller_id='%s'"%(seller_id)
	data['pdt']=select(q)
	print(data['pdt'])
	if 'search' in request.form:
		search=request.form['search']+'%'
		q="select * from products where product like '%s' and seller_id='%s'"%(search,seller_id)
		data['pdt']=select(q)

	if "action" in request.args:
		action=request.args['action']
		pid=request.args['pid']
		seller_id=request.args['seller_id']
		qty=request.args['qty']
		amt=request.args['amt']
		uid=session['userid']


	else:
		action=None

	# if "cart" in request.args:
	# 	pid=request.args['pid']
	# 	seller_id=request.args['seller_id']
	# 	qty=request.args['qty']
	# 	# data['quant']=qty
	# 	amt=request.args['amt']
	# 	# data['amm']=amt

		
	# 	# qu=request.form['qu']

	# 	uid=session['userid']
	# 	# to=request.form['to']

	if action=="cart":
		q="select * from  ordermaster where status='pending'"
		res=select(q)

		if res:
			omaster_id=res[0]['omaster_id']
		if res:
			q="select * from orderdetails where product_id='%s' and omaster_id='%s'"%(pid,omaster_id)
			res1=select(q)
			if res1:
				flash('product is already in your cart')
				return redirect(url_for('user.userviewallproduct',seller_id=seller_id))
			else:	
				om_id=res[0]['omaster_id']
				q="insert into orderdetails values (null,'%s','%s','%s','%s')"%(om_id,pid,qty,amt)
				r=insert(q)
				q="update  ordermaster set total=total+'%s' where omaster_id='%s'"%(amt,om_id)
				r=update(q)
				flash("Added to cart successfully")
		else:
			q="insert into ordermaster values(null,'%s','%s','%s',curdate(),'pending') "%(seller_id,uid,amt)
			id=insert(q)
			q="insert into orderdetails values (null,'%s','%s',1,'%s')"%(id,pid,amt)
			insert(q)

		# q="update products set quantity=quantity-'%s' where product_id='%s'"%(qty,pid)
		# update(q)
			flash("Added to cart successfully")
			return redirect(url_for('user.userviewallproduct',seller_id=seller_id))
	return render_template('userviewallproduct.html',data=data)


@user.route('/userviewmybookings')
def userviewmybookings():
	data={}
	uid=session['userid']
	q="SELECT * FROM`orderdetails` INNER JOIN `ordermaster` USING(`omaster_id`)INNER JOIN seller USING (seller_id) INNER JOIN products using(product_id) where user_id='%s'"%(uid)
	r=select(q)
	data['bookings']=r

	return render_template('userviewmybookings.html',data=data)

@user.route('/userviewmycart')
def userviewmycart():
	data={}
	uid=session['userid']
	q="SELECT * FROM`orderdetails` INNER JOIN `ordermaster` USING(`omaster_id`)INNER JOIN seller USING (seller_id) INNER JOIN products using(product_id) where user_id='%s' and status='pending'"%(uid)
	r=select(q)
	print(q)
	data['bookings']=r
	if "action" in request.args:
		action=request.args['action']
		omaster_id=request.args['omaster_id']
		odetail_id=request.args['odetail_id']
		amount=request.args['amount']
		# qty=request.args['qty']
		# data['qty']=qqtty
		# amtt=request.args['amt']
		# data['amtt']=ammtt
	else:
		action=None
	if action=="delete":
		q="delete from orderdetails where odetail_id='%s'"%(odetail_id)
		delete(q)
		q="update ordermaster set total=total-'%s' where omaster_id='%s'"%(amount,omaster_id)
		update(q)
		return redirect(url_for('user.userviewmycart'))
	return render_template('userviewmycart.html',data=data)

@user.route('/userbook',methods=['get','post'])
def userbook():
	data={}
	pid=request.args['pid']
	# seller_id=request.args['seller_id']
	qty=request.args['qty']
	data['quant']=qty
	amt=request.args['amt']
	data['amm']=amt
	if "book" in request.form:
		omaster_id=request.args['omaster_id']
		pid=request.args['pid']
		
		cur_qty=request.form['qu']
		data['cur_qty']=cur_qty

		uid=session['userid']
		cur_to=request.form['to']
		data['cur_to']=cur_to
	
		
		q="update ordermaster set total=total+'%s'-'%s' where omaster_id='%s'"%(cur_to,amt,omaster_id)
		update(q)
		q="update orderdetails set amount='%s',quantity='%s' where product_id='%s' and omaster_id='%s'"%(cur_to,cur_qty,pid,omaster_id)
		update(q)
		flash("Update successfully")
		return redirect(url_for('user.userviewmycart',cur_qty=cur_qty,cur_to=cur_to))

	return render_template('userbook.html',data=data)


@user.route("useraddmoneytowallet",methods=['get','post'])
def useraddmoneytowallet():
	data={}
	login_id=session['login_id']
	q="select * from wallet where user_id='%s' and type='user'"%(login_id)
	r=select(q)
	data['view']=r


	if 'payment' in request.form:
		wamt=request.form['wamt']
		q="select * from wallet where user_id='%s' and type='user'"%(login_id)
		r=select(q)
		if r:
			q="update wallet set wamount=wamount+'%s' where user_id='%s'"%(wamt,login_id)
			update(q)
			flash('Added successfully')
			return redirect(url_for('user.useraddmoneytowallet'))
		else:

			q="insert into wallet values(null,'%s','%s','user')"%(login_id,wamt)
			r=insert(q)
			q="update wallet set wamount=wamount-'%s' where user_id='%s'"%(wamt,login_id)
			update(q)
			flash('Added successfully')
			return redirect(url_for('user.useraddmoneytowallet'))

	return render_template('useraddmoneytowallet.html',data=data)