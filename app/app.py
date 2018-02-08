import logging
import os
import re

from flask import Flask, render_template, request, redirect, url_for, abort

from app.utils import *

logging.basicConfig(format="%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s",
                    level=logging.INFO)

app = Flask(__name__, template_folder="templates", static_url_path="/static", static_folder="static")
app.secret_key = os.urandom(32)
app.add_template_filter(prepare_text)
app.add_template_filter(priority_as_str)
app.add_template_filter(status_as_str)


_theme = get_property("theme")
if not _theme or _theme not in themes:
    _theme = Theme.LIGHT


@app.route('/')
def index():
    return render_template('task/list.html', tasks=get_all_tasks(), tags=get_all_tags(), statuses=statuses,
                           priorities=priorities, theme=_theme, themes=themes, Status=Status)


@app.route('/tasks/tag/<tag_name>')
def tasks_by_tag(tag_name: str):
    tag = get_tag_by_name(tag_name)
    if not tag:
        abort(404)
    return render_template('task/list.html', tasks=get_tasks_by_tag(tag), tags=get_all_tags(), statuses=statuses,
                           priorities=priorities, tag=tag, theme=_theme, themes=themes, Status=Status)


@app.route('/tasks/search', methods=['GET', 'POST'])
def task_search():
    query = ""
    tasks = []
    if request.method == 'POST':
        query = strip_html_tags(request.form.get("query"))
        if query:
            tasks = search_tasks(query)
    return render_template('task/list.html', tasks=tasks, tags=get_all_tags(), statuses=statuses,
                           priorities=priorities, query=query, theme=_theme, themes=themes, Status=Status)


@app.route('/tasks/new', methods=["POST"])
def new_task():
    title = strip_html_tags(request.form.get("title"))
    description = strip_html_tags(request.form.get("description"))
    priority = Priority.NORMAL.value
    tags = extract_tags(strip_html_tags(request.form.get("tags")))
    if title:
        task = Task.create(title=title, description=description, status=Status.TODO.value, priority=priority,
                           status_changed=utc_timestamp())
        for tag in tags:
            TaskTag.create(task=task, tag=tag)
    return redirect(url_for('index'))


@app.route('/tasks/<int:id>/edit', methods=["POST"])
def edit_task(id: int):
    task = get_task_by_id(id)
    if task:
        title = strip_html_tags(request.form.get("title"))
        description = strip_html_tags(request.form.get("description"))
        tags = extract_tags(strip_html_tags(request.form.get("tags")))
        if title:
            task.title = title
            task.description = description
            task.save()
            delete_task_tags(task)
            for tag in tags:
                TaskTag.create(task=task, tag=tag)
            return redirect(url_for('task', id=task.id))
        else:
            return redirect(url_for('index'))


@app.route('/tasks/<int:id>')
def task(id: int):
    task = get_task_by_id(id)
    if not task:
        abort(404)
    return render_template("task/one.html", task=task, tags=get_all_tags(), statuses=statuses, priorities=priorities,
                           theme=_theme, themes=themes)


@app.route('/tasks/<int:id>/add-comment', methods=["POST"])
def add_comment_to_task(id: int):
    task = get_task_by_id(id)
    if task:
        content = strip_html_tags(request.form.get("content"))
        if content:
            Comment.create(task=task, content=content, time=utc_timestamp())
    return redirect(url_for('task', id=id))


@app.route('/tasks/<int:id>/set-status/<int:status>')
def set_task_status(id: int, status: int):
    task = get_task_by_id(id)
    if task and status in [s.value for s in statuses]:
        task.status = status
        task.status_changed = utc_timestamp()
        task.save()
    return redirect(request.referrer)


@app.route('/tasks/<int:id>/set-priority/<int:priority>')
def set_task_priority(id: int, priority: int):
    task = get_task_by_id(id)
    if task and priority in [p.value for p in priorities]:
        task.priority = priority
        task.status_changed = utc_timestamp()
        task.save()
    return redirect(request.referrer)


@app.route('/set-theme/<theme>')
def set_theme(theme: str):
    global _theme
    if theme in themes:
        _theme = theme
        set_property("theme", theme)
    return redirect(request.referrer)


@app.route('/comments/<int:id>/delete')
def delete_comment(id: int):
    comment = get_comment_by_id(id)
    if comment:
        delete_comment_by_id(id)
    return redirect(request.referrer)


@app.route('/tasks/<int:id>/delete', methods=["POST"])
def delete_task(id: int):
    task = get_task_by_id(id)
    if task:
        delete_task_tags(task)
        delete_task_by_id(id)
    return redirect(url_for('index'))


@app.route('/tasks/<int:id>/archive', methods=["POST"])
def archive_task(id: int):
    task = get_task_by_id(id)
    if task:
        task.archived = True
        task.save()
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html', theme=_theme, themes=themes), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('error/500.html', theme=_theme, themes=themes), 500



