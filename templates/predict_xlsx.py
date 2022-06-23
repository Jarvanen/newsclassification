import xlrd
import xlwt
from clean_text import clean_text
import numpy as np
def predict_xlsx(read_path, save_path, maxlen, tokenizer, model, label_dict):
     '''
     param: read_path  未打标签的xlsx格式数据集读取路径
     param: save_path  打好标签的xlsx格式数据集保存路径
     param: maxlen, tokenizer, model, label_dict   模型参数
     return
     '''
     book = xlwt.Workbook()                                      #新建xlsx表格
     sheet = book.add_sheet('类别',cell_overwrite_ok = True)     #新建sheet
     workbook = xlrd.open_workbook(read_path)                    #读取xlsx表格
     worksheet = workbook.sheet_by_index(0)                      #读取第一个sheet
     nrows = worksheet.nrows                                     #读取sheet行数
     for i in range(nrows):
          if i ==0:                                              #第一行
               num = worksheet.cell_value(i, 0)                  #编号表头
          else:  
               num = int(worksheet.cell_value(i, 0))
          sheet.write(i, 0, num)
          title = worksheet.cell_value(i, 2)                     #标题
          sheet.write(i, 2, title)                               
          content = worksheet.cell_value(i, 3)                   #正文
          sheet.write(i, 3, content)                             
          if i == 0:
               channelName = worksheet.cell_value(i, 1)          #类别表头
               sheet.write(i, 1, channelName)
          else:
               text = clean_text(title + ' ' + content)          #标题加正文清洗
               text = text[:maxlen]
               x1, x2 = tokenizer.encode(first=text)
               X1 = x1 + [0] * (maxlen-len(x1)) if len(x1) < maxlen else x1
               X2 = x2 + [0] * (maxlen-len(x2)) if len(x2) < maxlen else x2
               predicted = model.predict([[X1], [X2]])
               y = np.argmax(predicted[0])
               channelName = label_dict[str(y)]                  #预测类别
               sheet.write(i, 1, channelName)                    #写入类别
          print(num, '/', nrows)
     book.save(save_path)
     print('打好标签的测试集已保存：', save_path)
     return
               
               
               
               
          
          
          
