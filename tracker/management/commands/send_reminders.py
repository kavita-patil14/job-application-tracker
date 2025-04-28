from django.core.management.base import BaseCommand
from tracker.models import JobApplication
from django.contrib.auth.models import User
from django.core.mail import send_mail
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Send reminder emails based on status and deadlines'

    def handle(self, *args, **kwargs):
        today = date.today()
        upcoming = today + timedelta(days=3)

        apps = JobApplication.objects.filter(
            status__in=["Not Applied", "Interview Scheduled","Exam Scheduled"],
            deadline__isnull=False,
            deadline__gte=today,
            deadline__lte=upcoming
        )

        users = User.objects.filter(jobapplication__in=apps).distinct()

        for user in users:
            user_apps = apps.filter(user=user)
            if not user.email:
                continue

            message_lines = [f"Hi {user.username}, 👋\n"]
            message_lines.append("Here are your job updates:\n")

            for app in user_apps:
                if app.status == "Not Applied":
                    message_lines.append(
                        f"⏰ Reminder: You haven't applied for the position {app.job_title} at {app.company_name}.\n"
                        f"📅 Deadline: {app.deadline}\n"
                        f"🔗 Apply here: {app.job_link or 'No link provided'}\n"
                    )
                elif app.status == "Interview Scheduled":
                    message_lines.append(
                        f"📅 Interview Scheduled: You have an upcoming interview for {app.job_title} at {app.company_name}.\n"
                        f"🗓️ Interview Deadline: {app.deadline}\n"
                       
                        "💡 Make sure to prepare well!\n"
                    )

                elif app.status == "Exam Scheduled":
                    message_lines.append(
                        f"📝 Exam Scheduled: You have an upcoming exam for {app.job_title} at {app.company_name}.\n"
                        f"📅 Exam Date: {app.deadline}\n"
                    
                        "📖 Make sure to revise important topics and stay confident!\n"
                     )

                message_lines.append("-" * 50)  # Separator

            message_lines += [
                "\nTake quick action and give your best! 💪",
                "— Your Job Tracker App 🚀"
            ]

            try:
                send_mail(
                    subject="📬 Job Tracker Reminder: Your Upcoming Deadlines",
                    message="\n".join(message_lines),
                    from_email=None,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                self.stdout.write(self.style.SUCCESS(f"✅ Email sent to {user.email}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Failed to send email to {user.email}: {e}"))
