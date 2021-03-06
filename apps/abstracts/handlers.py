from typing import (
    Optional,
)
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse

from abstracts.mixins import HttpResponseMixin


class ViewHandler(HttpResponseMixin):
    """Handler for validating request and generating response."""

    template_login_page: str = 'my_new_app/user_login.html'

    def get_validated_response(
        self,
        request: WSGIRequest
    ) -> Optional[HttpResponse]:
        """Get validated response."""
        if request.user.is_authenticated:
            return None

        return self.get_http_response(
            request,
            self.template_login_page
        )
