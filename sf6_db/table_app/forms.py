from django import forms
from .models import GameCharacter
import os
from django.conf import settings

from django.core.exceptions import ValidationError

class GameCharacterForm(forms.ModelForm):
    image = forms.FileField(required=False)  # Используем FileField для загрузки файла

    class Meta:
        model = GameCharacter
        fields = ['character_name', 'lore', 'image']  # Включаем поле для изображения

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            print('fuck', image)
            # Проверяем, что файл изображения загружен и имеет правильное расширение
            # if not image.name.endswith(('.jpg', '.jpeg', '.png')):
            #     raise ValidationError("Неподдерживаемый формат файла. Загружайте только .jpg, .jpeg или .png.")
            
            # Генерируем путь для сохранения изображения
            image_path = os.path.join('characters', image.name)  # Путь к файлу в папке characters

            # Сохраняем файл в директории MEDIA_ROOT
            with open(os.path.join(settings.MEDIA_ROOT, image_path), 'wb+') as f:
                for chunk in image.chunks():
                    f.write(chunk)

            # Возвращаем путь к файлу, который будет сохранен в CharField модели
            return image_path
        return None  # Если файл не был загружен, возвращаем None
