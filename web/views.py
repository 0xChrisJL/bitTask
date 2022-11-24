import time
import requests

from taskCode.actions import Config
from taskCode.actions.driver import Driver
from taskCode.task import taskBase
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from web.models import AdsTask


def index(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username == "cc" and password == "123":
            return render(request, 'task_status.html')
        else:
            return HttpResponse("登录失败！")
    return render(request, 'index.html')


def list(request):
    date = request.GET.get('start_time')
    if date is None:
        date = time.strftime('%Y-%m-%d')
    date_list = AdsTask.objects.filter(dayTime=date).all()
    return render(request, 'task_list.html', {'data_list': date_list, 'date': date})


def status(request):
    date = request.GET.get('start_time')
    if date is None:
        date = time.strftime('%Y-%m-%d')
    allTask = AdsTask.objects.filter(dayTime=date).all()

    # carv任务判断成功数和失败数
    carvSuccess = AdsTask.objects.filter(Q(Carv__contains="成功") & Q(dayTime=date)).all()
    carvFail = AdsTask.objects.filter(Q(Carv__contains="失败") & Q(dayTime=date) | Q(Carv=None) & Q(dayTime=date)).all()

    # CoinGecko任务判断成功数和失败数
    CGKSuccess = AdsTask.objects.filter(
        Q(Coingecko__contains="分钟前") & Q(dayTime=date) | Q(Coingecko__contains="下次") & Q(dayTime=date)).all()
    CGKFail = AdsTask.objects.filter(
        Q(Coingecko__contains="天前") & Q(dayTime=date) | Q(Coingecko=None) & Q(dayTime=date)).all()

    # Zetalabs任务判断成功数和失败数
    ZetaSuccess = AdsTask.objects.filter(Q(Zetalabs__contains="swap") & Q(dayTime=date)).all()
    ZetaToken = AdsTask.objects.filter(Q(Zetalabs__contains="测试币") & Q(dayTime=date)).all()
    ZetaFail = AdsTask.objects.filter(Q(Zetalabs=None) & Q(dayTime=date)).all()

    allStatus = [
        len(allTask), len(carvSuccess), len(carvFail), len(CGKSuccess), len(CGKFail),
        len(ZetaSuccess), len(ZetaToken), len(ZetaFail),
        carvFail, CGKFail, ZetaFail, date
    ]

    return render(request, 'task_status.html', {'task_status': allStatus})


def runTask(request):
    checkboxValue = request.GET.get('checkboxValue')
    checkboxValue = checkboxValue[1:len(checkboxValue) - 1]
    inputValue = request.GET.get('inputValue')
    # checkbox为复选框的值
    checkboxNum = []
    inputNum = []
    # 获取checkbox里面的值
    for i in checkboxValue.split(','):
        checkboxNum.append(i[1:len(i) - 1])

    for a in inputValue.split(','):
        inputNum.append(int(a))

    for x in inputNum:
        # 定义acc为账号id
        adsId = Config.adsId(x)
        # 定义adsNUm为窗口编号
        adsNum = Config.adsNum(x)
        url = "http://local.adspower.net:50325/api/v1/browser/"
        open_url = url + "start?user_id=" + adsId + "&open_tabs=1"
        close_url = url + "stop?user_id=" + adsId
        driver = Driver.Driver(open_url)
        tb = taskBase(driver)

        try:
            tb.wallet.metamask_login(adsNum)
        except BaseException:
            continue

        if '1' in checkboxNum:
            try:
                tb.carv.carv_checkin(adsNum)
            except BaseException:
                pass

        # if '2' in checkboxNum:
        #     try:
        #         tb.coinmarketcap.coinmarketcap_get(adsNum)
        #     except BaseException:
        #         pass

        if '3' in checkboxNum:
            try:
                tb.coingecko.coingecko_get(adsNum)
            except BaseException:
                pass

        if '4' in checkboxNum:
            try:
                tb.zetalabs.zeta_getToken(adsNum)
            except BaseException:
                pass

        driver.quit()
        requests.get(close_url)

    return JsonResponse({'code': 0})
