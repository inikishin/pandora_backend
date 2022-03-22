from django.contrib import admin
from django.urls import include, path
from .views import index_view

from quote.urls import router as quote_router
from prediction.urls import router as prediction_router
from daily_analysis.urls import router as daily_analysis_router

urlpatterns = [
    path('', index_view),
    path('admin/', admin.site.urls),
    path('api/quotes/', include(quote_router.urls)),
    path('api/predictions/', include(prediction_router.urls)),
    path('api/daily-analysis/', include(daily_analysis_router.urls))
]
