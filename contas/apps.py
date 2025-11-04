import os

from django.apps import AppConfig


class ContasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contas'

    _cleared_on_start = False

    def ready(self):
        run_main = os.environ.get("RUN_MAIN")
        if run_main and run_main != "true":
            return

        if self.__class__._cleared_on_start:
            return
        self.__class__._cleared_on_start = True

        from threading import Timer

        def clear_sessions():
            from django.contrib.sessions.models import Session
            from django.db.utils import OperationalError, ProgrammingError

            try:
                Session.objects.all().delete()
            except (ProgrammingError, OperationalError):
                # Banco ainda não aplicou migrações de sessão
                pass

        Timer(0, clear_sessions).start()
