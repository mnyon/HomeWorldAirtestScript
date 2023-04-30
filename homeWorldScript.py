from airtest.core.api import *
import threading

# 请按照路线顺序安排 用来当作循环航路的路线设计 可以用作刷新信号
travelingGalaxyPlanList = [
    "./resources/galaxyNameList/DEVADAASI.png", 
    "./resources/galaxyNameList/NIIREA PAAS.png", 
    "./resources/galaxyNameList/KALUARI.png",
    "./resources/galaxyNameList/KEID.png", 
    "./resources/galaxyNameList/VISAAN KI.png", 
    "./resources/galaxyNameList/JONALLI.png",
    "./resources/galaxyNameList/LIUSATA.png",
    "./resources/galaxyNameList/KISHO RE.png",
    "./resources/galaxyNameList/SOBEL REM.png",
    "./resources/galaxyNameList/BESCAVA.png",
    "./resources/galaxyNameList/LARCAVA.png"
    ]

# 需要进行信号任务的类型
SignalMissionTypeList = [
    {
        "path": "./resources/signalType/ProgenitorSignal.png",
        "signalType": "ProgenitorSignal"
    },
    {
        "path": "./resources/signalType/RelicSignal.png",
        "signalType": "RelicSignal"
    }
]

# 起始站是特殊的信号点,从这个点开始反复的进行信号处理任务
specialSignalMissionLoop =[
    "./resources/galaxyNameList/COIXL.png",
    "./resources/galaxyNameList/IXTLAN.png",
    "./resources/galaxyNameList/TECOACUI.png",
    "./resources/galaxyNameList/TELAPENTE.png",
    "./resources/galaxyNameList/CUERNAVA.png",
    "./resources/galaxyNameList/ZEMPOALA.png",
    "./resources/galaxyNameList/TEPECOAL.png"
]


class GameControllor:
    # 并发的任务 用来检查
    def __init__(self):
        self.test = True
        self.galaxySignalMissionReady = True
        # no need to init at first 
        self.lostConnectionCheck = False
        # 按照5分钟的周期检查掉线情况
        self.connectionCheckInterval = 60 * 5
        # 初始化掉线检查线程变量
        self.checkLostConnectThread = None
    
    def checkGameStarted(self):
        # 检查游戏是否启动并启动
        app_checker = AppChecker("HomeWorld", "com.stratospheregames.nimbusgbx")
        app_checker.launch_app()
        stop_app("com.stratospheregames.nimbusgbx")

    def launch_app(self):
        # 启动游戏
        print(f"Launching {self.app_name}...")
        start_app(self.package_name)
        sleep(5)
    
    def close_app(self):
        # 关闭游戏
        if self.check_app():
            print(f"Closing {self.app_name}...")
            stop_app(self.package_name)
            sleep(5)
            if not self.check_app():
                print(f"{self.app_name} is closed!")   

    def resetToMainScreen(self):
        # 点击Combat
        touch([1122, 93])
        sleep(3.0)
        touch([1122, 93])
        # 检查当前正在MainScreen
        playerHeadPicCheck = exists(Template(r"./resources/customFeature/playerPic.png", record_pos=(-0.446, -0.231), resolution=(1600, 900)))
        if playerHeadPicCheck:
            return True 
        else:
            # something wrong 
            log("某些奇怪的错误发生了,为什么没有回到主界面?")
            return False
    
    def moveToSystemScreen(self):
        # 进入System界面 当前的界面似乎不需要什么前置条件 但是在商店不行
        # into system
        touch([1251, 93])
        # 进入系统需要一定的缓冲刷新
        sleep(5.0)
        return True
    
    def openSignalList(self):
        # 打开信号列表
        touch([1508,368])
        return True

    def toScan(self):
        # 开始扫描 应该配合进入System或者Galaxy使用!
        # 请注意 一次调用只进行了一次的扫描
        log("准备开始扫描!")
        # Scan!
        touch([800, 715])
        # 防止没有点上 再来一次
        touch([800, 715])
        # Focus!! 我的传感器需要大约8s的时间重复
        sleep(8.0)
        return True
    
    def goToGalaxy(self):
        # open galaxy screen
        touch([1381, 91])
        sleep(5.0)
        return True

    def goToGalaxyAndOpenList(self):
        # make sure that you are in the main screen to do this
        # open galaxy screen
        touch([1381, 91])
        sleep(5.0)
        # Click and open galaxy list
        touch([1513, 370])
        sleep(5.0)
    
    def checkLostConnect(self,FleetCommander,MissionCommander):
        # Main 按照一定的周期检查掉线 我们就两个都传递进来吧! 我设计的太垃圾了
        first_time = True
        while True:
            if not first_time:
                log("舰队领航员:准备检查连接情况")
                # 检查是否存在掉线状态
                warningFlagCheck = exists(Template(r"./resources/lostConnectionFeature/WarningFlag.png", record_pos=(0.002, -0.092), resolution=(1600, 900)))
                # 提高检查速度 不进行第二个检查了
                # restartGameCheck = exists(Template(r"./resources/lostConnectionFeature/RestartGameButton.png", record_pos=(0.003, 0.168), resolution=(1600, 900)))
                # warningFlagCheck == False and restartGameCheck == False
                if warningFlagCheck == False:
                    log("连接状态良好")
                    # 舰队可以继续执行任务
                    FleetCommander.workingState = True
                    MissionCommander.connectionReadyToWorkFlag = True
                    # 继续周期性检查掉线情况 
                    sleep(self.connectionCheckInterval)
                # 准备重新连接
                # if warningFlagCheck or restartGameCheck:
                if warningFlagCheck:
                    log("舰队领航员:检查到掉线情况发生,准备重新连接")
                    # 侦测到连接中断,通知舰队停止行动
                    FleetCommander.workingState = False
                    MissionCommander.connectionReadyToWorkFlag = False
                    # click restart button
                    touch([800,720])
                    # 加载时间缓冲
                    sleep(60.0)
                    # 确认是否加载成功 检查是否可以StartGame
                    startGameCheck = exists(Template(r"./resources/startGameFeature/startGameButton.png", record_pos=(-0.001, 0.197), resolution=(1600, 900)))
                    if startGameCheck==False :
                        # 如果没有加载成功那么延迟继续加载
                        sleep(30.0)
                        startGameCheck = exists(Template(r"./resources/startGameFeature/startGameButton.png", record_pos=(-0.001, 0.197), resolution=(1600, 900)))
                        if startGameCheck==False :
                            # 重大错误出现 准备Log
                            log("something wrong happened.. Please check your network connection")
                    # 准备开始连接到游戏
                    startGameFinishedCheck = self.startGameandClearAdvertisement()
                    if startGameFinishedCheck == True:
                        # 舰队可以继续执行任务
                        FleetCommander.workingState = True
                        MissionCommander.connectionReadyToWorkFlag = True
                    # 继续周期性检查掉线情况
                    sleep(self.connectionCheckInterval)
            else:
                # 第一次执行的时候并不进行检查 放行舰队行动
                # 舰队可以继续执行任务
                FleetCommander.workingState = True
                MissionCommander.connectionReadyToWorkFlag = True
                sleep(self.connectionCheckInterval)
            first_time = False

    def startGameandClearAdvertisement(self):
        # 准备开始检测是否存在目标
        welcomeFlagCheck = exists(Template(r"./resources/startGameFeature/welcomeFlag.png", record_pos=(-0.081, -0.221), resolution=(1600, 900)))
        startGameButtonCheck = exists(Template(r"./resources/startGameFeature/startGameButton.png", record_pos=(-0.002, 0.197), resolution=(1600, 900)))

        # 只要检查到其中一个可以启动游戏的特征就可以继续
        if welcomeFlagCheck or startGameButtonCheck:
            # 点击开始游戏按钮
            touch([790,766])
            # 游戏加载时间
            sleep(35.0)
        # 检查加载情况 实际上这个地方可以利用Train的当前位置进行检查 
        # closeButtonCheck = exists(Template(r"tpl1682335645537.png", record_pos=(0.445, 0.004), resolution=(1600, 900)))
        # 等待游戏加载时间长一点 这是一个可能错位的地方
        sleep(30.0)


        # 广告界面的关闭
        log("准备关闭广告", desc="初始化过程", snapshot=True)
        touch([1064,105])
        # 短暂的加载时间
        sleep(10.0)
        # 检查是否进入游戏MainScreen
        checkEnterGameState = exists(Template(r"./resources/customFeature/playerPic.png", record_pos=(-0.446, -0.231), resolution=(1600, 900)))
        # 检查当前是否进入游戏界面
        return checkEnterGameState
    
    def startCheckLostConnect(self, FleetCommander,MissionCommander):
        # 开始执行checkLostConnect方法
        # 如果线程已经在运行，那么就不需要再启动了
        if self.checkLostConnectThread is not None and self.checkLostConnectThread.is_alive():
            return
        # 创建一个新的线程
        self.checkLostConnectThread = threading.Thread(target=self.checkLostConnect, args=(FleetCommander,MissionCommander))
        # 将线程设置为守护线程，这样当主线程结束时，子线程也会随之结束
        self.checkLostConnectThread.daemon = True
        # 启动线程
        self.checkLostConnectThread.start()
    
    def stopCheckLostConnect(self):
        # 停止执行checkLostConnect方法
        # 如果线程已经在运行，那么就停止它
        if self.checkLostConnectThread is not None and self.checkLostConnectThread.is_alive():
            self.checkLostConnectThread.stop()
    def clickSkipButton(self):
        # click skip
        touch([1408, 677])
        sleep(1.0)
        touch([1408, 677])
    
    def openSocial(self):
        # 开始条件 应该是主界面 不然点不了右上角的图标
        # open channel list
        touch([1521, 72])
        sleep(1.0)
    
    def switchToChat(self):
        # 打开通信之后确定不是进入邮箱而是通信列表
        # open chat list
        touch([1309, 106])
        log("确认切换到ChatList")
        sleep(1.0)
    
    def openChatTextInputLine(self):
        # 打开输入框 但是还没有输入内容
        # open text line
        touch([1053, 837])
        sleep(1.0)
    
    def inputTextAndSend(self):
        # input输入框输入内容 请提前已经打开输入框了 也就是已经打开输入法界面了
        # ready to create channel 准备开始在输入框输入内容
        # 清除输入框内容
        for i in range(10):
            keyevent("KEYCODE_DEL")
        text("/join 21", enter=True)
        sleep(1.0)
        # confirm inputline 系统输入框的确认按钮
        touch([1493, 802])
        sleep(1.0)
        # 点击游戏内的输入信息的绿色的回车
        touch([1496, 816])
        sleep(1.0)
    
    def openGroupList(self):
        # open group list
        # click group
        touch([1514, 557])
        log("打开GroupList")
        sleep(1.0)
    
    def createGroup(self):
        # create group 创建队伍
        log("准备点击创建队伍按钮")
        # create group
        touch([1187, 456])
        sleep(1.0)
    
    def closeSocialList(self):
        touch([1514,54])
        log("关闭Social功能!")
    
    def joinChannelAndGroup(self):
        # 用来加入频道并进入队伍 从主界面(可能)来最后回到主界面
        log("准备开始创建Group")
        self.openSocial()
        self.switchToChat()
        self.openChatTextInputLine()
        self.inputTextAndSend()
        log("成功加入频道21!")
        self.openGroupList()
        self.createGroup()
        log("成功加入Group!")
        self.closeSocialList()
        self.resetToMainScreen()
        
    def closeCommunicationLsitUI(self):
        # 相当于也关闭GroupUI 
        # 关闭通信界面
        touch([1513, 57])
        sleep(1.0)

    def findSignalStartButtonAndBeginMission(self) -> bool:
        # 选中一个Signal之后检索Start按钮进入
        startButtonExistCheck = exists(Template(r"./resources/commonCommand/SignalStartButton.png", record_pos=(0.253, 0.072), resolution=(1600, 900)))
        if startButtonExistCheck == False:
            return False
        log("导航员:准备进入战场!")
        touch(startButtonExistCheck)
        return True
        
    def emergencyJump(self):
        # 在战场上紧急跃迁
        # 直接点击目标位置退出
        touch([1195, 96])
        sleep(2.0)
        # 触发确认
        touch([1385, 91])

    def recordSignalMission(self):
        # 假设已经完成了队伍创建 并且已经刷新出来了两个信号 现在等待记录两个信号 
        # TODO 现在只能直接固定两个类型的任务 第一个是Progenitor 同类型的还有Tanoch 第二个是Relic
        log("准备开始信号记录到Group")
        self.resetToMainScreen()  # 从主界面开始这个任务
        self.moveToSystemScreen()
        self.openSignalList()
        # locate Progenitor mission
        typeOne_1 = exists(Template(r"./resources/signalType/ProgenitorSignal.png", record_pos=(0.258, -0.095), resolution=(1600, 900)))
        typeOne_2 = exists(Template(r"./resources/signalType/TanochSignal.png", record_pos=(0.258, -0.095), resolution=(1600, 900)))
        resultOne = typeOne_1 or typeOne_2
        if resultOne:
            log("准备记录Progenitor信号")
            touch(resultOne)
            sleep(3.0)
            self.findSignalStartButtonAndBeginMission()
            self.clickSkipButton()
            
            sleep(45.0)             # 保证战场加载完毕的最小时间
            self.emergencyJump()
            log("信号记录完毕,准备跃迁!")
            
            self.clickSkipButton()  # 需要这一步骤 防止舰队人没有快速归队
            
            sleep(40.0)             # 保证真的加载完毕的最小时间
            log("Progenitor信号准备完毕!")
        else:
            log("Progenitor信号检索失败,没有发现该信号")
            return False
        log("准备开始信号记录到Group")
        self.resetToMainScreen()
        self.moveToSystemScreen()
        self.openSignalList()
        # locate second mission
        secondMission = exists(Template(r"./resources/signalType/RelicSignal.png", record_pos=(0.253, 0.031), resolution=(1600, 900)))
        if secondMission:
            log("准备记录Relic信号")
            touch(secondMission)
            sleep(3.0)
            self.findSignalStartButtonAndBeginMission()
            self.clickSkipButton()
            sleep(45.0)             # 保证战场加载完毕的最小时间
            self.emergencyJump()
            self.clickSkipButton()  # 需要这一步骤 防止舰队人没有快速归队
            sleep(40.0)             # 保证真的加载完毕的最小时间
            log("Relic信号准备完毕!")
        else:
            log("Relic信号检索失败,没有发现该信号")
            return False
        return True

    def openResourceAndTargetListUI(self):
        touch([1506, 545])  # 打开物资列表 蓝色舰队图标
        sleep(1.0)


    def AbandonedFreightContainerLocate(self):
        # 返回False或者成功执行
        # AbandonedFreightContainer 物资检查
        AbandonedFreightContainerLocation = exists(Template(r"./resources/signalResources/AbandonedFreightContainer.png", record_pos=(
            0.281, -0.096), resolution=(1600, 900)))
        # 打开物资控制面板
        if AbandonedFreightContainerLocation:
            touch(AbandonedFreightContainerLocation)
            sleep(1.0)
            return True
        else:
            return False
    def ProgenitorArtifactLocate(self):
        # AbandonedFreightContainer 物资检查
        resourceCheck = exists(Template(r"./resources/signalResources/ProgenitorArtifact.png", record_pos=(0.249, -0.095), resolution=(1600, 900)))
        # 打开物资控制面板
        if resourceCheck:
            touch(resourceCheck)
            sleep(1.0)
            return True
        else:
            return False
    def TargetPositionLocate(self):
        # TargetPosition 物资检查
        resourceCheck = exists(Template(r"./resources/signalResources/TargetPosition.png", record_pos=(0.281, -0.096), resolution=(1600, 900)))
        # 打开物资控制面板
        #if resourceCheck:
        #    touch(resourceCheck)
        #    sleep(1.0)
        #    return True
        #else:
        #    return False
        touch([1235,301])
        sleep(1.0)
    def moveToTargetResources():
        # !! 开启目标资源行动之后开始准备舰队移动
        # 绿色的Move操作
        #destinationCoordinates = exists(Template(r"./resources/commonCommand/fleetMoveTo.png", record_pos=(0.329, 0.038), resolution=(1600, 900)))
        #if destinationCoordinates:
            #touch(destinationCoordinates)
            # 这里只能模拟情况了 很难直接检查到是否已经到达目标位置
            #sleep(40.0)
        touch([1232,492])
        sleep(1.0)

    def collectorInterpack():
         # collectorInterpack 矿机准备进行回收工作
        interpackCheck = exists(Template(
                r"./resources/commonCommand/Interpact.png", record_pos=(0.229, 0.036), resolution=(1600, 900)))
        if interpackCheck:
                touch(interpackCheck)
                # 给出足够的行动时间
                sleep(5.0)
                return True
        else:
            return False
    
    def rewardSettlement(self):
        communicationsOfficerCheck = exists(Template(
            r"./resources/signalResources/communicationsOfficer.png", record_pos=(-0.336, -0.149), resolution=(1600, 900)))
        if communicationsOfficerCheck:
            touch([821, 340])       # 和通信官对话,触发奖励结算
            touch([821, 340])
            touch([821, 340])
            touch([821, 340])
            sleep(13.0)             # 等待奖励结算
            return True
        else:
            return False

    def signalFinishedDecision_stay():
        # 留在原地
        touch([597, 775])

    def signalFinishedDecision_station():
        # 返回空间站
        touch([977, 778])

class FleetCommander:
    # 管理所有舰队的Galaxy行动
    def __init__(self):
        # Template list
        self.stations = []
        # 记录当前在第几章
        self.current_station_index = 0
        # 从起始站出发为正方向设置为1 终点为反方向设置为-1
        self.direction = 1
        # 当前是否可以执行任务
        self.workingState = False

    def callMethodByName(methodName, targetClass,*args):
        # 这里定义了一个工具类函数它的意义是为了通过一个字符串来调用一个方法
        # 该方法返回一个函数的指向 仍然需要手动调用
        targetMethod = getattr(targetClass, methodName)
        # 执行我们需要的目标方法
        targetMethod(*args)
    
    def initGalaxyTemplateResources(self,imagePathList):
        # 初始化一个路线
        for elem in imagePathList:
            # 此处的record_pos已经优化为GalaxyList的UI框内,提高了很多准确程度
            self.stations.append(Template(elem,record_pos=(0.284, 0.014),resolution=(1600, 900)))
        # default 分辨率
    def next_station(self, one_loop=False):
        # 只能在起始站出发 不可以从中间的站点出发
        # one_loop 参数，如果传递为 True，则在遍历完整个数组后，只会进行一次循环。
        # 返回Template
        if self.current_station_index == 0:
            # 如果当前站点是第一个站点，设置方向为向后移动
            self.direction = 1
        elif self.current_station_index == len(self.stations) - 1:
            # 如果当前站点是最后一个站点，根据参数值设置方向
            if one_loop:
                # 如果只需要循环一次，则不再改变方向，直接返回 False
                self.direction = 0
                return False
            else:
                # 否则，改变方向为向前移动
                self.direction = -1
        # 计算下一站的索引
        next_index = self.current_station_index + self.direction
        # 如果到达了数组的末尾或开头，则根据参数值返回 False 或 True
        if next_index >= len(self.stations) or next_index < 0:
            return not one_loop
        # 更新当前站点索引
        self.current_station_index = next_index
        
        # 返回下一站的定位资源
        return self.stations[self.current_station_index]
    
    def cleanLocalSignals(self,GameControllor,CombatCommander):
        # 清理本星系的信号任务 是完全的打完还是仅仅是有限的次数?
        # 进行有限次数的任务 进行2遍 一般一个类型的任务也就出现两遍
        for index in range(2):
            # 进入System界面
            GameControllor.moveToSystemScreen()
            # 进行至少三次扫描 因为我的传感器非常的差劲
            GameControllor.toScan()
            GameControllor.toScan()
            GameControllor.toScan()
            # 打开信号列表
            GameControllor.openSignalList()
            # 准备逐个类型的处理 获得当前信号类型检查任务
            # 获得SignalData 成员 templateObject signalType
            while CombatCommander.get_SignalMissionTypeAndReadyForNext():
            # True or 对应的Object
                signalExistFlag = exists(signalData.templateObject)
                if signalExistFlag: 
                    # !!! 这个地方有错误 应该存在之后然后点击这个任务然后蓝色Start 
                    # 准备战斗
                    log("准备跃迁至信号!进入战斗!")
                    # 通过对应的信号类型进行对应的战斗
                    # 此处的signalExistFlag并不是真的进入战斗的START
                    self.callMethodByName(signalData.signalType,CombatCommander,GameControllor,signalExistFlag,"List","station")
                else:
                    log("没有找到当前信号类型!")
        return True
    
    def moveToNextStaion(self,GameControllor,pathNoLoopFlag = False):
        # 这个操作包含一定的UI控制的需要 请在MainScreen开始
        # 重置为游戏主界面
        if GameControllor.resetToMainScreen():
            GameControllor.goToGalaxyAndOpenList()
            # 获取下一站的Template
            nextStationTemplate = self.next_station(pathNoLoopFlag)
            log("下一站是:"+str(nextStationTemplate))
            if nextStationTemplate == False:
                log("未能检索到下一站,出现异常错误")
                return False
            
            nextStationCheck = exists(nextStationTemplate)  # Selecct next jump from list
            if nextStationCheck:
                
                touch(nextStationCheck)  # 准备前往下一站
                sleep(5.0)
                
                jumpButtonCheck = exists(Template(r"./resources/commonCommand/jumpButton.png", record_pos=(
                    0.309, 0.072), resolution=(1600, 900))) # 是否加载出来了跳跃界面
                if jumpButtonCheck:
                    touch(jumpButtonCheck)
                    GameControllor.clickSkipButton()
                    
                    sleep(40.0) # 等待加载时间 注释:此处的加载指进行的跨越星系之间的加载时间 应该尽可能宽裕一些
                    return True
                    # Focus 为了提高效率不进行下面的处理了
                    # 根据头像是否存在来检查是否回到了主界面
                    # if exists(Template(r"./resources/customFeature/playerPic.png", record_pos=(-0.446, -0.231), resolution=(1600, 900))):
                        # return True
                    #else:
                        # 进行更长时间的缓冲加载时间
                        # sleep(15.0)
                        # return True
            else:
                log("Something wrong to locate NextGlaxy")
                return False

    def action(self,GameControllor,CombatCommander):
        # 需要考虑到底执行几次 怎么才能干净的清除 次数 和 返回可能的失误检查
        # 返回正数则是成功到达下个星系
        # 返回负数则是未能成功到达下个星系
        # Try 在当前站点执行任务
        try:
            # 初始化 CombatCommander 将所有的Tpye转化为Template 
            CombatCommander.initGalaxyTemplateResources(SignalMissionTypeList)
            # 清理当前的Signals
            cleanCheck = self.cleanLocalSignals(GameControllor,CombatCommander)
            # 如果任务完成 True 那么准备前往下一站 如果Count出错太多那么准备矫正姿势重试
            if cleanCheck:
                # 前往下一站
                return self.moveToNextStaion(GameControllor)
            else:
                raise ValueError('Too much error happend!')
        # Catch 如果出现了错误 发生了过多的问题 那么开始进行矫正
        except Exception:
            # 矫正当前到工作状态
            if GameControllor.resetToMainScreen():
                # 重新进行清理任务
                if self.cleanLocalSignals(GameControllor,CombatCommander):
                    # 前往下一站
                    return self.moveToNextStaion(GameControllor)
                else:
                    # 本星系积累了过多的错误,应该留下日志等待具体检查 log
                    # 前往下一站
                    return self.moveToNextStaion(GameControllor)
    
    def departureWithAction(self,GameControllor,CombatCommander):
        # main function No returning value 这个似乎不需要做成线程
        # 无限循环走向下一站
        while True:
            # if 如果当前连接正常 那么继续工作 workingState is good 
            if self.workingState == True:
                log("舰队信号通畅,准备行动")
                # 从本质上来说这里不负责确定完成情况 只是执行任务
                actionCheck = self.action(GameControllor,CombatCommander)
            # else 如果检查到工作状态不正常 那么停止工作 workingState is bad 等待状态恢复
            elif self.workingState == False:
                log("等待状态恢复")
                # 等待信号重新连接 阻塞舰队行动
                while True:
                    # 主线程进行等待 直到 舰队被通知可以进行任务
                    sleep(60)
                    if self.workingState:
                        # 结束阻塞的循环 准备继续触发
                        break
                # 阻塞结束 准备继续工作
                actionCheck = self.action(GameControllor,CombatCommander)
                if actionCheck: 
                    log("舰队正常执行任务.该Log出自departure elif")
                self.moveToNextStaion(GameControllor)

    def departureWithScan(self,GameControllor,pathNoLoopFlag = False):
        # 从指定星系开始逐个System扫描 最终会回到原来的地方 请提前配置刷新线路
        # 无限循环走向下一站
        while True:
            # 如果连接正常那么继续工作
            if self.workingState == True:
                log("舰队指挥官:舰队信号通畅,准备开始扫描")
                GameControllor.moveToSystemScreen()
                GameControllor.toScan()
                self.moveToNextStaion(GameControllor,pathNoLoopFlag)
                log("舰队指挥官:准备进入下个星系!")
            # 如果检查到工作状态不正常那么停止工作
            elif self.workingState == False:
                log("舰队指挥官:等待连接状态恢复")
                # 等待信号重新连接 阻塞舰队行动
                while True:
                    # 主线程进行等待直到舰队被通知可以进行任务
                    sleep(60)
                    if self.workingState:
                        # 结束阻塞的循环 准备出发
                        break
                # 阻塞结束 准备继续工作
                GameControllor.moveToSystemScreen()
                GameControllor.toScan()
                self.moveToNextStaion(GameControllor,pathNoLoopFlag)
                log("舰队指挥官:准备进入下个星系!")

class CombatCommander:
    # 信号任务的战斗 突袭战斗 
    def __init__(self):
        self.test = True
        # 自动释放技能间隔
        self.autoSkillInterval = 15
        self.running = False
        # 用来记录需要进行的信号战斗类型 用于LocalSignal清除任务
        # 其中的包含了对象 字段为 templateObject 对象 signalType string
        self.signalTypeDataList = []
        # 记录当前需要进行任务的信号类型下标 初始化为0
        self.signalTypeIndex = 0

    def initGalaxyTemplateResources(self,imagePathList):
        # 初始化signalTypeTemplateList 方便UI的使用
        self.signalTypeList = imagePathList
        # 第一个成员是Path路径 第二个是信号类型 这些信号类型会和对应的方法结合在一起
        for elem in imagePathList:
            # 注意,这里直接指定了大致的检测位置提高检测效率和分辨率!
            self.signalTypeDataList.append({
                templateObject:Template(elem.path,record_pos=(0.261, -0.095), resolution=(1600, 900)),
                signalType:elem.signalType
                })
    
    def get_SignalMissionTypeAndReadyForNext(self):
        # 获取当前需要进行任务的信号类型并你准备下一个任务类型 返回Template
        if self.signalTypeIndex < len(self.signalTypeDataList):
            element = self.signalTypeDataList[self.signalTypeIndex]
            self.signalTypeIndex += 1
            return element
        else:
            return False
    def retrieveResources(self):
        return True
    def defeatEnemy(self):
        return True
    def moveToTargetLocation(self):
        return True
    def protectTarget(self):
        return True

    def ProgenitorSignal(self,GameControllor,signalJumpUICoordination,UISource:str,destination:str):
        # ! 请注意 每个新增的Signal战斗策略都必须和SignalMissionTypeList中的类型Type保持一致
        # 传递进来一个任务的Jump参数 从这里开始进行操作 所以如果根本没有Jump的时候也不会随便的触发这个部分 
        # UISource 既可以是Group进入信号也可以是普通的SignalList进入
        # destination 最终返回的地方 例如空间站还是留在原地
        # 这是一个UI模拟战斗功能函数
        # 先祖任务的描述 这类任务往往是击退两次敌人和回收资源
        touch(signalJumpUICoordination)
        log("点击Skip")
        GameControllor.clickSkipButton()
        log("战斗指挥官:准备进入战场 开始Progenitor任务")
        sleep(30.0) # 准备加载到战场
        if UISource == "Group":         # UI处理
            log("关闭无关UI")
            GameControllor.closeCommunicationLsitUI()   # 关闭通信频道的无关UI 如果是Group进来的话

        touch([1512,547])   # 打开物资列表
        touch([1250,300])   # 打开第一个物资的控制面板 
        touch([1336,511])   # 舰队协同保护矿机 前进Move
        sleep(30.0)         # 前进等待
        touch([1250,300])   # 打开第一个物资的控制面板
        touch([1169,508])   # 开始回收工作
        sleep(13.0)         # 正在进行回收

        touch([1250,300])   # 打开第二个物资的控制面板
        touch([1336,511])   # 舰队协同保护矿机 前进Move
        sleep(60.0)         # 前进等待
        touch([1169,508])   # 开始回收工作
        sleep(13.0)         # 正在进行回收
        sleep(12.0)         # 等待敌人被歼灭

        if GameControllor.rewardSettlement():   # 准备奖励结算和目的地
            if destination == "station":
                # 返回空间站
                touch([977, 778])
            elif destination == "stay":
                # 留在原地
                touch([597, 775])

    def RlicSignal(self,gameControllor,signalJumpUICoordination,UISource:str,destination:str):
        # 处理Relic信号任务
        # 这类任务的特征是 1.前往目标地带 2.回收资源 该任务不需要消灭敌人
        
        touch(signalJumpUICoordination)     # 进行跃迁,开始战场加载
        gameControllor.clickSkipButton()    # 跳过加载动画
        sleep(30.0)                         # 等待完全加载
        # 如果是Group进入战场则进行UI处理
        if UISource == "Group":
            log("关闭无关UI")
            gameControllor.closeCommunicationLsitUI()   # 关闭通信频道的无关UI 如果是Group进来的话
        
        touch([1512,547])   # 打开物资列表
        touch([1250,300])   # 打开物资控制面板 
        touch([1253,494])   # 舰队前去目标位置 绿色的实心箭头
        sleep(25.0)         # 等待舰队就位 实际上只要发现目标即可 
        touch([1250,300])   # 打开物资控制面板
        touch([1166,510])   # 进行回收工作
        sleep(62.0)         # 等待回收完成 这个过程相当的漫长
        log("回收预计完成")

        if gameControllor.rewardSettlement():   # 准备奖励结算和目的地
            if destination == "station":
                # 返回空间站
                touch([977, 778])
            elif destination == "stay":
                # 留在原地
                touch([597, 775])
    
    def start(self):
        # 自动施法的初级形式
        self.running = True
        while self.running:
            # touch(self.pos)
            sleep(self.autoSkillInterval)
    
    def stop(self):
        self.running = False

class ResourceManagementOfficer:
    def __init__(self):
        self.test = True

class MissionOperationsOfficer:
    # 任务管理官 负责处理办公室任务
    def __init__(self):
        self.test = True
        # 重置队伍信号内容 当掉线发生时 循环暂停 并且重置
        self.connectionReadyToWorkFlag = False

    def SpecificSignalMissionLoop_Test(self,GameControllor,FleetCommander,CombatCommander,isSignalAlreadyPrepare = False):
        # 这两种时最常见的信号 不要自己提前开组队 会影响脚本
        # 测试Progenitor and Relic信号循环 这是个特别的任务仅仅需要用户直接跃迁到目标位置即可 无需多余操作
        
        GameControllor.joinChannelAndGroup()    # 准备创建频道并进入小队
        while True:
            if self.connectionReadyToWorkFlag:  # 隐式被GameControllor控制的变量
                log("舰队指挥官:连接状态正常 准备进行信号作业")
                if isSignalAlreadyPrepare:      # 用户准备好了信号状态不必重新进行刷新信号了
                    log("舰队指挥官:准备扫描信号")
                    GameControllor.moveToSystemScreen()
                    GameControllor.toScan()     # 进行充足的扫描来防止没有刷新
                    GameControllor.toScan()
                    GameControllor.toScan()
                    GameControllor.toScan()
                    GameControllor.toScan()      
                    GameControllor.recordSignalMission()
                    isSignalAlreadyPrepare = False      # 用户准备好了信号状态不必重新进行刷新信号了   
                    while True:                         # 循环刷两个信号 此处开始可以模拟操作 while True
                        if self.connectionReadyToWorkFlag:  # 如果条件不好就break
                            GameControllor.openSocial()     # 进入group
                            #GameControllor.switchToChat()
                            #GameControllor.openGroupList()
                            ProgenitorSignalEnterCoordinate = [1201,635] # 进入第一个信号 留在原地
                            CombatCommander.ProgenitorSignal(GameControllor,ProgenitorSignalEnterCoordinate,"Group","stay")
                            # 进入group
                            GameControllor.openSocial()
                            #GameControllor.switchToChat()
                            #GameControllor.openGroupList()
                            # 进入第二个信号 留在原地
                            RelicSignalEnterCoordinate =[1147,723]
                            CombatCommander.ProgenitorSignal(GameControllor,RelicSignalEnterCoordinate,"Group","stay")
                else:   # 指挥官没有准备好信号刷新机制需要自动刷新
                    FleetCommander.departureWithScan(GameControllor,True) # 刷新信号任务 从线路出发然后回来
                    log("舰队指挥官:准备扫描信号")                          # 支持继续断线继续
                    GameControllor.moveToSystemScreen()
                    GameControllor.toScan()                               # 进行充足的扫描来防止没有刷新
                    GameControllor.toScan()
                    GameControllor.toScan()
                    GameControllor.toScan()
                    GameControllor.toScan()
                    # !! 记录信号 这个方法只能按照Progenitor和Relic的顺序记录 
                    GameControllor.recordSignalMission()
                    # 循环刷两个信号 此处开始可以模拟操作 while True
                    while True:
                        # 利用if判定是否存在connectionReadyToWorkFlag如果条件不好就break
                        if self.connectionReadyToWorkFlag:
                            # 进入group
                            GameControllor.openSocial()
                            #GameControllor.switchToChat()
                            #GameControllor.openGroupList()
                            # 进入第一个信号 留在原地
                            ProgenitorSignalEnterCoordinate = [1201,635]
                            CombatCommander.ProgenitorSignal(GameControllor,ProgenitorSignalEnterCoordinate,"Group","stay")
                            # 进入group
                            GameControllor.openSocial()
                            #GameControllor.switchToChat()
                            #GameControllor.openGroupList()
                            # 进入第二个信号 留在原地
                            RelicSignalEnterCoordinate =[1147,723]
                            CombatCommander.ProgenitorSignal(GameControllor,RelicSignalEnterCoordinate,"Group","stay")
            else:
                log("舰队指挥官:失去舰队连接 正在重新连接")
                # 等待信号重新连接 阻塞舰队行动
                while True:
                    # 主线程进行等待 直到 舰队被通知可以进行任务
                    sleep(60)
                    if self.connectionReadyToWorkFlag:
                        # 结束阻塞的循环 准备继续触发
                        break
                # 阻塞结束 准备继续工作
                # FleetCommander 刷新信号任务 从线路出发然后回来
                # 一旦掉线会通知FleetCommander停下来 然后一会继续
                FleetCommander.departureWithScan(GameControllor,True)
                log("舰队指挥官:准备扫描信号")
                GameControllor.moveToSystemScreen()
                # 进行充足的扫描来防止没有刷新
                GameControllor.toScan()
                GameControllor.toScan()
                GameControllor.toScan()
                GameControllor.toScan()
                GameControllor.toScan()
                # !! 记录信号 这个方法只能按照Progenitor和Relic的顺序记录 
                GameControllor.recordSignalMission()
                # 循环刷两个信号 此处开始可以模拟操作 while True
                while True:
                    # 利用if判定是否存在connectionReadyToWorkFlag如果条件不好就break
                    if self.connectionReadyToWorkFlag:
                        # 进入group
                        GameControllor.openSocial()
                        #GameControllor.switchToChat()
                        #GameControllor.openGroupList()
                        # 进入第一个信号 留在原地
                        ProgenitorSignalEnterCoordinate = [1201,635]
                        CombatCommander.ProgenitorSignal(GameControllor,ProgenitorSignalEnterCoordinate,"Group","stay")
                        # 进入group
                        GameControllor.openSocial()
                        #GameControllor.switchToChat()
                        #GameControllor.openGroupList()
                        # 进入第二个信号 留在原地
                        RelicSignalEnterCoordinate =[1147,723]
                        CombatCommander.ProgenitorSignal(GameControllor,RelicSignalEnterCoordinate,"Group","stay")
def relicBattleTest():
    # 测试Code 
    gameControllor = GameControllor()

    if gameControllor.rewardSettlement():   # 准备奖励结算和目的地
        touch([597, 775])

def twoWaveAndResourcesCollectBattelTest():
    gameControllor = GameControllor()

    if gameControllor.rewardSettlement():   # 准备奖励结算和目的地
        touch([597, 775])

def simpleLoopTest():
    gameControllor = GameControllor()
    combatCommander = CombatCommander()
    loopCount = 0
    while True:
        gameControllor.openSocial()                     # 进入group 准备ProgenitorSignal
        ProgenitorSignalEnterCoordinate = [1201,635]    # 进入第一个信号 留在原地
        combatCommander.ProgenitorSignal(gameControllor,ProgenitorSignalEnterCoordinate,"Group","stay")
        gameControllor.openSocial()                     # 进入group 准备RlicSignal
        RelicSignalEnterCoordinate =[1147,723]          # 进入第二个信号 留在原地
        combatCommander.RlicSignal(gameControllor,RelicSignalEnterCoordinate,"Group","stay")
        loopCount += 1
        log("循环已经发生了"+str(loopCount))
def fleetAdvancesAccordingToTheLineAndClearSignal():
    # main Function
    # 模块初始化准备
    # 舰队飞行控制模块准备
    fleetCommander = FleetCommander()
    # 游戏姿态矫正模块
    guider = GameControllor()
    # 战斗模块准备
    combatCommander = CombatCommander()
    missionOperationsOfficer = MissionOperationsOfficer()
    # 基础功能准备
    # 连接丢失重连检查
    guider.startCheckLostConnect(fleetCommander,missionOperationsOfficer)
    # 舰队任务信息初始化
    # 星图路线初始化
    fleetCommander.initGalaxyTemplateResources(travelingGalaxyPlanList)
    # 准备起航
    fleetCommander.departureWithAction(guider,combatCommander)

def refreshSignalFromTartgetGalaxy():
    # 模块初始化准备
    fleetCommander = FleetCommander()
    # 游戏姿态矫正模块
    guider = GameControllor()
    # 战斗模块准备
    combatCommander = CombatCommander()
    missionOperationsOfficer = MissionOperationsOfficer()
    # 连接丢失重连检查
    guider.startCheckLostConnect(fleetCommander,missionOperationsOfficer)
    # 舰队任务信息初始化
        # specialSignalMissionLoop
        # travelingGalaxyPlanList
    fleetCommander.initGalaxyTemplateResources(travelingGalaxyPlanList)
    # 准备起航
    fleetCommander.departureWithScan(guider,True)

def specialOperation():
    # 双信号行动
    # 舰队飞行控制模块准备
    fleetCommander = FleetCommander()
    # 游戏姿态矫正模块
    guider = GameControllor()
    # 战斗模块准备
    combatCommander = CombatCommander()
    # 任务官准备执行任务
    missionOperationsOfficer = MissionOperationsOfficer()
    # 连接丢失重连检查
    guider.startCheckLostConnect(fleetCommander,missionOperationsOfficer)
    # 舰队任务信息初始化
    fleetCommander.initGalaxyTemplateResources(specialSignalMissionLoop)
    missionOperationsOfficer.SpecificSignalMissionLoop_Test(guider,fleetCommander,combatCommander,True)