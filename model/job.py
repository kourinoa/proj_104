from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
import datetime


class Job(declarative_base()):
    __tablename__ = 'job'
    id = Column(String, primary_key=True)
    name = Column(String)
    company_name = Column(String)
    company_url = Column(String)
    url = Column(String)
    job_detail = Column(String)
    create_time = Column(DateTime, default=datetime.datetime.utcnow())
    modify_time = Column(DateTime)
    create_user = Column(String)

    """
    CREATE TABLE `data`.`job`  (
      `id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '編號',
      `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '職位名稱',
      `company_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '公司名稱',
      `company_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '公司相關連接',
      `url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '職位相關連接',
      `job_detail` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '職位描述',
      `create_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '建立時間',
      `create_user` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '建立的使用者',
      `modify_time` datetime(0) NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改時間',
      `skill` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '技能對應編號',
      PRIMARY KEY (`id`) USING BTREE,
      INDEX `job_time_idx`(`create_time`, `modify_time`) USING BTREE
    ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;
    """
