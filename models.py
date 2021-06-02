import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    date = db.Column(db.Date)

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "date": str(self.due_date.strftime('%d-%m-%Y'))
        }
