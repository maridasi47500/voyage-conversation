from directory import Directory
from render_figure import RenderFigure
from myscript import Myscript
from mycommandline import Mycommandline
from mydb import Mydb
from scriptpython import Scriptpython


from mypic import Pic
from javascript import Js
from stylesheet import Css
import re
import traceback
import sys

class Route():
    def __init__(self):
        self.Program=Directory("trouve 1 job ")
        self.Program.set_path("./")
        self.mysession={"notice":None,"email":None,"name":None}
        self.dbScript=Myscript()
        self.scriptpython=Scriptpython
        self.dbCommandline=Mycommandline()
        self.db = Mydb()
        self.render_figure=RenderFigure(self.Program)
        self.getparams=("id",)
    def set_post_data(self,x):
        self.post_data=x
    def get_post_data(self):
        return self.post_data
    def set_my_session(self,x):
        print("set session",x)
        self.Program.set_my_session(x)
        self.render_figure.set_session(self.Program.get_session())
    def get_exception_routes(self):
        #form n'est pas envoye avec javascript/jquery
        return ["/chercherjob"]
    def get_some_post_data(self,params=()):
        #if route in  some routes
        x={}
        try:
            for y in params:
                print(self.post_data) #erreur
                print(self.post_data[y]) #erreur
                x[y]=self.post_data[y][0]
        except Exception as e:
            print("wow",e)
        return x
    def set_redirect(self,x):
        self.Program.set_redirect(x)
        self.render_figure.set_redirect(self.Program.get_redirect())
    def render_some_json(self,x):
        self.Program.set_json(True)
        return self.render_figure.render_some_json(x)
    def set_json(self,x):
        self.Program.set_json(x)
        self.render_figure.set_json(self.Program.get_json())
    def set_notice(self,x):
        print("set session",x)
        self.Program.set_session_params({"notice":x})
        self.render_figure.set_session(self.Program.get_session())
    def set_session(self,x):
        print("set session",x)
        self.Program.set_session(x)
        self.render_figure.set_session(self.Program.get_session())
    def get_this_route_param(self,x,params):
        print("set session",x)
        return dict(zip(x,params["routeparams"]))
    def logout(self,search):
        self.Program.logout()
        self.set_redirect("/")
        return self.render_figure.render_redirect()
    def welcome(self,search):
        hi=self.dbScript.getall()
        self.render_figure.set_param("scripts",hi)
        return self.render_figure.render_figure("welcome/allscript.html")
    def allscript(self,search):
        #myparam=self.get_post_data()(params=("name","content","monscript",))
        hi=self.dbScript.getall()
        self.render_figure.set_param("scripts",hi)
        return self.render_figure.render_figure("welcome/allscript.html")
    def lancerscript(self,search):
        myparam=search["myid"][0]
        hi=self.dbScript.getbyid(myparam)
        print(hi, "my script")
        a=self.scriptpython(hi["name"]).lancer()
        return self.render_some_json("welcome/monscript.json")
    def monscript(self,search):
        myparam=self.get_post_data()(params=("name","content","monscript",))
        hey=self.dbCommandline.create(myparam)
        hi=self.dbScript.create(myparam)
        print(hey,hi)
        return self.render_some_json("welcome/monscript.json")
    def hello(self,search):
        print("hello action")
        return self.render_figure.render_figure("welcome/index.html")
    def newjob(self,search={}):
        return self.render_figure.render_figure("welcome/newjob.html")
    def createjob(self,params={}):
        myparams=self.get_post_data()(params=("name","lat","lon","description",))
        job=self.db.Job.create(myparams)
        if job["job_id"]:
          self.set_notice(job["notice"])
          self.set_json("{\"redirect\":\"/voirjob/"+job["job_id"]+"\"}")
        else:
          self.set_json("{\"redirect\":\"/\"}")
        return self.render_figure.render_json()
    def searchjob(self,params={}):
        print("yay")
        myparams=self.get_some_post_data(params=("job","lieu"))
        self.render_figure.set_param("s",(myparams["job"] + " " +myparams["lieu"]))
        ok=self.db.Job.getplacesnearby(myparams["job"],myparams["lieu"])["rows"]
        self.render_figure.set_param("jobs",ok["rows"])
        self.render_figure.set_param("message",ok["message"])
        return self.render_figure.render_figure("welcome/searchjob.html")
    def voirjob(self,params={}):
        getparams=("id",)
        myparam=self.get_this_route_param(getparams,params)
        self.render_figure.set_param("job",self.db.Job.getbyid(myparam["id"]))
        return self.render_figure.render_figure("welcome/voirjob.html")
    def voirtoutcequejaiajoute(self,data):

        print("tout")
        tout=self.db.Job.getall()
        print("tout")
        print(tout,"tout")
        self.render_figure.set_param("tout",tout)
        return self.render_some_json("welcome/hey.json")
    def run(self,redirect=False,redirect_path=False,path=False,session=False,params={},url=False,post_data=False):
        if params:
            print("mes only params : ", params)
        if post_data:
            print("post data")
            self.set_post_data(post_data)
            print("post data set",post_data)
        if url:
            print("url : ",url)
            self.Program.set_url(url)
        self.set_my_session(session)

        if redirect:
            self.redirect=redirect
        if redirect_path:
            self.redirect_path=redirect
        if not self.render_figure.partie_de_mes_mots(balise="section",text=self.Program.get_title()):
            self.render_figure.ajouter_a_mes_mots(balise="section",text=self.Program.get_title())
        if path and path.endswith("jpg"):
            self.Program=Pic(path)
            self.Program.set_path("./")
        elif path and path.endswith(".png"):
            self.Program=Pic(path)
        elif path and path.endswith(".jfif"):
            self.Program=Pic(path)
        elif path and path.endswith(".css"):
            self.Program=Css(path)
        elif path and path.endswith(".js"):
            self.Program=Js(path)
        elif path:
            path=path.split("?")[0]
            print("link route ",path)
            ROUTES={


                    '^/lancerscript$': self.lancerscript,
                    '^/chercherjob$': self.searchjob,
                    '^/newjob$': self.newjob,
                    "^/voirjob/([0-9]+)$":self.voirjob,
                    '^/createjob$': self.createjob,
                    '^/toutcequejaiajoute$': self.voirtoutcequejaiajoute,
                    '^/allscript$': self.allscript,
                    '^/welcome$': self.welcome,
                    '^/monscript$': self.monscript,
                    '^/$': self.hello

                    }
            REDIRECT={"/save_user": "/welcome"}
            for route in ROUTES:
               print("pattern=",route)
               mycase=ROUTES[route]
               x=(re.match(route,path))
               print(True if x else False)
               if x:
                   params["routeparams"]=x.groups()
                   try:
                       self.Program.set_html(html=mycase(params))


                   except Exception:  
                       self.Program.set_html(html="<p>une erreur s'est produite "+str(traceback.format_exc())+"</p><a href=\"/\">retour à l'accueil</a>")
                   return self.Program
               else:
                   self.Program.set_html(html="<p>la page n'a pas été trouvée</p><a href=\"/\">retour à l'accueil</a>")
        return self.Program
