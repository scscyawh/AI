import time
import dlocr
import re
import os
import xlrd
import xlwings as xw

excel_file_path = "excel_files"
excel_result_path = "excel_result_files"
txt_result_path = "txt_result_files"
pic_file_path = "pic_files"
az = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
if not os.path.exists(excel_file_path):
    os.mkdir(excel_file_path)
if not os.path.exists(excel_result_path):
    os.mkdir(excel_result_path)
if not os.path.exists(txt_result_path):
    os.mkdir(txt_result_path)
if not os.path.exists(pic_file_path):
    os.mkdir(pic_file_path)


def find_all_useful_cell(work_book):
    # 获取到所有表格名称
    sheet_names = work_book.sheet_names()
    result_dict = {}
    # 循环每一个表格，从中获取到所有第2行的数据，
    # 注意，这里的行是从0开始算的，所以2行对应的是1，所以是row_values(1)
    for temp_sheet_name in sheet_names:
        # 获取到当前表格
        unchange_sheet = work_book.sheet_by_name(temp_sheet_name)
        # 获取到第2行数据
        unchange_line = unchange_sheet.row_values(1)
        # 获取到“件号”的位置
        local = unchange_line.index('件号')
        # 位置+1就是要填入的位置
        my_local = local + 1
        # 根据要填入的位置，获取到单元格名，比如 1就获取到A ，2就获取到B依次类推
        my_letter = az[my_local]
        # 将获取到的位置写入到要传回的excel字典中
        result_dict[temp_sheet_name] = "{}2".format(my_letter)
    return result_dict


def read_pic_to_excel(line, excel_path, excel_result, txt_result):
    '''
    line: 识别出来的文字行
    excel_path: excel文件夹路径
    excel_result: excel结果文件夹
    txt_result: txt结果文件夹
    '''
    line_list = line.split("-")
    number_part = line_list[0]
    # 第一步读取待更改的原始excel文件,可以从excel_path中读取到待更改的文件名
    old_excel_file_name = os.listdir(excel_path)[0]
    # 第二步根据传入的识别出来的文字行生成一个新的文件名待用
    old_name_end = old_excel_file_name.split("-")
    new_excel_file_name = "{}-{}".format(number_part, old_name_end[1])
    # 第三步，读取旧excle文件中的全部内容,从每个表格中找到需要填充的单元格名称例如：{"封面":"H2"}
    rb = xlrd.open_workbook('{}/{}'.format(excel_path, old_excel_file_name))
    find_result = find_all_useful_cell(rb)
    # 第四步，用另一个包，打开excel文件，改变件号后面的值
    app = xw.App(visible=False, add_book=False)
    app.display_alerts = False
    app.screen_updating = False
    wb = app.books.open('{}/{}'.format(excel_path, old_excel_file_name))
    # 第五步循环第三部得到的结果，给表格上对应位置赋值
    for sheet_name in find_result:
        wb.sheets[sheet_name].range(find_result[sheet_name]).value = line
    # 第六步保存，注意一下，使用结果文件夹，和第二步生成的新文件名
    wb.save('{}/{}'.format(excel_result, new_excel_file_name))
    wb.close()
    app.quit()
    print("写入excel表格完成")
    # 第七步生成txt文件
    with open("{}/{}.txt".format(txt_result, line), "a", encoding='utf8') as f:
        f.write(line)
    print("写入txt完成")


if __name__ == '__main__':
    ocr = dlocr.get_or_create()
    start = time.time()
    # 列出图片路径中的所有文件名
    file_list = os.listdir(pic_file_path)
    # 循环所有的文件名
    for file in file_list:
        # 识别图片
        print("开始识别图片")
        bboxes, texts = ocr.detect("{}/{}".format(pic_file_path, file))
        # 循环识别到的文字列表
        for line in texts:
            if "检具代号" in line:
                # 根据竖线符号切割该行，最后结果是一个列表
                number_line_list = re.split(r"[│|]", line)
                # 循环切割之后的列表
                for number_line_part in number_line_list:
                    # 判断是否有一个对象符合 ： “多个数字-任意符号” 这种类型
                    if re.match("\d+-.", number_line_part):
                        # 将【识别出来的这个对象,excel文件所在路径，excel结果文件预存路径，txt文件结果路径】传入到read_pic_to_excel函数进行下一步处理
                        print("识别到文字，正在修改及写入新的文件")
                        read_pic_to_excel(number_line_part, excel_file_path, excel_result_path, txt_result_path)
    # print('\n'.join(texts))
    # print(f"cost: {(time.time() - start) * 1000}ms")
