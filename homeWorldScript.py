from airtest.core.api import *
import threading

class GameControllor:
    # 游戏UI控制模块
    def __init__(self):
        self.galaxySignalMissionReady = True
        self.lostConnectionCheck = False        # no need to init at first 
        self.connectionCheckInterval = 60 * 5   # 按照5分钟的周期检查掉线情况
        self.checkLostConnectThread = None      # 初始化掉线检查线程变量
        self.disconnectedCount = 0              # 掉线重连的次数
        self.flags = []                         # 需要进行通知断线重连的标志位

    def gameControllorInitTest():
        log("GameControllor init success")
    def checkGameStarted(self):
        # 检查游戏是否启动并启动
        app_checker = AppChecker("HomeWorld", "com.stratospheregames.nimbusgbx")
        app_checker.launch_app()
        stop_app("com.stratospheregames.nimbusgbx")

    def launch_app(self):   # 启动游戏
        print(f"Launching {self.app_name}...")
        start_app(self.package_name)
        sleep(5)
    
    def close_app(self):    # 关闭游戏
        if self.check_app():    
            print(f"Closing {self.app_name}...")
            stop_app(self.package_name)
            sleep(5)
            if not self.check_app():
                print(f"{self.app_name} is closed!")   

    def resetToMainScreen(self):
        touch([1122, 93])   # 点击Combat
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
        # 进入System界面 前置条件:在商店不行
        touch([1251, 93])   # into system
        sleep(5.0)          # 进入系统需要一定的缓冲刷新
    
    def openSignalList(self):
        touch([1508,368])   # 打开信号列表
        return True

    def moveToGalaxy(self):
        touch([1381, 91])   # open galaxy screen
        sleep(5.0)

    def toScan(self,timeInterval = 8.0):
        touch([800, 715])       # Scan! 应该配合进入System或者Galaxy使用!
        touch([800, 715])       # 防止没有点上 再来一次
        sleep(timeInterval)     # 默认间隔8秒才能执行下一次
    
    def multipleScan(self,scanTime):
        for index in range(scanTime):   # 进行多次扫描
            self.toScan()

    def moveToGalaxyAndOpenList(self):
        # make sure that you are in the main screen to do this
        touch([1381, 91])   # open galaxy screen
        sleep(5.0)
        touch([1513, 370])  # Click and open galaxy list
        sleep(5.0)
    
    def clickSkipButton(self):
        touch([1408, 677])  # click skip
        touch([1408, 677])
        touch([1408, 677])
        touch([1408, 677])
        sleep(3.0)          # 保证能完全的跳过加载过程 这一点加载时间可能会影响整个循环
        touch([1408, 677])
        touch([1408, 677])

    def openSocial(self):   # 开始条件 应该是主界面 不然点不了右上角的图标
        touch([1521, 72])   # open channel list
        sleep(1.0)
    
    def switchToChat(self): # 打开通信之后确定不是进入邮箱而是通信列表
        touch([1309, 106])  # open chat list
        log("确认切换到ChatList")
        sleep(1.0)
    
    def openChatTextInputLine(self):    # 打开输入框 但是还没有输入内容
        touch([1053, 837])  # open text line
        sleep(1.0)
    
    def inputTextAndSend(self):
        # input输入框输入内容 请提前已经打开输入框了 也就是已经打开输入法界面了
        # ready to create channel 准备开始在输入框输入内容
        for i in range(10): # 清除输入框内容
            keyevent("KEYCODE_DEL")
        text("/join 21", enter=True)
        sleep(1.0)
        touch([1493, 802])  # confirm inputline 系统输入框的确认按钮
        sleep(1.0)
        touch([1496, 816])  # 点击游戏内的输入信息的绿色的回车
        sleep(1.0)
    
    def openGroupList(self):    # open group list
        touch([1514, 557])  # click group
        log("打开GroupList")
        sleep(1.0)
    
    def createGroup(self):  # create group 创建队伍
        log("准备点击创建队伍按钮")
        touch([1187, 456])  # create group
        sleep(1.0)
    
    def closeSocialList(self):
        touch([1514,54])
        log("关闭Social功能!")
    
    def clickCreditsStayButton(self):  # 留在原地
        touch([597, 775])   
        touch([597, 775])   # 确保真的点到了避免卡顿

    def clickCreditsGoToStationButton(self):   # 返回空间站
        touch([977, 778])
        touch([977, 778])   # 确保真的点到了避免卡顿

    def joinChannelAndGroup(self):  # 用来加入频道并进入队伍 从主界面(可能)来最后回到主界面
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
        touch([1514, 55])   # 关闭通信界面
        touch([472, 482])   # 也关闭GroupUI 
        touch([472, 482])

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
        touch([1195, 96])   # 直接点击目标位置退出
        sleep(2.0)
        touch([1385, 91])   # 触发确认

    def recordSignalMission(self):
        # 假设已经完成了队伍创建 并且已经刷新出来了两个信号 现在等待记录两个信号 
        # TODO 现在只能直接固定两个类型的任务 第一个是Progenitor 同类型的还有Tanoch 第二个是Relic
        log("准备开始信号记录到Group")
        self.resetToMainScreen()  # 从主界面开始这个任务
        self.moveToSystemScreen()
        self.openSignalList()
        # locate Progenitor mission
        ProgenitorSignal = exists(Template(r"./resources/signalType/ProgenitorSignal.png", record_pos=(0.284, 0.014), resolution=(1600, 900)))
        if ProgenitorSignal:
            log("准备记录Progenitor信号")
            touch(ProgenitorSignal)
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
        RelicSignal = exists(Template(r"./resources/signalType/RelicSignal.png", record_pos=(0.284, 0.014), resolution=(1600, 900)))
        if RelicSignal:
            log("准备记录Relic信号")
            touch(RelicSignal)
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

    def TargetPositionLocate(self): # TargetPosition 物资检查
        #resourceCheck = exists(Template(r"./resources/signalResources/TargetPosition.png", record_pos=(0.281, -0.096), resolution=(1600, 900)))
        touch([1235,301])
        sleep(1.0)

    def moveToTargetResources():    # 开启目标资源行动之后开始准备舰队移动
        #destinationCoordinates = exists(Template(r"./resources/commonCommand/fleetMoveTo.png", record_pos=(0.329, 0.038), resolution=(1600, 900)))
        #if destinationCoordinates:
            #touch(destinationCoordinates)
            # 这里只能模拟情况了 很难直接检查到是否已经到达目标位置
            #sleep(40.0)
        touch([1232,492])   # 绿色的Move操作
        sleep(1.0)

    def collectorInterpack():   # collectorInterpack 矿机准备进行回收工作
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

    def registerConnectionCheckFlag(self,actionFlagObject):
        self.flags.append(actionFlagObject) # the actionFlag should be reference of a object

    def stopAllFlag(self):
        for flag in self.flags:
            log("游戏检查程序:通知"+str(flag)+"停止行动")
            flag.connectionReadyToWorkFlag = False

    def startAllFlag(self):
        for flag in self.flags:
            log("游戏检查程序:通知"+str(flag)+"可以继续行动")
            flag.connectionReadyToWorkFlag = True

    def checkLostConnect(self):
        first_time = True # 检查是否是第一次执行,在常规情况下第一次是不用进行掉线检查的
        while True:
            log("UI控制程序:掉线发现的次数:"+str(self.disconnectedCount)+"次")
            if first_time:  # 第一次执行的时候并不进行检查 放行舰队行动
                log("游戏检查程序:第一次连接检查默认连接正常")
                self.startAllFlag()
                first_time = False  # 结束第一次的状态
                sleep(self.connectionCheckInterval) 
            log("游戏检查程序:准备检查连接情况")
            warningFlagCheck = exists(Template(r"./resources/lostConnectionFeature/WarningFlag.png", record_pos=(0.002, -0.092), resolution=(1600, 900)))
            if warningFlagCheck == False:
                log("游戏检查程序:连接状态良好")
                self.startAllFlag()  # 舰队可以继续执行任务
                sleep(self.connectionCheckInterval) # 继续周期性检查掉线情况 
            else:    # 准备重新连接
                log("游戏检查程序:检查到掉线情况发生,准备重新连接")
                self.disconnectedCount += 1
                self.stopAllFlag()
                touch([800,720])    # click restart button
                sleep(60.0)         # 加载时间缓冲
                startGameCheck = exists(Template(r"./resources/startGameFeature/startGameButton.png", record_pos=(-0.001, 0.197), resolution=(1600, 900)))
                if startGameCheck==False:
                    sleep(30.0) # 如果没有加载成功那么延迟继续加载
                    startGameCheck = exists(Template(r"./resources/startGameFeature/startGameButton.png", record_pos=(-0.001, 0.197), resolution=(1600, 900)))
                    if startGameCheck==False:
                        log("游戏检查程序:无法识别开始游戏按钮,发生错误")
                # 准备开始连接到游戏
                startGameFinishedCheck = self.startGameandClearAdvertisement()
                if startGameFinishedCheck == True:
                    self.startAllFlag()             # 舰队可以继续执行任务
                sleep(self.connectionCheckInterval) # 继续周期性检查掉线情况
    
    def startCheckLostConnect(self):
        log("游戏控制程序:开始监控游戏连接情况")
        # 如果线程已经在运行，那么就不需要再启动了
        if self.checkLostConnectThread is not None and self.checkLostConnectThread.is_alive():
            return
        # 创建一个新的线程
        self.checkLostConnectThread = threading.Thread(target=self.checkLostConnect, args=())
        # 将线程设置为守护线程，这样当主线程结束时，子线程也会随之结束
        self.checkLostConnectThread.daemon = True
        self.checkLostConnectThread.start() # 启动线程
    
    def stopCheckLostConnect(self): # 停止执行checkLostConnect方法
        # 如果线程已经在运行，那么就停止它
        if self.checkLostConnectThread is not None and self.checkLostConnectThread.is_alive():
            self.checkLostConnectThread.stop()

    def startGameandClearAdvertisement(self):   # 准备开始检测是否存在目标
        welcomeFlagCheck = exists(Template(r"./resources/startGameFeature/welcomeFlag.png", record_pos=(-0.081, -0.221), resolution=(1600, 900)))
        startGameButtonCheck = exists(Template(r"./resources/startGameFeature/startGameButton.png", record_pos=(-0.002, 0.197), resolution=(1600, 900)))

        if welcomeFlagCheck or startGameButtonCheck:    # 只要检查到其中一个可以启动游戏的特征就可以继续
            touch([790,766])    # 点击开始游戏按钮
            sleep(35.0)         # 游戏加载时间
        # 检查加载情况 实际上这个地方可以利用Train的当前位置进行检查 
        # closeButtonCheck = exists(Template(r"tpl1682335645537.png", record_pos=(0.445, 0.004), resolution=(1600, 900)))
        sleep(30.0)     # 等待游戏加载时间长一点 这是一个可能错位的地方
        log("准备关闭广告")
        touch([1064,105])
        sleep(10.0)     # 短暂的加载时间
        # 检查是否进入游戏MainScreen
        checkEnterGameState = exists(Template(r"./resources/customFeature/playerPic.png", record_pos=(-0.446, -0.231), resolution=(1600, 900)))
        return checkEnterGameState  # 检查当前是否进入游戏界面

class FleetCommander:   # 管理所有舰队的Galaxy行动 Galaxy功能模块
    def __init__(self,GameControllor_instance,imagePathList = []):
        self.stations = []              # Template list
        self.current_station_index = 0  # 记录当前在第几站
        self.direction = 1              # 从起始站出发为正方向设置为1 终点为反方向设置为-1
        self.connectionReadyToWorkFlag = False       # 当前是否可以执行任务
        self.gameControllor = GameControllor_instance
        self.initGalaxyTemplateResources(imagePathList)

    def fleetCommanderInitTest():
        log("FleetCommander init success")

    def callMethodByName(methodName, targetClass,*args):
        # 这里定义了一个工具类函数它的意义是为了通过一个字符串来调用一个方法
        # 该方法返回一个函数的指向 仍然需要手动调用
        targetMethod = getattr(targetClass, methodName)
        targetMethod(*args) # 执行我们需要的目标方法
    
    def initGalaxyTemplateResources(self,imagePathList):    # 初始化一个路线
        for elem in imagePathList:
            # 此处的record_pos已经优化为GalaxyList的UI框内,提高了很多准确程度
            self.stations.append(Template(elem,record_pos=(0.284, 0.014),resolution=(1600, 900)))
        # default 分辨率

    def next_station(self, one_loop=False):
        # 只能在起始站出发 不可以从中间的站点出发
        # one_loop 参数，如果传递为 True，则在遍历完整个数组后，只会进行一次循环。
        # TODO 返回一个封装好的Class 返回Template
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
        self.current_station_index = next_index             # 更新当前站点索引
        return self.stations[self.current_station_index]    # 返回下一站的定位资源
    
    def moveToNextStaion(self,pathNoLoopFlag = False): # 请在MainScreen开始
        if self.gameControllor.resetToMainScreen(): # 重置为游戏主界面
            self.gameControllor.moveToGalaxyAndOpenList()
            nextStationTemplate = self.next_station(pathNoLoopFlag) # 获取下一站的Template
            log("舰队航线控制:下一个前往的星系是:"+str(nextStationTemplate))
            if nextStationTemplate == False:
                log("舰队航线控制:无下一站,已经到达终点站")
                return False
            nextStationCheck = exists(nextStationTemplate)  # Selecct next jump from list
            if nextStationCheck:
                touch(nextStationCheck)     # 准备前往下一站
                sleep(5.0)                  #
                jumpButtonCheck = exists(Template(r"./resources/commonCommand/jumpButton.png", record_pos=(
                    0.309, 0.072), resolution=(1600, 900))) # 是否加载出来了跳跃界面
                if jumpButtonCheck:
                    touch(jumpButtonCheck)
                    self.gameControllor.clickSkipButton()
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
                log("舰队航线控制:无下一站,已经到达终点站")
                return False

class CombatCommander:  # 信号任务的战斗 突袭战斗 战斗任务控制模块
    def __init__(self):
        self.autoSkillInterval = 15                      # 自动释放技能间隔
        self.autoTacticsFireFlag = False                 # 自动释放母舰战术技能
        self.autoTacticsFireEvent = threading.Event()    # 创建一个Event对象
    def combatCommanderInitTest():
        log("CombatCommander init success")

    def tacticsFire(self,slotSequence: int) -> None: # 母舰武器系统战术技能开火栏位 slotSequence技能槽序数
        positions = {
            1: [82, 364],
            2: [83, 451],
            3: [88, 536],
            4: [85, 622]
        }
        if slotSequence in positions:
            # log("战斗指挥官:使用第"+str(slotSequence)+"战术技能")
            touch(positions[slotSequence])
    def _autoTacticsFire_loop(self, stop_event):
        while not stop_event.is_set():  # 判断是否需要停止
            for slotIndex in range(4):
                self.tacticsFire(slotIndex)  # 调用tacticsFire方法
            stop_event.wait(self.autoSkillInterval)  # 等待指定的时间

    def autoTacticsFire_start(self, skillInterval=None):
        if skillInterval is not None:
            self.autoSkillInterval = skillInterval

        self.autoTacticsFireFlag = True
        self.autoTacticsFireEvent.clear()  # 初始化Event对象的状态
        # 创建一个新的线程并启动
        self.autoTacticsFireThread = threading.Thread(
            target=self._autoTacticsFire_loop, args=(self.autoTacticsFireEvent,))
        self.autoTacticsFireThread.start()

    def autoTacticsFire_stop(self):
        self.autoTacticsFireFlag = False
        self.autoTacticsFireEvent.set()  # 设置Event对象的状态，通知线程停止
        # 等待线程停止
        if self.autoTacticsFireThread is not None:
            self.autoTacticsFireThread.join()

    def getSignalMissionType(self): # 获取信号类型并你准备下一个任务类型 返回Template
        # 从Type array中获取一个
        return True
    def ProgenitorSignal(self,gameControllor,signalJumpUICoordination,UISource:str,destination:str):
        touch(signalJumpUICoordination)
        log("UI控制程序:点击Signal加载Skip")
        gameControllor.clickSkipButton()
        log("战斗指挥官:准备进入战场 开始Progenitor任务")
        sleep(38.0) # 准备加载到战场
        if UISource == "Group":         # UI处理
            log("UI控制程序:关闭无关UI")
            gameControllor.closeCommunicationLsitUI()   # 关闭通信频道的无关UI 如果是Group进来的话
        log("战斗指挥官:开始战场指挥")
        touch([1512,547])   # 打开物资列表
        touch([1250,300])   # 打开第一个物资的控制面板 
        touch([1336,511])   # 舰队协同保护矿机 前进Move
        sleep(30.0)         # 前进等待
        touch([1250,300])   # 打开第一个物资的控制面板
        touch([1169,508])   # 开始回收工作
        sleep(13.0)         # 正在进行回收

        touch([1250,300])   # 打开第二个物资的控制面板
        touch([1336,511])   # 舰队协同保护矿机 前进Move
        touch([1336,511])   # 保证Move指令确实发出了 并且控制面板收回
        sleep(60.0)         # 前进等待
        touch([1250,300])   # 打开第二个物资的控制面板
        touch([1169,508])   # 开始回收工作
        self.autoTacticsFire_start(skillInterval=6)   # 开始自动释放战术技能，每 10 秒执行一次
        sleep(13.0)         # 正在进行回收
        sleep(12.0)         # 等待敌人被歼灭
        self.autoTacticsFire_stop()      # 自动释放战术技能停止
        if gameControllor.rewardSettlement():   # 准备奖励结算和目的地
            if destination == "station":
                # 返回空间站
                gameControllor.clickCreditsGoToStationButton()
            elif destination == "stay":
                # 留在原地
                gameControllor.clickCreditsStayButton()

    def RlicSignal(self,gameControllor,signalJumpUICoordination,UISource:str,destination:str):
        # 处理Relic信号任务
        # 这类任务的特征是 1.前往目标地带 2.回收资源 该任务不需要消灭敌人
        
        touch(signalJumpUICoordination)     # 进行跃迁,开始战场加载
        gameControllor.clickSkipButton()    # 跳过加载动画
        log("战斗指挥官:准备进入战场 开始Relic任务")
        sleep(38.0)                         # 等待完全加载
        # 如果是Group进入战场则进行UI处理
        if UISource == "Group":
            log("关闭无关UI")
            gameControllor.closeCommunicationLsitUI()   # 关闭通信频道的无关UI 如果是Group进来的话
        log("战斗指挥官:开始战场指挥")
        touch([1512,547])   # 打开物资列表
        touch([1250,300])   # 打开物资控制面板 
        touch([1253,494])   # 舰队前去目标位置 绿色的实心箭头
        sleep(25.0)         # 等待舰队就位 实际上只要发现目标即可 
        touch([1250,300])   # 打开物资控制面板
        touch([1166,510])   # 进行回收工作
        log("战斗指挥官:开始战术技能自动释放")
        self.autoTacticsFire_start(skillInterval=6)   # 开始自动释放战术技能，每 10 秒执行一次
        sleep(62.0)         # 等待回收完成 这个过程相当的漫长
        log("任务官:回收预计完成")
        self.autoTacticsFire_stop()      # 自动释放战术技能停止
        if gameControllor.rewardSettlement():   # 准备奖励结算和目的地
            if destination == "station":    # 返回空间站
                gameControllor.clickCreditsGoToStationButton()
            elif destination == "stay":     # 留在原地
                gameControllor.clickCreditsStayButton()
        
class OperationOfficer: # 任务管理官 负责处理办公室任务
    def __init__(self,GameControllor_instance,FleetCommander_instance,CombatCommander_instance):
        self.test = True
        self.gameControllor = GameControllor_instance
        self.fleetCommander = FleetCommander_instance
        self.combatCommander = CombatCommander_instance
        self.connectionReadyToWorkFlag = False  # 重置队伍信号内容 当掉线发生时 循环暂停 并且重置

    def initClassTest(self):
        self.gameControllor.gameControllorInitTest()
        self.combatCommander.combatCommanderInitTest()
        self.fleetCommander.fleetCommanderInitTest()
    def operationInit(self):
        self.gameControllor.registerConnectionCheckFlag(self.fleetCommander)
        self.gameControllor.registerConnectionCheckFlag(self)
        self.gameControllor.startCheckLostConnect()  # 连接丢失重连检查

    def simpleProgenitorAndRelicGroupSignalLoop(self):
        loopCount = 0
        while True:
            self.gameControllor.openSocial()                # 进入group
            ProgenitorSignalEnterCoordinate = [1201,635]    # 进入第一个信号 留在原地
            self.combatCommander.ProgenitorSignal(self.gameControllor,ProgenitorSignalEnterCoordinate,"Group","stay")    
            self.gameControllor.openSocial()                # 进入group
            RelicSignalEnterCoordinate =[1147,723]          # 进入第二个信号 留在原地
            self.combatCommander.RlicSignal(self.gameControllor,RelicSignalEnterCoordinate,"Group","stay") 
            loopCount += 1
            log("循环已经发生了"+str(loopCount))

    def withReconnectProgenitorAndRelicGroupSignalLoop(self):    # 指挥官没有准备好信号刷新机制需要自动刷新
        log("任务官:开始创建频道和加入Group")
        self.gameControllor.joinChannelAndGroup()    # 准备创建频道并进入小队
        while True:
            log("任务官:开始连接状态,准备执行循环Signal任务")
            if self.connectionReadyToWorkFlag:  # 隐式被GameControllor控制的变量
                log("任务官:连接状态正常,准备按照预定路线刷新Signal")
                self.galaxyFowardWithScan(True) # 刷新信号任务 从线路出发然后回来
                self.gameControllor.moveToSystemScreen()
                log("任务官:开始反复扫描")
                self.gameControllor.multipleScan(6) # 进行充足的扫描来防止没有刷新
                log("任务官:开始记录信号")
                self.gameControllor.recordSignalMission()
                while True: # 开始进行循环任务
                    if self.connectionReadyToWorkFlag:
                        log("任务官:开始信号循环任务")
                        self.simpleProgenitorAndRelicGroupSignalLoop()
                    else:
                        break # 结束内层循环
            else:
                log("任务官:失去连接,正在重新连接")
                while True:     # 等待信号重新连接 阻塞舰队行动
                    sleep(5.0)   # 主线程进行等待 直到 舰队被通知可以进行任务
                    if self.connectionReadyToWorkFlag:
                        break   # 结束阻塞的循环 准备继续触发
                log("任务官:阻塞结束,准备继续任务")
                log("任务官:开始创建频道和加入Group")
                self.gameControllor.joinChannelAndGroup()
                log("任务官:连接状态正常,准备按照预定路线刷新Signal")
                self.galaxyFowardWithScan(True) # 刷新信号任务 从线路出发然后回来
                self.gameControllor.moveToSystemScreen()
                log("任务官:开始反复扫描")
                self.gameControllor.multipleScan(20) # 进行充足的扫描来防止没有刷新
                log("任务官:开始记录信号")
                self.gameControllor.recordSignalMission()
                while True: # 开始进行循环任务
                    if self.connectionReadyToWorkFlag:
                        log("任务官:开始信号循环任务")
                        self.simpleProgenitorAndRelicGroupSignalLoop()
                    else:
                        break # 结束内层循环

    def cleanLocalSignals(self,GameControllor,CombatCommander):
        # 清理本星系的信号任务 是完全的打完还是仅仅是有限的次数?
        # 进行有限次数的任务 进行2遍 一般一个类型的任务也就出现两遍
        for index in range(2):
            GameControllor.moveToSystemScreen() # 进入System界面
            self.gameControllor.multipleScan(5) # 进行充足的扫描来防止没有刷新
            GameControllor.openSignalList()     # 打开信号列表
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

    def galaxyFowardWithScan(self,pathNoLoopFlag = False): # MainFuncion 从指定星系逐个System扫描 请配置线路
        while True: # 如果路线为单程票或者遇到错误就会停止Script 
            if self.fleetCommander.connectionReadyToWorkFlag == True:   # 如果连接正常那么继续工作
                log("舰队指挥官:舰队信号通畅,准备开始扫描")
                self.gameControllor.moveToSystemScreen()
                self.gameControllor.toScan()
                if self.fleetCommander.moveToNextStaion(pathNoLoopFlag) == False:
                    log("舰队指挥官:无下个跃迁地点,结束任务")
                    return False
                log("舰队指挥官:准备进入下个星系!")
            else:   # 连接失败,进行错误修正
                log("舰队指挥官:等待连接状态恢复")
                while True: # 等待信号重新连接 阻塞舰队行动
                    sleep(60)   # 主线程进行等待直到舰队被通知可以进行任务
                    if self.fleetCommander.connectionReadyToWorkFlag:
                        break   # 阻塞结束 准备继续工作
                self.gameControllor.moveToSystemScreen()
                self.gameControllor.toScan()
                if self.fleetCommander.moveToNextStaion(pathNoLoopFlag) == False:
                    log("舰队指挥官:无下个跃迁地点,结束任务")
                log("舰队指挥官:准备进入下个星系!")