from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from sua.models import Sua, Student, Sua_Application, GSua


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


@receiver(
    post_save,
    sender=GSua,
    dispatch_uid="GSua_post_save",
)
def GSua_post_save_handler(sender, instance, *args, **kwargs):
    for sua in instance.suas.all():
        if instance.is_valid:
            sua.is_valid = True
            sua.save()
        else:
            sua.is_valid = False
            sua.save()


@receiver(
    pre_delete,
    sender=GSua,
    dispatch_uid="GSua_pre_delete",
)
def GSua_pre_delete_handler(sender, instance, *args, **kwargs):
    for sua in instance.suas.all():
            sua.delete()


@receiver(
    m2m_changed,
    sender=GSua.suas.through,
    dispatch_uid="GSua_suas_m2m_changed",
)
def GSua_suas_m2m_changed_handler(sender, instance, action, *args, **kwargs):
    if action == "post_add":
        for sua in instance.suas.all():
            if instance.is_valid:
                sua.is_valid = True
                sua.save()
            else:
                sua.is_valid = False
                sua.save()
