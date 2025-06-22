from django import forms
from .models import FabricImage


class FabricImageForm(forms.ModelForm):
    """옷 이미지 업로드 폼"""

    class Meta:
        model = FabricImage
        fields = ["image"]
        widgets = {
            "image": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                    "id": "fabric-image-input",
                }
            )
        }
        labels = {"image": "옷 이미지 선택"}

    def clean_image(self):
        """이미지 파일 유효성 검사"""
        image = self.cleaned_data.get("image")

        if image:
            # 파일 크기 제한 (5MB)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("이미지 파일 크기는 5MB 이하여야 합니다.")

            # 이미지 형식 확인
            if not image.content_type.startswith("image/"):
                raise forms.ValidationError("올바른 이미지 파일을 선택해주세요.")

        return image
