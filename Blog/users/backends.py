from django.conf import settings
from django.contrib.auth.hashers import check_password
from users.models import CustomUser
import sys


class CustomUserBackend:
	
	def authenticate(self,request,email=None,password=None):
		print(sys.stderr,' authenticate ......')
		if email and password:
			try:
				user = CustomUser.objects.get(email=email)
				if check_password(password,user.password):
					if user.is_active:
						return user
			except CustomUser.DoesNotExist:
				print(sys.stderr,' except ......')
				return None
		print(sys.stderr,' return None ......')
		return None

	def get_user(self,user_id):
		try:
			print(sys.stderr,' get_user ......')
			return CustomUser.objects.get(pk=user_id)
		except CustomUser.DoesNotExist:
			print(sys.stderr,' get_user ......')
			return None

