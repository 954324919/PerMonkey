import subprocess
import os
import re
from wsgiref.validate import validator
import time
import pickle
import platform

from root import PROJECT_ROOT

from common.adbUtils import ADB
# from HtmlParser import result
# 判断系统类型，windows使用findstr，linux使用grep
system = platform.system()
if system is "Windows":
    find_util = "findstr"
else:
    find_util = "grep"

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)
result=PROJECT_ROOT+"/result"
class CpuMem():
    #获取到应用的内存信息
    def __init__(self,device_id = ""):

        self.adb=ADB(device_id=device_id)
    def get_mem(self,pkg_name):
        try:
            output=self.adb.shell("dumpsys meminfo "+pkg_name).stdout.read().split()
            s_men = ".".join([x.decode() for x in output])  # 转换为string
            #使用正则获取到total表示的mem值
            mem2 = int(re.findall("TOTAL:.(\d+)*", s_men, re.S)[0])
            mem2=round(mem2/1024,2)

        except Exception as e:
            print(e)
            mem2 = 0
        self.writeInfo(mem2, PATH(result+"/mem.yaml"))
        return mem2

    # 得到fps
    def get_fps(self,pkg_name):
        results=self.adb.shell("dumpsys gfxinfo "+pkg_name).stdout.read().strip().decode()

        frames = [x for x in results.split('\n') if validator(x)]
        # print(frames)
        frame_count = len(frames)
        jank_count = 0
        vsync_overtime = 0
        render_time = 0
        for frame in frames:
            time_block = re.split(r'\s+', frame.strip())
            # print(time_block)
            if len(time_block) == 3:
                try:
                    render_time = float(time_block[0]) + float(time_block[1]) + float(time_block[2])
                except Exception as e:
                    render_time = 0

            '''
            当渲染时间大于16.67，按照垂直同步机制，该帧就已经渲染超时
            那么，如果它正好是16.67的整数倍，比如66.68，则它花费了4个垂直同步脉冲，减去本身需要一个，则超时3个
            如果它不是16.67的整数倍，比如67，那么它花费的垂直同步脉冲应向上取整，即5个，减去本身需要一个，即超时4个，可直接算向下取整
    
            最后的计算方法思路：
            执行一次命令，总共收集到了m帧（理想情况下m=128），但是这m帧里面有些帧渲染超过了16.67毫秒，算一次jank，一旦jank，
            需要用掉额外的垂直同步脉冲。其他的就算没有超过16.67，也按一个脉冲时间来算（理想情况下，一个脉冲就可以渲染完一帧）
    
            所以FPS的算法可以变为：
            m / （m + 额外的垂直同步脉冲） * 60
            '''
            if render_time > 16.67:
                jank_count += 1
                if render_time % 16.67 == 0:
                    vsync_overtime += int(render_time / 16.67) - 1
                else:
                    vsync_overtime += int(render_time / 16.67)

        _fps = int(frame_count * 60 / (frame_count + vsync_overtime))
        # writeInfo(_fps, PATH("../info/" + devices + "_fps.pickle"))

        # return (frame_count, jank_count, fps)
        # print("-----fps------")

        # writeInfo(_fps,PATH(result+"/fps.yaml"))
        return _fps

    #获取手机电量
    def get_battery(self):
        try:
            output=self.adb.shell("dumpsys battery").stdout.read().split()
            # output = subprocess.check_output(cmd).split()
            # _batter = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
            #                            stderr=subprocess.PIPE).stdout.readlines()
            st = ".".join([x.decode() for x in output])  # 转换为string
            battery2 = int(re.findall("level:.(\d+)*", st, re.S)[0])

        except:
            battery2 = 90
        self.writeInfo(battery2,PATH(result+"/battery.yaml"))
        return battery2

    #获取测试应用的PID
    def get_pid(self,pkg_name):
        return self.adb.getPid(pkg_name)
    #获取测试应用的UID
    def get_uid(self,pid):
        return self.adb.getUid(pid)
    #获取应用上行、下行流量
    def get_flow(self,uid):
        upflow = downflow = 0
        if uid is not None:
            _flow=self.adb.shell("cat /proc/net/xt_qtaguid/stats |"+ find_util+ " "+uid).stdout.readlines()

            for item in _flow:
                #一个uid可能对应多个进程，所以这两列流量累加求和就行
                rx_bytes=int(item.split()[5].decode()) #第6列为 rx_bytes(接收数据)
                tx_bytes=int(item.split()[7].decode()) #第8列为 tx_bytes(传输数据) 都包含tcp、udp等所有网络流量传输统计。
                downflow+=rx_bytes
                upflow+=tx_bytes
            upflow=round(upflow/1024/1024,2)  #单位MB
            downflow=round(downflow/1024/1024,2)

        self.writeFlowInfo(upflow, downflow, PATH(result + "/flow.yaml"))
        return upflow,downflow


    def totalCpuTime(self):
        user = nice = system = idle = iowait = irq = softirq = 0
        '''
        user:从系统启动开始累计到当前时刻，处于用户态的运行时间，不包含 nice值为负进程。
        nice:从系统启动开始累计到当前时刻，nice值为负的进程所占用的CPU时间
        system 从系统启动开始累计到当前时刻，处于核心态的运行时间
        idle 从系统启动开始累计到当前时刻，除IO等待时间以外的其它等待时间
        iowait 从系统启动开始累计到当前时刻，IO等待时间(since 2.5.41)
        irq 从系统启动开始累计到当前时刻，硬中断时间(since 2.6.0-test4)
        softirq 从系统启动开始累计到当前时刻，软中断时间(since 2.6.0-test4)
        stealstolen  这是时间花在其他的操作系统在虚拟环境中运行时（since 2.6.11）
        guest 这是运行时间guest 用户Linux内核的操作系统的控制下的一个虚拟CPU（since 2.6.24）
        '''
        p=self.adb.shell("cat /proc/stat")
        # cmd = "adb -s " + devices + " shell cat /proc/stat"
        # print(cmd)
        # p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
        #                      stderr=subprocess.PIPE,
        #                      stdin=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        res = output.split()

        for info in res:
            if info.decode() == "cpu":
                # print(res)
                user = res[1].decode()
                nice = res[2].decode()
                system = res[3].decode()
                idle = res[4].decode()
                iowait = res[5].decode()
                irq = res[6].decode()
                softirq = res[7].decode()
                # print("user=" + user)
                # print("nice=" + nice)
                # print("system=" + system)
                # print("idle=" + idle)
                # print("iowait=" + iowait)
                # print("irq=" + irq)
                # print("softirq=" + softirq)
                result = int(user) + int(nice) + int(system) + int(idle) + int(iowait) + int(irq) + int(softirq)
                # print("totalCpuTime" + str(result))
                return result
    '''
    每一个进程快照
    '''

    def processCpuTime(self,pid):
        '''

        pid     进程号
        utime   该任务在用户态运行的时间，单位为jiffies
        stime   该任务在核心态运行的时间，单位为jiffies
        cutime  所有已死线程在用户态运行的时间，单位为jiffies
        cstime  所有已死在核心态运行的时间，单位为jiffies
        '''
        utime = stime = cutime = cstime = 0

        try:
            p=self.adb.shell("cat /proc/"+str(pid)+"/stat")
            # cmd = "adb -s " + devices + " shell cat /proc/" + str(pid) + "/stat"
            # print(cmd)
            # p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
            #                      stderr=subprocess.PIPE,
            #                      stdin=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            res = output.split()

            utime = res[13].decode()
            stime = res[14].decode()
            cutime = res[15].decode()
            cstime = res[16].decode()
            # print("utime="+utime)
            # print("stime="+stime)
            # print("cutime="+cutime)
            # print("cstime="+cstime)
            result = int(utime) + int(stime) + int(cutime) + int(cstime)
            # print("processCpuTime=" + str(result))
        except Exception as r:
            # print('-----异常', r)
            result = 0
        return result


    # 得到几核cpu
    def get_cpu_kel(self):
        output=self.adb.shell("cat /proc/cpuinfo").stdout.read().split()
        # cmd = "adb -s " + devices + " shell cat /proc/cpuinfo"
        # print(cmd)
        # output = subprocess.check_output(cmd).split()
        # output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read().split()
        sitem = ".".join([x.decode() for x in output])  # 转换为string
        # print('几核:----', len(re.findall("processor", sitem)))
        return len(re.findall("processor", sitem))

    '''
    计算某进程的cpu使用率
    100*( processCpuTime2 – processCpuTime1) / (totalCpuTime2 – totalCpuTime1) (按100%计算，如果是多核情况下还需乘以cpu的个数);
    cpukel cpu几核
    pid 进程id
    '''

    def cpu_rate(self,pid, cpukel):
        processCpuTime1 = self.processCpuTime(pid)
        totalCpuTime1 = self.totalCpuTime()
        time.sleep(1)
        processCpuTime2 = self.processCpuTime(pid)
        totalCpuTime2 = self.totalCpuTime()

        processCpuTime3 = processCpuTime2 - processCpuTime1
        totalCpuTime3 = (totalCpuTime2 - totalCpuTime1) * cpukel

        cpu = round(100 * (processCpuTime3) / (totalCpuTime3),2)
        self.writeInfo(cpu,PATH(result+"/cpu.yaml"))
        return cpu
    def writeInfo(self,data, path="data.pickle"):
        _read = self.readInfo(path)
        result = []
        if _read:
            _read.append(data)
            result = _read
        else:
            result.append(data)
        with open(path, 'wb') as f:
            pickle.dump(result, f)
    def readInfo(self,path):
        data = []
        with open(path, 'rb') as f:
            try:
                data = pickle.load(f)
                # print(data)
            except EOFError:
                data = []
                # print("读取文件错误")
        return data
    def writeFlowInfo(self,upflow, downflow, path="data.pickle"):

        _read = self.readInfo(path)
        result = [[], []]
        if _read:
            _read[0].append(upflow)
            _read[1].append(downflow)
            result = _read
        else:
            result[0].append(upflow)
            result[1].append(downflow)
        with open(path, 'wb') as f:
            pickle.dump(result, f)
    def pickleDemo(self,path):
        da=["a","b",2]
        with open(path,"rb") as f:
            try:
                data=pickle.load(f,encoding='utf-8')
            except Exception as e:
                data=[]
                print(e)
        result=[]
        if data:
            data.append(da)
            result=data
        else:
            result.append(data)
        with open(path,"wb") as f:
            pickle.dump(result,f)
        return result
if __name__ == '__main__':
    # writeExcel()
    pkg="com.guokr.mentor"
    men=CpuMem()
    pid=men.get_pid(pkg)
    uid=men.get_uid(pid)

    upflow,downflow=men.get_flow(uid)
    print(upflow,downflow)
    cpu_kel = men.get_cpu_kel()
    print(cpu_kel)
    rate=men.cpu_rate(pid, cpu_kel)
    print(rate)
    '''
    pid = get_pid("com.tengyue360.student", "CLB0218621003370")
    # print(pid)
    # get_flow(pid, "wifi", "DU2TAN15AJ049163")
    z=get_battery("CLB0218621003370")
    print(z)
    '''
