记一次打败坑爹魅族的手机管家经历
================================
:slug: how-do-i-fvck-flymed
:date: 2017-07-20
:tags: flyme, 折腾

.. contents::

吐槽
----

前两天我的魅族手机终于在过保 10 天前达成了 同一部件损坏成就 [3/3] ！于是根据魅族的售后政策，果断申请了换新。新手机到之后，由于辣鸡魅族不让刷第三方固件，我选择更新到了 flyme 5 的最后一个稳定版本。

之所以没更新到 flyme 6，是因为 6 相比 5 多了很多产品经理帮用户作出的脑残决定。诸如新增了“智能”通知栏，大概是就是把垃圾通知屏蔽了，然而它一点也不智能，经常把我的 Gmail 呀、微信呀之类重要通知屏蔽了，最脑残的是，这货没有白名单机制，也就是说，用户不能选择屏蔽哪些应用不屏蔽哪些应用，所有的屏蔽都是由系统“智能”决定的！还有那个“安全”键盘，每次输密码的时候强制使用，还把数字打乱，极大降低了打字效率。而且这两个功能都是用户没法关闭的，实在是没法忍受。

拿到新手机后，看了看魅族的保修政策，居然又有新的一年的保修期，不得不说，魅族的品控虽然不咋，但售后还真是蛮良心的！无论去售后中心，还是网上客户，或者是电话客户，态度都很棒，这点要点个赞！本来想着过保了就 root，但现在又有了新的一年，不能忍了，所以还是选择了解锁 root。

问题
----

然后新的问题出现了！安装科学上网工具之后，发现居然没法使用！开启 SS 后，基本上每隔半分钟就要重新进入 SS 程序主界面重新唤醒，不能忍啊！你想你在看个网页，每半分钟得切出浏览器再切回来，ingress 放两三个 xmp 又切出去得重新唤醒一次，多难受啊！我尝试找遍了魅族所有能设置的地方，包括自带的手机管家里的自启动权限、后台保留权限、联网权限，一切该设置的都设置了，能拖白名单的地方都拖白名单了，还是没能解决这个问题。而且在联网失败的时候通过 ``ps`` 查看进程，SS 的几个进程完全正常没有被杀，在换手机前使用这个版本的固件也没有出现过这样的问题，所以我一度怀疑是 SS 自己的问题，回滚了 SS 几个版本后，问题依然得不到解决。不能忍了，决心好好研究下这个问题。

折腾
----

既然进程运行正常没有被后台管理杀了，那么如果是程序自己的错误，就应该从日志查起。果然，``adb logcat`` 看到一堆报错！

.. code:: 

    $ adb logcat sha自dso由cks:V *:S
    E/sha自dso由cks(15911): connect: Network is unreachable
    E/sha自dso由cks(15911): connect: Network is unreachable
    E/sha自dso由cks(15911): connect: Network is unreachable
    E/sha自dso由cks(15911): connect: Network is unreachable
    E/sha自dso由cks(15911): connect: Network is unreachable
    E/sha自dso由cks(15924): getpeername: Transport endpoint is not connected
    E/sha自dso由cks(15924): getpeername: Transport endpoint is not connected
    E/sha自dso由cks(15924): getpeername: Transport endpoint is not connected
    E/sha自dso由cks(15924): getpeername: Transport endpoint is not connected
    E/sha自dso由cks(15924): getpeername: Transport endpoint is not connected

而且正好这些报错都是在浏览器无法正常访问后出现，问题应该就在这了。看了看 ss-libev 的代码，应该是在连接远程服务器时出错的，然而我的手机直接访问远程服务器正常啊！好吧，用 ``watch -n1 "netstat -atnp"`` 看看连接状态，发现断网后 SS 不停地进入 SYN_SENT 状态，然后连接马上就断了。那就抓包吧！之前看过万能的百合仙子的一篇 `文章 <https://blog.lilydjwg.me/2015/6/1/wireshark-capturing-over-ssh.95147.html>`_ 讲如何用 wireshark 远程抓包，这次正好用上了：

.. code:: 

    $ nc -l 8899 | wireshark-gtk -i - -k                     # 电脑端 nc 收包然后传给 wireshark
    # tcpdump -U -w - -p -f 'port 8388' | nc <ip_addr> 8899  # 手机端用 tcpdump 抓包发送给 nc

当然似乎可以直接用 adb 执行 ``tcpdump`` 命令把输出传给 wireshark ，然而我对 adb 不熟，不懂怎么直接以 root 执行命令……开始抓包时一切正常，浏览器也能正常访问网页，不到半分钟果然网断了，这时候 wireshark 这边居然一个包都收不到了！之前说过断网的时候 SS 是会调用 ``connect`` 然后进入 SYN_WAIT 状态的，然而现在连 SYN 包的影子都没见到！既然连 TCP 包都直接被阻断了，直接想到就是被内核过滤，执行 ``iptables`` 查看防火墙策略：

.. code:: 

    (ins)root@localhost /# /system/bin/iptables -L -v
    ...
    Chain mobile (13 references)
     pkts bytes target     prot opt in     out     source               destination
        0     0 REJECT     all  --  any    any     anywhere             anywhere             owner UID match u0_a133 reject-with icmp-net-prohibited
        0     0 REJECT     all  --  any    any     anywhere             anywhere             owner UID match u0_a113 reject-with icmp-net-prohibited
        0     0 REJECT     all  --  any    any     anywhere             anywhere             owner UID match u0_a128 reject-with icmp-net-prohibited
    ...
    Chain wifi (1 references)
     pkts bytes target     prot opt in     out     source               destination
       88  5815 REJECT     all  --  any    any     anywhere             anywhere             owner UID match u0_a133 reject-with icmp-net-prohibited
        0     0 REJECT     all  --  any    any     anywhere             anywhere             owner UID match u0_a113 reject-with icmp-net-prohibited
        0     0 REJECT     all  --  any    any     anywhere             anywhere             owner UID match u0_a128 reject-with icmp-net-prohibited
    ...

哈哈，果然！我的 SS 的用户是 u0_a133, 果然是被防火墙过滤了，被过滤的还有其他一些被我添加到联网黑名单的程序！那么到底是什么东西修改的防火墙表呢？想一个一个进程去追踪也没那么容易，只好先看看日志来碰碰运气吧……

.. code:: 

    (ins)root@localhost /# logcat |grep iptables
    E/flymed  (  362): exec() res=0, status=0 for /system/bin/iptables -I wifi -m owner --uid-owner 10133 -j REJECT --reject-with icmp-net-prohibited
    E/flymed  (  362): exec() res=0, status=0 for /system/bin/iptables -I mobile -m owner --uid-owner 10133 -j REJECT --reject-with icmp-net-prohibited

不得不说，运气真是太好，感觉一个月人品都被败光了……明天支付宝的奖励金应该会少很多吧 _(:з」∠)_

丑陋的解决方案
--------------

用 ``ps aux | grep flymed`` 可以看到 flymed 的启动命令是 ``/system/bin/flymed`` 且 ppid 是 1，原生的二进制文件。由于手机管家只是一个普通的安卓应用，而且清除手机管家的数据后再启动手机管家后发现黑名单并没有改变，说明这些黑名单一定是存在手机管家数据之外的地方。之后用 ``strace`` 追踪了 ``flymed`` ，发现这货和手机管家用 unix socket 进行通信，设置黑白名单的时候手机管家通过 socket 传一条指令给 ``flymed`` ， ``flymed`` 收到后会修改防火墙，然而却没有发现任何的文件写入操作，再之后用 ``ls -l /proc/`pidof flymed`/fd`` 查看了这货打开的文件，也没能找到线索。最终用 ``grep`` + 人眼暴力搜索，在 ``/data/system/`` 找到了联网黑名单 ``netpolicy.xml`` ，应用权限配置 ``appops.xml`` ， 然而一切都是正常的，没有对 u0_a133 的封杀规则……所以，我猜对 SS 的联网限制大概又是魅族产品经理/工程师推出的“智能”操作吧……

既然不能通过修改策略完成，那就直接 ``kill `pidof flymed``` 吧！kill 之后发现 init 进程立刻把它重启了 _(:з」∠)_。没办法了，我只好写了个伪程序来把它替换掉了……在电脑上用 ``echo -e '#include<unistd.h>\n#include<limits.h>\nint main(){ for(;;)sleep(UINT_MAX); }' | aarch64-linux-gnu-gcc -xc -s -static -o flymed -`` 交叉编译了一个静态链接的 flymed 然后把 ``/system/bin`` 里的替换掉，再 kill 一次，整个世界都变得美好了。

虽然失去了 flymed 可能会让手机管家没法工作，但是用 xposed 可以很好地解决这个问题吧。除此之外，目前手机还没有出现任何异常。

**EOF**
