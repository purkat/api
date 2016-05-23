#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import jinja2
import webapp2

import json

from google.appengine.api import urlfetch

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        data = open("people.json", "r").read()
        json_data = json.loads(data)

        url = "http://api.openweathermap.org/data/2.5/weather?q=Gorica&units=metric&appid=fda39e0d77211fac42e93aa53699f62e"
        result = urlfetch.fetch(url)
        vreme = json.loads(result.content)

        parametri = {
            "seznam": json_data,
            "vreme": vreme
        }

        return self.render_template("start.html", parametri)

app = webapp2.WSGIApplication(
    [
        webapp2.Route('/', MainHandler)
    ],
    debug=True)
