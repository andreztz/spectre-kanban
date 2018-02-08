from app.model import *


# account propertis


def set_property(key: str, value: str):
    try:
        prop = Property.select().where(Property.key == key).get()
        prop.value = value
        prop.save()
    except DoesNotExist:
        Property.create(key=key, value=value)


def get_property(key: str):
    try:
        return Property.select().where(Property.key == key).get().value
    except DoesNotExist:
        return None


# tasks


def get_all_tasks():
    return Task.select()\
        .where(Task.archived == False) \
        .order_by(Task.priority.desc(), Task.status_changed.desc())\
        .execute()


def get_tasks_by_tag(tag: Tag):
    return Task.select(Task, TaskTag)\
        .join(TaskTag).where(TaskTag.tag == tag) \
        .where(Task.archived == False) \
        .order_by(Task.priority.desc(), Task.status_changed.desc())\
        .execute()


def search_tasks(query: str):
    return Task\
        .select() \
        .where(Task.title.contains(query) | Task.description.contains(query)) \
        .order_by(Task.priority.desc(), Task.status_changed.desc())\
        .execute()


def get_task_by_id(id: int):
    try:
        return Task.select().where(Task.id == id).get()
    except DoesNotExist:
        return None


def delete_task_by_id(id: int):
    Task.delete().where(Task.id == id).execute()


# tags


def get_all_tags():
    return Tag.select() \
        .order_by(Tag.name) \
        .execute()


def get_tag_by_name(name: str):
    try:
        return Tag.select().where(Tag.name == name).get()
    except DoesNotExist:
        return None


def delete_task_tags(task: Task):
    TaskTag.delete().where(TaskTag.task == task).execute()


# comments


def get_comment_by_id(id: int):
    try:
        return Comment.select().where(Comment.id == id).get()
    except DoesNotExist:
        return None


def delete_comment_by_id(id: int):
    Comment.delete().where(Comment.id == id).execute()