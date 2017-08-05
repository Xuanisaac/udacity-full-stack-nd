from item_database_config import Category
from database_operations import DatabaseOperations

# Modified from https://github.com/aaronharmon/Item-Catalog
db = DatabaseOperations()
new_categories = [Category(name='Soccer'),
                  Category(name='Baseball'),
                  Category(name='Football'),
                  Category(name='Badminton'),
                  Category(name='Archery'),
                  Category(name='Bobsleigh'),
                  Category(name='Boxing')]
for new_category in new_categories:
    db.addToDatabase(new_category)
