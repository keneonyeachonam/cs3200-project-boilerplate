from flask import Blueprint, request, jsonify, make_response
import json
from src import db


users = Blueprint('Users', __name__)


# Get user detail for user with particular userID
@users.route('/Users/<userID>', methods=['GET'])
def get_customer_with_id(userID):
    cursor = db.get_db().cursor()
    cursor.execute('select * from user where userID = {0}'.format(userID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# Get user detail for user with particular userID
@users.route('/Users/<userID>', methods=['PUT'])
def update_customer_with_id(userID):
    # collecting data from the request object 
    the_data = request.json
    #current_app.logger.info(the_data)

    #(firstName, lastName, userYear, major, preferredSubject)
    #extracting the variable
    firstName = the_data['firstName']
    lastName = the_data['lastName']
    userYear = the_data['userYear']
    major = the_data['major']
    preferredSubject = the_data['preferredSubject']



    # Constructing the query
    query = 'update user set firstName = ' + firstName + ', lastName = ' + lastName + ', userYear = ' + str(userYear) + ', major = ' + str(major) + ', preferredSubject = ' + str(preferredSubject)
    query += ' where userID = {0}'.format(userID)
    #current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!' 



@users.route('/Users/<userID>', methods=['DELETE'])
def delete_user(userID):

    query = 'UPDATE user set banned = 1 WHERE userID = ' + str(userID)
    #current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return 'Success!'   