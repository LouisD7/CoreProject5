from pydantic import BaseModel, Field

class patient_item(BaseModel):
    #Data class for validating patient data
    patientID: int
    Age: int
    first_name: str
    Gender: str
    general_practice: str
    home_address: str
    last_name: str
    phone_number: str
    GP_notes: dict[str,str] = Field(default_factory=dict)

    def __post_init__(self):
        #Validate inputs
        self.validate_patientID()
        self.validate_age()
        self.validate_name()
        self.validate_gender()
        self.validate_phone_number()

    
    def validate_patientID(self):
        #validate patient ID
        if len(str(self.patientID)) != 6:
            raise ValueError(f'patientID {self.patientID} is invalid format')
        
    
    def validate_age(self):
        if self.Age < 0 or self.Age > 200:
            raise ValueError(f'Age {self.Age} is invalid not within valid age range')
        
    
    def validate_name(self):
        if any(char.isdigit() for char in self.first_name) is True:
            raise ValueError(f'first name {self.first_name} is invalid contains numeric characters')
        if any(char.isdigit() for char in self.last_name) is True:
            raise ValueError(f'last name {self.last_name} is invalid contains numeric characters')
        
    
    def validate_gender(self):
        if len(self.Gender) > 15 or self.Gender is "":
            raise ValueError(f'Gender {self.Gender} is invalid too long')
        
    
    def validate_phone_number(self):
        if self.phone_number.startswith("+") is False:
            raise ValueError(f'Phone number {self.phone_number} is invalid missing area code')
        if self.phone_number.replace("+", "").isnumeric() is False:
            raise ValueError(f'Phone number {self.phone_number} contains non numeric chars')
        