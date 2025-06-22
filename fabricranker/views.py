from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from .models import FabricImage
from .forms import FabricImageForm
from .ml_predictor import predict_fabric_material
import logging

logger = logging.getLogger(__name__)


class FabricPredictionView(FormView):
    """옷 재질 예측 메인 뷰"""

    template_name = "fabric_prediction/index.html"
    form_class = FabricImageForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "옷 재질 예측 시스템"
        return context

    def form_valid(self, form):
        """폼이 유효할 때 처리"""
        try:
            # 이미지 저장
            fabric_image = form.save()

            # 딥러닝 모델로 예측 수행
            prediction_result = predict_fabric_material(fabric_image.image.path)

            # 예측 결과를 모델에 저장 (선택사항)
            fabric_image.prediction_result = prediction_result
            fabric_image.save()

            # 결과를 백분율로 변환 (0~1 -> 0~100)
            result_with_percentage = [
                (material, confidence * 100)
                for material, confidence in prediction_result
            ]

            # 템플릿에 결과 전달
            context = self.get_context_data()
            context["result"] = result_with_percentage
            context["uploaded_image"] = fabric_image

            return render(self.request, self.template_name, context)

        except Exception as e:
            logger.error(f"예측 중 오류 발생: {str(e)}")
            messages.error(
                self.request, "이미지 분석 중 오류가 발생했습니다. 다시 시도해주세요."
            )
            return self.form_invalid(form)

    def form_invalid(self, form):
        """폼이 유효하지 않을 때 처리"""
        messages.error(self.request, "올바른 이미지 파일을 선택해주세요.")
        return super().form_invalid(form)


def fabric_prediction_view(request):
    """함수 기반 뷰 (대안)"""
    form = FabricImageForm()
    result = None
    uploaded_image = None

    if request.method == "POST":
        form = FabricImageForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                # 이미지 저장
                fabric_image = form.save()

                # 딥러닝 모델로 예측 수행
                prediction_result = predict_fabric_material(fabric_image.image.path)

                # 예측 결과를 모델에 저장
                fabric_image.prediction_result = prediction_result
                fabric_image.save()

                # 결과를 백분율로 변환
                result = [
                    (material, confidence * 100)
                    for material, confidence in prediction_result
                ]

                uploaded_image = fabric_image

            except Exception as e:
                logger.error(f"예측 중 오류 발생: {str(e)}")
                messages.error(request, "이미지 분석 중 오류가 발생했습니다.")
        else:
            messages.error(request, "올바른 이미지 파일을 선택해주세요.")

    context = {
        "form": form,
        "result": result,
        "uploaded_image": uploaded_image,
        "title": "옷 재질 예측 시스템",
    }

    return render(request, "index.html", context)
