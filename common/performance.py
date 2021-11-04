#coding=utf-8
from common.POUtils import ParseXml
from common.CpuMem import CpuMem
import pickle,os,shutil,xlwt,xlsxwriter
from pyxlswriter import write_chart
from root import PROJECT_ROOT
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)
result=PROJECT_ROOT+"/result"
class Performance():
    def __init__(self):
        self.xmlData = ParseXml().getXmlParser()
        self.PerInfo=CpuMem()
        self.ending=dict()

    def writePerInfo(self):
        Package = self.xmlData["Package"]
        pid = self.PerInfo.get_pid(Package)
        cpu_kel = self.PerInfo.get_cpu_kel()  # 获取cpu核数
        uid=self.PerInfo.get_uid(pid)

        self.PerInfo.get_battery()  # 获取电量
        self.PerInfo.get_mem(Package)  # 获取内存
        self.PerInfo.cpu_rate(pid, cpu_kel)  # cpu使用率
        self.PerInfo.get_fps(Package)  # 获取fps
        self.PerInfo.get_flow(uid)  # 获取应用上传、下载流量



    def writeExcel(self):
        filepath = PROJECT_ROOT + "/result/testPerformance.xls"
        if os.path.exists(filepath):
            shutil.rmtree(filepath, True)
        book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        sheet = book.add_sheet(u"sheet", cell_overwrite_ok=True)
        cpu = PATH(result + "/cpu.yaml")
        flow = PATH(result + "/flow.yaml")
        battery = PATH(result + "/battery.yaml")
        # fps=PATH(result+"/fps.yaml")
        mem = PATH(result + "/mem.yaml")

        cpu_list = self.readInfo(cpu)
        battery_list = self.readInfo(battery)
        # fps_list=readInfo(fps)
        mem_list = self.readInfo(mem)
        flow_list = self.readInfo(flow)
        upflow_list = flow_list[0]
        downflow_list = flow_list[1]

        title = [u'CPU使用率', u'内存使用', u'电量', u'上传的流量', u'下载的流量']
        data = (title, cpu_list, mem_list, battery_list, upflow_list, downflow_list)
        # print(type(data))

        self.xlsWriter(data)  # 写入excel,并执行生成折线图方法
    def xlsWriter(self,data):
        workbook = xlsxwriter.Workbook(PROJECT_ROOT+'/result/testPerformance.xls')
        worksheet = workbook.add_worksheet('sheet_test')

        for i, line in enumerate(data):
            # print(i)
            for j, col in enumerate(line):
                # print(j,col)
                if i == 0:
                    worksheet.write(i, j, col)
                else:
                    worksheet.write(j + 1, i - 1, col)

        nrow_len = len(data[1])
        avg_cpu=round(sum(data[1])/nrow_len,2)  #统计出平均cpu占用
        avg_mem=round(sum(data[2])/nrow_len,2)  #统计出平均mem占用
        if avg_cpu>float(0.60):
            self.ending["cpu"]="不符合标准"
        else:
            self.ending["cpu"]="符合标准"
        if avg_mem>float(300.0):
            self.ending["mem"]="不符合标准"
        else:
            self.ending["mem"]="符合标准"

        worksheet.write(nrow_len+1,0,avg_cpu)
        worksheet.write(nrow_len+1,1,avg_mem)

        write_chart(workbook,worksheet,data[0][0], [0, 0], [1, 0, nrow_len + 1, 0], 0)  # 写入 CPU占有率
        write_chart(workbook,worksheet,data[0][1], [0, 1], [1, 1, nrow_len + 1, 1], 3)  # 写入  内存使用
        # write_chart(workbook,worksheet,data[0][2], [0, 2], [1, 2, nrow_len + 1, 2], 5)  # 写入fps
        write_chart(workbook,worksheet,data[0][2], [0, 2], [1, 2, nrow_len + 1, 2], 7)  # 写入电量
        write_chart(workbook,worksheet,data[0][3], [0, 3], [1, 3, nrow_len + 1, 3], 9)  # 写入上传的流量
        write_chart(workbook,worksheet,data[0][4], [0, 4], [1, 4, nrow_len + 1, 4], 11)  # 写入下载的流量

        workbook.close()

    def createFile(self, file):
        if not os.path.isfile(file):
            f = open(file, "w")
            f.close()
    # 初始化创建文件
    def init(self):
        if not os.path.exists(result):
            os.makedirs(result)
        else:
            shutil.rmtree(result, True)
            os.makedirs(result)
        cpu = PATH(result + "/cpu.yaml")
        mem = PATH(result + "/mem.yaml")
        flow = PATH(result + "/flow.yaml")
        battery = PATH(result + "/battery.yaml")
        # fps =PATH(result+"/fps.yaml")
        self.createFile(cpu)
        self.createFile(mem)
        self.createFile(flow)
        self.createFile(battery)
    '''
    def logWriter(self):
        log=ParseXml().all_file_path(result+"/log","crash.txt")
        z=0
        for i in log:
            with open(log[i],"r") as f:
                a=''.join(f.readlines())

                self.writePer(PROJECT_ROOT+"/result/testPerformance.xls",z,7,a)
            z+=1
    def writePer(self,filepath,i,j,data):
        workbook=xlrd.open_workbook(filepath,formatting_info=True)
        book=copy(workbook)
        sheet=book.get_sheet(0)
        sheet.write(i,j,data)
        book.save(filepath)
    '''