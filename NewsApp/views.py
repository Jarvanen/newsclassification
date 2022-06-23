import time
import json
import numpy as np
from templates.model_train import token_dict, OurTokenizer
from keras.models import load_model
from templates.albert import get_custom_objects
import tensorflow as tf
import keras
from django.http import JsonResponse
from django.shortcuts import render
import xlrd
import xlwt
from clean_text import clean_text

config = tf.ConfigProto(
    device_count={'GPU': 0},
    intra_op_parallelism_threads=1,
    allow_soft_placement=True
)

config.gpu_options.allow_growth = True
config.gpu_options.per_process_gpu_memory_fraction = 0.6
session = tf.Session(config=config)
keras.backend.set_session(session)
text = "新闻"
print('load model...')
model = load_model("templates/albert_base_cls_254.h5", custom_objects=get_custom_objects())
print('load done...')
tokenizer = OurTokenizer(token_dict)
x1, x2 = tokenizer.encode(first=text)
X1 = x1 + [0] * (256 - len(x1)) if len(x1) < 256 else x1
X2 = x2 + [0] * (256 - len(x2)) if len(x2) < 256 else x2
print('test model...')
res = np.argmax(model.predict([[X1], [X2]]))
print(res)
print('test done...')


def index(request):
    return render(request, 'index.html')


def singleNews(request):
    maxlen = 254
    tokenizer = OurTokenizer(token_dict)
    with open("templates/label.json", "r", encoding="utf-8") as f:
        label_dict = json.loads(f.read())
    s_time = time.time()
    text = request.POST['news']

    # 利用BERT进行tokenize
    text = text[:maxlen]
    x1, x2 = tokenizer.encode(first=text)

    X1 = x1 + [0] * (maxlen - len(x1)) if len(x1) < maxlen else x1
    X2 = x2 + [0] * (maxlen - len(x2)) if len(x2) < maxlen else x2

    # 模型预测并输出预测结果
    with session.as_default():
        with session.graph.as_default():
            predicted = model.predict([[X1], [X2]])
    y = np.argmax(predicted[0])

    print("原文: %s" % text)
    print("预测标签: %s" % label_dict[str(y)])
    e_time = time.time()
    print("cost time:", e_time - s_time)
    context = {'a': text + '<br>' + '预测结果：' + label_dict[str(y)]}
    return render(request, 'show.html', context)


num_progress = 0


def fileNews(request):
    res = list()
    newstext = list()
    maxlen = 254
    tokenizer = OurTokenizer(token_dict)
    global num_progress
    with open("templates/label.json", "r", encoding="utf-8") as f:
        label_dict = json.loads(f.read())
    s_time = time.time()
    file = request.FILES['newsFile']
    file_name = str(file)
    if file_name.split(".")[-1] == 'csv':
        file_content = file.read()
        file_content = file_content.decode('utf-8')
        news = file_content.split('\n')
        for line in news:
            text = line[:maxlen]
            text=clean_text(text)
            newstext.append(text)
            x1, x2 = tokenizer.encode(first=text)

            X1 = x1 + [0] * (maxlen - len(x1)) if len(x1) < maxlen else x1
            X2 = x2 + [0] * (maxlen - len(x2)) if len(x2) < maxlen else x2

            # 模型预测并输出预测结果
            with session.as_default():
                with session.graph.as_default():
                    predicted = model.predict([[X1], [X2]])
            y = np.argmax(predicted[0])
            print("原文: %s" % text)
            print("预测标签: %s" % label_dict[str(y)])
            e_time = time.time()
            print("cost time:", e_time - s_time)
            res.append(label_dict[str(y)])
            num_progress = round(len(res) / len(news) * 100, 2)
    else:
        book = xlwt.Workbook()  # 新建xlsx表格
        sheet = book.add_sheet('类别', cell_overwrite_ok=True)  # 新建sheet
        workbook = xlrd.open_workbook(filename=None, file_contents=file.read())  # 读取xlsx表格
        worksheet = workbook.sheet_by_index(0)  # 读取第一个sheet
        print(worksheet)
        nrows = worksheet.nrows  # 读取sheet行数
        for i in range(nrows):
            if i == 0:  # 第一行
                num = worksheet.cell_value(i, 0)  # 编号表头
            else:
                num = int(worksheet.cell_value(i, 0))
            sheet.write(i, 0, num)
            title = worksheet.cell_value(i, 2)  # 标题
            sheet.write(i, 2, title)
            content = worksheet.cell_value(i, 3)  # 正文
            if (i != 0):
                newstext.append(content[:maxlen])
            sheet.write(i, 3, content)
            if i == 0:
                channelName = worksheet.cell_value(i, 1)  # 类别表头
                sheet.write(i, 1, channelName)
            else:
                text = clean_text(title + ' ' + content)  # 标题加正文清洗
                text = text[:maxlen]
                x1, x2 = tokenizer.encode(first=text)
                X1 = x1 + [0] * (maxlen - len(x1)) if len(x1) < maxlen else x1
                X2 = x2 + [0] * (maxlen - len(x2)) if len(x2) < maxlen else x2
                with session.as_default():
                    with session.graph.as_default():
                        predicted = model.predict([[X1], [X2]])
                y = np.argmax(predicted[0])
                e_time = time.time()
                print("cost time:", e_time - s_time)
                channelName = label_dict[str(y)]  # 预测类别
                res.append(label_dict[str(y)])
                sheet.write(i, 1, channelName)  # 写入类别
                num_progress = round(i / (nrows - 1) * 100, 2)
            print(num, '/', nrows)
            book.save('C:/Users/Jarvan/Desktop/result.xlsx')
            print('打好标签的测试集已保存：', 'C:/Users/Jarvan/Desktop/result.xlsx')
    fin = ''
    for i in range(len(res)):
        fin = fin + newstext[i] + '</br>' + '预测结果：' + res[i] + '</br></br>'
    context = {'a': fin}
    num_progress = 0
    return render(request, 'show.html', context)


'''
前端JS需要访问此程序来更新数据
'''
def show_progress(request):
    print('show_progress----------' + str(num_progress))
    return JsonResponse(num_progress, safe=False)
