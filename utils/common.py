from flask import session

from models import db


def set_before_request_handle_fuc(app):
	"""
	对flask对象 设置 每次调用视图函数之前，要执行的事情
	"""

	@app.before_request
	def before_request():
		# 查询当前登录用户，如果未登录那么g.user为None，如果登录了g.user就是当前登录用户对象
		# 之所有用g变量，是因为我们可以把需要给视图函数传递的参数，通过给g对象添加属性的方式让g进行携带
		# 然后在视图函数中就可以通过g.user提取出来。也就是说g能够帮我们在多个函数之间传递参数
		user_id = session.get ("user_id")

		g.user = db.session.query (User).filter (User.id == user_id).first ()

		# if request.path.startswith("/admin") and not g.user.is_admin:
		#     # 如果不是管理员，还想访问URL以/admin开始页面，则返回首页
		#     return redirect(url_for('index_blu.index'))

		# 如下代码的功能：如果用户未在访问后台时以管理员方式登录，那么也就没有"is_admin"这个信息时，就跳转到后台登录页面
		# print("----->", request.host, request.path)
		if request.host.startswith ("admin") and not session.get ("is_admin"):
			if not (request.path.startswith ("/login") or request.path.startswith ("/static")):
				# 如果不是管理员，则返回首页
				return redirect (url_for ('admin_blu.login'))


