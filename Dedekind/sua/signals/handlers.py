from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from sua.models import Sua


@receiver(pre_save, sender=Sua, dispatch_uid="Sua_pre_save")
def Sua_pre_save_handler(sender, **kwargs):
    sua = kwargs['instance']
    if sua.is_valid:
        sua.update_student_suahours()
    else:
        if sua.last_time_suahours != 0.0:
            sua.clean_suahours()


@receiver(pre_delete, sender=Sua, dispatch_uid="Sua_pre_delete")
def Sua_pre_delete_handler(sender, **kwargs):
    sua = kwargs['instance']
    if sua.is_valid:
        sua.suahours = 0.0
        sua.update_student_suahours()
