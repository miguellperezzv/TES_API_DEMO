from flask import Blueprint, Response, flash, session, request, g, render_template, redirect, url_for, jsonify, make_response
import sqlalchemy
from sqlalchemy.sql import text
from flask_jwt_extended import jwt_required
from ..login.views import  token_required

home = Blueprint('home', __name__)
CIE = Blueprint('CIE', __name__ , url_prefix = '/CIE')


connection_string = 'mssql+pyodbc://admintes:g$M878W6gNfwcY4caA@172.16.3.54/DesprendibleTES?driver=SQL+Server'
str_conn_novasoft = 'mssql+pyodbc://admintes:g$M878W6gNfwcY4caA@172.16.3.54/Novasoft?driver=SQL+Server'

#connection_string = 'mssql+pyodbc://admintes:g$M878W6gNfwcY4caA@172.16.2.54/SQLWEB_R/DesprendibleTES?driver=SQL+Server'
#str_conn_novasoft = 'mssql+pyodbc://admintes:g$M878W6gNfwcY4caA@172.16.2.54/SQLWEB_R/Novasoft?driver=SQL+Server'

@CIE.route("/")
def index():
    return render_template("home.html") 



@CIE.route('/log_desprendibles')
def desprendibles():
        # Step 2: Create an engine
        engine = sqlalchemy.create_engine(connection_string)

        # Step 3: Connect to the database
        connection = engine.connect()

        # Step 4: Execute SQL queries
        result = connection.execute(text("SELECT * FROM log")).fetchall()
        print(result.keys())
        rs = [tuple(row) for row in result]
        df = []
        for row in result:
            #print(row)
            df.append(row)

        # Step 5: Close the connection
        connection.close()

        return jsonify(rs)

#@jwt_required(fresh=True)

@CIE.route('/alumno/<string:cod_alu>')
@token_required
def getAlumno(cod_alu):
    # Step 2: Create an engine
    engine = sqlalchemy.create_engine(str_conn_novasoft)

    # Step 3: Connect to the database
    connection = engine.connect()

    # Step 4: Execute SQL queries
    result = connection.execute(text("SELECT * FROM dbo.cie_alumnos WHERE cod_alu = '" + cod_alu + "'"))

    # Step 5: Get column names from the result object
    column_names = list(result.keys())

    # Step 6: Fetch the first row
    row = result.fetchone()

    # Step 7: Create a dictionary for the row if it exists
    data = {}
    if row:
        for i in range(len(column_names)):
            data[column_names[i]] = row[i]

    # Step 8: Close the connection
    connection.close()

    return jsonify(data)


@CIE.route('/familia/<string:cod_fam>')
@token_required
def getFamilia(cod_fam):
    engine = sqlalchemy.create_engine(str_conn_novasoft)
    connection = engine.connect()
    result = connection.execute(text("SELECT * FROM dbo.cie_familia WHERE cod_fam = '" + cod_fam + "'"))
    column_names = list(result.keys())
    row = result.fetchone()

    data = {}
    if row:
        for i in range(len(column_names)):
            data[column_names[i]] = row[i]

    
    connection.close()

    return jsonify(data)

@CIE.route('/familia/', methods=["POST"])
def postFamiliia():

    data = request.json
    #print(data)
    rs = obtenerUltimaFamilia()
    print("rs ", rs[0]["cod_fam"])
    nueva_familia = rs[0]["cod_fam"]
    data["cod_fam"] = int(nueva_familia) + 1
 
    strSQL = 'insert into cie_familia ('
    cant = len(data.items())
    i=0
    for key,value in data.items():
        strSQL += key
        i = i+1
        if i<cant:
            strSQL +=","

    strSQL+=') VALUES ('
    
    i=0
    for key,value in data.items():
        if value is None or (type(value) == str and (value.isspace() or not value)):
            print("valores vacios", key)
            strSQL += "''"
        else:
            strSQL += "'"+str(value).strip()+"'"
        i = i+1
        if i<cant:
            strSQL +=","
    strSQL+=')'
    #print(strSQL)
    try:
        engine = sqlalchemy.create_engine(str_conn_novasoft)

    # Step 3: Connect to the database
        connection = engine.connect()

    # Step 4: Execute SQL queries
        result = connection.execute(text(strSQL))
        print(type(result))
    except  Exception as e:
        print(e.args)
        return {"Error ": str(e)}, 500
    return {},200



@CIE.route("/familia/ultima_familia", methods=["GET"])
def obtenerUltimaFamilia():
    try:
        result = getUltimaFamilia()
        print(result)
        column_names = list(result.keys())
        row = result.fetchone()

        data = {}
        if row:
            for i in range(len(column_names)):
               data[column_names[i]] = row[i].strip()
        return data,200
    except Exception as e:
        return {"error": str(e)},400

def getUltimaFamilia():
    engine = sqlalchemy.create_engine(str_conn_novasoft)

    # Step 3: Connect to the database
    connection = engine.connect()

    # Step 4: Execute SQL queries
    result = connection.execute(text("SELECT top(1) f.cod_fam as cod_fam FROM CIE_FAMILIA f INNER JOIN CIE_ALUMNOs a on a.cod_fam = f.cod_fam order by a.fec_ing desc"))
    return result

#@ldap_auth_required()
@home.route('/')
def index():
    """
        Verificar que el aplicativo está funcionando
    :return:
    """
    return jsonify({
        "Message": "app up and running successfully"
    })