from support.models import StaffProfile,ClientProfile
def get_user_profile( user ):
    profile = None
    try: 
        profile = StaffProfile.objects.get(user = user)
    except StaffProfile.DoesNotExist:
        profile = ClientProfile.objects.get(user = user)
    except ClientProfile.DoesNotExist:
        profile = None
    finally:
        return profile