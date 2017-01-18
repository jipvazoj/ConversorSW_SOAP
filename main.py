#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
# import suds
import jinja2
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))
import suds
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
	
FORM="""
<STYLE>
BODY { margin: 15px 10px 10px 10px }
</STYLE>
<img src="/images/billetes.jpg" height="250" width="400"></img>
<h2>CONVERSOR DE MONEDAS...</h2>
Introducir la cantidad de Euros ...
<form name="f" action="/convertir" method="POST"/>
<input name="euros" type="number" step="any" required/>
<p>Seleccionar una moneda ...
<p><select name="moneda">
  <option value="Dolar">Dolar</option>
  <option value="Libra">Libra</option>
  <option value="Kuna">Kuna</option>
</select>
<input value="Convertir moneda" type="submit"/> </form>
"""
class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(FORM)

class Convertir(webapp2.RequestHandler):
    def post(self):
		url = 'http://www.webservicex.net/CurrencyConvertor.asmx?WSDL'
		client = suds.client.Client(url)
		e=self.request.get("euros")
		m=self.request.get("moneda")
		if m=="Dolar":
			
			# funcionara el servicio web de matriculas de hostinger????
			respuesta = client.service.ConversionRate('EUR','USD')
			p= round(float(e) * respuesta , 2)
			#self.response.write(respuesta)
			self.response.write('<script>alert("'+ e + ' Euros son --> '+ str(p) + ' Dolares");</script>')

		if m=="Libra":
			respuesta = client.service.ConversionRate('EUR','GBP')
			p= round(float(e) * respuesta, 2)
			self.response.write('<script>alert("'+ e + ' Euros son --> '+ str(p) + ' Libras");</script>')

		if m=="Kuna":
			respuesta = client.service.ConversionRate('EUR','HRK')
			p= round(float(e) * respuesta, 2)
			self.response.write('<script>alert("'+ e + ' Euros son --> '+ str(p) + ' Kunas");</script>')

		self.response.write(FORM)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
	('/convertir', Convertir)
], debug=True)
