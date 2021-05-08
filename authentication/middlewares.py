from .models import UserStat

from django.utils import timezone


# This middleware is to log every request to all API endpoints and record that in the user stat table to calculate user
# time spend on the site. This is not very accurate method but this get the job done
class LastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            # Getting user from session and get user stat and update last_activity field
            user_stat = UserStat.objects.get(user__email=request.user.email)
            user_stat.last_activity = timezone.now()
            user_stat.save()

        except UserStat.DoesNotExist:
            # If user stat not available because this is a first api request of the user, Creating new record to the
            # user
            user_stat = UserStat(user=request.user, last_activity=timezone.now())
            user_stat.save()

        except Exception as e:
            # Handling exception because if user is calling login for example, there is no session data.
            pass

        return self.get_response(request)
