import models.download as download
import models.issue as issue
import models.resource_comment as resource_comment
import models.utilization as utilization
from sqlalchemy import MetaData, Table, create_engine

# Declare the target database connection string
engine = create_engine('postgresql://ckan:ckan@db:5432/ckan')
# Create a metadata object
metadata_obj = MetaData(download.__all__)
# Bind the database-connected engine to the metadata object
metadata_obj.bind = engine
# Get all tables from ckan DB
metadata_obj.reflect()

# Add all imported model tables to the metadata object
for table in download.__all__:
    Table(table, metadata_obj)

for table in issue.__all__:
    Table(table, metadata_obj)

for table in resource_comment.__all__:
    Table(table, metadata_obj)

for table in utilization.__all__:
    Table(table, metadata_obj)


# @create.command(name=u'create',
# short_help=u'データベースにckanext-feedback用のテーブルを作成します。')
# Method to show all tables currently recognized by SQLAlchemy
# def show_tables():
# for t in metadata_obj.sorted_tables:
# print(t.name)

# Run show_tables()
# show_tables()

try:
    metadata_obj.create_all(engine)
    print('テーブルの作成が成功しました。')
except Exception as e:
    print('テーブルの作成が失敗しました。理由：', e)
    engine.dispose()
    print('接続を閉じました。')
