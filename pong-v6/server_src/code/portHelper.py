import psutil

def check_port(port:int) -> bool:
    '''Return True if Port is in Use'''
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port == port:
            return True
    
    return False