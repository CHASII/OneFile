
### 配置说明
> 路径:/etc/pfile/config.ini

#### 参数
* Ftp VSFtp服务信息

|配置项|说明|备注|
|:-:|:-:|:-:|
|Host|VSFtp主机|
|User|VSFtp用户||
|Passwd|VSFtp密码||

* Yourls 短网址服务信息

|配置项|说明|备注|
|:-:|:-:|:-:|
|Host|Yourls主机||
|User|Yourls用户||
|Passwd|YOurls用户密码||

* Ngx NginX服务信息

|配置项|说明|备注|
|:-:|:-:|:-:|
|Host|Nginx主机|注意域名最后面必须+/|
|User|Nginx Basic Auth用户||
|Passwd|Nginx Basic Auth密码||

### 执行命令
`pfile /data/Software/sougou_pinyin.deb`

2018-04-12 11:53:26,072 - INFO : Uploading /data/Software/sougou_pinyin.deb Into VSFtp...  
2018-04-12 11:53:26,085 - WARNING : /data/Software/sougou_pinyin.deb no a compressed file!  
2018-04-12 11:53:26,085 - INFO : Compressing /data/Software/sougou_pinyin.deb  
2018-04-12 11:53:26,380 - INFO : Compressed Success.  
2018-04-12 11:53:26,466 - INFO : Uploaded Success.  
2018-04-12 11:53:26,467 - INFO : Converting Down Url to Short Url...  
2018-04-12 11:53:26,618 - INFO : Shorted Success.

\-------文件信息--------  
文件名称-sougou_pinyin.deb  
下载链接-http://u.io/1d  
验证账号-test  
验证密码-test