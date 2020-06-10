from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
import datetime


class Contact(declarative_base()):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    visit = Column(String)
    other = Column(String)
    reply = Column(String)
    jobid = Column(String)
    create_time = Column(DateTime, default=datetime.datetime.utcnow())
    modify_time = Column(DateTime)
    create_user = Column(String)

    """
    CREATE TABLE `data`.`Untitled`  (
  `id` int(0) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '流水號',
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '聯絡人名稱',
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '郵箱',
  `phone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '電話',
  `create_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '建立時間',
  `modify_time` datetime(0) NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改時間',
  `create_user` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '建立的試用者',
  `jobid` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '對應的職缺',
  `visit` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `reply` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `other` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '其他說明',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `f_job`(`jobid`) USING BTREE,
  CONSTRAINT `f_job` FOREIGN KEY (`jobid`) REFERENCES `data`.`job` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;
    """

