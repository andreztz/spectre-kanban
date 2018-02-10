Spectre-Kanban
---
It's basic kanban-like board based on flask + spectre.css for single user. This project oriented to two points: 

* Minimal usage of additional techologies. You don't need mongo/redis/bower/gulp/webpack/npm or something similar to start using it.
* Minimal usage of javascript. Right now javascript is not used at all. But I think that this will be done in the future.

Well, if you like it, let's go.

Dependencies
---
It requires Python 3.4+ and packgages from the requeirements.txt file.

Installation
---
Run this commands in your terminal:
```
sudo apt-get update
sudo apt-get install virtualenv
git clone https://github.com/oqwa/spectre-kanban.git
cd spectre-kanban
cp app/data/settings.example.py app/data/settings.py
mkvirtualenv spectre-kanban
pip install -r requirements.txt
python reset.py
python run.py
```
And open your web browser in the address http://127.0.0.1:8000. If the port already in use you can change it in:
```
app/data/settings.py
``` 
There you can also:
 * change path to the sqlite file
 * switch to https mode

Feedback
---
Bug reports, feature requests, pull requests, any feedback, etc. are welcome. 