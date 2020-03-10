import sys
import datetime

normal_mode_process_path = '/external/b/HSAF'
mode = 'online'
date_mode = 'single'
product = None
process_path = normal_mode_process_path
offlin_mode_process_path = '/external/b/HSAF/OFFLINE'
product_list = {'H10', 'H12', 'H34', 'H35', 'H13'}


def check_date(date_str):
    try:
        datetime.datetime.strptime(date_str, '%Y%m%d')
        return True
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYYMMDD (20190328)")


def get_working_dates(date1, date2=None, date_mask='%Y%m%d'):
    if check_date(date1):
        date_list = []
        date1 = datetime.datetime.strptime(date1, date_mask)
        if date2 is None:
            date_list.extend([date1.strftime(date_mask)])
            return date_list
        else:
            date2 = datetime.datetime.strptime(date2, date_mask)
            delta_days = date2 - date1
            icr_date = date1
            if date2 < date1:
                icr_date = date2
            for day_ in range(abs(delta_days.days) + 1):
                date_list.extend([(icr_date + datetime.timedelta(day_)).strftime(date_mask)])
            return date_list


if len(sys.argv) > 1 and sys.argv[1] in product_list:
    # print("Normal mode has been selected for: ", sys.argv[1])
    product = sys.argv[1]
else:
    raise Exception("ERROR", "product type is not selected")

if len(sys.argv) == 3:
    raise Exception("ERROR", "Offline mode needs date")

if len(sys.argv) == 4:
    if sys.argv[2] == 'offline' and check_date(sys.argv[3]):
        product = sys.argv[1]
        mode = sys.argv[2]
        working_date = get_working_dates(sys.argv[3])
        # print("Offline Mode has been activated for: ", sys.argv[3])
        process_path = offlin_mode_process_path
    else:
        raise Exception("ERROR", "Undefined date or mode has been given")

if len(sys.argv) == 5:
    if sys.argv[2] == 'offline' and check_date(sys.argv[3]) and check_date(sys.argv[4]):
        mode = sys.argv[2]
        product = sys.argv[1]
        working_date = get_working_dates(sys.argv[3], sys.argv[4])
        # print("Offline Mode has been activated for: ", sys.argv[3], "and", sys.argv[4])
        process_path = offlin_mode_process_path
    else:
        raise Exception("ERROR", "Undefined date or mode has been given")
