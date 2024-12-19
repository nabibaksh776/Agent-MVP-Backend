from django.contrib import admin
from .models import Customer, Agent, Visitor, Chat, SalesTechnique,AgentDocument,SalesTechniquesDocument

# Register your models here.


admin.site.register(Customer)
admin.site.register(Agent)
admin.site.register(AgentDocument)
admin.site.register(Visitor)
admin.site.register(Chat)
admin.site.register(SalesTechnique)
admin.site.register(SalesTechniquesDocument)