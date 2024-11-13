from account.models import SidebarGroup


def get_sidebar_urls(request):
    sidebar_urls = SidebarGroup.objects.all().order_by('name').prefetch_related('items', 'items__url')
    version = '0.1'
    # operation_date = "---" if request.user.is_anonymous else get_operation_date(request.user.get_branch().id)
    # operation_date = datetime.now().date()

    context = {
        'sidebar_urls': sidebar_urls,
        'version': version,
    }

    return context
