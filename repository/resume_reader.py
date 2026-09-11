from utils.file_system_reader import FileSystemReader


class ResumeReader:
    def __init__(self):
        self.file_name = "resume.json"
        self.resume = self._read_resume(self.file_name)
        
    
    def get_name(self):
        return self.resume.get("name")
    
    def get_alias(self):
        return self.resume.get("alias")
    
    def get_email(self):
        return self.resume.get("primaryEmail")
    
    def get_contact(self):
        return self.resume.get("contact")
    
    def get_github(self):
        return self.resume.get("github")
    
    def get_linkedin(self):
        return self.resume.get("linkedin")
    def get_location(self):
        return self.resume.get("location")
    
    def get_aboutMe(self):
        return self.resume.get("aboutMe")
    
    def get_demos(self, demo_type):

        demos = self.resume.get(
            "demos",
            []
        )

        if not demos:
            return []

        categories = demos[0].get(
            "categories",
            []
        )

        for category in categories:

            if category.get("key") == demo_type:
                return category.get(
                    "projects",
                    []
                )

        return []
    
    def get_education(self):
        return self.resume.get("education",[])
    
    def get_work_experience(self, work_type):

        work_experience = self.resume.get(
            "workExperience",
            []
        )

        if not work_experience:
            return []

        result = []

        for work in work_experience:

            if work.get("type") == work_type:
                result.append(work)

        return result       
        
    def _read_resume(self, file_name):
        reader = FileSystemReader(file_name)
        result = reader.read_file()
        if not result:
            raise ValueError("Resume is Null")
        
        return result
        
    