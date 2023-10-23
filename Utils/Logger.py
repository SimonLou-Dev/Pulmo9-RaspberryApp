
class Logger:
    def print(self, current_class, level, message ):
        if level == 0:
            level = "DEBUG"
        elif level == 1:
            level = "INFO"
        elif level == 2:
            level = "WARNING"
        elif level == 3:
            level = "ERROR"
        else:
            level = "UNKNOWN"
        print("[" + current_class + "] " + level + " : " + message)