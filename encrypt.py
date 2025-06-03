import telebot
import os
import subprocess

# Token bot Telegram
TOKEN = '7951780731:AAGHbY_7fp9_sExAmL4x70xYND0ARiQgXzU'

# Inisialisasi bot
bot = telebot.TeleBot(TOKEN)

# Folder untuk menyimpan file sementara
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@bot.message_handler(content_types=['document'])
def handle_file(message):
    try:
        # Cek apakah file adalah .sh
        file_id = message.document.file_id
        file_name = message.document.file_name

        if not file_name.endswith('.sh'):
            bot.reply_to(message, "Silakan kirim file berformat .sh")
            return

        # Download file
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Simpan file
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        with open(file_path, 'wb') as f:
            f.write(downloaded_file)

        bot.reply_to(message, "File diterima. Memulai enkripsi...")

        # Jalankan perintah shc
        dir_path = os.path.dirname(file_path)
        shc_command = ['shc', '-f', file_path]

        try:
            subprocess.run(shc_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            bot.reply_to(message, f"❌ Gagal mengenkripsi file:\n{e.stderr.decode()}")
            return

        encrypted_file = os.path.join(UPLOAD_FOLDER, 'main.sh.x')

        if not os.path.exists(encrypted_file):
            bot.reply_to(message, "❌ Enkripsi gagal. File sh.x tidak ditemukan.")
            return

        # Kirim file hasil enkripsi
        with open(encrypted_file, 'rb') as f:
            bot.send_document(message.chat.id, f, caption="✅ File telah dienkripsi dengan shc.")

        # Hapus file sementara
        os.remove(file_path)
        os.remove(encrypted_file)

    except Exception as e:
        bot.reply_to(message, f"⚠️ Terjadi kesalahan: {str(e)}")

# Mulai polling
print("Bot sedang berjalan...")
bot.polling(none_stop=True)
