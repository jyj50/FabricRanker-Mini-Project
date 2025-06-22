from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "fabric_prediction"

urlpatterns = [
    path("", views.fabric_prediction_view, name="index"),
    # 클래스 기반 뷰를 사용하려면:
    # path('', views.FabricPredictionView.as_view(), name='index'),
]

# 개발 환경에서 미디어 파일 서빙
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
