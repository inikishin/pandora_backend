from rest_framework import routers
from .views import FeaturesViewSet, FeaturesCodeViewSet

router = routers.DefaultRouter()
router.register(r'features', FeaturesViewSet)
router.register(r'feature-codes', FeaturesCodeViewSet)
