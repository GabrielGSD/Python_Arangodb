from dataclasses import asdict
from tkinter import INSERT
from venv import create
from pyArango.connection import *

conn = Connection(username="root", password="rootpassword")

try: 
   db = conn["school"]
except:
   db = conn.createDatabase(name="school")
   print("Banco criado com sucesso")

try: 
   studentsCollection = db["Students"]
   print("Collection encontrada")
except:
   studentsCollection = db.createCollection(name="Students")
   print("Collection criada com sucesso")

def readData(collection):
   print(collection.fetchAll())

#readData(studentsCollection)

def insertData(collection, document):
   try:
      collection.createDocument(document).save()
      print("Dados inseridos com sucesso")
   except:
      print("Erro ao inserir dados")

# insertData(studentsCollection, { "name": "Pedro", "surname": "Santos", "age": 20, "tech": False })

def updateData(collection, key, fieldNewValue, newValue):
   try:
      doc = collection[key]
      doc[fieldNewValue] = newValue
      doc.save()
      print("Dados alterados com sucesso")
   except:
      print("Erro ao alterar dados")
      
# updateData(studentsCollection, '5494', 'age', 23)

def deleteData(collection, key):
   try:
      collection[key].delete()
      print("Dado deletado com sucesso")
   except:
      print("Erro ao deletar dados")

# deleteData(studentsCollection, '5213')

'''   Utilizando AQL Usage   '''
aql = "FOR x IN Students RETURN { [x._key] : {['name']:x.name, ['surname']:x.surname, ['age']: x.age} }"
queryResult = db.AQLQuery(aql, rawResults=True, batchSize=100)
print(list(queryResult))