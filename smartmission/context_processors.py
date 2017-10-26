# context processor for custom settings
from course.models import CourseCategory, CourseDuration


def get_category(request):

    return {'categories': CourseCategory.objects.filter(is_active=True)}


def get_duration(request):

    return {'durations': CourseDuration.objects.all()}
