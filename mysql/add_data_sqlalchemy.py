from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
Session = sessionmaker()
print(Session)

"""
CREATE TABLE news
(
  id         INT AUTO_INCREMENT
    PRIMARY KEY,
  title      VARCHAR(200) DEFAULT ''  NOT NULL
  COMMENT '标题',
  content    VARCHAR(2048) DEFAULT '' NOT NULL
  COMMENT '内容',
  types      VARCHAR(10) DEFAULT ''   NOT NULL
  COMMENT '类型',
  image      VARCHAR(300)             NULL
  COMMENT '图片',
  author     VARCHAR(20)              NULL
  COMMENT '作者',
  view_count INT DEFAULT '0'          NOT NULL
  COMMENT '浏览次数',
  is_valid   SMALLINT(6) DEFAULT '1'  NOT NULL
  COMMENT '是否有效',
  created_at DATETIME                 NULL
  COMMENT '创建时间'
)
  ENGINE = InnoDB;
"""


class News(Base):
    __tablename__ = "news"

    # 字段映射
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(String(2048), nullable=False)
    types = Column(String(10), nullable=False)
    image = Column(String(300))
    author = Column(String(20))
    view_count = Column(Integer)
    is_valid = Column(Boolean)
    created_at = Column(DateTime)


# 新增一条数据
newObj = News(title="测试标题", content="测试内容", types="百家", image="/static/1.jpg", author="测试作者",
              view_count=101, is_valid=True, created_at="2018-12-20 13:20:10")

