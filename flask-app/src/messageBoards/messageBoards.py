from flask import Blueprint, request, jsonify, make_response
import json
from src import db


messageBoards = Blueprint('messageBoards', __name__)


# Get msgboard details 
@messageBoards.route('/MessageBoards', methods=['GET'])
def get_messageBoards():
    cursor = db.get_db().cursor()
    cursor.execute('select * from messageBoard')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get msgboard details 
@messageBoards.route('/MessageBoards', methods=['POST'])
def post_messageBoards():
     # collecting data from the request object 
    the_data = request.json
    #current_app.logger.info(the_data)

    #(boardName)
    #extracting the variable
    boardName = the_data['boardName']


    # Constructing the query
    query = 'insert into messageBoard (boardName) values (\''
    query += boardName + '\')'
    #current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

# Get msgboard details 
@messageBoards.route('/MessageBoards/<id>', methods=['GET'])
def get_messageBoards_by_id(id):
    cursor = db.get_db().cursor()
    cursor.execute('select * from messages WHERE messageBoardID = ' + str(id))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response



# Get msgboard details 
@messageBoards.route('/MessageBoards/<id>', methods=['POST'])
def post_messagetoBoard(id):
     # collecting data from the request object 
    the_data = request.json
    #current_app.logger.info(the_data)

    #(author, replyToID, messageBoardID, content)
    #extracting the variable
    author = the_data['author']
    replyToID = 'NULL'
    messageBoardID = id   
    content = the_data['content']  
 
    # Constructing the query
    query = 'insert into messages (author, replyToID, messageBoardID, content) values ("'
    query += author + '", '
    query += replyToID + ', '
    query += messageBoardID + ')'
    #current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'    



# Get msgboard details 
@messageBoards.route('/MessageBoards/<id>', methods=['DELETE'])
def delete_messageBoard(id):
     # collecting data from the request object 
    
 
    query = 'UPDATE messageBoard set banned = 1 WHERE messageBoardID = ' + str(id)
    #current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return 'Success!'  



# Get msgboard details 
@messageBoards.route('/MessageBoards/<id>/<messageID>', methods=['POST'])
def post_message_reply(id, messageID):
     # collecting data from the request object 
    the_data = request.json
    #current_app.logger.info(the_data)

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
    query += messageBoardID + ')'
    #current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'    

# Get msgboard details 
@messageBoards.route('/MessageBoards/<id>/<messageID>', methods=['DELETE'])
def delete_messageBoard_message(id, messageID):
     # collecting data from the request object 
    
 
    query = 'UPDATE messages set published = 0 WHERE messageID = ' + str(id)
    #current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return 'Success!'            