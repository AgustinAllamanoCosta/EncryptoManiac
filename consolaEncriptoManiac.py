#!/usr/bin/env python
# -*- coding: utf-8 -*-
from encriptoManiac import EncriptoManiac 
import CustomException as ce
import re

class ContextoConsolaManiac(object):

	def __init__(self):
		self.consola = ConsolaEncryptoManiacWin()
		self.historial = HistorialConsola()
		self.patronConsola = re.compile('\S+')

	def bucleDeConsola(self):
		self.escribirEnConsola(ConstanteConsola.mensajeBienvenida)
		self.escribirEnConsola(ConstanteConsola.mensajeComandosBasicos)
		while self.consola.correrLoop:
			self.analizarEntrada(self.ingresarEntradas())

	def ingresarEntradas(self):
		return input()

	def analizarEntrada(self,entrada):
		valoresEntrada = self.patronConsola.findall(entrada)
		try:
			comando = self.consola.operacionesConsola(valoresEntrada[0].lower(),valoresEntrada[1:])	
			resultado = comando.ejecutar()

			if(resultado != None):
				self.escribirEnConsola(resultado)

		except ce.ParametrosComandoIncompletos as expt:
			self.escribirEnConsola(expt.mensaje)
		except ce.ParametrosComandosNullos:
			self.escribirEnConsola(ConstanteConsola.mensajeErrorComandoParametros)
		except ce.InterrumpirConsola:
			self.consola.correrLoop = False
		except ce.ComandoNoEncontradoExcepcion:
			self.escribirEnConsola(ConstanteConsola.mensajeComandosAvanzados)
		except IndexError:
			self.escribirEnConsola(ConstanteConsola.mensajeAyudaComandoAgregar)

		self.historial.agregarEntrada(entrada)

	def escribirEnConsola(self,mensaje):
		print(mensaje)
		self.historial.agregarEntrada(mensaje)

	def obtenerHistorial(self):
		return self.historial.obtener()

class HistorialConsola(object):
	
	def __init__(self):
		self.entradas = []

	def agregarEntrada(self,entrada):
		self.entradas.append(entrada)

	def obtener(self):
		return self.entradas

class ConsolaEncryptoManiac():

	def __init__(self):
		self.correrLoop = True

	def operacionesConsola(self,operacion,argumentos=[]):
		if operacion == 'exit':
			return ComandoExit()
		elif operacion == 'listar':
			return ComandoListar()
		elif operacion == 'vermas':
			return ComandoVerMas()
		elif operacion == 'agregar':
			return ComandoAgregar(argumentos)		
		elif operacion  == 'modificar':
			return ComandoModificar(argumentos)
		elif operacion == 'eliminar':
			return ComandoEliminar(argumentos)
		elif operacion == 'mostrar':
			return ComandoMostrar(argumentos)
		else:
			raise ce.ComandoNoEncontradoExcepcion()

class ConsolaEncryptoManiacWin(ConsolaEncryptoManiac):
	pass

class ComandoConParametro(object):

	def __init__(self,parametros):
		self.parametroComadno = parametros

	def ejecutar(self):
		if(self.parametroComadno == []):
			raise ce.ParametrosComandosNullos()

class ComandoAgregar(ComandoConParametro):
	
	def ejecutar(self):
		super().ejecutar()
		if(len(self.parametroComadno)==1):
			raise ce.ParametrosComandoIncompletos(ConstanteConsola.mensajeAyudaComandoAgregar)
		return None

class ComandoModificar(ComandoConParametro):
	pass

class ComandoEliminar(ComandoConParametro):
	pass

class ComandoMostrar(ComandoConParametro):
	pass

class ComandoConsola(object):

	def ejecutar(self):
		return None

class ComandoVerMas(ComandoConsola):

	def ejecutar(self):
		return ConstanteConsola.mensajeComandosAvanzados

class ComandoExit(ComandoConsola):

	def ejecutar(self):
		raise ce.InterrumpirConsola()

class ComandoListar(ComandoConsola):
	pass

class ConstanteConsola:

	mensajeBienvenida = 'ENCRYPTO MANIAC'
	mensajeComandosBasicos = '''Para agregar una contraseña escribi agregar.\nPara ver las cuentas escribi listar.\nPara ver la lista completa de comandos escribi vermas'''
	mensajeComandosAvanzados = '''Escribi: 
	modificar -> para cambiar la clave de una cuenta
	eliminar  -> para borrar una cuenta
	mostrar   -> para ver la contraseña de una cuenta
	listar    -> para ver todas las cuentas en la base
	agregar   -> para agregar una nueva cuenta y contraseña en la base
	vermas    -> para ver este mensaje :D
	Pd: para ver como usar un comando escribi -> ayuda nombreComando <- ej: ayuda modificar'''
	mensajeErrorComandoParametros = '''Error al ingresar los parametros del comando porfavor vuelva a intentarlo. Si tiene dudas puede usar el comando ayuda'''
	mensajeAyudaComandoAgregar = '''Comando agregar-> agregar parametro1 parametro2 
	parametro1: es el nombre de la cuenta a agregar
	parametro2: es la contraseña de la cuenta
	LOS DOS PARAMETROS SON OBLIGATORIOS'''