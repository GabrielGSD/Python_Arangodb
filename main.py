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
def listWithAQL():
   aql = "FOR x IN Students RETURN { [x._key] : {['name']:x.name, ['surname']:x.surname, ['age']: x.age} }"
   queryResult = db.AQLQuery(aql, rawResults=True, batchSize=100)
   print(list(queryResult))

# listWithAQL()

def insertWithAQL(doc, collection):
   try:
      bind = {"doc": doc}
      aql = "INSERT @doc INTO " + collection + " LET newDoc = NEW RETURN newDoc"
      queryResult = db.AQLQuery(aql, bindVars=bind)
      print("Dados adicionado com sucesso")   
   except: 
      print("Erro ao adicionar dados")

doc = {'name': 'Denis', 'surname': 'Diderot', 'age': 27, 'tech': True}
# insertWithAQL(doc, 'Students')

def updateWithAQL(doc, key, collection):
   bind = {"doc": doc, "key": key}
   aql = "UPDATE @key WITH @doc IN " + collection
   result = db.AQLQuery(aql, bindVars=bind)
   print("Os dados foram atualizado com sucesso")

doc = {"age": 25}
# updateWithAQL(doc, '6424', 'Students')

def listWithFilterAQL():
   sample_chars_query = """
      FOR c IN Students
         FILTER c.tech == true
         SORT c.name
         LIMIT 10
         RETURN { Nome: c.name, Sobrenome: c.surname, Idade: c.age }
   """
   query_result = db.AQLQuery(sample_chars_query, rawResults=True)
   for doc in  query_result:
      print(doc, sep='\n')

# listWithFilter()

def deleteWithAQL():
   bind = {"@collection": "Students"}
   aql = """
      FOR x IN @@collection
         FILTER x.age == 25
         REMOVE x IN @@collection
         LET removed = OLD RETURN removed
   """
   aql = "REMOVE @key IN @@collection"
   queryResult = db.AQLQuery(aql, bindVars=bind)
   print(queryResult)

# deleteWithAQL()