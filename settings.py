import secrets

class Settings():
    def variables(self):
        """
        Set up variables for database connection, grades, courses, file paths, etc.
        """
        self.DB_USERNAME = "root"  # Database username
        self.DB_PASSWORD = "DEVILO.K@2019"  # Database password
        self.DB_HOST = "127.0.0.1"  # Database host
        self.GRADE_ID = {4:"G4",5:"G5",6:"G6",7:"G7",8:"G8"}  # Mapping of grade levels to grade IDs
        self.GRADE = [4,5,6,7,8]  # List of grade levels
        self.COURSE = [  # List of courses
            "Amharic", "Moral", "General science", "Afanoromo",
            "Science", "Maths", "English", "Ict", "Cte", "Citizen ship",
            "Harari", "Social studies"
        ]
        self.COURSE_ID = {  # Mapping of course names to course IDs
            "Amharic": "a-mharic",
            "Moral": "m-oral",
            "General science": "general-science",
            "Afanoromo": "a-fanoromo",
            "Science": "s-cience",
            "Maths": "m-aths",
            "English": "e-nglish",
            "Ict": "i-ct",
            "Cte": "c-te",
            "Citizen ship": "citizen-ship",
            "Harari": "h-arari",
            "Social studies": "social-studies"
        }
        self.UPLOAD_RESOURCE = "C:\\Users\\hacker\\PycharmProjects\\final\\blueprint\\view\\static\\upload\\resource"  # Path for uploading resources
        self.UPLOAD_PROFILE = "C:\\Users\\hacker\\PycharmProjects\\final\\blueprint\\view\\static\\upload\\profile"  # Path for uploading profiles
        self.DB_NAME = "Development"  # Database name
        self.SECRET_KEY = secrets.token_hex(16)  # Secret key for Flask application
        self.profiles = {  # Mapping of user roles to profile templates
            "student": "student/student_profile.html",
            "teacher": "teacher/teacher_profile.html"
        }
        GENERAL_ID = {  # Mapping of grade ranges to grade IDs
            "Grade4-6": ["G4","G5","G6"],
            "Grade7-8": ["G7","G8"]
        }
        self.COURSE_TAKE = {  # Mapping of courses to grades where they are taught
            "a-mharic": ["G4","G5","G6","G7","G8"],
            "m-oral": ["G4","G5","G6"],
            "general-science": ["G7","G8"],
            "a-fanoromo": ["G4","G5","G6","G7","G8"],
            "s-cience": ["G4","G5","G6"],
            "m-aths": ["G4","G5","G6","G7","G8"],
            "e-nglish": ["G4","G5","G6","G7","G8"],
            "i-ct": ["G4","G5","G6","G7","G8"],
            "c-te": ["G7","G8"],
            "citizen-ship": ["G7","G8"],
            "h-arari": ["G4","G5","G6","G7","G8"],
            "social-studies": ["G7","G8"]
        }
        MAPED_KEY = ["Grade4-6","Grade7-8"]
        self.COURSE_TAKE_BY_GRADE = {  # Mapping of grades to courses they take
            MAPED_KEY[0]: [
                "a-mharic", "a-fanoromo", "s-cience", "m-aths", "e-nglish",
                "i-ct", "h-arari"
            ],
            MAPED_KEY[1]: [
                "a-mharic", "a-fanoromo", "m-aths", "e-nglish", "i-ct",
                "general-science", "c-te", "citizen-ship", "social-studies"
            ]
        }
