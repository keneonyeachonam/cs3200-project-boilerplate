from flask import Blueprint, request, jsonify, make_response
import json
from src import db


reviews = Blueprint('reviews', __name__)

# Get all the reviews for a Study Group
@reviews.route('/reviews/<studyGroupID>', methods=['GET'])
def get_reviewsForGroup(studyGroupID):
    query = '''
        SELECT author, review, rating
        FROM review
        WHERE groupID =''' + str(studyGroupID)
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@reviews.route('/reviews/<studyGroupID>', methods=['GET'])
def get_reviewsForGroup(studyGroupID):
    query = '''
        SELECT author, review, rating
        FROM review
        WHERE groupID =''' + str(studyGroupID)
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response