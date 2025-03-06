# HWcloud_ddns

# 使用场景

自动将华为云上管理的域名解析到当前设备所在网络的公网IP

# 起源

在合租屋内，多人的路由器通过DHCP连接光猫上网，因此不太方便将光猫设置为桥接模式，并用路由器拨号上网，因此虽然光猫有公网IP，但在路由器上也无法直接实现DDNS，而光猫的DDNS服务局限性太大，无法操作华为云的域名。

所以写了这个简单的项目，来在局域网的电脑上获取光猫的公网IP，然后操作华为云域名解析实现DDNS。

# 思路

首先需要在局域网的电脑上获取光猫的公网IP，这里有多种方法。有一些API提供了这样的功能，但我找了一圈，要么是国外的连不上，要么是收费的。但很多网站提供了查看自己公网IP的功能，因此使用爬虫进行获取也是可以的。但无论是使用爬虫，还是寻找免费的API，还需要注册API，这都太麻烦了。所以在拥有自己的云服务器的情况下，我直接利用Flask写了一个简单的获取公网IP的API。（app.py）

可以获取公网IP后，下一步就是对华为云的域名解析服务进行操作了。这里都是使用华为云提供的python SDK来实现的，这样可以免去很多鉴权方面的繁琐操作。

在华为云上进行域名解析操作我们需要知道自己需要操作的域名的zone_id和recordset_id，这些id从控制台是找不到的，只能从华为云提供的API获取，get_id.py就是用来获取自己账户下所有的zone_id和recordset_id的。

同样使用华为云提供的SDK来操作域名解析（ddns.py）

最后只需要定时获取公网IP然后进行比对，判断公网IP是否发生了变化，如果发生变化，则运行ddns.py对域名解析进行修改。这里还增加了发送邮件提醒的功能。使用SMTP服务进行邮件发送。

# 使用方法

首先安装好所有了依赖库，并且你有一台具有公网IP的服务器，或者你可以通过其他方式获取到自己的公网IP。

如果你有自己的服务器，请将app.py放到你的服务器中，并运行，此时通过http://ip:5010/get_ip即可获取到自己的公网IP。请注意开放服务器端口和云服务器安全组。

然后将ddns.py中的AK和SK设置为你的华为云账号的AK和SK，我这里是将其添加到了环境变量中，但你也可以直接写到代码中。然后运行ddns.py，他将获取你的账户下所有的域名和记录集的zone_id和recordset_id，并记录到ids.txt中，从中找到你所要操作的解析记录的zone_id和recordset_id，填入getip.py中对应的部分。

在getip.py中你还需要设置发送邮件的相关信息，也可以删除此部分。

最后在run.py中设置你希望进行IP检查的时间间隔，然后运行run.py即可，后面也可以通过run.bat一键启动服务。

# 与我联系

如果你还有什么疑问或者遇到了什么问题，可以微信联系 lyzds2017
