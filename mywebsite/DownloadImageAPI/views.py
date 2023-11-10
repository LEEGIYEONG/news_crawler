from django.http import HttpResponse
from django.conf import settings
import os


def download_image(request, filename):
    # 정적 파일이 위치한 폴더 경로를 설정합니다.
    static_dir = os.path.join(settings.BASE_DIR, 'static')

    # 이미지 파일의 전체 경로를 구성합니다.
    filepath = os.path.join(static_dir, 'images', filename)

    # 파일 존재 여부를 확인하고, 해당 파일을 제공합니다.
    if os.path.exists(filepath):
        with open(filepath, 'rb') as f:
            response = HttpResponse(f.read(), content_type="image/jpeg")
            response['Content-Disposition'] = 'attachment; filename=' + filename
            return response
    else:
        return HttpResponse("Requested image not found", status=404)
