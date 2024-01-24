
def read_configs(group:str, data:str):
    from configparser import ConfigParser
    import os
    
    config = ConfigParser()
    config.read(f"{os.path.dirname(os.path.abspath(__file__))}/../config/config.ini")
    
    return config.get(group, data) if config.get(group, data) else None
