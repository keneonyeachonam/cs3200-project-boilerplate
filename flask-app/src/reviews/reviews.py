from flask import Blueprint, request, jsonify, make_response, current_app
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

# User writes a review
@reviews.route('/reviews/<studyGroupID>/<userID>', methods=['POST'])
def write_reviewsForGroup(studyGroupID, userID):
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    text_review = the_data['review']
    rating = the_data['rating']

    # Constructing the query
    query = 'INSERT INTO review (groupID, author, review, rating) values ('
    query += studyGroupID + ', '
    query += userID + ', "'
    query += text_review + '", '
    query += rating + ')'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Review submitted!'