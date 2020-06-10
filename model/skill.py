from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
import datetime


class Skill(declarative_base()):
    __tablename__ = "skill"
    id = Column(String, primary_key=True)
    name = Column(String)
    create_time = Column(DateTime, default=datetime.datetime.utcnow())
    modify_time = Column(DateTime)
    create_user = Column(String)


    """
    CREATE TABLE `data`.`skill`  (
    `id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '技能編號',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '技能名稱',
  `create_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '建立時間',
  `modify_time` datetime(0) NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改時間',
  `create_user` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '建立的使用者',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `skl_time_idx`(`create_time`, `modify_time`) USING BTREE,
  INDEX `skl_name_idx`(`name`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;
"""