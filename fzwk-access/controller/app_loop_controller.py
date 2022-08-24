class AppLoopController(object):
    __instance = None
    _isRunning = None

    def __new__(cls, *args, **kwargs):
        if AppLoopController.__instance is None:
            AppLoopController.__instance = object.__new__(cls)
            AppLoopController.__instance.start_app_loop
        return AppLoopController.__instance

    def start_app_loop(self):
        self._isRunning = True
        # TODO: implement start_app_loop()

    def stop_app_loop(self):
        self._isRunning = False
        # TODO: implement stop_app_loop()

    def toggle_app_loop(self):
        if self._isRunning:
            self.stop_app_loop()
        else:
            self.start_app_loop()
