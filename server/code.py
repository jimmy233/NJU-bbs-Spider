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
try:
	with open('info.json','rb') as f:
		All = json.load(f) 
	print(All)
except:
	All = {}
	All.setdefault('topic',dict())
	All.setdefault('user',dict())
	All.setdefault('forum',dict())

class test:
	def GET(self):
		i = web.input(id="")
		web.setcookie('name', i.id, 3600)
		return render.test()
class Set:
	def POST(self):
		i = web.input()
		name = web.cookies().get('name')
		if name == "":
			raise web.seeother('/test')
			return
		if name in All[i.choice].setdefault(i.key,list()):
			All[i.choice][i.key].remove(name)
			if All[i.choice][i.key]==[]:
				del All[i.choice][i.key]
		else:
			All[i.choice].setdefault(i.key,list()).append(name)
		with open('info.json','w') as f:
                        jsObj = json.dumps(All)
			f.write(jsObj)
		print(All)
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
