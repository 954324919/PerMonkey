#coding=utf-8
from root import PROJECT_ROOT,base_url
from common.POUtils import ParseXml
import HtmlParser,xlrd,os
result_dir=PROJECT_ROOT+'/result'
result_log_dir=PROJECT_ROOT+'/result/log/'
result=[]
parseXml=ParseXml()

def logResult():
    all_crash=parseXml.all_file_path(PROJECT_ROOT+'/result',"crash.txt")
    if len(all_crash)!=0:
        result.append("执行过程中有崩溃，测试不通过。")
    else:
        result.append("执行过程中没有崩溃，测试通过。")

def write_result_html(base_url):
    description="测试标准:CPU使用不能超过60%,内存使用不超过300M,没有崩溃信息。"
    name=["查看性能数据","查看log"]

    lst=[]
    xmlJson = parseXml.getXmlParser()
    if xmlJson['type_name'] == 'performance':
        lst.append(HtmlParser.res_list(name[0],base_url+"/result_per.html"))
    lst.append(HtmlParser.res_list(name[1],base_url+"/result_log.html"))
    HtmlParser.result_Html(''.join(lst),result_dir,description,''.join(result))


def write_log_html(base_url):
    pathDir = os.listdir(result_log_dir)
    lst = []
    for allDir in pathDir:
        child = os.path.join('%s%s' % (result_log_dir, allDir))

        if child.endswith(".txt"):
            filepath,filename=os.path.split(child)
            lst.append(HtmlParser.get_log(base_url+'/log/'+filename))
    HtmlParser.log_html(result_dir, ''.join(lst))
    #调用生成log结果
    logResult()


def write_per_html():
    try:
        data=xlrd.open_workbook(PROJECT_ROOT+'/result/testPerformance.xls')
        table=data.sheet_by_name(u"sheet_test")
        if table==None:
            pass
        else:
            lst=[]
            rows=table.nrows
            CpuUse=str(table.cell(rows-1,0).value)
            MemUse=str(table.cell(rows-1,1).value)
            if float(CpuUse)>float(0.6):
                result.append("CPU平均使用率测试未通过。")
            else:
                result.append("CPU平均使用率测试通过。")
            if float(MemUse)>float(300):
                result.append("内存平均使用率测试未通过。")
            else:
                result.append("内存平均使用率测试通过。")
            for i in range(1,rows):
                cpu=str(table.cell(i,0).value)
                mem=str(table.cell(i,1).value)
                battery=str(table.cell(i,2).value)
                up=str(table.cell(i,3).value)
                down=str(table.cell(i,4).value)
                lst.append(HtmlParser.get_tr_file(cpu,mem,battery,up,down))
            HtmlParser.Parsing_Html(''.join(lst),result_dir,CpuUse,MemUse)
    except:
        pass
def main():
    write_log_html(base_url)
    xmlJson=parseXml.getXmlParser()
    if xmlJson['type_name']=='performance':
        write_per_html()
    write_result_html(base_url)
if __name__=='__main__':
    main()