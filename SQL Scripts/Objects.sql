CREATE SCHEMA MASTER.STUDYBUDDY;

CREATE TABLE STUDYBUDDY.Users (
    user_id INT PRIMARY KEY IDENTITY(1,1) NOT NULL,
    username NVARCHAR(50) NOT NULL,
    password NVARCHAR(100) NOT NULL,
    email NVARCHAR(100),
    school NVARCHAR(100),
    role NVARCHAR(100) NOT NULL
);

CREATE TABLE master.STUDYBUDDY.Classes (
	class_id int IDENTITY(1,1) NOT NULL,
	teacher_id int NULL,
	class_name nvarchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	class_code nvarchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	CONSTRAINT PK__Classes__FDF47986125F76E0 PRIMARY KEY (class_id)
);

CREATE TABLE master.STUDYBUDDY.StudentClass (
    student_class_id INT PRIMARY KEY IDENTITY(1,1) NOT NULL,
    user_id INT NOT NULL,
    class_id INT NOT NULL,
    CONSTRAINT FK_StudentClass_User FOREIGN KEY (user_id) REFERENCES STUDYBUDDY.Users(user_id),
    CONSTRAINT FK_StudentClass_Class FOREIGN KEY (class_id) REFERENCES master.STUDYBUDDY.Classes(class_id)
);

CREATE TABLE STUDYBUDDY.FAQs (
    faq_id INT PRIMARY KEY IDENTITY(1,1) NOT NULL,
    question NVARCHAR(1000) NOT NULL,
    answer NVARCHAR(1000),
    class_id INT NOT NULL,
    user_id INT NOT NULL,
    CONSTRAINT FK_FAQs_Class FOREIGN KEY (class_id) REFERENCES master.STUDYBUDDY.Classes(class_id),
    CONSTRAINT FK_FAQs_User FOREIGN KEY (user_id) REFERENCES STUDYBUDDY.Users(user_id)
);
