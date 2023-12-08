import base64
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


resources = Blueprint('resources', __name__)


# Get all resources in group
@resources.route('/resources/<GroupID>', methods=['GET'])
def get_resources(GroupID):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM resources WHERE groupID = {0} AND published = 1'.format(GroupID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        # Convert binary data to base64 before adding it to the JSON response
        row_dict = dict(zip(row_headers, row))
        if 'uploadedResource' in row_dict:
            row_dict['uploadedResource'] = base64.b64encode(row_dict['uploadedResource']).decode('utf-8')
        json_data.append(row_dict)
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Deletes the given resource
@resources.route('/resources/<resourceID>', methods=['DELETE'])
def delete_resources(resourceID):
    query = 'UPDATE resources set published = 1 WHERE resourceID = ' + str(resourceID)
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return 'Deleted resource!'  

# User posts a resource
@resources.route('/resources/<studyGroupID>/<userID>', methods=['POST'])
def post_resource(studyGroupID, userID):
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    uploadedResource = the_data['uploadedResource']
    
    # Base64 encode the binary data
    uploadedResource_base64 = uploadedResource.encode('utf-8')  # Assuming 'uploadedResource' is a base64-encoded string

    # Constructing the query
    query = 'INSERT INTO resources (uploader, uploadedResource, groupID) values ('
    query += str(userID) + ', '
    query += '%s, '  # Use placeholder for binary data
    query += str(studyGroupID) + ')'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query, (uploadedResource_base64,))  # Pass the base64-encoded data as a parameter
    db.get_db().commit()
    
    return 'Resource uploaded!'