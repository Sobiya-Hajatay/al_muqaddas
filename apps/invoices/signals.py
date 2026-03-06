#import uuid
#from django.db.models.signals import post_save
#from django.dispatch import receiver
#from .models import Invoice
#from .utils import generate_invoice_pdf


#@receiver(post_save, sender=Invoice)
#def create_invoice_pdf(sender, instance, created, **kwargs):
 #   if created and not instance.pdf_file:
  #      pdf_path = generate_invoice_pdf(instance)
   #     instance.pdf_file = pdf_path
    #    instance.save(update_fields=["pdf_file"])