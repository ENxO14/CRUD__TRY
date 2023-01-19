from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash,  render_template, Response
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import pymssql
import pandas as pd
from bson import json_util
import json

import psycopg2 #pip install psycopg2 
import psycopg2.extras

app = Flask(__name__)

app.secret_key = 'xyzsdfg'

def connection():
    conn = pymssql.connect(server='213.140.22.237\SQLEXPRESS',
                           user='livera.sasmitha', password='xxx123##', database='livera.samsmitha')
    return conn


mysql = MySQL(app)
CORS(app)

@app.route('/')
def index():
    return "Ciao"

@app.route('/exams')
def exams():
    # Create a connection
    conn = connection()
    # Create a cursor
    cur = conn.cursor(as_dict=True)
    # Execute the SQL SELECT statement
    cur.execute("SELECT * FROM verificaTec")
    # Fetch all rows from the SELECT statement
    list_users = cur.fetchall()
    # Render the index.html template and pass the list of students
    #return render_template('hehe.html', list_users = list_users)

    return jsonify (list_users)
    resp = jsonify(list_users)
    #return json.dumps(list_users)
    resp = json_util.dumps(list_users)
    return Response(resp, mimetype = 'application/json') 

@app.route('/teachers')
def teachers():
    # Create a connection
    conn = connection()
    # Create a cursor
    cur = conn.cursor(as_dict=True)
    # Execute the SQL SELECT statement
    cur.execute("SELECT * FROM docente")
    # Fetch all rows from the SELECT statement
    list_users = cur.fetchall()
    # Render the index.html template and pass the list of students
    #return render_template('hehe.html', list_users = list_users)

    return jsonify (list_users)
    resp = jsonify(list_users)
    #return json.dumps(list_users)
    resp = json_util.dumps(list_users)
    return Response(resp, mimetype = 'application/json')


@app.route('/users', methods=['POST', 'GET'])
def data():
    conn = connection()
    # Create a cursor
    cur = conn.cursor(as_dict=True)
    # POST a data to database
    if request.method == 'POST':
        body = request.json
        title = body['title']
        course = body['course']
        tipo = body['tipo']
        difficulty = body['difficulty']
        duration = body['duration']
        classe = body['classe']
        subject = body['subject']
        
        cur.execute("INSERT INTO verificaTec (title,course,tipo,difficulty,duration, classe,subject) VALUES (%s,%s,%s,%s,%s,%s,%s)", (title, course,tipo,difficulty,duration,classe,subject))
        conn.commit()
        return jsonify({
            'status': 'Data is posted to SQLite!',
            'title': title,
            'course': course,
            'tipo':tipo,
            'difficulty':difficulty,
            'duration':duration,
            'classe':classe,
            'subject':subject
        })

    # GET all data from database
    if request.method == 'GET':
        conn = connection()
        # Create a cursor
        cur = conn.cursor(as_dict=True)
        cur.execute("SELECT * FROM verificaTec")
        data = cur.fetchall()
        dataJson = []
        print(data)
        for doc in data:
            id = doc['id']
            title = doc['title']
            course = doc['course']
            tipo = doc['tipo']
            difficulty = doc['difficulty']
            duration = doc['duration']
            classe = doc['classe']
            subject = doc['subject']
            dataDict = {
                'id' :id,
                'title': title,
                'course': course,
                'tipo': tipo,
                'difficulty': difficulty,
                'duration': duration,
                'classe': classe,
                'subject': subject
            }
            dataJson.append(dataDict)
        return jsonify(dataJson)

@app.route('/users/<int:id>', methods=['GET', 'DELETE', 'PUT'])
def onedata(id):

    # GET a specific data by id
    if request.method == 'GET':
        conn = connection()
        # Create a cursor
        cur = conn.cursor(as_dict=True)
        cur.execute("SELECT * FROM verificaTec WHERE id = %s", (id, ))
        ver = cur.fetchone()
        dataDict = {
            'id': ver['id'],
            'title': ver['title'],
            'course': ver['course'],
            'tipo': ver['tipo'],
            'difficulty': ver['difficulty'],
            'duration': ver['duration'],
            'classe': ver['classe'],
            'subject': ver['subject']
        }
        cur.close()
        conn.close()
        return jsonify(dataDict)
        

    # DELETE a data
    if request.method == 'DELETE':
        conn = connection()
        cur = conn.cursor()

        cur.execute('SELECT * FROM verificaTec WHERE id = %s', (id,))
        ver = cur.fetchone()
        if ver:
            cur.execute('DELETE FROM verificaTec WHERE id = %s', (id,))
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({'status': 'Data id: ' + str(id) + ' is deleted!'})
        else:
            return jsonify({"message": "Data not found"}), 404

    # UPDATE a data by id
    if request.method == 'PUT':
        body = request.json
        title = body['title']
        course = body['course']
        tipo = body['tipo']
        difficulty = body['difficulty']
        duration = body['duration']
        classe = body['classe']
        subject = body['subject']

        conn = connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM verificaTec WHERE id = %s", (id,))
        ver = cur.fetchone()
        if ver:
            cur.execute("UPDATE verificaTec SET title = %s, course = %s, tipo = %s, difficulty = %s, duration = %s, classe = %s, subject = %s WHERE id = %s", (title, course, tipo, difficulty, duration, classe, subject, id))
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({'status': 'Data id: ' + str(id) + ' is updated!'})
        else:
            return jsonify({"message": "Data not found"}), 404



if __name__ == '__main__':
    app.run(debug=True)