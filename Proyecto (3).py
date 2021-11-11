from Tkinter import* 
import Tkinter,Tkconstants,tkFileDialog,os
import tkMessageBox
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
import sys
import os
#------------Metodos del programa-------------


BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])]

#===========Clases===========================  
class Explorer:
	def __init__(self):
		self.path=""
		self.archivo=None
		self.archivos=None
		self.archivoEscritura=None
		self.extension=None
		self.key=""
	def setArchivo(self,archivo):
		self.archivo=archivo
	def getArchivo(self):
		return self.archivo
	def setPath(self,path):
		self.path=path
	def getPath(self):
		return self.path
		'''
		Metodo de encriptacion el cual transforma el parametro
		password y lo convierte en un key de base 16
		@param raw, password
		@return cadena encriptada
		@since 1.0
		'''
	def encrypt(self,raw, password):
	    private_key = hashlib.sha256(password.encode("utf-8")).digest()
	    raw = pad(raw)
	    iv = Random.new().read(AES.block_size)
	    cipher = AES.new(private_key, AES.MODE_CBC, iv)
	    return base64.b64encode(iv + cipher.encrypt(raw))
	'''
		Metodo de desencriptacion el cual transforma el parametro
		password y lo convierte en un key de base 16
		@param ENC, password
		@return cadena DESENCRIPTADA
		@since 1.0
	'''

	def decrypt(self,enc, password):
	    private_key = hashlib.sha256(password.encode("utf-8")).digest()
	    enc = base64.b64decode(enc)
	    iv = enc[:16]
	    cipher = AES.new(private_key, AES.MODE_CBC, iv)
	    return unpad(cipher.decrypt(enc[16:]))
		
	'''
	Metodo para encriptar desde la consola
	@param direccion,nombre,pasword
	@return
	@since 1.0
	'''
	def encriptarConsola(self,direccion,nombre,pasword):
		inp=open(direccion,"rb")
		out=open(nombre,"w")
		self.key=pasword
		print self.key
		if self.key==""or self.key==None:
			print "no hay clave"
		else:
			for linea in inp.readlines():
				out.write(self.encrypt(str(linea),str(self.key))+'\n')
			print "Archivo a sido encriptado"

		return
		
	 '''
	verifica si existe un key, si no existe una key
	pondra un aviso en pantalla, si hay una key procedera
	ha encriptar el archivo
	@since 1.0
	'''

	def buttonEncriptar(self):
		inp=open(self.path,"r")
		out=open(self.archivo,"w")
		self.key=t2.get("1.0",END)
		print self.key
		if self.key==""or self.key==None:
			tkMessageBox.showerror("Error","No ha introducido ninguna clave")
		else:
			for linea in inp.readlines():
				out.write(self.encrypt(str(linea),str(self.key))+'\n')
			tkMessageBox.showinfo("Encriptar","Archivo encriptado correctamente")

		return
	'''
		metodo para desencriptar desde la consola
		@param direccion,nombre,pasword
		@since 1.0
	'''	

	def desencriptarconsola(self, direccion,nombre,pasword):
		inp=open(direccion,"r")
		out=open(nombre,"w")
		self.key=pasword
		if self.key=="" or self.key==None:
			print "No ha introducido ninguna clave"
		else:
			for linea in inp.readlines():
				out.write(bytes.decode(self.decrypt(str(linea),str(self.key))))
			print "Archivo desencriptado correctamente"


	'''
		verifica si existe un key, si no existe una key
		pondra un aviso en pantalla, si hay una key procedera
		ha deseencriptar el archivo
		@since 1.0
	'''	

	def buttonDesencriptar(self):
		inp=open(self.path,"r")
		out=open(self.archivo,"w")
		self.key=t2.get("1.0",END)
		if self.key=="" or self.key==None:
			tkMessageBox.showerror("Error","No ha introducido ninguna clave")
		else:
			for linea in inp.readlines():
				out.write(bytes.decode(self.decrypt(str(linea),str(self.key))))
			tkMessageBox.showinfo("Desencriptar","Archivo desencriptado correctamente")
		
		'''
		verifica la extension del archivo qeu deseamos cifrar
		si es un archivo .cryp  habilitara el boton desencriptar
		si es cualquier tipo de archivo habilitara el botn de
		encriptar
		@since 1.0
		'''
	def cargarArchivo(self):
		if self.path!="":
			if str(self.extension)=="cryp":
				b2.config(state=DISABLED)
				b3.config(state=NORMAL)
				self.archivo+=".decry"
			else:
				self.archivo+=".cryp"
				b3.config(state=DISABLED)
				b2.config(state=NORMAL)

			tkMessageBox.showinfo("Aviso","Archivo se cargo correctamente")
			
		else:
			tkMessageBox.showerror("Error","No ha agregdo ninguna ruta")
			return 
	
	def integrantes(self):
		tkMessageBox.showinfo("Integrantes del Grupo","\nOrson Manuel Henandez \n #20131017330\nAriel Isai \n #20131017330\nJakmeni Quilico\n #20161004456")
		'''
	Metodo que abre el explorador de archvos de Linux
	Guarda la direccion del archivo en un String path
	Agrega la ubicacion a un witget t1
	@since 1.0
	'''
	def ExFileNameEncriptar(self):
		self.path=interfaz.filename=tkFileDialog.askopenfilename(title="Buscar Archivo")
		t1.insert(INSERT,self.path)
		self.key=t2.get("1.0",END)
		self.archivo=self.path.split("/")
		self.archivo=self.archivo[len(self.archivo)-1].split(".")
		self.extension=self.archivo[1]
		self.archivo=self.archivo[0]
		self.cargarArchivo()
	def ExFolderCifrado(self):
		self.path=interfaz.filename=tkFileDialog.askdirectory(title="Buscar Directorio")
		t3.insert(INSERT,self.path)
		self.key=t2.get("1.0",END)
		self.archivos=os.listdir(self.path)
		self.cargarArchivo()
		pass
		

	
#------------Estancias-------------
cryp=Explorer()

#-----------------Interfaz---------------------
interfaz=Tk()
interfaz.resizable(0,0)
interfaz.title("Encriptador ")
#-----------------Frame------------------------
frame=Frame(interfaz,bg="#581845",width=300,height=380)
frame.pack()
#----------------Cuadros de texto-------------
t1=Text(frame,height=1,width=23,padx=10,)
t1.place(x=10,y=40)
t2=Text(frame,height=1,width=17,padx=10,)
t2.place(x=110,y=150)
t3=Text(frame,height=1,width=23,padx=10,)
t3.place(x=10,y=100)
#-----------------Menu------------------------
menu=Menu(interfaz)
interfaz.config(menu=menu)
filemenu=Menu(menu)
menu.add_cascade(label="Acerca",menu=filemenu)
menu.config(bg="#900C3F",fg="#DAF7A6")
filemenu.config(bg="#FF5733",fg="#DAF7A6")
filemenu.add_command(label="Integrantes",command=cryp.integrantes)
filemenu.add_separator()
filemenu.add_command(label="Salir",command=interfaz.quit)
#-----------------Etiquetas-------------------
Label(frame,text="Ruta del archivo ",bg="#581845",fg="#DAF7A6",font=("Arial",13)).place(x=10,y=5)
Label(frame,text="Directorio ",bg="#581845",fg="#DAF7A6",font=("Arial",13)).place(x=10,y=70)
Label(frame,text="Contrasena:",bg="#581845",fg="#DAF7A6",font=("Arial",13)).place(x=10,y=150)
#----------------Botones----------------------
b1=Button(frame,bg="#C70039",fg="#DAF7A6",height=1,width=3,text="Buscar",command=cryp.ExFileNameEncriptar)
b1.place(x=230,y=35)
b4=Button(frame,bg="#C70039",fg="#DAF7A6",height=1,width=3,text="Buscar",command=cryp.ExFolderCifrado)
b4.place(x=230,y=95)
b2=Button(frame,bg="#C70039",fg="#DAF7A6",font=("Arial",16),height=2,width=8,text="Encriptar",command=cryp.buttonEncriptar)
b2.place(x=90,y=210)
b3=Button(frame,bg="#C70039",fg="#DAF7A6",font=("Arial",16),height=2,width=8,text="Desencriptar",command=cryp.buttonDesencriptar)
b3.place(x=90,y=270)

a = sys.argv[1]
if a=="--gui":
	interfaz.mainloop()
else:
	if len(sys.argv)==3:
		directory=sys.argv[1]
		pasword=sys.argv[2]

		#ver si es encriptacion o desencriptacion

		b=directory.split(".")
		c=directory.split("/")

		if len(b)>1:
		#desencriptar
			if b[-1]=="cryp":
				nae=c[-1]
				nae2=nae.split(".")
				nae3=nae2[0]
				nae3=nae3+".decrypt"

				cryp.desencriptarconsola(directory,nae3,pasword) 
			else:#encriptacion
				name=c[-1]
				name2=name.split(".")
				name3=name2[0]
				name3=name3+".cryp"

				salida=name3
				cryp.encriptarConsola(directory,salida,pasword)
		else:
			#encriptar toda la carpeta
			path=directory
			dirs=os.listdir(path)

			for file in dirs:
				if file[-1]=="cryp":
					name=file.split(".")
					name2=name[0]
					name3=name2+".decrypt"

					cryp.desencriptarconsola(directory+"/"+file,directory+"/"+name3,pasword) 
				else:
					name=file
					name2=name.split(".")
					name3=name2[0]
					name3=name3+".cryp"

					salida=name3
					cryp.encriptarConsola(directory+"/"+file,directory+"/"+salida,pasword)

	else:#si nos da la direccion para guardar
		directory=sys.argv[1]
		out=sys.argv[2]
		pasword=sys.argv[3]

		#ver si es encriptacion o desencriptacion

		b=directory.split(".")
		c=directory.split("/")

		if len(b)>1:
			#desencriptar
			if b[-1]=="cryp":
				name=c[-1]
				name2=name.split(".")
				name3=name2[0]
				name3=out+name3+".decrypt"

				cryp.desencriptarconsola(directory,name3,pasword)
			else:#encriptar
				name=c[-1]
				name2=name.split(".")
				name3=name2[0]
				name3=out+name3+".cryp"

				salida=name3
				cryp.encriptarConsola(directory,salida,pasword)
		else:#encriptar toda la carpeta
			path=directory
			dirs=os.listdir(path)

			for file in dirs:
				if file[-1]=="cryp":
					name=file.split(".")
					name2=name[0]
					name3=out+name2+".decrypt"

					cryp.desencriptarconsola(directory+"/"+name3,pasword) 
				else:
					name=file
					name2=name.split(".")
					name3=name2[0]
					name3=name3+".cryp"

					salida=out+name3
					cryp.encriptarConsola(directory+"/"+file,salida,pasword)


	