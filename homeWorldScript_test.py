
from homeWorldScript import *

def relicBattle_Test(): # 测试Code inside and beginning of signal mission
    gameControllor = GameControllor() 
    log("战斗指挥官:开始战场指挥")
    touch([1512,547])   # 打开物资列表
    touch([1250,300])   # 打开物资控制面板 
    touch([1253,494])   # 舰队前去目标位置 绿色的实心箭头
    sleep(25.0)         # 等待舰队就位 实际上只要发现目标即可 
    touch([1250,300])   # 打开物资控制面板
    touch([1166,510])   # 进行回收工作
    sleep(62.0)         # 等待回收完成 这个过程相当的漫长
    log("回收预计完成")

    if gameControllor.rewardSettlement():   # 准备奖励结算和目的地
        touch([597, 775])

def progenitorBattel_Test(): # 测试Code inside and beginning of signal mission
    gameControllor = GameControllor()
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
    sleep(60.0)         # 前进等待
    touch([1250,300])   # 打开第二个物资的控制面板
    touch([1169,508])   # 开始回收工作
    sleep(13.0)         # 正在进行回收
    sleep(12.0)         # 等待敌人被歼灭
    if gameControllor.rewardSettlement():   # 准备奖励结算和目的地
        touch([597, 775])

def simpleLoop_Test():
    gameControllor = GameControllor()
    fleetCommander = FleetCommander(gameControllor)
    combatCommander = CombatCommander()
    operationOfficer = OperationOfficer(gameControllor,fleetCommander,combatCommander)
    operationOfficer.simpleProgenitorAndRelicGroupSignalLoop()

def fleetAdvancesAccordingToTheLineAndClearSignal_Test():
    fleetCommander = FleetCommander()
    guider = GameControllor()
    combatCommander = CombatCommander()
    missionOperationsOfficer = OperationOfficer()
    guider.startCheckLostConnect(fleetCommander,missionOperationsOfficer)
    fleetCommander.initGalaxyTemplateResources(travelingGalaxyPlanList)
    fleetCommander.departureWithAction(guider,combatCommander)
    # main function No returning value 这个似乎不需要做成线程
    # 无限循环走向下一站
    while True:
        # if 如果当前连接正常 那么继续工作 workingState is good 
        if self.connectionReadyToWorkFlag == True:
            log("舰队信号通畅,准备行动")
            # 从本质上来说这里不负责确定完成情况 只是执行任务
            actionCheck = self.action(GameControllor,CombatCommander)
        # else 如果检查到工作状态不正常 那么停止工作 workingState is bad 等待状态恢复
        elif self.connectionReadyToWorkFlag == False:
            log("等待状态恢复")
            # 等待信号重新连接 阻塞舰队行动
            while True:
                # 主线程进行等待 直到 舰队被通知可以进行任务
                sleep(60)
                if self.connectionReadyToWorkFlag:
                    # 结束阻塞的循环 准备继续触发
                    break
            # 阻塞结束 准备继续工作
            actionCheck = self.action(GameControllor,CombatCommander)
            if actionCheck: 
                log("舰队正常执行任务.该Log出自departure elif")
            self.moveToNextStaion(GameControllor)
    try:    # 在当前站点执行任务
        # 初始化 CombatCommander 将所有的Tpye转化为Template 
        CombatCommander.initGalaxyTemplateResources(SignalMissionTypeList)
        cleanCheck = self.cleanLocalSignals(GameControllor,CombatCommander) # 清理当前的Signals
        if cleanCheck:  # 准备前往下一站 如果Count出错太多那么准备矫正姿势重试
            return self.moveToNextStaion(GameControllor)  # 前往下一站
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

def refreshSignalFromTartgetGalaxy_Test():
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
    # specialSignalMissionLoop
    # travelingGalaxyPlanList
    gameControllor = GameControllor()
    fleetCommander = FleetCommander(gameControllor,travelingGalaxyPlanList)
    combatCommander = CombatCommander()
    operationOfficer = OperationOfficer(gameControllor,fleetCommander,combatCommander)
    operationOfficer.galaxyFowardWithScan(True)

def ProgenitorAndRelicSignalLoopOperation_Test():
    gameControllor = GameControllor()
    fleetCommander = FleetCommander(gameControllor,specialSignalMissionLoop)
    combatCommander = CombatCommander()
    operationOfficer = OperationOfficer(gameControllor,fleetCommander,combatCommander)
    operationOfficer.SpecificSignalMissionLoop_Test(True)
