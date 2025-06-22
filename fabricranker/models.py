from django.db import models
from django.core.validators import FileExtensionValidator
import os


class FabricImage(models.Model):
    """옷 이미지 모델"""

    image = models.ImageField(
        upload_to="fabric_images/",
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])],
        help_text="JPG, JPEG, PNG 파일만 업로드 가능합니다.",
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # 예측 결과 저장 (선택사항)
    prediction_result = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = "옷 이미지"
        verbose_name_plural = "옷 이미지들"

    def __str__(self):
        return f"Fabric Image {self.id} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"

    def delete(self, *args, **kwargs):
        """이미지 파일도 함께 삭제"""
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)
