import binascii
import os


FILE_NAME_DB: str = "AppLucky.db"
SESSION: dict = {}
SESSION_ANON: callable = lambda: binascii.b2a_hex(os.urandom(12)).decode()
DES_EVENT_CLOSED = "האירוע {en} נסגר!\n ב {eo} האירוע ייפתח שוב"


# /* static definition for database AppLucky */
"""
        setEvent("rasta", time(), time()+EManager.rasta_time)
        setEvent("alpha", time(), time()+EManager.alpha_time)
        setEvent("product", time(), time()+EManager.product_time)
"""


class EManager:
    # /* static */
    alpha, alpha_time = "1", (3600*24)*7
    rasta, rasta_time = "2", (3600*24)*4
    product, product_time = "3", (3600*24)*7
    event_break = (3600*24)

    @staticmethod
    def get_time(event) -> int:
        if EManager.alpha == event:
            return EManager.alpha_time
        elif EManager.rasta == event:
            return EManager.rasta_time
        elif EManager.product == event:
            return EManager.product_time
        return 0



