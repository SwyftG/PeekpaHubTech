# encoding: utf-8
__author__ = 'lianggao'
__date__ = '2019/11/6 1:11 AM'
import datetime
from django.core.mail import send_mail, send_mass_mail, EmailMultiAlternatives
from PeekpaHubWebsite.settings.base import CONFIG_JSON
from .models import CaoliuFid2, CaoliuFid4, CaoliuFid7, CaoliuFid15, CaoliuFid25, CaoliuFid26


def send_daily_check_mail():
    print("send_daily_mail")
    cur_day = datetime.datetime.now().strftime('%Y-%m-%d')
    subject = "PeekpaHub:" + cur_day
    message = CONFIG_JSON.get("email_setting").get("daily_check").get("EMAIL_IP_ADDRESS") + \
              " \nTime:" + datetime.datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')

    from_email = CONFIG_JSON.get("email_setting").get("daily_check").get("EMAIL_FROM_EMAIL")
    recipient_list = CONFIG_JSON.get("email_setting").get("daily_check").get("EMAIL_RECIPIENT_LIST")

    result_2, result_size_2 = CaoliuFid2.check_by_time(cur_day)
    result_4, result_size_4 = CaoliuFid4.check_by_time(cur_day)
    result_7, result_size_7 = CaoliuFid7.check_by_time(cur_day)
    result_15, result_size_15 = CaoliuFid15.check_by_time(cur_day)
    result_25, result_size_25 = CaoliuFid25.check_by_time(cur_day)
    result_26, result_size_26 = CaoliuFid26.check_by_time(cur_day)
    if int(result_size_2) == 0 and int(result_size_4) == 0 and int(result_size_7) == 0 and int(result_size_15) == 0 and int(result_size_25) == 0 and int(result_size_26) == 0:
        subject = subject + ":NoData!NoData!NoData!"
        message = message \
                  + '\n' + '技术讨论区: ' + result_size_7 \
                  + '\n' + '亚洲无码区: ' + result_size_2 \
                  + '\n' + '亚洲有码区: ' + result_size_15 \
                  + '\n' + '欧美影视区: ' + result_size_4 \
                  + '\n' + '国产原创区: ' + result_size_25 \
                  + '\n' + '中字原创区: ' + result_size_26
    else:
        subject = subject + ":DailyCheck success.Total:" + str(int(result_size_2) + int(result_size_4) + int(result_size_7) + int(result_size_15) + int(result_size_25) + int(result_size_26))
        message = message \
                  + '\n' + '技术讨论区: ' + result_size_7 \
                  + '\n' + '亚洲无码区: ' + result_size_2 \
                  + '\n' + '亚洲有码区: ' + result_size_15 \
                  + '\n' + '欧美影视区: ' + result_size_4 \
                  + '\n' + '国产原创区: ' + result_size_25 \
                  + '\n' + '中字原创区: ' + result_size_26

    res = send_mail(subject, message, from_email, recipient_list)
    print("result:", res)