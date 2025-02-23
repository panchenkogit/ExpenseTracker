from pydantic import BaseModel, EmailStr

class EmailReminder(BaseModel):
    email: EmailStr
    sub_title: str
    frequency_id: int = 3  # Default to monthly frequency

    def to_dict(self) -> dict:
        return {
            "email": self.email,
            "sub_title": self.sub_title,
            "frequency_id": self.frequency_id
        }
    
    @property
    def theme(self) -> str:
        return f"Subscription Reminder - {self.sub_title}"

    @property
    def message(self) -> str:
        return f"Hello! You have a subscription reminder. Payment for {self.sub_title} is in the next 3 days."

    def __hash__(self):
        return hash((self.email, self.sub_title))

    def __eq__(self, other):
        return isinstance(other, EmailReminder) and self.email == other.email and self.sub_title == other.sub_title
