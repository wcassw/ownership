from sqlormmodel import Session, engine, User

"""
        cd /Volumes/work/dev/sqlorm/; virtualenv venv; source venv/bin/activate

        cd /Volumes/work/dev/sqlorm/; clear; python3.9 sqlormupdate.py

        https://docs.sqlalchemy.org/en/14/core/metadata.html

"""

local_session=Session(bind=engine)

# start -- add due too in-memory
add_users =[
    {
        "username":"jerry",
        "email":"jerry@company.com"
    },
    {
        "username":"jerry2",
        "email":"jerry2@company.com"
    },
    {
        "username":"jerry3",
        "email":"jerry3@company.com"
    },
    {
        "username":"jerry4",
        "email":"jerry4@company.com"
    },
    {
        "username":"jerry5",
        "email":"jerry5@company.com"
    }
]

print(f'*** adding users {("*"*20)}')
for u in add_users:
    new_user=User(username=u["username"],email=u["email"])
    local_session.add(new_user)
local_session.commit()
# End -- add due too in-memory ###################################

user_to_update=local_session.query(User).filter(User.username =='jerry4').first()

#print('typeUser', type(User))
#print('type',type(user_to_update)) # if AttributeError: 'NoneType' object has no attribute 'username'   no data in table.
#print('fields',user_to_update.username, user_to_update.email)
user_to_update.username = "tom4"
local_session.commit()

"""
<class 'NoneType'> None
Traceback (most recent call last):
  File "/Volumes/work/dev/sqlorm/sqlormupdate.py", line 16, in <module>
    print(user_to_update, user_to_update.username, user_to_update.email)
AttributeError: 'NoneType' object has no attribute 'username'
(venv) wcass@wcass-ltmqiq6 sqlorm % 

add due too in-memory, there data no existing

"""

print(f'update results {("*"*20)}\n{("*"*20)}')
results = local_session.query(User).all()
print(results)

print(f'order_by results {("*"*20)}')
results_filter=local_session.query(User).order_by(User.username).all()
for r in results_filter:
    print(r)

