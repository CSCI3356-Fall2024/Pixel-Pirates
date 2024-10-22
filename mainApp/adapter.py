# from allauth.account.adapter import DefaultAccountAdapter
# from django.http import HttpResponse

# class NoSignupAccountAdapter(DefaultAccountAdapter):
#     def is_open_for_signup(self, request):
#         return False  # Disable all sign-up attempts

#     def respond_user_inactive(self, request, user):
#         return HttpResponse('Account is inactive. Please contact support.', status=403)
