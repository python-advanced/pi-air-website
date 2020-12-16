from datetime import timezone
import pytz


def utc_to_local(utc_dt):
    tw = pytz.timezone('Asia/Taipei')
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=tw)


def format_title(source, y):
    unit = ''
    if source == 'VOC-CCS':
        unit = 'PPB'
    elif source == 'VOC-TGS':
        unit = ''
    elif source == 'PM2.5':
        unit = 'μg/m3'
    elif source == 'PM10':
        unit = 'μg/m3'

    return source + ':  {:20,.0f}'.format(y) + ' ' + unit


def get_account_text(is_online):
    acct_status_text = '離線'
    acct_class_name = 'dot-offline'
    if is_online:
        acct_status_text = '線上'
        acct_class_name = 'dot-online'
    return acct_status_text, acct_class_name
