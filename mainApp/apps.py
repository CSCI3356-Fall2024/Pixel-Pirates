from django.apps import AppConfig

class MainappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mainApp"

    def ready(self):
        print("Signals loaded!")  
        import mainApp.signals 
        # import mainApp.adapter