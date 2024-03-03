from rest_framework.routers import DefaultRouter

from product import views

router = DefaultRouter()
router.register('products', views.ProductsViewSet)

urlpatterns = router.urls
