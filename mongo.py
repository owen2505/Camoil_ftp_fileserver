# 此代码示例通过pymongo操作mongodb数据库
from pymongo import MongoClient

# 创建数据库连接
conn = MongoClient("0.0.0.0", 27017)

# 创建数据库对象
db = conn.stu

# 创建集合对象
myset = db.class4

# 数据操作
# myset.insert_one({"name":"张铁林","king":"乾隆"})
# myset.insert_many([{"name": "张国立", "king": "康熙"},
#                    {"name": "陈道明", "king": "康熙"}])
# myset.insert([{"name": "唐国强", "king": "雍正"}, \
#               {"name": "陈建斌", "king": "雍正"}, \
#               {"_id": 1, "name": "吴奇隆", "king": "四爷"}])
# myset.save({"_id": 1, "name": "聂远", "king": "乾隆"})
# cursor = myset.find({"name": {"$exists": True}}, {"_id": 0})
# for i in cursor.limit(3).sort([("name",-1),("king",-1)]):
#     print(i)
# dict0 = {"$or":[{"king":"乾隆"},{"name":"陈道明"}]}
# d = myset.find_one(dict0)
# print(d)

# myset.update_many({"king": "康熙"}, {"$set": {"king_name": "玄烨"}})
# myset.update_one({"king": "雍正"}, {"$set": {"king_name": "胤禛"}})
# myset.update_one({"name": "郑少秋"}, {"$set": {"king": "乾隆"}}, upsert=True)
# myset.update({"king": "乾隆"}, {"$set": {"king_name": "弘历"}})
# myset.update({"king": "乾隆"}, {"$set": {"king_name": "弘历"}}, multi=True)
# myset.delete_one({"king": "康熙"})
# myset.delete_many({"king": "雍正"})
# myset.remove({"king_name": None}, multi=True)
# myset.remove()

# data = myset.find_one_and_delete({"name": "张铁林"})
# print(data)

a = myset.find_one_and_update({"name": "张铁林"}, {"$set": {"king": "乾隆"}})
print(a)
# 关闭数据库连接
conn.close()

# 此代码示例通过pymongo操作mongodb数据库
from pymongo import MongoClient

# 创建数据库连接
conn = MongoClient("0.0.0.0", 27017)

# 创建数据库对象
db = conn.stu

# 创建集合对象
myset = db.class4
================================================================================
以上是owen写的代码
