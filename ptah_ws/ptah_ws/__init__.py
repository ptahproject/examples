# ptah_ws
import ptah


def get_session():
    return ptah.transaction(_Session())
