#!/usr/bin/env python
# coding:utf-8
'''
This Scripts help Ops Upload Some Files Like JvmDump,APPLogFile To Ftp Server And
Return Ftp InfoMation About Those Files With Short Urls And Authentication!

'''

import ConfigParser
import argparse
import ftplib
import json
import logging
import os
import sys
import tarfile
import random
import string
import requests
from requests.auth import HTTPBasicAuth

FORMAT = '%(asctime)-15s - %(levelname)s : %(message)s'
logging.basicConfig(format=FORMAT,level=logging.INFO)
logger = logging.getLogger(__name__)


#Operation LogFile in VSFtp
class My_Ftp(object):

    def __init__(self):
        self.host = Ftp_Host
        self.user = Ftp_User
        self.passwd = Ftp_Passwd

    def Compress(self,FileName):
        try:
            logger.info("Compressing {0}".format(FileName))
            os.chdir(os.path.dirname(os.path.abspath(FileName)))
            # Set Compress File Path to tmp
            random_str = str(''.join(random.sample(string.digits + string.letters, 6)))
            New_Ftp_FileName = os.path.join('/tmp','{0}_{1}.tar.gz'.format(FileName.split('/')[-1],random_str))
            # Set Compress File Path and Compress model
            archive = tarfile.open(New_Ftp_FileName, 'w:gz')
            # Add which File would be Compress
            archive.add(FileName)
            archive.close()
            return New_Ftp_FileName
        except Exception as e:
            logger.error(str(e))
        finally:
            logger.info("Compressed Success.")

    # Processing Dir
    def  Dir(self,DirName):
        for root, dir, files in os.walk(DirName):
            if len(files) < int(File_Counts):
                for file in files:
                    # 只遍历一级目录
                    if DirName == root:
                        self.File(os.path.join(root, file))
            else:
                logger.error("To many Files in {0}，Ensure less than {1} files！".format(root,File_Counts))
                sys.exit()

    #Processing File
    def File(self,FileName):
        try:
            logger.info('Uploading {0} Into VSFtp...'.format(FileName))
            self.ftps = ftplib.FTP(host=self.host,user=self.user,passwd=self.passwd)
            WelCome=self.ftps.getwelcome()
            logging.debug(WelCome)
            bufsize = 1024
            if  tarfile.is_tarfile(FileName):
                    fp = open(FileName, 'rb')
                    random_str = str(''.join(random.sample(string.digits + string.letters, 6)))
                    FileName = random_str + FileName.split('/')[-1]
                    self.ftps.storbinary('STOR ' + FileName, fp, bufsize)
            else:
                logger.warn(FileName + ' no a compressed file!')
                FileName = self.Compress(FileName)
                fp = open(FileName, 'rb')
                # Set Ftp FileName could not include Path
                self.ftps.storbinary('STOR ' + FileName.split('/')[-1], fp, bufsize)
                os.remove(FileName)
            self.ftps.quit()
            self.ftps.close()
            logger.info("Uploaded Success.")
            My_Ngx().Check(Ngx_Host + FileName.split('/')[-1])
        except Exception as e:
            logging.error(str(e))
            sys.exit()

# Check LogFile Correctness
class My_Ngx(object):
    def __init__(self):
        self.host = Ngx_Host
        self.User = Ngx_User
        self.passwd = Ngx_Passwd

    def Check(self,url):
        try:
            logger.info("Converting Down Url to Short Url...")
            self.Url_Code = requests.get(self.host, auth=HTTPBasicAuth(self.User, self.passwd)).status_code
            if int(self.Url_Code) == 200:
                self.Url_Code = requests.get(url, auth=HTTPBasicAuth(self.User, self.passwd)).status_code
                if self.Url_Code == 200:
                    My_Yourls().Short(url)
                else:
                    logger.info(url + ' Not Exit!')
            else:
                logger.info(self.host + ' Ngx BasicAuth User or Password Incorrect!')
        except Exception as e:
            logger.error(str(e))
            sys.exit()


# Operation Urls in Yours
class My_Yourls(object):
    def __init__(self):
        self.host = Yourls_Host
        self.user = Yourls_User
        self.passwd = Yourls_Passwd

    def Short(self,url):
        try:
            args = 'username=%s&password=%s&action=%s&url=%s&format=json' % (self.user, self.passwd, 'shorturl', url)
            resp = requests.get(self.host,args)
            content = json.loads(resp.content)
            # global shorturl
            original_file = url.split('/')[-1].split('.tar.gz')[0]
            short_url = content['shorturl']
            down_info = "文件名称：{0}\n下载链接：{1}".format(original_file,short_url)
            Pfile_Msg.append(down_info)
            logger.info("Shorted Success.")
        except Exception as e:
            logger.error(str(e))
            sys.exit()


    def OutPut(self):
        print("\n------------------- 下载信息 -------------------")
        for list in Pfile_Msg:
            print(list)
            print('--------')
        print("验证账号：{0}\n验证密码：{1}\n".format(Ngx_User,Ngx_Passwd))


if __name__ == '__main__':
    # --------------
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '/etc/pfile/conf.ini')
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    # --------------
    Ftp_Host = config.get('Ftp', 'Host')
    Ftp_User = config.get('Ftp', 'User')
    Ftp_Passwd = config.get('Ftp', 'Passwd')
    File_Counts = config.get('Ftp', 'FileCounts')
    # --------------
    Yourls_Host = config.get('Yourls', 'Host')
    Yourls_User = config.get('Yourls', 'User')
    Yourls_Passwd = config.get('Yourls', 'Passwd')
    # --------------
    Ngx_Host = config.get('Ngx', 'Host')
    Ngx_User = config.get('Ngx', 'User')
    Ngx_Passwd = config.get('Ngx', 'Passwd')
    # --------------
    Pfile_Msg = []
    # --------------

    def isfile(string):
        if os.path.isfile(string):
            return True
        else:
            msg = "%r is not a file" % string
            logger.error(argparse.ArgumentTypeError(msg))
            # print argparse.ArgumentTypeError(msg)
            return False

    def isdir(string):
        if os.path.isdir(string):
            return True
        else:
            msg = "%r is not a dir" % string
            logger.error(argparse.ArgumentTypeError(msg))
            # print argparse.ArgumentTypeError(msg)
            return False

    #创建一个解析对象
    parser = argparse.ArgumentParser(description='Description:Put Files or Dirs to Some One Who Need.')
    #向该对象中添加你要关注的命令行参数和选项
    parser.add_argument("-f", "--file", type=isfile, help="Archive File into VsFtp and Short Down Url")
    parser.add_argument("-d", "--dir", type=isdir, help="Archive Dir into VsFtp and Short Down Url")

    #解析对象
    args = parser.parse_args()

    if args.file:
        archive_args = sys.argv[2]
        My_Ftp().File(archive_args)
        My_Yourls().OutPut()
    if args.dir:
        archive_args = sys.argv[2]
        My_Ftp().Dir(archive_args)
        My_Yourls().OutPut()