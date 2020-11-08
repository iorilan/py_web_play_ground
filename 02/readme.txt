*python 3.7
pip install flask
pip install flask_sqlalchemy
pip install sqlalchemy

*Description
A CRUD sample to start with flask web service + mysql with python
"create" POST
"update/<id>" PUT
"delete/<id>" DELETE
"search" POST 
{
    "operation": (or, and)
    keywords ..
}
"all":GET
"detail/<id>":GET

*Run
python run.py