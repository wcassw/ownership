from sqlormmodel import User, Session, engine

"""
        cd /Volumes/work/dev/sqlorm/; virtualenv venv; source venv/bin/activate

        cd /Volumes/work/dev/sqlorm/; clear; python3.9 sqlormdelete.py

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

print(f'*** deleting a user {("*"*20)}')
for u in add_users:
    new_user=User(username=u["username"],email=u["email"])
    local_session.add(new_user)
local_session.commit()
# End -- add due too in-memory ###################################


user_to_delete=local_session.query(User).filter(User.username=='jerry3').first()
local_session.delete(user_to_delete)
local_session.commit()

print(f'update results - jerry3 deleted {("*"*20)}\n{("*"*20)}')
results_filter = local_session.query(User).all()
print(results_filter)


print(f'order_by results {("*"*20)}')
results_filter=local_session.query(User).order_by(User.username).all()
for r in results_filter:
    print(r)

