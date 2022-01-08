# -*- coding: UTF-8 -*-
'''提供错误报告的基本操作及方法 顺便提供版本更新、安装库等功能'''







def makeZip(sourceDir, outFilename,compression = 8,exceptFile = None):
    '''使用compression指定的算法打包目录为zip文件\n
    默认算法为DEFLATED(8),可用算法如下：\n
    STORED = 0\n
    DEFLATED = 8\n
    BZIP2 = 12\n
    LZMA = 14\n
    '''
    import os, zipfile
    zipf = zipfile.ZipFile(outFilename, 'w',compression)
    pre_len = len(os.path.dirname(sourceDir))
    for parent, dirnames, filenames in os.walk(sourceDir):
        for filename in filenames:
            if filename == exceptFile:
                continue;
            print(filename)
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)   #相对路径
            zipf.write(pathfile, arcname)
        
    zipf.close()
    del zipf,pre_len
#以上函数节选并修改自 正在攀登的小蜗牛 的博客：https://blog.csdn.net/qq_21127151/article/details/107503942







class report():
    '''发送报告以及相应的任务处理'''
    def __init__(self,senderName:str = 'Unknown',senderContact:str = 'None',describetion:str = ''):
        ''':param senderName 发送者名称
        :param senderContact 发送者联系方式
        :param describetion 问题描述'''
        self.senderName = senderName;
        self.senderContact = senderContact;
        self.describetion = describetion;
        if not self.senderName :
            self.senderName = 'Unknown';
        if not self.senderContact :
            self.senderContact = 'None';
    
    
    
    def emailReport(self):
        '''使用E-mail方法发送当前的日志和临时文件等'''
        import smtplib
        from email.mime.text import MIMEText;
        from email.mime.multipart import MIMEMultipart;
        from email.header import Header;
        from oemsup.log import log 
        log("发送错误报告")
        import os;
        log("添加标题与正文")
        msg = MIMEMultipart();
        #发送者与接收者显示名称
        msg["From"] = Header(self.senderName,'utf-8');
        msg["To"] = Header("W-YI (QQ2647547478)",'utf-8');
        #标题
        msg["Subject"] = '奇偶数阵 - 来自 '+self.senderName+' 的错误报告';
        #正文
        msg.attach(MIMEText("来自"+self.senderName+"( "+self.senderContact+" )的错误描述：\n"+self.describetion,'plain','utf-8'));
        log("添加完毕，正在生成压缩包...")
        makeZip("./","Temps&Logs.zip",exceptFile="Temps&Logs.zip");
        attafile=MIMEText(open("Temps&Logs.zip",'rb').read(),"base64",'gb2312');
        attafile["Content-Type"] = 'application/octet-stream';
        attafile["Content-Disposition"] = 'attachment;filename="BugReport_from_'+self.senderName+'.zip"';
        msg.attach(attafile);
        log("完毕，准备发送")
        try:
            smtp = smtplib.SMTP()
            smtp.connect("smtp.163.com");
            smtp.login("RyounDevTeam@163.com","SIQQKQQYCZRVIDFJ");
            smtp.sendmail("RyounDevTeam@163.com",["RyounDevTeam@163.com",],msg.as_string())
            log("错误汇报邮件已发送")
        except smtplib.SMTPException as e:
            log("错误汇报邮件发送失败：\n"+str(e));
        log("清空内存和临时文件")
        del msg,attafile
        os.remove("./Temps&Logs.zip")






class version:

    libraries = ('pyinstaller','py7zr','websockets')
    '''当前所需库，有一些是开发用的，用户不需要安装'''

    version = ('0.0.2','Alpha',)
    '''当前版本'''

    def __init__(self) -> None:

        self.libraries = version.libraries
        '''当前所需库，有一些是开发用的，用户不需要安装'''

        self.version = version.version
        '''当前版本'''

    def installLibraries(self):
        '''安装全部开发用库'''
        from sys import platform
        import os
        if platform == 'win32':
            # 纪念那一段辉煌灿烂的青春年华
            # 以梦想为驱使 创造属于自己的未来
            # import shutil
            # try:
            #     shutil.rmtree(os.getenv('APPDATA')+'\\Musicreater\\')
            # except:
            #     pass;
            for i in self.libraries:
                print("安装库："+i)
                os.system("python -m pip install "+i+" -i https://pypi.tuna.tsinghua.edu.cn/simple")
        elif platform == 'linux':
            os.system("sudo apt-get install python3-pip")
            for i in self.libraries:
                print("安装库："+i)
                os.system("sudo python3 -m pip install "+i+" -i https://pypi.tuna.tsinghua.edu.cn/simple")

