伪·如何在 Linux 下使用深信服 SSL VPN
====================================
:slug: how-to-use-sangfor-sslvpn-in-linux
:date: 2018-01-12
:tags: sangfor, vpn, linux

.. contents::

背景
----

本文大概会很水……

由于要在外网访问校内的资源，包括实验室的服务器什么的，所以学校提供了接入校内的 VPN 服务。三本院校的采用国内著名的深信服 SSL VPN。众所周知，国内各种企业的产品都是没有 Linux 版本的，所以要在 Linux 下使用深信服的 SSL VPN，还是得装个虚拟机 _(:з」∠)_ 好了，感觉读到这里你要就失望了，哎，没办法呀，有谁去破解下辣鸡深信服的 SSL VPN 协议呗？

配置
----
嗯，用 qemu 装个 Bugdows，在 Bugdows 上装个深信服的 EasyConnect。

在 Linux 下创建一个 bridge：

.. code::

    ip l add qbr0 type bridge
    ip l set qbr0 up

启动虚拟机的时候需要给 Windows 添加两块网卡，一块采用 user 模式，也就是 `SLiRP <https://en.wikipedia.org/wiki/Slirp>`_ 模式，另一块采用 bridge 模式：

.. code::

    qemu-system-x86-64 \
    -netdev user,id=mynet0,net=192.168.76.0/24,dhcpstart=192.168.76.9 \
    -device virtio-net,netdev=mynet0 \
    -netdev bridge,id=mynet1,br=qbr0 \
    -device virtio-net,netdev=mynet1 \
    ...

这一步 qemu 会利用 qemu-bridge-helper 自动创建一个 tap 设备，并且把这个 tap 连到 qbr0 里。因为 qemu-bridge-helper 是 setuid 的，qemu-bridge-helper 会检查授权，如果这一步出现 ACL 错误提示，需要在 ``/etc/qemu/bridge.conf`` 里添加上 ``allow qbr0`` ，如果要允许接入任意的网桥，就添加 ``allow all`` 。

启动 Windows，启动 EasyConnect，这时 Windows 下应该出现 3 块网卡，一块 user 模式，我们叫它「Network 1」，一块是 bridge 模式，叫他「Network 2」，还有一个是 SSL VPN 的虚拟网卡，叫它「spicy chicken sangfor」。下面把 Linux 称为 Host，Windows 称为 Guest。

- 「Network 1」用于接入互联网，这块网卡只能从 Guest 访问 Host，没法从 Host 访问 Guest，类似与 vbox 的 NAT 模式；
- 「Network 2」用于 Host 和 Guest 间的相互通信，这里主要是把 Host 的数据传个 VPN；
- 「spicy chicken sangfor」当然是用来访问内网了。

这时候共享 「spicy chicken sangfor」，右键属性 -> 共享 -> 选「Network 2」 -> 确定。之后 Windows 会自动把「Network 2」的 IP 设置成 192.168.137.1，并且在这个网络上启动一个 DHCP 服务器。我不太懂 Windows 为啥要把 IP 改成这个，用原来的不好么？

在 Linux 上对 qbr0 启动 dhcpcd，qbr0 会自动分配到一个 192.168.137.X/24 的地址，当然也可以手动设置，只要在这个网段内就可以了。再配置一下路由表，让内网的 IP 走 qbr0 接口就好了：

.. code::

    ip r add 10.0.0.0/8 via 192.168.137.1 dev qbr0

画张图
------
其实很好理解，现在访问内网的路由大概是这样：

.. code::

                                   (VPN)                          (ICS)
    Guest(Windows)    [Network 1] <----- [spicy chicken sangfor] <----- [Network 2]
                           |                                                 ^
                           | (SLiRP)                                         |
    -----------------------|-------------------------------------------------|-------------
                           |                                                 |
                           v                                                 |
    Host(Linux)          [eth0]                                           [qbr0] <- [tap0]
                           |                                                          ^
                           v                                                          |
                         target                                                    request

**EOF**
