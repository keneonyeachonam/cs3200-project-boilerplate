from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


messageBoards = Blueprint('messageBoards', __name__)


# Get all messaageboards and their details 
@messageBoards.route('/MessageBoards', methods=['GET'])
def get_messageBoards():
    cursor = db.get_db().cursor()
    cursor.execute('select * from messageBoard where banned = 0')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Post a new msgboard  
@messageBoards.route('/MessageBoards', methods=['POST'])
def post_messageBoards():
     # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #(boardName)
    #extracting the variable
    boardName = the_data['messageText']


    # Constructing the query
    query = 'insert into messageBoard (boardName) values (\''
    query += boardName + '\')'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

# Get a specific Message Boards messages 
@messageBoards.route('/MessageBoards/<id>', methods=['GET'])
def get_messageBoards_by_id(id):
    cursor = db.get_db().cursor()
    cursor.execute('select messageID, author, replyToID, publishTime, content, messages.moderatorID, firstName, lastName from messages join user on userID = author WHERE messageBoardID = ' + str(id) + ' and published = 1')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response



# Post a new message to an existing message board
@messageBoards.route('/MessageBoards/<id>/<author>', methods=['POST'])
def post_messagetoBoard(id, author):
     # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #(author, replyToID, messageBoardID, content)
    #extracting the variable
    author = author
    replyToID = 'NULL'
    messageBoardID = id   
    content = the_data['messageText']  
 
    # Constructing the query
    query = 'insert into messages (author, replyToID, messageBoardID, content) values ("'
    query += author + '", '
    query += replyToID + ', '
    query += messageBoardID  + ', "'
    query += content + '")'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'    



# Delete a message board by updating and setting banned to true
@messageBoards.route('/MessageBoards/<id>', methods=['DELETE'])
def delete_messageBoard(id):
     # collecting data from the request object 
    
 
    query = 'UPDATE messageBoard set banned = 1 WHERE messageBoardID = ' + str(id)
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return 'Success!'  



# Create a new message which replies to an existing message
@messageBoards.route('/MessageBoards/<id>/<messageID>', methods=['POST'])
def post_message_reply(id, messageID):
     # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #(author, replyToID, messageBoardID, content)
    #extracting the variable
    author = the_data['author']
    replyToID = messageID
    messageBoardID = id   
    content = the_data['content']  
 
    # Constructing the query
    query = 'insert into messages (author, replyToID, messageBoardID, content) values ("'
    query += author + '", '
    query += replyToID + ', '
    query += messageBoardID  + ', "'
    query += content + '")'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'    

# Delete a specific comment by setting published to 0 
@messageBoards.route('/MessageBoards/<id>/<messageID>', methods=['DELETE'])
def delete_messageBoard_message(id, messageID):
     # collecting data from the request object 
    
 
    query = 'UPDATE messages set published = 0 WHERE messageID = ' + str(id)
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return 'Success!' 


    # Update message with specific messageID
@messageBoards.route('/MessageBoards/<id>/<messageID>', methods=['PUT'])
def update_messageBoard_message(id, messageID):
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    content = the_data['content']
    
    # Constructing the query
    query = 'update messages set content = "' + content + '"'
    query += ' where messageID = {0}'.format(messageID)
    current_app.logger.info(query)

    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'                   