from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from model.job import Job
from model.skill import Skill
from model.contact import Contact
import myutils

db_user = "root"
db_pswd = "123456"
db_name = "data"
port = "3306"
db_ip = "localhost"
db_url = "mysql+pymysql://{db_user}:{db_pswd}@{db_ip}:{port}/{db_name}?charset=UTF8MB4".format(db_user= db_user, db_pswd=db_pswd, db_ip=db_ip, port=port, db_name=db_name)
engine = create_engine(db_url, )
# 建立資料表操作物件 sessionmaker
DB_session = sessionmaker(engine)
db_session = DB_session()


def add_job(job):
    print(job)
    # 新增skill
    skill_list = job["skill"]
    if len(skill_list) != 0:
        for skill in skill_list:
            s = db_session.query(Skill).filter(Skill.id == skill["code"]).first()
            print(s)
            if s is None:
                db_session.add(
                    Skill(id=skill["code"], name=skill["description"], modify_time=myutils.get_datetime_str(), create_user=db_user))
                db_session.commit()
            else:
                print(skill, "已經存在")
    try:
        # 新增job
        db_session.add(
            Job(id=job["id"], name=job["job_name"], company_name=job["company_name"], company_url=job["company_url"],
                url=job["url"], job_detail=job["job_detail"][:1000], modify_time=myutils.get_datetime_str(), create_user=db_user))
        db_session.commit()
        # print("after insert Job", db_session.query(Job).filter(Job.id == job["id"]).first())
        # 新增contact
        contact = job["contact"]
        db_session.add(
            Contact(name=contact["hrName"], email=contact["email"], visit=contact["visit"], reply=contact["reply"],
                    phone=contact["phone"], other=contact["other"], jobid=job["id"], modify_time=myutils.get_datetime_str(), create_user=db_user))
        db_session.commit()
    except Exception as e:
        print(e)
        print("----------錯誤資料-----------")
        print(job)
        print("----------------------------")
    finally:
        db_session.close()

