from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


bookmarks = Blueprint('bookmarks', __name__)

# Get all messages boards and messages this user has bookmarked
@bookmarks.route('/bookmarks/<userID>', methods=['GET'])
def get_bookmarkedMessages(userID):
    query = '''
        SELECT messageBoard.boardName, messages.*
        FROM messageBoard
            JOIN bookmark ON messageBoard.messageBoardID = bookmark.messageBoardID
            JOIN messages ON messageBoard.messageBoardID = messages.messageBoardID
        WHERE bookmark.userID = {0} AND messageBoard.banned = 0 AND messages.published = 1;'''.format(userID)
    
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

# User bookmarks a message board
@bookmarks.route('/bookmarks/<userID>/<messageBoardID>', methods=['POST'])
def create_newBookmark(userID, messageBoardID):
    # Constructing the query
    query = 'INSERT INTO bookmark (userID, messageBoardID) VALUES ({0},{1})'.format(userID, messageBoardID)
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Message board saved!'