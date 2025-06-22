from django.contrib import admin
from .models import FabricImage


@admin.register(FabricImage)
class FabricImageAdmin(admin.ModelAdmin):
    """관리자 페이지에서 FabricImage 모델 관리"""

    list_display = ["id", "image", "uploaded_at", "has_prediction"]
    list_filter = ["uploaded_at"]
    search_fields = ["id"]
    readonly_fields = ["uploaded_at", "prediction_result"]

    def has_prediction(self, obj):
        """예측 결과 존재 여부"""
        return bool(obj.prediction_result)

    has_prediction.boolean = True
    has_prediction.short_description = "예측 완료"

    def get_queryset(self, request):
        return super().get_queryset(request).order_by("-uploaded_at")
