from django.contrib import admin

from .models import user_account, user_type, user_info, cust_transaction

admin.site.register(user_account)
admin.site.register(user_type)
admin.site.register(user_info)
admin.site.register(cust_transaction)