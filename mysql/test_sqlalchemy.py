from sqlalchemy import Column, String, Integer, SmallInteger, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类
Base = declarative_base()

# 定义news对象
"""
CREATE TABLE `news` (
  `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY ,
  `title` VARCHAR(200) NOT NULL DEFAULT '' COMMENT '标题',
  `content` VARCHAR(2048) NOT NULL DEFAULT '' COMMENT '内容',
  `types` VARCHAR(10) NOT NULL DEFAULT '' COMMENT '类型',
  `image` VARCHAR(300) NULL COMMENT '图片',
  `author` VARCHAR(20) NULL COMMENT '作者',
  `view_count` INT NOT NULL DEFAULT 0 COMMENT '浏览次数',
  `is_valid` SMALLINT NOT NULL DEFAULT 1 COMMENT '是否有效',
  `created_at` DATETIME NULL COMMENT '创建时间'
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;
"""


class News(Base):
    __tablename__ = 'news'

    # 表的结构
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(String(2000), nullable=False)
    types = Column(String(10), nullable=False)
    image = Column(String(300))
    author = Column(String(20))
    view_count = Column(Integer)
    is_valid = Column(SmallInteger)
    created_at = Column(DateTime)

    def __repr__(self):
        return "<News(id=%s, title='%s', content='%s', types='%s', image='%s', author='%s', view_count=%s, is_valid=%s, created_at='%s')>" % (
            self.id, self.title, self.content, self.types, self.image, self.author, self.view_count, self.is_valid,
            self.created_at)


engine = create_engine('mysql://root:123456@127.0.0.1:3306/news', echo=True)

print(engine)
