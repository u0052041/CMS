from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from product.views import ProductViewSet
from order.views import OrderViewSet
from userprofile.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("product", ProductViewSet)
router.register("order", OrderViewSet)
router.register("user", UserViewSet)

app_name = "api"
urlpatterns = router.urls
