import xlwt
def Excel_Style():
    """
    設置單元格格式
    :return:
    """
    # 設置居中
    style_center = xlwt.XFStyle()
    a1 = xlwt.Alignment()
    a1.horz = 0x02  # 水平居中
    a1.vert = 0x01  # 垂直居中
    style_center.alignment = a1

    #設置表頭為黃色背景色且居中
    pattern_yellow = xlwt.Pattern()
    pattern_yellow.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern_yellow.pattern_fore_colour=5# 5代表黃色
    style_bgcolor_yellow = xlwt.XFStyle()
    style_bgcolor_yellow.pattern = pattern_yellow
    style_bgcolor_yellow.alignment=a1

    #設置單元格紅色背景且居中
    pattern_red = xlwt.Pattern()
    pattern_red.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern_red.pattern_fore_colour = 2  # 2代表紅色
    style_bgcolor_red = xlwt.XFStyle()
    style_bgcolor_red.pattern = pattern_red
    style_bgcolor_red.alignment = a1

    return [style_bgcolor_yellow, style_center, style_bgcolor_red]
