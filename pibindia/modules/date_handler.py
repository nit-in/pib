from datetime import datetime


def yyyymmmdd(idate):
    strp_date = datetime.strptime(idate, "%Y-%m-%d")
    return strp_date.strftime("%Y/%b/%d")


def yyyy(idate):
    strp_date = datetime.strptime(idate, "%Y-%m-%d")
    return strp_date.strftime("%Y")


def bbb(idate):
    strp_date = datetime.strptime(idate, "%Y-%m-%d")
    return strp_date.strftime("%b")


def mm(idate):
    strp_date = datetime.strptime(idate, "%Y-%m-%d")
    return strp_date.strftime("%m")


def dd(idate):
    strp_date = datetime.strptime(idate, "%Y-%m-%d")
    return strp_date.strftime("%d")


def ddmmmyyyy(idate):
    strp_date = datetime.strptime(idate, "%Y-%m-%d")
    return strp_date.strftime("%d/%b/%Y")


def dd_mmm_yyyy(idate):
    strp_date = datetime.strptime(idate, "%Y/%b/%d")
    return strp_date.strftime("%d_%b_%Y")
