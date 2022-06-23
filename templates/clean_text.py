import re

def clean_text(raw):
     '''
     文本预处理，数据清理
     param: raw 未处理的文本
     return: str 处理过后的文本
     '''
     str = ' '.join(raw.split())   #去除多余的空格和制表符'\t'
     str = re.sub('[’!"#$%&\'()*+,-./:;<=>?@?★▲●■、…【】《》“”‘’[\\]^_`{|}~\s]+', "", str)                         #去除特殊符号
     str = re.sub("[http://|ftp://|https://|www]?[^\u4e00-\u9fa5\s]*?\.[com|net|cn|me|tw|fr][^\u4e00-\u9fa5\s]*",'',str)     #去除网址URL
     str = re.sub(u"[0-9]{4}年[0-9]{1,2}月[\d日]{0,}", '', str)    #去除时间信息 X年X月X日
     str = re.sub(u"[0-9]{1,2}月[\d日]{0,}", '', str)              #去除时间信息 X月X日
     str = re.sub(u"[0-9]{1,2}时[\d分]{0,}", '', str)              #去除时间信息 X时X分
     str = re.sub(u"[0-9]{1,2}点[\d分]{0,}", '', str)              #去除时间信息 X点X分
     stop_words_list = ['新浪','新闻','报道','消息','记者','媒体','讯','编辑',\
                        '来源：','原标题：','本报','本网','北京时间','当地时间']           #停用词字典
     for stop_word in stop_words_list:                                                     #去除停用词
          str = str.replace(stop_word,'')
     return str
