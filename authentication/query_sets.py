from django.db.models import QuerySet


# Overriding query set to extend my custom queries
class OTPQuerySet(QuerySet):
    def get_data_by_email(self, email, otp):
        return self.get(user__email=email, otp_code=otp)

    def get_data_by_otp_id_and_email(self, email, id):
        return self.get(user__email=email, id=id)
