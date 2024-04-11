import mysql.connector
from settings import Settings
import datetime

var = Settings()
var.variables()
username = var.DB_USERNAME
DB_name = var.DB_NAME
host = var.DB_HOST
password = var.DB_PASSWORD

db_names = {
        "Development": "development",
        "Testing": "testing",
        "Production": "production"
    }
db_name = db_names[DB_name]

# Function to create the specified database if it doesn't exist
def create_database():
    """
    :return: True if the database creation is successful, otherwise False
    """
    conn = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
    )
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    conn.commit()
    return True

# Function to establish a connection to the database
def connect():
    """
    :return: Connection object if connection is successful, otherwise None
    """
    conn = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=db_name
    )
    return conn
# Function to create all the necessary tables for the project
def create_tables(conn):
    """
    :param conn: Database connection object
    :return: True if table creation is successful, otherwise False
    """
    q = [
    """CREATE TABLE IF NOT EXISTS USER(
        UserID VARCHAR(50) PRIMARY KEY,
        UserName VARCHAR(50),
        UID VARCHAR(50),
        Role VARCHAR(50)
    );""",
    """CREATE TABLE IF NOT EXISTS TEACHER(
        UserID VARCHAR(50),
        GradeID VARCHAR(50),
        CourseID VARCHAR(10),
        FirstName VARCHAR(50),
        LastName VARCHAR(50),
        Speciality VARCHAR(50)
    );""",
    """CREATE TABLE IF NOT EXISTS STUDENT(
        UserID VARCHAR(50),
        ParentID VARCHAR(10),
        SectionID VARCHAR(10),
        FirstName VARCHAR(50),
        LastName VARCHAR(50),
        DateOfBirth DATE
    );""",
    """CREATE TABLE IF NOT EXISTS PARENT(
        ParentID VARCHAR(10) PRIMARY KEY,
        FirstName VARCHAR(50),
        LastName VARCHAR(50),
        PhoneNumber INTEGER
    );""",
    """CREATE TABLE IF NOT EXISTS COURSE(
        CourseID VARCHAR(10) PRIMARY KEY,
        Title VARCHAR(50),
        GradeID VARCHAR(10),
        Description VARCHAR(50)
    );""",
    """CREATE TABLE IF NOT EXISTS ASSESSMENT(
        Test1 INTEGER,
        Test2 INTEGER,
        Assignment1 INTEGER,
        Assignment2 INTEGER,
        Notbook INTEGER,
        Mid INTEGER,
        Final INTEGER,
        StudentID VARCHAR(10),
        TeacherID VARCHAR(10)
    );""",
    """CREATE TABLE IF NOT EXISTS ATTENDANCE(
        TeacherID VARCHAR(10),
        StudentID VARCHAR(10),
        Date DATE,
        Status INTEGER,
        CourseID VARCHAR(10),
        GradeID VARCHAR(10)
    );""",
    """CREATE TABLE IF NOT EXISTS GRADE(
        GradeID VARCHAR(10) PRIMARY KEY,
        TeacherID VARCHAR(10),
        Section VARCHAR(10)
    );""",
    """CREATE TABLE IF NOT EXISTS RESOURCE(
        ResourceID VARCHAR(10) PRIMARY KEY,
        ResourceName VARCHAR(50),
        Description VARCHAR(100),
        GradeID VARCHAR(10)
    );""",
    """CREATE TABLE IF NOT EXISTS SECTION(
        SectionID VARCHAR(10) PRIMARY KEY,
        GradeID VARCHAR(10),
        Section VARCHAR(10)
    );
    """
]
    # Add ALTER TABLE statements for foreign key constraints
    '''alter_statements = [
        """ALTER TABLE TEACHER
           ADD CONSTRAINT fk_teacher_course
           FOREIGN KEY (CourseID) REFERENCES COURSE(CourseID),
           ADD CONSTRAINT fk_teacher_user
           FOREIGN KEY (UserID) REFERENCES USER(UserID)""",
        """ALTER TABLE STUDENT
           ADD CONSTRAINT fk_student_grade
           FOREIGN KEY (SectionID) REFERENCES SECTION(SectionID),
           ADD CONSTRAINT fk_student_user
           FOREIGN KEY (UserID) REFERENCES USER(UserID),
           ADD CONSTRAINT fk_student_parent
           FOREIGN KEY (ParentID) REFERENCES PARENT(ParentID)""",
        """ALTER TABLE COURSE
           ADD CONSTRAINT fk_course_grade
           FOREIGN KEY (GradeID) REFERENCES GRADE(GradeID)""",
        """ALTER TABLE ASSESSMENT
           ADD CONSTRAINT fk_assessment_teacher
           FOREIGN KEY (TeacherID) REFERENCES TEACHER(UserID),
           ADD CONSTRAINT fk_assessment_student
           FOREIGN KEY (StudentID) REFERENCES STUDENT(UserID)""",
        """ALTER TABLE ATTENDANCE
           ADD CONSTRAINT fk_attendance_grade
           FOREIGN KEY (GradeID) REFERENCES GRADE(GradeID),
           ADD CONSTRAINT fk_attendance_course
           FOREIGN KEY (CourseID) REFERENCES COURSE(CourseID),
           ADD CONSTRAINT fk_attendance_teacher
           FOREIGN KEY (TeacherID) REFERENCES TEACHER(UserID),
           ADD CONSTRAINT fk_attendance_student
           FOREIGN KEY (StudentID) REFERENCES STUDENT(UserID);
        """,
        """ALTER TABLE GRADE
           ADD CONSTRAINT fk_grade_teacher
           FOREIGN KEY (TeacherID) REFERENCES TEACHER(UserID)""",
        """ALTER TABLE RESOURCE
           ADD CONSTRAINT fk_resource_grade
           FOREIGN KEY (GradeID) REFERENCES GRADE(GradeID)""",
        """ALTER TABLE SECTION
           ADD CONSTRAINT fk_section_grade
           FOREIGN KEY (GradeID) REFERENCES GRADE(GradeID)"""
    ]'''

    cursor = conn.cursor()
    for query in q:
        cursor.execute(query)
    '''for q in alter_statements:
        cursor.execute(q)'''
    conn.commit()
    cursor.close()

def user(conn,username, uid,ToDo="login"):
    """
    :param conn: Database connection object
    :param username: Username
    :param uid: User ID
    :param ToDo: Operation to perform (default is "login")
    :return: Result of the operation
    """
    cur = conn.cursor()
    if ToDo == "login":
        try:
            cur.execute("SELECT * FROM USER WHERE UserName = %s AND  UID = %s", (username,uid))
            data = cur.fetchall()
            return "[LOGIN] Successful"
        except Exception as e:
            return f"[ERR] {e}"
    elif ToDo == "selectall":
        try:
            cur.execute("SELECT * FROM USER;")
            data = cur.fetchall()
            return data
        except Exception as e:
            return f"[ERROR] {e}"
    elif ToDo == "search":
        try:
            cur.execute("SELECT * FROM USER WHERE UserName = %s AND  UID = %s", (username, uid))
            data = cur.fetchall()
            return data
        except Exception as e:
            return f"[ERROR] {e}"

#fecth info for each table

def Students_info(conn,SearchBy=None,Search=None,flage=True):
    """
    :param conn: Database connection object
    :param SearchBy: Search criteria (default is None)
    :param Search: Search keyword (default is None)
    :param flage: Flag to indicate whether to fetch all students or filtered (default is True)
    :return: Information about students
    """
    cur = conn.cursor()
    if flage:
        try:
            cur.execute("SELECT * FROM STUDENT;")
            info = cur.fetchall()
            return info
        except Exception as e:
            return f"[ERROR] {e}"
    elif not(flage):
        if SearchBy == "geade":
            try:
                cur.execute("SELECT * FROM STUDENT WHERE GradeID = %s;",(Search,))
                info = cur.fetchall()
                return info
            except Exception as e:
                return f"[ERROR] {e}"
        elif SearchBy == "id":
            try:
                cur.execute("SELECT * FROM STUDENT WHERE UserID = %s;",(Search,))
                info = cur.fetchall()
                return info
            except Exception as e:
                return f"[ERROR] {e}"

def Course_info(conn,ID,SearchBy):
    """
    :param conn: Database connection object
    :param SearchBy: Search criteria (default is None)
    :param Search: Search keyword (default is None)
    :param flage: Flag to indicate whether to fetch all students or filtered (default is True)
    :return: Information about students
    """
    cur = conn.cursor()
    try:
        if SearchBy == "Course":
            cur.execute(f"SELECT * FROM COURSE WHERE CourseID = %s;",(ID,))
            info = cur.fetchall()
            return info
        elif SearchBy == "Grade":
            cur.execute(f"SELECT * FROM COURSE WHERE GradeID = %s;",(ID,))
            info = cur.fetchall()
            return info
    except Exception as e:
        return f"[ERROR] {e}"

def Techears_info(conn,SeasrchBy=None,ID=None,flage=True):
    """
    :param conn: Database connection object
    :param SearchBy: Search criteria ("User", "Grade", "Course") (default is None)
    :param ID: User ID, Grade ID, or Course ID (default is None)
    :param flage: Flag to indicate whether to fetch all teachers or filtered (default is True)
    :return: Information about teachers
    """
    cur = conn.cursor()
    if flage:
        try:
            cur.execute("SELECT * FROM TEACHER;")
            info = cur.fetchall()
            return info
        except Exception as e:
            return f"[ERROR] {e}"
    elif not(flage):
        if SearchBy == "User":
            try:
                cur.execute("SELECT * FROM TEACHER WHERE UserID = %s;",(ID,))
                student_info = cur.fetchall()
                return info
            except Exception as e:
                return f"[ERROR] {e}"
        elif SearchBy == "Grade":
            try:
                cur.execute("SELECT * FROM TEACHER WHERE GradeID = %s;",(ID,))
                student_info = cur.fetchall()
                return info
            except Exception as e:
                return f"[ERROR] {e}"
        elif SearchBy == "Course":
            try:
                cur.execute("SELECT * FROM TEACHER WHERE CourseID = %s;",(ID,))
                student_info = cur.fetchall()
                return info
            except Exception as e:
                return f"[ERROR] {e}"

def Parents_info(conn,ID=None,flage=True):
    """
    :param conn: Database connection object
    :param ID: Parent ID (default is None)
    :param flage: Flag to indicate whether to fetch all parents or filtered (default is True)
    :return: Information about parents
    """
    cur = conn.cursor()
    if flage:
        try:
            cur.execute("SELECT * FROM PARENT;")
            info = cur.fetchall()
            return info
        except Exception as e:
            return f"[ERROR] {e}"
    elif not(flage):
        try:
            cur.execute("SELECT * FROM PARENT WHERE ParentID = %s;",(ID,))
            info = cur.fetchall()
            return info
        except Exception as e:
            return f"[ERROR] {e}"

def Assessements_ifo(conn,ID,flage=True,SearchBy="Student"):
    """
    :param conn: Database connection object
    :param ID: Student ID or Teacher ID
    :param flage: Flag to indicate whether to fetch all assessments or filtered (default is True)
    :param SearchBy: Search criteria ("Student" or "Teacher") (default is "Student")
    :return: Information about assessments
    """
    cur = conn.cursor()
    if flage:
        try:
            cur.execute("SELECT * FROM ASSESSMENT;")
            info = cur.fetchall()
            return info
        except Exception as e:
            return f"[ERROR] {e}"
    elif not(flage):
        if SearchBy == "Student":
            try:
                cur.execute("SELECT * FROM ASSESSMENT WHERE StudentID = %s;",(ID,))
                info = cur.fetchall()
                return info
            except Exception as e:
                return f"[ERROR] {e}"
        elif SearchBy == "Teacher":
            try:
                cur.execute("SELECT * FROM ASSESSMENT WHERE TeacherID = %s;",(ID,))
                info = cur.fetchall()
                return info
            except Exception as e:
                return f"[ERROR] {e}"

def Attendace_info(conn,ID,SearchBy="Student",flage=True):
    """
    :param conn: Database connection object
    :param ID: Student ID or Teacher ID
    :param SearchBy: Search criteria ("Student" or "Teacher") (default is "Student")
    :param flage: Flag to indicate whether to fetch all attendance records or filtered (default is True)
    :return: Information about attendance
    """
    cur = conn.cursor()
    if flage:
        try:
            cur.execute("SELECT * FROM ASSESSMENT;")
            info = cur.fetchall()
            return info
        except Exception as e:
            return f"[ERROR] {e}"
    elif not(flage):
        if SearchBy == "Student":
            try:
                cur.execute("SELECT * FROM ATTENDANCE WHERE StudentID = %s;",(ID,))
                info = cur.fetchall()
                return info
            except Exception as e:
                return f"[ERROR] {e}"
        elif SearchBy == "Teacher":
            try:
                cur.execute("SELECT * FROM ATTENDANCE WHERE TeacherID = %s;",(ID,))
                info = cur.fetchall()
                return info
            except Exception as e:
                return f"[ERROR] {e}"

def Grades_info(conn,ID=None,flage=True,SearchBy="student"):
    """
    :param conn: Database connection object
    :param ID: Student ID or Teacher ID (default is None)
    :param flage: Flag to indicate whether to fetch all grades or filtered (default is True)
    :param SearchBy: Search criteria ("student" or "teacher") (default is "student")
    :return: Information about grades
    """
    cur = conn.cursor()
    if flage:
        try:
            cur.execute("SELECT * FROM GRADE;")
            info = cur.fetchall()
            return info
        except Exception as e:
            return f"[ERROR] {e}"
    elif not(flage):
        if SearchBy == "student":
            try:
                cur.execute("SELECT * FROM GRADE WHERE StudentID = %s;",(ID,))
                info = cur.fetchall()
                return info
            except Exception as e:
                return f"[ERROR] {e}"
        elif SearchBy == "teacher":
            try:
                cur.execute("SELECT * FROM GRADE WHERE TeacheID = %s;",(ID,))
                info = cur.fetchall()
                return info
            except Exception as e:
                return f"[ERROR] {e}"

def Resource_info(conn):
    """
    :param conn: Database connection object
    :return: Information about resources
    """
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM RESOURCE;")
        info = cur.fetchall()
        return info
    except Exception as e:
        return f"[ERROR] {e}"
def Section_info(conn,ID,SearchBy):
    """
    :param conn: Database connection object
    :param ID: Section ID or Grade ID
    :param SearchBy: Search criteria ("Section" or "Grade")
    :return: Information about sections
    """
    cur = conn.cursor()

    try:
        if SearchBy == "Section":
            cur.execute(f"SELECT * FROM SECTION WHERE SectionID = %s;",(ID,))
            info = cur.fetchall()
            return info
        elif SearchBy == "Grade":
            cur.execute(f"SELECT * FROM SECTION WHERE GradeID = %s;",(ID,))
            info = cur.fetchall()
            return info
    except Exception as e:
        return f"[ERROR] {e}"

#inserting info into each table
def Insert_User_info(conn,UserID,UserName,UID,Role):
    """
    :param conn: Database connection object
    :param UserID: User ID
    :param UserName: Username
    :param UID: User ID
    :param Role: User role
    :return: True if insertion is successful, otherwise False
    """
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO USER VALUES(%s,%s,%s,%s);",(UserID,UserName,UID,Role))
        conn.commit()
        return True
    except Exception as e:
        return e

def insert_Teacher_info(conn,UserID,CourseID,GradeID,FirstName,LastName,Specialty):
    """
    :param conn: Database connection object
    :param UserID: Teacher's user ID
    :param CourseID: Course ID
    :param GradeID: Grade ID
    :param FirstName: Teacher's first name
    :param LastName: Teacher's last name
    :param Specialty: Teacher's specialty
    :return: True if insertion is successful, otherwise False
    """
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO TEACHER VALUES(%s,%s,%s,%s,%s,%s);",(UserID,CourseID,GradeID,FirstName,LastName,Specialty))
        conn.commit()
        return True
    except Exception as e:
        return e

def insert_student_info(conn,UserID,ParentID,GradeID,FirstName,LastName,DateOfBerth):
    """
    :param conn: Database connection object
    :param UserID: Student's user ID
    :param ParentID: Parent's ID
    :param GradeID: Grade ID
    :param FirstName: Student's first name
    :param LastName: Student's last name
    :param DateOfBirth: Student's date of birth
    :return: True if insertion is successful, otherwise False
    """
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO STUDENT VALUES(%s,%s,%s,%s,%s,%s);",(UserID,ParentID,GradeID,FirstName,LastName,DateOfBerth))
        conn.commit()
        return True
    except Exception as e:
        return False

def insert_parent_info(conn,UserID,FirstName,LastName,PhoneNumber):
    """
    :param conn: Database connection object
    :param UserID: Parent's user ID
    :param FirstName: Parent's first name
    :param LastName: Parent's last name
    :param PhoneNumber: Parent's phone number
    :return: True if insertion is successful, otherwise False
    """
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO PARENT VALUES(%s,%s,%s,%s);",(UserID,FirstName,LastName,PhoneNumber))
        conn.commit()
        return True
    except Exception as e:
        return False
def insert_course_info(conn,CourseID,Title,GradeID,Description):
    """
    :param conn: Database connection object
    :param CourseID: Course ID
    :param Title: Course title
    :param GradeID: Grade ID
    :param Description: Course description
    :return: True if insertion is successful, otherwise False
    """
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO COURSE VALUES(%s,%s,%s,%s);",(CorseID,Title,GradeID,Description))
        conn.commit()
        return True
    except Exception as e:
        return False

def insert_assessment_info(conn,Test1,Test2,Assigment1,Assigment2,NoteBook,StudentID,TeacherID):
    """
    :param conn: Database connection object
    :param Test1: Test 1 score
    :param Test2: Test 2 score
    :param Assignment1: Assignment 1 score
    :param Assignment2: Assignment 2 score
    :param Notebook: Notebook score
    :param StudentID: Student's ID
    :param TeacherID: Teacher's ID
    :return: True if insertion is successful, otherwise False
    """
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO ASSESSMENT VALUES(%s,%s,%s,%s,%s,%s,%s);",(Test1,Test2,Assigment1,Assigment2,NoteBook,StudentID,TeacherID))
        conn.commit()
        return True
    except Exception as e:
        return False

def insert_attendance_info(conn,TeacherID,StudentID,Status,GradeID):
    """
    :param conn: Database connection object
    :param TeacherID: Teacher's ID
    :param StudentID: Student's ID
    :param Status: Attendance status
    :param GradeID: Grade ID
    :return: True if insertion is successful, otherwise False
    """
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO ATTENDANCE VALUES(%s,%s,%s,%s);",(TeacherID,StudentID,Status,GradeID))
        conn.commit()
        return True
    except Exception as e:
        return False

def insert_Grade_info(conn,GradeID,TeacherID,Section):
    """
    :param conn: Database connection object
    :param TeacherID: Teacher's ID
    :param StudentID: Student's ID
    :param Status: Attendance status
    :param GradeID: Grade ID
    :return: True if insertion is successful, otherwise False
    """
    cur = conn.coursor()
    try:
        cur.execute("INSERT INTO COURSE VALUES(%s,%s,%s,);",(GradeID,TeacherID,Section))
        conn.commit()
        return True
    except Exception as e:
        return False

def insert_Resource_info(conn,ResourseID,ResoureName,Description,GradeID):
    """
    :param conn: Database connection object
    :param ResourceID: Resource ID
    :param ResourceName: Resource name
    :param Description: Resource description
    :param GradeID: Grade ID
    :return: True if insertion is successful, otherwise False
    """
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO USER VALUES(%s,%s,%s,%s);",(ResourceID,ResourceName,Description,GradeID))
        conn.commit()
        return True
    except Exception as e:
        return False

#update section qurey = UPDATE TABLENAME SET Update = %s  WHERE ID = %s

def updet(conn,Update,table,UpdateBy,ID):
    """
    :param conn: Database connection object
    :param Update: Field to update
    :param table: Table name
    :param UpdateBy: Value to update
    :param ID: ID of the record to update
    :return: True if update is successful, otherwise False
    """
    cur = conn.cursor()
    try:
        if table == "user":
            _ID = "UserID"
            table = "Table"
        elif table == "teacher":
            _ID = "UserID"
            table = "TEACHER"
        elif table == "student":
            _ID = "UserID"
            table = "STUDENT"
        elif table == "parent":
            _ID = "ParentID"
            table = "PARENT"
        elif table == "Course":
            _ID = "CourseID"
            table = "COURSE"
        elif table == "assessment":
            _ID = "StudentID"
            table = "ASSESSMENT"
        elif table == "attendance":
            _ID = "StudentID"
            table = "ATTENDANCE"
        elif table == "grade":
            _ID = "GradeID"
            table = "GRADE"
        query = f"UPDATE {table} SET {update} = %s WHERE {_ID} = %s;"
        cur.execute(query,(UpdateBy,ID))
        conn.commit()
        return True
    except Exception as e:
        return False
#delete section

def delete(conn,table,ID):
    """
    :param conn: Database connection object
    :param table: Table name
    :param ID: ID of the record to delete
    :return: True if deletion is successful, otherwise False
    """
    cur = conn.cursor()
    try:
        if table == "user":
            _ID = "UserID"
            table = "Table"
        elif table == "teacher":
            _ID = "UserID"
            table = "TEACHER"
        elif table == "student":
            _ID = "UserID"
            table = "STUDENT"
        elif table == "parent":
            _ID = "ParentID"
            table = "PARENT"
        elif table == "Course":
            _ID = "CourseID"
            table = "COURSE"
        elif table == "assessment":
            _ID = "StudentID"
            table = "ASSESSMENT"
        elif table == "attendance":
            _ID = "StudentID"
            table = "ATTENDANCE"
        elif table == "grade":
            _ID = "GradeID"
            table = "GRADE"
        query = f"DELETE FROM {table} WHERE {_ID} = %s;"
        cur.execute(query,(ID,))
        conn.commit()
        return True
    except Exception as e:
        return False

