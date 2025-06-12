with open("backup.json", "rb") as f:
    content = f.read()

# جرب decode بـ encoding تاني غير utf-8، مثلاً utf-16 أو latin-1
try:
    decoded = content.decode("utf-16")  # أو جرّب "latin-1"
    with open("backup_fixed.json", "w", encoding="utf-8") as out:
        out.write(decoded)
    print("تم حفظ النسخة بصيغة UTF-8.")
except Exception as e:
    print("خطأ:", e)
