reminder_manager = None

def get_reminder_manager():
    global reminder_manager
    if reminder_manager is None:
        raise Exception("ReminderManager ещё не инициализирован")
    return reminder_manager
