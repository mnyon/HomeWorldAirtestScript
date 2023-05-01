### 使用办法

    下载IDE

    加载项目

### 功能

任务

    条件

    开始执行

SpecificSignalMissionLoop_Test

    测试Progenitor and Relic信号循环 这是个特别的任务仅仅需要用户直接跃迁到目标位置即可 无需多余操作

ProgenitorSignal

    请注意 每个新增的Signal战斗策略都必须和SignalMissionTypeList中的类型Type保持一致

    传递进来一个任务的Jump参数 从这里开始进行操作 所以如果根本没有Jump的时候也不会随便的触发这个部分

    UISource 既可以是Group进入信号也可以是普通的SignalList进入

    destination 最终返回的地方 例如空间站还是留在原地

    这是一个UI模拟战斗功能函数

    先祖任务的描述 这类任务往往是击退两次敌人和回收资源

### 使用注意

    不要自己提前开组队 会影响脚本

    如果你不慎在没有掉线的情况下需要重新开始脚本，那么你需要重新打开游戏，因为当前的游戏不支持退出Group

    

### 参考星系

| Galaxy   | 势力   | Signal           |
| -------- | ------ | ---------------- |
| ACATLAHU | Tanoch | Progenitor Relic |
|          |        |                  |

### 未来预计更改的变动

考虑如果矿机损坏了不能继续执行回收任务怎么处理。

如果可以的话，我们提前保证已经出现了目标信号是最好的，因为似乎有一种情况即便扫描多次也无法得到目标的两个信号。

GameControllor.recordSignalMission() !! 记录信号 这个方法只能按照Progenitor和Relic的顺序记录

FleetCommander.departureWithScan(GameControllor,True)

    FleetCommander 刷新信号任务 从线路出发然后回来

    一旦掉线会通知FleetCommander停下来 然后一会继续
