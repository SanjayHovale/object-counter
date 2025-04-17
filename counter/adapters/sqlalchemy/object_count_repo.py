from counter.adapters.sqlalchemy.models import ObjectCount
from counter.adapters.sqlalchemy.db import SessionLocal  # Use the session from db.py

class ObjectCountRepo:
    def __init__(self):
        self.session = SessionLocal()

    def save_object_count(self, object_type, count):
        object_count = ObjectCount(object_type=object_type, count=count)
        self.session.add(object_count)
        self.session.commit()

    def get_all_counts(self):
        return self.session.query(ObjectCount).all()

    def get_count_by_id(self, count_id):
        return self.session.query(ObjectCount).filter_by(id=count_id).first()

# Example Usage
if __name__ == "__main__":
    repo = ObjectCountRepo()

    # Save an object count
    repo.save_object_count("example_object", 5)

    # Fetch all object counts
    counts = repo.get_all_counts()
    for count in counts:
        print(count)
