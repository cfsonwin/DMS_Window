# coding=utf-8
def ColorList():
    '''
    有序地颜色序列
    :return: list(红-》绿-》蓝 的对应编码)
    '''
    color = []
    for i in range(0, 15):
        a = hex(15 - i)
        color.append('#' + str(a)[2] * 2 + '0000')
    for i in range(0, 15):
        a = hex(15 - i)
        color.append('#00' + str(a)[2] * 2 + '00')
    for i in range(0, 15):
        a = hex(15 - i)
        color.append('#0000' + str(a)[2] * 2)
    for i in range(0, 15):
        a = hex(15 - i)
        color.append('#' + str(a)[2] * 2 + '0000')
    for i in range(0, 15):
        a = hex(15 - i)
        color.append('#00' + str(a)[2] * 2 + '00')
    for i in range(0, 15):
        a = hex(15 - i)
        color.append('#0000' + str(a)[2] * 2)
    for i in range(0, 15):
        a = hex(15 - i)
        color.append('#' + str(a)[2] * 2 + '0000')
    for i in range(0, 15):
        a = hex(15 - i)
        color.append('#00' + str(a)[2] * 2 + '00')
    for i in range(0, 15):
        a = hex(15 - i)
        color.append('#0000' + str(a)[2] * 2)
    for i in range(0, 15):
        a = hex(15 - i)
        color.append('#' + str(a)[2] * 2 + '0000')
    for i in range(0, 15):
        a = hex(15 - i)
        color.append('#00' + str(a)[2] * 2 + '00')
    for i in range(0, 15):
        a = hex(15 - i)
        color.append('#0000' + str(a)[2] * 2)
    for i in range(0, 15):
        a = hex(15 - i)
        color.append('#' + str(a)[2] * 2 + '0000')
    for i in range(0, 15):
        a = hex(15 - i)
        color.append('#00' + str(a)[2] * 2 + '00')
    for i in range(0, 15):
        a = hex(15 - i)
        color.append('#0000' + str(a)[2] * 2)
    for i in range(0, 15):
        a = hex(15 - i)
        color.append('#' + str(a)[2] * 2 + '0000')
    for i in range(0, 15):
        a = hex(15 - i)
        color.append('#00' + str(a)[2] * 2 + '00')
    for i in range(0, 15):
        a = hex(15 - i)
        color.append('#0000' + str(a)[2] * 2)
    return color
