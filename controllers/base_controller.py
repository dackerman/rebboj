class BaseController(webapp.RequestHandler):
    def GetParam(self, name):
        return self.request.get(name)

    def Render(self, template_name, template_data):
        self.response.out.write(template.render(template_name, template_data))

def GetTemplate(view_name):
    return os.path.join(os.path.dirname(__file__),'../views/'+view_name+'.html')
