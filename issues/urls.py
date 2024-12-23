from rest_framework.routers import DefaultRouter
from .apis import IssueViewSet

router = DefaultRouter()
router.register(r'issues', IssueViewSet, basename='issue')

urlpatterns = [
    # Các URL khác
]
urlpatterns += router.urls
