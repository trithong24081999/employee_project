from django.core.management import call_command
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def load_initial_fixture(sender, **kwargs):
    # Đảm bảo chỉ load khi migrate đúng app
    if sender.name == 'employees':
        try:
            call_command('loaddata', 'groups.json')
            print("✅ Fixture initial_data.json đã được load")
        except Exception as e:
            print(f"⚠️ Không thể load fixture: {e}")