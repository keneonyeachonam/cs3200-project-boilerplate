-- This file is to bootstrap a database for the CS3200 project.
-- Create a new database.  You can change the name later.  You'll
-- need this name in the FLASK API file(s),  the AppSmith
-- data source creation.
create database virtualStudyGroupOrganizer_db;


-- Via the Docker Compose file, a special user called webapp will
-- be created in MySQL. We are going to grant that user
-- all privilages to the new database we just created.
-- TODO: If you changed the name of the database above, you need
-- to change it here too.
-- grant all privileges on virtualStudyGroupOrganizer_db.* to 'webapp' @ '%';
-- flush privileges;

-- Move into the database we just created.
-- TODO: If you changed the name of the database above, you need to
-- change it here too.
use virtualStudyGroupOrganizer_db;

-- OUR DDL



CREATE TABLE IF NOT EXISTS moderator  (
  moderatorID int PRIMARY KEY AUTO_INCREMENT,
  firstName varchar(50) NOT NULL,
  lastName varchar(50) NOT NULL
);


CREATE TABLE IF NOT EXISTS subjects (
  subjectID int PRIMARY KEY AUTO_INCREMENT,
  subjectName varchar(50) NOT NULL
);

-- user table
CREATE TABLE IF NOT EXISTS user (
  userID int PRIMARY KEY AUTO_INCREMENT,
  firstName varchar(50) NOT NULL,
  lastName varchar(50) NOT NULL,
  userYear int,
  major varchar(100),
  banned boolean NOT NULL DEFAULT 0,
  moderatorID int,
  preferredSubject int,
  FOREIGN KEY (moderatorID) REFERENCES moderator (moderatorID) ON UPDATE cascade ON DELETE restrict,
  FOREIGN KEY (preferredSubject) REFERENCES subjects (subjectID) ON UPDATE cascade ON DELETE cascade
);


-- messages board table
CREATE TABLE IF NOT EXISTS messageBoard (
    messageBoardID int PRIMARY KEY AUTO_INCREMENT,
    boardName varchar(50) NOT NULL,
    banned boolean NOT NULL DEFAULT 0,
    moderatorID int,
    FOREIGN KEY (moderatorID) REFERENCES moderator (moderatorID) ON UPDATE cascade ON DELETE restrict
);

-- messages table
CREATE TABLE IF NOT EXISTS messages (
  messageID int PRIMARY KEY AUTO_INCREMENT,
  author int NOT NULL,
  replyToID int,
  messageBoardID int NOT NULL,
  publishTime datetime DEFAULT CURRENT_TIMESTAMP,
  content text,
  published boolean DEFAULT 1,
  moderatorID int,
  FOREIGN KEY (author) REFERENCES user (userID) ON UPDATE cascade ON DELETE cascade,
  FOREIGN KEY (replyToID) REFERENCES messages (messageID) ON UPDATE cascade ON DELETE cascade,
  FOREIGN KEY (messageBoardID) REFERENCES messageBoard (messageBoardID) ON UPDATE cascade ON DELETE cascade,
  FOREIGN KEY (moderatorID) REFERENCES moderator (moderatorID) ON UPDATE cascade ON DELETE restrict
);

-- report table
CREATE TABLE IF NOT EXISTS report (
  authorID int NOT NULL,
  reporteeID int NOT NULL,
  reportedMessage int NOT NULL,
  reasoning text NOT NULL,
  resolved boolean NOT NULL DEFAULT 0,
  moderatorID int,
  PRIMARY KEY(authorID, reporteeID, reportedMessage),
  FOREIGN KEY (authorID) REFERENCES user (userID) ON UPDATE cascade ON DELETE restrict,
  FOREIGN KEY (reporteeID) REFERENCES user (userID) ON UPDATE cascade ON DELETE restrict,
  FOREIGN KEY (reportedMessage) REFERENCES messages (messageID) ON UPDATE restrict ON DELETE restrict,
  FOREIGN KEY (moderatorID) REFERENCES moderator (moderatorID) ON UPDATE cascade ON DELETE cascade
);

-- bookmark table
CREATE TABLE IF NOT EXISTS bookmark (
  userID int NOT NULL,
  messageBoardID int NOT NULL,
  PRIMARY KEY (userID, messageBoardID),
  FOREIGN KEY (userID) REFERENCES user (userID) ON UPDATE cascade ON DELETE cascade,
  FOREIGN KEY (messageBoardID) REFERENCES messageBoard (messageBoardID) ON UPDATE cascade ON DELETE cascade
);

CREATE TABLE IF NOT EXISTS studyGroup (
  groupID int PRIMARY KEY AUTO_INCREMENT,
  studySubject int NOT NULL,
  organizer int NOT NULL,
  groupName varchar(50) NOT NULL,
  meetingTime datetime,
  capacity int NOT NULL,
  enrollment int DEFAULT 0,
  goal text NOT NULL,
  moderatorID int,
  FOREIGN KEY (studySubject) REFERENCES subjects (subjectID) ON UPDATE cascade ON DELETE cascade,
  FOREIGN KEY (organizer) REFERENCES user (userID) ON UPDATE cascade ON DELETE cascade,
  FOREIGN KEY (moderatorID) REFERENCES moderator (moderatorID) ON UPDATE cascade ON DELETE restrict
);



CREATE TABLE IF NOT EXISTS attendance (
  userID int NOT NULL,
  groupID int NOT NULL,
  sessionDate DATETIME NOT NULL,
  attended boolean NOT NULL,
  PRIMARY KEY(userID, groupID, sessionDate),
  FOREIGN KEY (userID) REFERENCES user (userID) ON UPDATE cascade ON DELETE cascade,
  FOREIGN KEY (groupID) REFERENCES studyGroup (groupID) ON UPDATE cascade ON DELETE cascade
);






CREATE TABLE IF NOT EXISTS review (
  reviewID int PRIMARY KEY AUTO_INCREMENT,
  groupID int NOT NULL,
  author int NOT NULL,
  review text,
  rating int NOT NULL CHECK (rating >= 1 AND rating <= 5),
  FOREIGN KEY (groupID) REFERENCES studyGroup (groupID) ON UPDATE cascade ON DELETE cascade,
  FOREIGN KEY (author) REFERENCES user (userID) ON UPDATE cascade ON DELETE cascade
);

CREATE TABLE IF NOT EXISTS resources (
  resourceID int PRIMARY KEY AUTO_INCREMENT,
  uploader int NOT NULL,
  uploadDateTime datetime DEFAULT CURRENT_TIMESTAMP,
  uploadedResource blob NOT NULL,
  published boolean NOT NULL DEFAULT 1,
  groupID int NOT NULL,
  moderatorID int,
  FOREIGN KEY (uploader) REFERENCES user (userID) ON UPDATE cascade ON DELETE cascade,
  FOREIGN KEY (groupID) REFERENCES studyGroup (groupID) ON UPDATE cascade ON DELETE cascade
);


CREATE TABLE IF NOT EXISTS userInGroup (
  userID int NOT NULL,
  groupID int NOT NULL,
  PRIMARY KEY (userID, groupID),
  FOREIGN KEY (userID) REFERENCES user (userID) ON UPDATE cascade ON DELETE cascade,
  FOREIGN KEY (groupID) REFERENCES studyGroup (groupID) ON UPDATE cascade ON DELETE cascade
);

-- Sample Data

-- Inserting into the 'subjects' table
INSERT INTO subjects (subjectName)
VALUES ('Database Design'),
       ('Differential Equations'),
       ('Cornerstone of Engineering');

-- Inserting into the 'user' table
INSERT INTO user (firstName, lastName, userYear, major, preferredSubject)
VALUES ('John', 'Doe', '2023', 'Computer Science', 1),
       ('Alice', 'Smith', '2022', 'Engineering', 3),
       ('Bob', 'Johnson', '2023', 'Mathematics', 2);

-- Inserting into the 'studyGroup' table
INSERT INTO studyGroup (studySubject, organizer, groupName, meetingTime, capacity, enrollment, goal)
VALUES (1, 1, 'Programming Enthusiasts', '2023-01-01 18:00:00', 20, 10, 'Learn and discuss programming'),
       (2, 2, 'Math Study Group', '2023-01-05 15:30:00', 15, 8, 'Excel in advanced calculus'),
       (3, 3, 'Engineering Club', '2023-01-10 17:00:00', 25, 15, 'Explore various engineering topics');

-- Inserting into the 'attendance' table
INSERT INTO attendance (userID, groupID, sessionDate, attended)
VALUES (1, 1, '2023-01-01 18:00:00', 1),
       (2, 2, '2023-01-05 15:30:00', 1),
       (3, 3, '2023-01-10 17:00:00', 0);


-- Inserting into the 'review' table
INSERT INTO review (groupID, author, review, rating)
VALUES (1, 1, 'Great group for learning programming!', 5),
       (2, 2, 'Helpful study sessions for math lovers', 4),
       (3, 3, 'Enjoyable discussions about engineering projects', 5);

-- Inserting into the 'resources' table
INSERT INTO resources (uploader, uploadedResource, groupID)
VALUES (1, 'Introduction to Databases', 1),
       (2, 'Advanced Calculus Notes', 2),
       (3, 'Engineering Project Guidelines', 3);

-- Inserting into the 'messageBoard' table
INSERT INTO messageBoard (boardName)
VALUES ('General Discussion'),
       ('Programming Help'),
       ('Science Talks');


-- Inserting into the 'messages' table
INSERT INTO messages (author, replyToID, messageBoardID, publishTime, content, published)
VALUES (2, NULL, 2, '2023-01-01 08:00:00', 'Anybody needs help with programming?', 1),
       (3, NULL, 3, '2023-01-01 08:00:00', 'Let us discuss interesting engineering projects!', 1),
       (2, 1, 1, '2023-01-01 08:00:00', 'Sure, John!', 1),
       (3, 2, 2, '2023-01-01 08:00:00', 'I am struggling with calculus. Can anyone help?', 1),
       (1, 3, 3, '2023-01-01 08:00:00', 'I have a biology-related question. Anyone familiar?', 1);

-- Inserting into the 'bookmark' table
INSERT INTO bookmark (userID, messageBoardID)
VALUES (1, 1),
       (2, 2),
       (3, 3);

-- Inserting into the 'moderator' table
INSERT INTO moderator (firstName, lastName)
VALUES ('Moderator1', 'Smith'),
       ('Moderator2', 'Johnson'),
       ('Moderator3', 'Doe');

-- Inserting into the 'userInGroup' table
INSERT INTO userInGroup (userID, groupID)
VALUES (1, 1),
       (2, 2),
       (3, 3);

-- Inserting into the 'report' table
INSERT INTO report (authorID, reporteeID, reportedMessage, reasoning)
VALUES (1, 2, 5, 'Inappropriate content'),
       (2, 3, 2, 'Spamming the board'),
       (3, 1, 3, 'Disrespectful behavior');