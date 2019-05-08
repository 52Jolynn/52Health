#!/usr/bin/env python
# -*- coding: GBK -*-

from bs4 import BeautifulSoup
import pytesseract
from PIL import Image
import time
import requests
from io import BytesIO
import json
import traceback


def main():
    # 张广兰 产科门诊主任 HIS_CD=100202 DEP_ID=2003400FEZX239893 DOC_ID=f0618
    # 刘红姣 成人中医主治 HIS_CD=100202 DEP_ID=20019100FEZX239894 DOC_ID=f0894
    # 刘晓青 成人中医主治 HIS_CD=100202 DEP_ID=20019100FEZX239894 DOC_ID=2225
    # 医院id
    his_id = "100202"
    # 科室id
    dep_id = "2003400FEZX239893"
    # 科室名称
    dep_nm = "产科门诊主任"
    # 医生id
    doc_id = "f0618"
    # 医生名称
    doc_nm = "张广兰"
    # 预约挂号时间
    date = "2017-06-14"
    # 挂号费
    reg_fee = 100
    # 诊疗费
    tre_fee = 800
    # id card
    ope_idc = "您的身份证号"
    # sex
    ope_sex = "F"

    # 登录
    session = requests.session()
    login(session, username=ope_idc)

    while True:
        try:
            # 查询号源
            # queryResult = query(session, his_id, dep_id, doc_id, date, tim_flag)
            # print queryResult
            # if 0 == int(queryResult["max_elapse"]):
            # print "no available doctor!"
            # time.sleep(0.001)
            # continue
            # start_tim = queryResult["start_time"]
            # end_tim = queryResult["end_time"]

            start_time = "start_time"
            end_time = "end_time"
            am_times = [{start_time: "08:00", end_time: "08:30"}, {start_time: "08:30", end_time: "09:00"},
                        {start_time: "09:00", end_time: "09:30"}, {start_time: "09:30", end_time: "10:00"},
                        {start_time: "10:00", end_time: "10:30"}, {start_time: "10:30", end_time: "11:00"},
                        {start_time: "11:00", end_time: "11:30"}]
            pm_times = [{start_time: "14:00", end_time: "14:30"}, {start_time: "14:30", end_time: "15:00"},
                        {start_time: "15:00", end_time: "15:30"}, {start_time: "15:30", end_time: "16:00"},
                        {start_time: "16:00", end_time: "16:30"}]
            if guahao(session, am_times, his_id, dep_id, dep_nm, doc_id, doc_nm, date, 1, reg_fee, tre_fee, ope_sex,
                      ope_idc) or guahao(session, pm_times, his_id, dep_id, dep_nm, doc_id, doc_nm, date, 2, reg_fee,
                                         tre_fee, ope_sex, ope_idc):
                print "gua dao hao la!!!"
                break
            #time.sleep(10)
        except:
            traceback.print_exc()


def guahao(session, times, his_id, dep_id, dep_nm, doc_id, doc_nm, date, tim_flag, reg_fee, tre_fee, ope_sex, ope_idc):
    for availableTime in times:
        response = session.get("http://www.guahao.gov.cn/pmodule/include/codeImage.jsp")
        image = Image.open(BytesIO(response.content))
        vcode = pytesseract.image_to_string(image)
        # print vcode

        token = long(time.time() * 100)
        # print "token: %s" % token

        guahao_params = {
            "token": token,
            "YB_CHK_FLG": 1,
            "REG_FLG": 0,
            "REG_PAY_TYP": "",
            "HIS_CD": his_id,
            "DEP_ID": dep_id,
            "DEP_NM": dep_nm,
            "DOC_ID": doc_id,
            "DOC_NM": doc_nm,
            "REG_DAT": date,
            "TIM_FLG": tim_flag,
            "STA_TIM": availableTime["start_time"],
            "END_TIM": availableTime["end_time"],
            "REG_FEE": reg_fee,
            "TRE_FEE": tre_fee,
            "VER_ID": vcode,
            "OPE_SEX": ope_sex,
            "OPE_IDC": ope_idc,
            "CONN_NO": "",
            "CONN_TYP": "",
            "CONN_BIRTH_DT": "",
            "GRAVIDAFLAG": "",
            "SUCKLEFLAG": ""
        }

        guahao_response = session.post(url="http://www.guahao.gov.cn/guahao.xhtml", data=guahao_params)
        #print guahao_response.content
        response_json = json.loads(guahao_response.content, "gbk")
        if "ORD_NO" in response_json.keys() and response_json["ORD_NO"] != "":
            print response_json["ORD_NO"]
            return True
        else:
            print "try to guahao... %s" % time.time()
    return False


def login(session, username):
    session.get(url="http://www.guahao.gov.cn/")

    # 登录
    params = {"CARD_NO": username, "CARD_TYPE": "1", "PWD": "您的密码"}
    url = "http://www.guahao.gov.cn/logined.xhtml"
    response = session.post(url=url, data=params)
    print response.content

    session.get(url="http://www.guahao.gov.cn/index.xhtml")
    session.get(url="http://www.guahao.gov.cn/sso-client-user.jsp")
    session.post(url="http://www.guahao.gov.cn/notice.xhtml?r=0.6644507846651349")
    session.get(url="http://www.guahao.gov.cn/ajxarea.xhtml?r=0.3952968216541546")
    session.get(url="http://www.guahao.gov.cn/ajxhospitals.xhtml?ARE_ID=&r=0.533437125219655")
    session.get(url="http://www.guahao.gov.cn/disList.xhtml?channel=CH1")
    session.get(url="http://www.guahao.gov.cn/friend_link_typ.xhtml?r=0.3707343001758905")
    session.get(url="http://www.guahao.gov.cn/hospitals.xhtml?ARE_ID=")
    session.get(url="http://www.guahao.gov.cn/ajxarea.xhtml?r=0.6194890991807969")
    session.get(
        url="http://www.gzhealth.gov.cn/cuteframework-sso-server/login?service=http%3A%2F%2F172.16.150.185%2Fsso-client-user.jsp&portalLoginUrl=/smjkfw/login.jsp")
    session.get(url="http://www.guahao.gov.cn/ordernum.xhtml ")


def query(session, his_cd, dep_id, doc_id, reg_dat, tm_fag=1):
    url = "http://www.guahao.gov.cn/ajx_regtime.xhtml?HIS_CD=%s&DEP_ID=%s&DOC_ID=%s&REG_DAT=%s&TM_FLG=%d" % (
        his_cd, dep_id, doc_id, reg_dat, tm_fag)
    response = session.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    trList = soup.select("tr")
    parse_result = []
    for i in range(len(trList)):
        if i == 0:
            continue
        parse_stat = {}
        tdList = trList[i].select("td")
        for j in range(len(tdList)):
            tdItem = tdList[j]
            if j == 0:
                parse_stat["start_time"] = tdItem.string[:5]
                parse_stat["end_time"] = tdItem.string[-5:]
            elif j == 2:
                parse_stat["elapse"] = tdItem.string
                break
        parse_result.append(parse_stat)

    start_time = None
    end_time = None
    max_elapse = 0;
    for r in parse_result:
        if r["elapse"] >= max_elapse:
            max_elapse = r["elapse"]
            start_time = r["start_time"]
            end_time = r["end_time"]

    return {"start_time": start_time, "end_time": end_time, "max_elapse": max_elapse}


if __name__ == "__main__":
    main()
