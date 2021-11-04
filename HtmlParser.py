# -*- coding: utf-8 -*-
#!/usr/bin/python

import os,sys
absolutepath=os.path.abspath(os.curdir)
abspath=os.path.abspath("..")
sys.path.append(absolutepath)
sys.path.append(abspath)

def get_tr_file(cpu, mem, battery, up, down):
    tr = """
    <tr bgcolor="MintCream">
            %(cpu)s
            %(mem)s
            %(battery)s
            %(up)s
            %(down)s
    </tr>
    """

    cpu = '<td>{}</td>'.format(cpu)
    mem = '<td>{}</td>'.format(mem)
    battery = '<td>{}</td>'.format(battery)
    up = '<td>{}</td>'.format(up)
    down = '<td>{}</td>'.format(down)

    result = {'cpu': cpu, 'mem': mem, 'battery': battery, 'up': up, 'down': down}
    return tr % result

def Parsing_Html(logs,filedir,CpuUse,MemUse):
    """
    """
    #<p><span style="color:blue;">所有用例:,<span style="color:green;">通过的用例:,<span style="color:red;">失败的用例:<span style="color:pink;">异常的用例:</p>
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="Content-type" content="text/html; charset=utf-8"/>
        <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
        <title>Test Report</title>
    </head>
    <body>
    <span style="color:green;"><h1>Test Report</h1></span>
    <p><span style="color:red">CPU平均使用:{CpuUse}</span>,<span style="color:blue">内存平均使用:{MemUse}</span></p>

    <table border="1" cellpadding="10">
        <tbody>
        <tr bgcolor="MintCream">
            <th>cpu</th>
            <th>mem</th>
            <th>battery</th>
            <th>up</th>
            <th>down</th>
        </tr>
            %(tr)s

        </tbody>
    </table>
    </body>
    </html>
    '''.format(CpuUse=CpuUse,MemUse=MemUse)
    data={'tr':logs}
    save_html_file = '%s/result_per.html' % filedir
    with open(save_html_file, 'w',encoding='utf-8') as f:
        f.write(template % data)
        f.close()

def get_log(log_src):
    log='''
    &nbsp;&nbsp;&nbsp;&nbsp;<a href="{}">{}</a> <br/>
    '''.format(log_src,log_src)
    return log

def log_html(logdir,logs):
    #创建log html文件
    template='''
    <!DOCTYPE html>
    <html lang="en-US">
    <head><title>log详情页</title></head>
    <body>
    <span style="color:green;"><h1>Log</h1></span>
    %(logs)s
    </body>
    </html>
    '''
    save_html_file = '%s/result_log.html' % logdir
    data={'logs':logs}
    with open(save_html_file, 'w',encoding='utf-8') as f:
        f.write(template % data)
        f.close()

#主result中包含的 log查看、性能数据查看
def res_list(result_name,result_path):
    res = """
    <tr bgcolor="MintCream">
            %(result_name)s
            %(result_path)s
    </tr>
    """
    result_path='<td><a href="{}">{}</a></td>'.format(result_path,result_name)
    result_name='<td>{}</td>'.format(result_name)

    result = {'result_name': result_name, 'result_path': result_path}
    return res % result
#主result文件
def result_Html(name,dir,description,result):
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="Content-type" content="text/html; charset=utf-8"/>
        <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
        <title>Test Report</title>
    </head>
    <body>
    <span style="color:green;"><h1>Test Report</h1></span>
    
    %(name)s <br/>
    <span style="color:red;"><h3>%(description)s</h3></span> <br/>
    %(result)s <br/>
    </body>
    </html>
    '''.format()
    data={'name':name,'description':description,'result':result}
    save_html_file = '%s/test.html' % dir
    with open(save_html_file, 'w',encoding='utf-8') as f:
        f.write(template % data)
        f.close()
