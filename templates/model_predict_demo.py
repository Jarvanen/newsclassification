# -*- coding: utf-8 -*-
# @Time : 2020/12/23 15:28
# @Author : Jclian91
# @File : model_predict.py
# @Place : Yangpu, Shanghai
# 模型预测脚本

import time
import json
import numpy as np

from model_train import token_dict, OurTokenizer
from keras.models import load_model
from albert import get_custom_objects
import predict_xlsx
maxlen = 256

# 加载训练好的模型
model = load_model("albert_base_cls_news.h5", custom_objects=get_custom_objects())
tokenizer = OurTokenizer(token_dict)
with open("label.json", "r", encoding="utf-8") as f:
    label_dict = json.loads(f.read())

print('模型加载完毕，已开启实时预测...\n')
while True:
     op = input("预测单条新闻请输入'1',xlsx批量预测并保存请输入'2'\n(1或2) >> ")
     if op == '1':
          text = input('请输入单条新闻>>\n')
          s_time = time.time()
          text = text[:maxlen]
          x1, x2 = tokenizer.encode(first=text)

          X1 = x1 + [0] * (maxlen-len(x1)) if len(x1) < maxlen else x1
          X2 = x2 + [0] * (maxlen-len(x2)) if len(x2) < maxlen else x2

          # 模型预测并输出预测结果
          predicted = model.predict([[X1], [X2]])
          y = np.argmax(predicted[0])
          
          #print(label_dict)
          print('predicted',predicted[0])
          print("原文: %s" % text)
          print("预测标签: %s" % label_dict[str(y)])
          e_time = time.time()
          print("消耗时间:", e_time-s_time,'秒\n')
          print(predicted[0][y])
     if op == '2':
          read_path = input('请输入xlsx表格读取路径>>\n') # 1625536586359348.xlsx
          predict_xlsx.predict_xlsx(read_path, 'labeled_news.xlsx', maxlen, tokenizer, model, label_dict)
     else:
          pass


'''
s_time = time.time()
# 预测示例语句
text = "说到硬派越野SUV，你会想起哪些车型？是被称为“霸道”的丰田 普拉多 (配置 | 询价) ，还是被叫做“山猫”的帕杰罗，亦或者是“渣男专车”奔驰大G、" \
       "“沙漠王子”途乐。总之，随着世界各国越来越重视对环境的保护，那些大排量的越野SUV在不久的将来也会渐渐消失在我们的视线之中，所以与其错过，" \
       "不如趁着还年轻，在有生之年里赶紧去入手一台能让你心仪的硬派越野SUV。而今天我想要来跟你们聊的，正是全球公认的十大硬派越野SUV，" \
       "越野迷们看完之后也不妨思考一下，到底哪款才是你的菜，下面话不多说，赶紧开始吧。"


# 利用BERT进行tokenize
text = text[:maxlen]
x1, x2 = tokenizer.encode(first=text)

X1 = x1 + [0] * (maxlen-len(x1)) if len(x1) < maxlen else x1
X2 = x2 + [0] * (maxlen-len(x2)) if len(x2) < maxlen else x2

# 模型预测并输出预测结果
predicted = model.predict([[X1], [X2]])
y = np.argmax(predicted[0])


print("原文: %s" % text)
print("预测标签: %s" % label_dict[str(y)])
e_time = time.time()
print("cost time:", e_time-s_time)
'''
