from django.db import migrations

def create_missing_profiles(apps, schema_editor):
    # Get models dynamically to avoid dependency issues
    User = apps.get_model('auth', 'User')
    UserProfile = apps.get_model('core', 'UserProfile')

    # Loop through all users and create a profile if missing
    for user in User.objects.all():
        if not UserProfile.objects.filter(user=user).exists():
            UserProfile.objects.create(user=user)

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_userprofile'),
    ]

    operations = [
        migrations.RunPython(create_missing_profiles),
    ]

