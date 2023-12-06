from flask import Blueprint, request, jsonify, make_response
import json
from src import db


studyGroups = Blueprint('studyGroups', __name__)

# Get all customers from the DB
@studyGroups.route('/StudyGroups', methods=['GET'])
def get_studyGroups():
    cursor = db.get_db().cursor()
    cursor.execute('select groupID, groupName, subjectName,\
        goal, capacity, enrollment, meetingTime, organizer, firstName, lastName from studyGroup join subjects on studySubject = subjectID join user on organizer = userID')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@studyGroups.route('/StudyGroups', methods=['POST'])
def add_new_studyGroup():
    
    # collecting data from the request object 
    the_data = request.json
    #current_app.logger.info(the_data)

    #(studySubject, organizer, groupName, meetingTime, capacity, enrollment, goal)
    #extracting the variable
    studySubject = the_data['studySubject']
    organizer = the_data['organizer']
    groupName = the_data['groupName']
    meetingTime = the_data['meetingTime']
    capacity = the_data['capacity']
    enrollment = the_data['enrollment']
    goal = the_data['goal']


    # Constructing the query
    query = 'insert into studyGroup (studySubject, organizer, groupName, meetingTime, capacity, enrollment, goal) values ('
    query += studySubject + ', '
    query += organizer + ', "'
    query += groupName + '", "'
    query += meetingTime + '", '
    query += capacity + ', '
    query += enrollment + ', "'
    query += goal + '")'
    #current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'





@studyGroups.route('/StudyGroups/<id>', methods=['GET'])
def get_studyGroups_details(id):

    query = 'select groupName, subjectName,\
        goal, capacity, enrollment, meetingTime, organizer, firstName, lastName from studyGroup join subjects on studySubject = subjectID join user on organizer = userID where groupID = ' + str(id)
    #current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)



@studyGroups.route('/StudyGroups/<id>', methods=['DELETE'])
def delete_studyGroup_byId(id):

    query = 'DELETE FROM studyGroup WHERE groupID = ' + str(id)
    #current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return 'Success!'




@studyGroups.route('/StudyGroups/<id>/<date>/<userId>', methods=['POST'])
def set_attendance_for(id,date,userId):    
    # collecting data from the request object 


    #(userID, groupID, sessionDate, attended)
    


    # Constructing the query
    query = 'insert into attendance (userID, groupID, sessionDate, attended) values ('
    query += userId + ', '
    query += id + ', "'
    query += date + '", '
    query += str(1) + ')'
    #current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'    


@studyGroups.route('/StudyGroups/<id>/<date>', methods=['GET'])
def get_attendance_details(id, date):

    query = 'SELECT user.userID, firstName, lastName, studyGroup.groupID, groupName, subjectName, sessionDate,\
        attended FROM attendance join user on attendance.userID = user.userID join studyGroup on attendance.groupID = studyGroup.groupID join subjects on studySubject = subjectID WHERE attendance.groupID = ' + str(id) + ' AND attendance.sessionDate = \'' + str(date).replace("%20", " ") + '\''  #DATETIME(' + ');'
    #current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)    