from enum import Enum

from peewee import *

from app.data.settings import *


class Theme:
    LIGHT = "light"
    NIGHT = "night"


class Status(Enum):
    TODO = 1
    DOING = 2
    DONE = 3


class Priority(Enum):
    HIGH = 3
    NORMAL = 2
    LOW = 1


statuses = [
    Status.TODO,
    Status.DOING,
    Status.DONE
]

priorities = [
    Priority.LOW,
    Priority.NORMAL,
    Priority.HIGH
]

themes = [
    Theme.LIGHT,
    Theme.NIGHT
]

db = SqliteDatabase(SQLITE_FILE)


class Task(Model):
    class Meta:
        database = db
        db_table = "tasks"
    title = CharField()
    description = TextField(null=True)
    priority = SmallIntegerField()
    status = SmallIntegerField()
    status_changed = IntegerField()
    archived = BooleanField(default=False)


class Comment(Model):
    class Meta:
        database = db
        db_table = "comments"
    task = ForeignKeyField(Task, related_name="comments")
    content = TextField()
    time = IntegerField()


class Tag(Model):
    class Meta:
        database = db
        db_table = "tags"
    name = CharField(unique=True)


class TaskTag(Model):
    class Meta:
        database = db
        db_table = "tasks_tags"
        primary_key = False
    task = ForeignKeyField(Task, related_name="tags")
    tag = ForeignKeyField(Tag, related_name="tasks")


class Property(Model):
    class Meta:
        database = db
        db_table = "properties"
        primary_key = CompositeKey('key')
    key = CharField()
    value = CharField()


def reset():
    tables = [Task, Comment, Tag, TaskTag, Property]
    db.drop_tables(tables, safe=True)
    db.create_tables(tables, safe=True)
