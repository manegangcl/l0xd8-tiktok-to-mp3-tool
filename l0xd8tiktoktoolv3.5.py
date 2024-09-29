# this is a tool for downloading tiktok videos as mp3 files, the mp4 is downloaded first and stored in memory, than converted into mp3.

import sys
import uuid
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt
import io
from yt_dlp import YoutubeDL
from pydub import AudioSegment

class TikTokToMp3(QWidget):
    def __init__(self):
        super().__init__()
        self.dragging = False
        self.offset = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.title_bar = QWidget(self)
        title_layout = QHBoxLayout()

        self.title_label = QLabel('l0xd8s tiktok mp3 downloader', self)
        self.close_button = QPushButton('✕', self)
        self.close_button.setFixedSize(30, 30)
        self.close_button.clicked.connect(self.close)

        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.close_button)
        self.title_bar.setLayout(title_layout)

        layout.addWidget(self.title_bar)

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText('enter tiktok video url')
        layout.addWidget(self.url_input)

        self.convert_button = QPushButton('convert to mp3', self)
        self.convert_button.clicked.connect(self.download_and_convert)
        layout.addWidget(self.convert_button)

        self.status_label = QLabel('waiting for input', self)
        layout.addWidget(self.status_label)

        self.setLayout(layout)
        self.setFixedSize(400, 250)

        self.apply_styles()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

    def apply_styles(self):
        style = """
        QWidget {
            background-color: #1e1e1e;
            color: #f0f0f0;
        }
        QLineEdit {
            background-color: #333;
            color: #f0f0f0;
            border: 1px solid #555;
            padding: 5px;
            font-size: 14px;
            border-radius: 5px;
        }
        QPushButton {
            background-color: #555;
            color: #f0f0f0;
            border: none;
            padding: 8px;
            font-size: 14px;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #777;
        }
        QPushButton:pressed {
            background-color: #999;
        }
        QLabel {
            font-size: 14px;
            padding: 10px;
        }
        QLabel#title_label {
            font-size: 16px;
            font-weight: bold;
        }
        """
        self.setStyleSheet(style)
        self.title_label.setObjectName("title_label")

    def download_tiktok_video(self, video_url):
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'outtmpl': '-',
                'noplaylist': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp4',
                }],
                'postprocessor_args': ['-acodec', 'aac']
            }

            with YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(video_url, download=True)
                audio_data = ydl.urlopen(info_dict['url']).read()
                return audio_data
        except Exception as e:
            self.status_label.setText(f"error downloading video: {e}")
            return None

    def convert_to_mp3(self, audio_data):
        try:
            audio = AudioSegment.from_file(io.BytesIO(audio_data), format="mp4")
            unique_id = str(uuid.uuid4())
            mp3_output_path = f"output_{unique_id}.mp3"
            audio.export(mp3_output_path, format="mp3")
            self.status_label.setText(f"mp3 saved at {mp3_output_path}")
        except Exception as e:
            self.status_label.setText(f"error converting to mp3: {e}")

    def download_and_convert(self):
        video_url = self.url_input.text()
        
        if video_url:
            self.status_label.setText("downloading...")
            audio_data = self.download_tiktok_video(video_url)
            
            if audio_data:
                self.status_label.setText("converting to mp3...")
                self.convert_to_mp3(audio_data)
            else:
                self.status_label.setText("download failed")
        else:
            self.status_label.setText("please enter a valid url")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPosition().toPoint() - self.offset)

    def mouseReleaseEvent(self, event):
        self.dragging = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TikTokToMp3()
    window.show()
    sys.exit(app.exec())