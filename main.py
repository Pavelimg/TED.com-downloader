import ffmpeg
import requests
import os


def combine_video_audio(video_folder, audio_folder, output_file):
    try:
        # Получаем список файлов из папок
        video_files = sorted([os.path.join(video_folder, f) for f in os.listdir(video_folder) if f.endswith('.ts')])
        audio_files = sorted([os.path.join(audio_folder, f) for f in os.listdir(audio_folder) if f.endswith('.ts')])

        # Проверяем, что количество видео и аудиофайлов совпадает
        if len(video_files) != len(audio_files):
            raise ValueError("Количество видео и аудиофайлов не совпадает!")

        # Создаем списки входных файлов для FFmpeg
        video_inputs = [ffmpeg.input(video) for video in video_files]
        audio_inputs = [ffmpeg.input(audio) for audio in audio_files]

        # Объединяем видеофайлы
        combined_video = ffmpeg.concat(*video_inputs, v=1, a=0)

        # Объединяем аудиофайлы
        combined_audio = ffmpeg.concat(*audio_inputs, v=0, a=1)

        # Синхронизируем видео и аудио
        output = ffmpeg.output(combined_video, combined_audio, output_file)

        # Запускаем процесс
        ffmpeg.run(output)
        print(f"Объединение завершено: {output_file}")
    except ffmpeg.Error as e:
        print(f"Ошибка при объединении: {e.stderr.decode()}")
    except Exception as e:
        print(f"Ошибка: {e}")


def clear_folder(folder_path):
    if os.path.exists(folder_path):
        if os.path.isdir(folder_path):
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                try:
                    if os.path.isfile(file_path):  # Удаляем только файлы
                        os.unlink(file_path)
                except Exception as e:
                    print(f'Не удалось удалить {file_path}. Причина: {e}')
    else:
        os.mkdir(folder_path)


def download_video(video_id):
    i = 1
    while True:
        video = f"https://pu.tedcdn.com/consus/videos/{video_id}/segment-{i}-f11-v1.ts?"
        sound = f"https://pu.tedcdn.com/consus/videos/{video_id}/segment-{i}-f8-a1.ts?"

        req = requests.get(video)
        if req.status_code.real != 200:
            return
        with open(f"segments/video/segment_{str(i).rjust(3, '0')}.ts", "wb") as binary:
            binary.write(req.content)
        with open(f"segments/audio/segment_{str(i).rjust(3, '0')}.ts", "wb") as binary:
            binary.write(requests.get(sound).content)
        i += 1


if not os.path.isdir("segments"):
    os.mkdir("segments")
video_folder = 'segments/video'  # Папка с видеофайлами
audio_folder = 'segments/audio'  # Папка с аудиофайлами
output_file = 'output.mp4'  # Выходной файл

clear_folder(video_folder)
clear_folder(audio_folder)
download_video(4678)

combine_video_audio(video_folder, audio_folder, output_file)
