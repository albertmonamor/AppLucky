from Api.manager import EManager

DAY:float = 3600*24


def titleEventTime(time_s: float, time_e) -> tuple[str, bool]:
    countdown: float = time_e - time_s
    if countdown < 0:
        return "האירוע הסתיים!", False
    elif 0 <= countdown <= 100:
        return "האירוע מסתיים עכשיו!", False
    elif 100 < countdown < DAY*2:
        return "האירוע מתקרב לסיום!", True
    elif DAY*2 < countdown:
        return "האירוע בעיצומו!", True


def getPage(name_event: str) -> str:
    if name_event == EManager.alpha:
        return 'alpha'
    elif name_event == EManager.rasta:
        return 'rasta'
    elif name_event == EManager.product:
        return 'product'

    # return None


def idValid(_id: str):

    if _id.__len__() > 9 or not _id.isdigit():
        return 0

    size_of_id = 0
    for index, number in enumerate(_id):
        num_id = int(number)
        result = str(num_id * ((index % 2)+1))
        if result.__len__() % 2 == 0:
            result = str(int(result[0])+int(result[1]))
        size_of_id += int(result)

    return size_of_id % 10 == 0

