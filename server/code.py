# -*- coding: utf-8 -*- 
import web
import json
from web.httpserver import StaticMiddleware

urls = (
	'/test', 'test',
	'/set', 'Set',
	'/getdict','Get',
	'/end','End'
)
render = web.template.render('test')
All = dict()
All['topic']=dict()
All['user']=dict()
All['forum']=dict()
class test:
	def GET(self):
		i = web.input(id="")
		web.setcookie('name', i.id, 3600)
		return render.test()
class Set:
	def POST(self):
		i = web.input()
		name = web.cookies().get('name')
		if name == []:
			raise web.seeother('/test')
			return
		if i.key not in All[i.choice]:
			All[i.choice][i.key]=list()
		All[i.choice][i.key].append(name)
		raise web.seeother('/end')
class Get:
	def GET(self):
		return json.dumps(All)
class End:
	def GET(self):
		return render.test1()
if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
