# 导入tushare
import tushare as ts
# 设置token
ts.set_token('4723a8adcaba7690c037eb28094c0355d73dfe2d002d8c827e5712bc')

# 初始化接口
pro = ts.pro_api()
# pro = ts.pro_api('4723a8adcaba7690c037eb28094c0355d73dfe2d002d8c827e5712bc')  两者选一


# 数据调取
df = pro.trade_cal(exchange='', start_date='20180901', end_date='20181001', fields='exchange,cal_date,is_open,pretrade_date', is_open='0')
# df = pro.query('trade_cal', exchange='', start_date='20180901', end_date='20181001', fields='exchange,cal_date,is_open,pretrade_date', is_open='0')


# HTTP协议方式
# http restful 采用post方式，通过json body传入接口参数，请求地址为http://api.tushare.pro
#
# 输入参数
# api_name，接口名称；
# token，用于识别唯一用户的标识；
# params，接口参数，如daily接口中start_date和end_date；
# fields，字段列表，用于接口获取指定的字段，以逗号分隔，如"open,high,low,close"；
# 输出参数
# code: 接口返回码，2002表示权限问题。
# msg: 错误信息；
# data: 具体数据，成功的请求包含fields和items字段，fields与items数据一一对齐；
# 示例
# 采用命令行工具curl的请求示例如下：

curl -X POST -d '{"api_name": "trade_cal", "token": "xxxxxxxx", "params": {"exchange":"", "start_date":"20180901", "end_date":"20181001", "is_open":"0"}, "fields": "exchange,cal_date,is_open,pretrade_date"}' http://api.tushare.pro