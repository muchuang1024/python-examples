import xlrd
import os
import xlsxwriter

def merge_excel(source_xls, target_xls):
    data = []
    for i in source_xls:
        wb = xlrd.open_workbook(i)
        for sheet in wb.sheets():
            for rownum in range(sheet.nrows):
                data.append(sheet.row_values(rownum))
    #print(data)
    # 写入数据
    workbook = xlsxwriter.Workbook(target_xls)
    worksheet = workbook.add_worksheet()
    font = workbook.add_format({"font_size":14})
    for i in range(len(data)):
        for j in range(len(data[i])):
            worksheet.write(i, j, data[i][j], font)
    # 关闭文件流
    workbook.close()

# 读取数据
for root,dirs,fs in os.walk('.'):
  for d in dirs:
    path = os.path.join(root, d)
    print(path)
    source_xls = []
    target_file = '{}.xlsx'.format(d)
    target_xls = os.path.join(path, target_file)
    if os.path.exists(target_xls):
        os.remove(target_xls)
    items = os.listdir(d) 
    for f in sorted(items):
        if f.endswith('.xlsx'):
            source_xls.append(os.path.join(path, f))
    if len(source_xls) == 0:
        continue
    merge_excel(source_xls, target_xls)
