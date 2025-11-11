import qrcode

# URL base do endpoint
BASE_URL = "https://seudominio.com/validate?id=TEST000"

# Gera QR Code
img = qrcode.make(BASE_URL)
img.save("qrcode_certificado.png")

print("✅ QR Code gerado: qrcode_certificado.png")
