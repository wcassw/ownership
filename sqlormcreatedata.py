from sqlormmodel import User, Session, engine

"""
        cd /Volumes/work/dev/sqlorm/; virtualenv venv; source venv/bin/activate

        cd /Volumes/work/dev/sqlorm/; clear; python3.9 sqlormcreatedata.py

        https://docs.sqlalchemy.org/en/14/core/metadata.html

"""

local_session=Session(bind=engine)

new_user=User(username="wcass",email="wcass@net.com")


local_session.add(new_user)
local_session.commit()


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



print(f'*** adding users {("*"*20)}\n{("*"*20)}')
for u in add_users:
	new_user=User(username=u["username"],email=u["email"])
	local_session.add(new_user)
local_session.commit()



print(f'Mult-add results {("*"*20)}')
results = local_session.query(User).all()
print(results)


print(f'get usernames for 1st 3, results {("*"*20)}')
users=local_session.query(User).all()[:3]

for user in users:
	print(user.username)


print(f'\nfilter:  first {("*"*20)}')
results_filter = local_session.query(User).filter(User.username=='jerry').first()
print(results_filter)
