class AppLoopController(object):
    __instance = None
    isRunning = None

    def __new__(cls, *args, **kwargs):
        if AppLoopController.__instance is None:
            AppLoopController.__instance = object.__new__(cls)
            AppLoopController.__instance.start_app_loop
        return AppLoopController.__instance

    def start_app_loop(self):
        # TODO: implement start_app_loop()
        pass

    def stop_app_loop(self):
        # TODO: implement stop_app_loop()
        pass