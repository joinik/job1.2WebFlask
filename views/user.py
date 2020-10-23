import random

from flask import render_template, request, session, jsonify, redirect, url_for
from werkzeug.security import generate_password_hash

from models import db
from models.index import User
from . import user_blu


@user_blu.route ("/login")
def login():

	return render_template ("login.html")



@user_blu.route ("/passport/login", methods=["POST"])
def passport_login():

	mobile = request.json.get("mobile")
	pwd = request.json.get("password")


	user = db.session.query(User).filter(User.phone == mobile,).first()
	if not user.check_password(pwd):
		return jsonify({
			"errno": 2001,
			"errmsg": "用户名或者密码错误"
		})

	print ("登录成功-----")
	return jsonify ({
		"errno": 0,
		"errmsg": "登录成功"
	})


@user_blu.route ("/register")
def register():
	return render_template ("register.html")


@user_blu.route ("/passport/register", methods=["POST"])
def passport_register():
	print("-------1------")

	phone = request.json.get ("mobile")
	smscode = request.json.get ("smscode")
	pwd = request.json.get ("password")

	# 校验"短信验证码"是否正确
	if session.get ("sms_code") != smscode:
		ret = {
			"errno": 1003,
			"errmsg": "重新输入手机验证码"
		}
		return jsonify (ret)

	use = db.session.query (User).filter (User.phone == phone).first ()
	if use:
		return jsonify ({
			"errno": 1001,
			"errmsg": "该手机号已经注册..."
		})
	else:
		try:
			use = User ()
			use.name = phone
			# 调用方法 ，进行 加密
			use.password = pwd
			use.phone = phone
			db.session.add (use)
			db.session.commit ()
			print ("注册成功-----")
			ret = {
				"errno": 0,
				"errmsg": "注册成功..."
			}
			# 注册成功之后，立刻认为登录成功，也就说需要进行状态保持
			session['user_id'] = use.id
			session['nick_name'] = phone

		except Exception as e:
			print ("注册报错---")
			print (e)
			db.session.rollback ()  # 如果在将用户的信
			ret = {
				"errno": 1002,
				"errmsg": "注册失败..."
			}

		return jsonify (ret)


@user_blu.route ("/passport/smscode", methods=["POST"])
def smscode():
	# 1. 提取数据
	image_code = request.json.get ("image_code")
	mobile = request.json.get ("mobile")

	# # 2. 校验图片验证码是否正确
	# image_code_session = session.get ("image_code")
	# print ("输入的验证码", image_code)
	# print ("生成的验证码", image_code_session)
	# if image_code.lower () != image_code_session.lower ():
	# 	ret = {
	# 		"errno": 4004,
	# 		"errmsg": "图片验证码错误..."
	# 	}
	# 	return jsonify (ret)

	# 3. 生成一个随机的6位数
	sms_code = str (random.randint (100000, 999999))
	print ("短信验证码是:", sms_code)
	print ("-----短信验证码----")

	# 4. 存储到session中
	session['sms_code'] = sms_code

	# 5. 通过短信发送这个6位数
	# send_msg_to_phone (mobile, sms_code)

	ret = {
		"errno": 0,
		"errmsg": "发送短信验证码成功..."
	}

	return jsonify (ret)
