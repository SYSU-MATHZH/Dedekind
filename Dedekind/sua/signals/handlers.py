from django.db.models.signals import pre_save, pre_delete, post_delete
from django.dispatch import receiver
from sua.models import Sua, Student, Sua_Application


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


@receiver(post_delete, sender=Student, dispatch_uid="Student_post_delete")
def Student_post_delete_handler(sender, instance, *args, **kwargs):
    if instance.user:  # just in case user is not specified
        instance.user.delete()


@receiver(
    post_delete,
    sender=Sua_Application,
    dispatch_uid="Sua_Application_post_delete",
)
def Sua_Applicationpost_delete_handler(sender, instance, *args, **kwargs):
    if instance.sua:  # just in case user is not specified
        instance.sua.delete()
    if instance.proof:
        pf = instance.proof
        if pf.sua_application_set.count() == 0 and not pf.is_offline:
            instance.proof.delete()
