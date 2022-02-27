from flask import *
from database import *

public=Blueprint('public',__name__)

@public.route('/')
def home():
	return render_template('index.html')

@public.route('/login',methods=['get','post'])
def login():
	if "login" in request.form:
		uname=request.form['un']
		pwd=request.form['pa']
		q="select * from login where username='%s' and password='%s'"%(uname,pwd)
		res=select(q)
		if res:
			session['login_id']=res[0]['login_id']
			if res[0]['usertype']=="admin":
				flash("Login Successfully")

				return redirect(url_for('admin.adminhome'))


			elif res[0]['usertype']=="seller":
				q1="select * from seller where login_id='%s'"%(res[0]['login_id'])
				res1=select(q1)
				session['sellerid']=res1[0]['seller_id']
				flash("login successfully")
				return redirect(url_for('seller.sellerhome'))

			elif res[0]['usertype']=="user":
				q2="select * from user where login_id='%s'"%(res[0]['login_id'])
				res2=select(q2)
				session['userid']=res2[0]['user_id']
				flash("Login Successfully")

				return redirect(url_for('user.userhome'))
	return render_template('login.html')


@public.route('/sellerregister',methods=['get','post'])
def sellerregister():
	if "register" in request.form:
		fna=request.form['f']
		lna=request.form['l']
		pho=request.form['ph']
		pla=request.form['pl']
		em=request.form['e']
		cat=request.form['category']
		uname=request.form['u']
		pwd=request.form['p']
		ql="insert into login values(null,'%s','%s','seller')"%(uname,pwd)
		rl=insert(ql)
		qs="insert into seller values(null,'%s','%s','%s','%s','%s','%s','%s')"%(rl,fna,lna,pla,pho,em,cat)
		insert(qs)
		flash("Register Successfully")		
		return redirect(url_for('public.home'))
	return render_template('sellerregister.html')
@public.route('/userregister',methods=['get','post'])
def userregister():
	if "register" in request.form:
		fna=request.form['f']
		lna=request.form['l']
		pho=request.form['ph']
		pla=request.form['pl']
		em=request.form['e']
		uname=request.form['u']
		pwd=request.form['p']
		ql="insert into login values(null,'%s','%s','user')"%(uname,pwd)
		rl=insert(ql)
		qs="insert into user values(null,'%s','%s','%s','%s','%s','%s')"%(rl,fna,lna,pla,pho,em)
		insert(qs)
		flash("Register Successfully")
		return redirect(url_for('public.home'))
	return render_template('userregister.html')
