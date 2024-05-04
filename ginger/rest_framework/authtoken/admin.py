from ginger.contrib import admin
from ginger.contrib.admin.utils import quote
from ginger.contrib.admin.views.main import ChangeList
from ginger.contrib.auth import get_user_model
from ginger.core.exceptions import ValidationError
from ginger.urls import reverse
from ginger.utils.translation import gettext_lazy as _

from ginger.rest_framework.authtoken.models import Token, TokenProxy

User = get_user_model()


class TokenChangeList(ChangeList):
    """Map to matching User id"""
    def url_for_result(self, result):
        pk = result.user.pk
        return reverse('admin:%s_%s_change' % (self.opts.app_label,
                                               self.opts.model_name),
                       args=(quote(pk),),
                       current_app=self.model_admin.admin_site.name)


class TokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'created')
    fields = ('user',)
    search_fields = ('user__username',)
    search_help_text = _('Username')
    ordering = ('-created',)
    actions = None  # Actions not compatible with mapped IDs.

    def get_changelist(self, request, **kwargs):
        return TokenChangeList

    def get_object(self, request, object_id, from_field=None):
        """
        Map from User ID to matching Token.
        """
        queryset = self.get_queryset(request)
        field = User._meta.pk
        try:
            object_id = field.to_python(object_id)
            user = User.objects.get(**{field.name: object_id})
            return queryset.get(user=user)
        except (queryset.model.DoesNotExist, User.DoesNotExist, ValidationError, ValueError):
            return None

    def delete_model(self, request, obj):
        # Map back to actual Token, since delete() uses pk.
        token = Token.objects.get(key=obj.key)
        return super().delete_model(request, token)


admin.site.register(TokenProxy, TokenAdmin)
