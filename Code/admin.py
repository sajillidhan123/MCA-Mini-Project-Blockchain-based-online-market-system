from flask import *
from database import *

admin=Blueprint('admin',__name__)

@admin.route('/adminhome')
def adminhome():
	return render_template('adminhome.html')


@admin.route('/adminviewseller')
def adminviewseller():
	data={}
	q="select * from seller"
	r=select(q)
	data['sellers']=r
	return render_template('adminviewseller.html',data=data)

@admin.route('/adminviewproduct',methods=['get','post'])
def adminviewproduct():
	data={}
	seller_id=request.args['seller_id']
	q="select * from seller inner join products using(seller_id) where seller_id='%s'"%(seller_id)
	r=select(q)
	data['pdt']=r
	return render_template('adminviewproduct.html',data=data)


@admin.route('/adminviewuser')
def adminviewuser():
	data={}
	q="select * from user"
	r=select(q)
	data['users']=r
	return render_template('adminviewuser.html',data=data)


@admin.route('/adminviewbooking')
def adminviewbooking():
	data={}
	q="SELECT * FROM`orderdetails` INNER JOIN `ordermaster` USING(`omaster_id`)INNER JOIN seller USING (seller_id) INNER JOIN products using(product_id)"
	r=select(q)
	data['booking']=r
	return render_template('adminviewbooking.html',data=data)
