# coding=utf-8
#!/usr/bin/python
import os
import xml.dom.minidom
class ParseXml(object):
    #读取xml并返回
    def getXmlParser(self):
        xmlJson=dict()
        dom = xml.dom.minidom.parse("perverifyChajianEnv.xml")
        root = dom.documentElement

        startenv = root.getElementsByTagName('startEnv')
        Mypack = startenv[0].getAttribute("Package")
        xmlJson['Package']=Mypack
        startActi = startenv[0].getAttribute("Activity")
        xmlJson['Activity']=startActi
        eventinterval = startenv[0].getAttribute("eventinterval")
        xmlJson['eventinterval'] = eventinterval

        type = root.getElementsByTagName("type")
        type_name = type[0].getAttribute("name")
        xmlJson['type_name'] = type_name

        monkeyCmd=type[0].getAttribute("monkeyCmd")
        xmlJson['monkeyCmd']=monkeyCmd
        executeTotalAction=type[0].getAttribute("executeTotalAction")
        xmlJson['executeTotalAction']=executeTotalAction

        devId = root.getElementsByTagName("deviceId")
        UDID = devId[0].getAttribute("UDID")
        xmlJson['UDID'] = UDID
        return xmlJson
    def mkdir_file(self):
        """

        :return:创建日志存放文件夹 并返回dict json格式的列表
        """
        xmlDir=self.getXmlParser()
        resultDir=xmlDir['resultFileDir']

        file_list =dict()
        file_list['imgdir']=resultDir+'img/'
        file_list['logdir']=resultDir+'log/'
        file_list['perdir']=resultDir+'per/'
        if not os.path.exists(resultDir):
            os.mkdir(resultDir)
        for key,file_path in file_list.items():
            if not os.path.exists(file_path):
                os.mkdir(file_path)
        return file_list
    def all_file_path(self,root_directory, extension_name):
        """

        :return: 遍历文件目录
        """
        file_dic = {}
        for parent, dirnames, filenames in os.walk(root_directory):
            for filename in filenames:
                if 'filter' not in filename:
                    if filename.endswith(extension_name):
                        path = os.path.join(parent, filename).replace('\\', '/')
                        file_dic[filename] = path
        return file_dic
