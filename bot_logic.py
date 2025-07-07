import os
import requests
import json
import subprocess # Add this import
import pendulum

# Get timezone from environment variable, default to 'Asia/Jakarta'
timezone_name = os.getenv("TIMEZONE", "Asia/Jakarta")

class BotLogic:
    def __init__(self, wa_client, allow_self_message=False):
        self.wa_client = wa_client
        self.allow_self_message = allow_self_message

    def handle_message(self, sender, message_content, is_self):
        if is_self and not self.allow_self_message:
            print(f"Ignoring self-message from {sender}")
            return

        if message_content:
            message_content_lower = message_content.lower()
            if message_content_lower.startswith("ping"):
                print(f"Replying 'pong' to {sender}")
                self.wa_client.send_message(sender, "pong")
            elif message_content_lower.startswith("menu"):
                self._send_menu(sender)
            elif message_content_lower.startswith("send"):
                self._handle_send_command(sender, message_content_lower)
            # Add more bot logic here for other commands or interactions
            # elif message_content.lower() == "hello":
            #     self.wa_client.send_message(sender, "Hi there!")
            elif message_content_lower.startswith("time"):
                self._send_current_time(sender)

    def _send_current_time(self, sender):
        current_time = pendulum.now(tz=timezone_name)
        formatted_time_string = f"Current time: {current_time.format('HH:mm:ss ZZ')}"
        print(f"Sending current time '{formatted_time_string}' to {sender}")
        self.wa_client.send_message(sender, formatted_time_string)

    def _send_menu(self, sender):
        menu_text = (
            "Halo! Saya adalah bot WhatsApp. Berikut adalah daftar perintah yang bisa Anda coba:\n\n"
            "1. `send text <pesan>`: Mengirim pesan teks.\n"
            "2. `send image`: Mengirim gambar (contoh dari URL).\n"
            "3. `send file`: Mengirim file (contoh PDF).\n"
            "4. `send video`: Mengirim video (contoh dari URL).\n"
            "5. `send contact`: Mengirim kontak.\n"
            "6. `send link`: Mengirim link dengan preview.\n"
            "7. `send location`: Mengirim lokasi.\n"
            "8. `send audio`: Mengirim audio.\n"
            "9. `send poll`: Mengirim polling.\n"
            "10. `send presence <type>`: Mengatur status kehadiran (available, unavailable, composing, paused, recording).\n"
            "11. `ping`: Membalas dengan 'pong'.\n"
            "12. `time`: Mendapatkan waktu saat ini.\n\n"
            # "Contoh: `send text Halo dunia!`"
        )
        self.wa_client.send_message(sender, menu_text)

    def _handle_send_command(self, sender, command):
        parts = command.split(' ', 2) # Split into 'send', 'type', 'args...'
        if len(parts) < 2:
            self.wa_client.send_message(sender, "Perintah 'send' tidak lengkap. Gunakan `send menu` untuk melihat opsi.")
            return

        send_type = parts[1]
        args = parts[2] if len(parts) > 2 else ""

        if send_type == "text":
            self._send_sample_text(sender, args)
        elif send_type == "image":
            self._send_sample_image(sender)
        elif send_type == "file":
            self._send_sample_file(sender)
        elif send_type == "video":
            self._send_sample_video(sender)
        elif send_type == "contact":
            self._send_sample_contact(sender)
        elif send_type == "link":
            self._send_sample_link(sender)
        elif send_type == "location":
            self._send_sample_location(sender)
        elif send_type == "audio":
            self._send_sample_audio(sender)
        elif send_type == "poll":
            self._send_sample_poll(sender)
        elif send_type == "presence":
            self._send_sample_presence(sender, args)
        else:
            self.wa_client.send_message(sender, f"Tipe pengiriman '{send_type}' tidak dikenal. Gunakan `send menu`.")

    def _send_sample_text(self, sender, message):
        if not message:
            self.wa_client.send_message(sender, "Mohon berikan pesan untuk dikirim. Contoh: `send text Halo dunia!`")
            return
        print(f"Sending text message '{message}' to {sender}")
        self.wa_client.send_message(sender, message)
        self.wa_client.send_message(sender, f"Pesan teks '{message}' telah dikirim ke Anda.")

    def _send_sample_image(self, sender):
        image_path = "assets/sample_image.jpeg"
        caption = "Ini adalah contoh gambar dari aset lokal."
        print(f"Sending image from '{image_path}' to {sender}")
        try:
            with open(image_path, 'rb') as f:
                self.wa_client.send_image(sender, f, caption=caption)
            self.wa_client.send_message(sender, f"Gambar dari aset lokal telah dikirim ke Anda.")
        except FileNotFoundError:
            self.wa_client.send_message(sender, f"File gambar tidak ditemukan di: {image_path}")
            print(f"Error: Image file not found at {image_path}")
        except Exception as e:
            self.wa_client.send_message(sender, f"Gagal mengirim gambar: {e}")
            print(f"Error sending image: {e}")

    def _send_sample_file(self, sender):
        file_path = "assets/sample_document.pdf"
        caption = "Ini adalah contoh dokumen PDF dari aset lokal."
        print(f"Sending file from '{file_path}' to {sender}")
        try:
            with open(file_path, 'rb') as f:
                self.wa_client.send_file(sender, f, caption=caption)
            self.wa_client.send_message(sender, f"File dari aset lokal telah dikirim ke Anda.")
        except FileNotFoundError:
            self.wa_client.send_message(sender, f"File dokumen tidak ditemukan di: {file_path}")
            print(f"Error: Document file not found at {file_path}")
        except Exception as e:
            self.wa_client.send_message(sender, f"Gagal mengirim file: {e}")
            print(f"Error sending file: {e}")

    def _send_sample_video(self, sender):
        video_path = "assets/sample_video.mp4"
        caption = "Ini adalah contoh video dari aset lokal."
        print(f"Sending video from '{video_path}' to {sender}")
        try:
            with open(video_path, 'rb') as f:
                self.wa_client.send_video(sender, f, caption=caption)
            self.wa_client.send_message(sender, f"Video dari aset lokal telah dikirim ke Anda.")
        except FileNotFoundError:
            self.wa_client.send_message(sender, f"File video tidak ditemukan di: {video_path}")
            print(f"Error: Video file not found at {video_path}")
        except Exception as e:
            self.wa_client.send_message(sender, f"Gagal mengirim video: {e}")
            print(f"Error sending video: {e}")

    def _send_sample_contact(self, sender):
        contact_name = "John Doe"
        contact_phone = "6281234567891" # Example contact phone number
        print(f"Sending contact '{contact_name}' to {sender}")
        try:
            self.wa_client.send_contact(sender, contact_name, contact_phone)
            self.wa_client.send_message(sender, f"Kontak '{contact_name}' telah dikirim ke Anda.")
        except Exception as e:
            self.wa_client.send_message(sender, f"Gagal mengirim kontak: {e}")
            print(f"Error sending contact: {e}")

    def _send_sample_link(self, sender):
        link = "https://www.google.com"
        caption = "Ini adalah contoh link ke Google."
        print(f"Sending link '{link}' to {sender}")
        try:
            self.wa_client.send_link(sender, link, caption=caption)
            self.wa_client.send_message(sender, f"Link '{link}' telah dikirim ke Anda.")
        except Exception as e:
            self.wa_client.send_message(sender, f"Gagal mengirim link: {e}")
            print(f"Error sending link: {e}")

    def _send_sample_location(self, sender):
        latitude = "-6.2088" # Example latitude for Jakarta
        longitude = "106.8456" # Example longitude for Jakarta
        print(f"Sending location {latitude}, {longitude} to {sender}")
        try:
            self.wa_client.send_location(sender, latitude, longitude)
            self.wa_client.send_message(sender, f"Lokasi ({latitude}, {longitude}) telah dikirim ke Anda.")
        except Exception as e:
            self.wa_client.send_message(sender, f"Gagal mengirim lokasi: {e}")
            print(f"Error sending location: {e}")

    def _send_sample_audio(self, sender):
        audio_path = "assets/sample_audio.wav"
        output_audio_path = "assets/sample_audio.ogg" # New path for converted audio
        print(f"Sending audio from '{audio_path}' to {sender}")
        try:
            # Convert WAV to OGG Opus using ffmpeg
            command = [
                "ffmpeg",
                "-i", audio_path,
                "-c:a", "libopus",
                "-b:a", "64k",
                "-vbr", "on",
                "-compression_level", "10",
                output_audio_path
            ]
            subprocess.run(command, check=True, capture_output=True)
            print(f"Audio converted to OGG Opus: {output_audio_path}")

            with open(output_audio_path, 'rb') as f:
                self.wa_client.send_audio(sender, f)
            self.wa_client.send_message(sender, f"Audio dari aset lokal telah dikirim ke Anda.")

            # Clean up the converted file after successful sending
            if os.path.exists(output_audio_path):
                os.remove(output_audio_path)
                print(f"Cleaned up converted audio file: {output_audio_path}")

        except FileNotFoundError:
            self.wa_client.send_message(sender, f"File audio tidak ditemukan di: {audio_path}")
            print(f"Error: Audio file not found at {audio_path}")
        except subprocess.CalledProcessError as e:
            self.wa_client.send_message(sender, f"Gagal mengkonversi audio: {e.stderr.decode()}")
            print(f"Error converting audio: {e.stderr.decode()}")
        except Exception as e:
            self.wa_client.send_message(sender, f"Gagal mengirim audio: {e}")
            print(f"Error sending audio: {e}")

    def _send_sample_poll(self, sender):
        question = "Apa warna favoritmu?"
        options = ["Merah", "Biru", "Hijau", "Kuning"]
        max_answers = 1
        print(f"Sending poll '{question}' to {sender}")
        try:
            self.wa_client.send_poll(sender, question, options, max_answers)
            self.wa_client.send_message(sender, f"Polling '{question}' telah dikirim ke Anda.")
        except Exception as e:
            self.wa_client.send_message(sender, f"Gagal mengirim polling: {e}")
            print(f"Error sending poll: {e}")

    def _send_sample_presence(self, sender, presence_type):
        valid_presence_types = ["available", "unavailable", "composing", "paused", "recording"]
        if presence_type not in valid_presence_types:
            self.wa_client.send_message(sender, f"Tipe kehadiran '{presence_type}' tidak valid. Gunakan salah satu: {', '.join(valid_presence_types)}.")
            return
        print(f"Setting presence to '{presence_type}'")
        try:
            self.wa_client.send_presence(presence_type)
            self.wa_client.send_message(sender, f"Status kehadiran diatur ke '{presence_type}'.")
        except Exception as e:
            self.wa_client.send_message(sender, f"Gagal mengatur kehadiran: {e}")
            print(f"Error setting presence: {e}")
