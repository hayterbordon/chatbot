from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Token de verificación y acceso
VERIFY_TOKEN = '83cd232796b9046cf832323f696c69d2'  # Define tu token aquí
ACCESS_TOKEN = 'IGAAOFbcVgyD5BZAFBkenhZAOC04WDYxMEQ3SVVLVi05THF4VmQyZAnJHUWZA6cXZAza1lyR3NTeE5KRzFyeTJzejd2MUNsTkRzakFwMGhFUnpXeE9ocTRETHdUT2JDWXk5RXhhcGxxTHJSVGVuTVd5aU12RGlzWkRYOTlqVjItNGlHTQZDZD'  # Reemplaza con tu token generado en Meta

# Ruta raíz para mensaje de bienvenida
@app.route('/', methods=['GET'])
def home():
    return "Bienvenido al servidor Flask", 200

# Verificación del Webhook
@app.route('/webhook', methods=['GET'])
def verify_webhook():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode == 'subscribe' and token == VERIFY_TOKEN:
        print("Webhook verificado correctamente.")
        return challenge, 200
    else:
        print("Error en la verificación del webhook.")
        return 'No autorizado', 403

# Manejo de eventos
@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.get_json()
    print("Datos recibidos del webhook:", data)

    # Procesar mensajes directos (DM)
    try:
        if "entry" in data:
            for entry in data['entry']:
                for change in entry.get('changes', []):
                    if change.get('field') == 'messages':
                        sender_id = change['value']['from']['id']
                        message_text = change['value']['message']['text']
                        print(f"Nuevo mensaje de {sender_id}: {message_text}")

                        # Responder al mensaje
                        if message_text:
                            respond_to_message(sender_id, message_text)
    except Exception as e:
        print("Error al procesar el evento:", e)

    return jsonify({"status": "ok"}), 200

# Responder al mensaje
def respond_to_message(user_id, message_text):
    reply_text = get_reply(message_text)
    send_reply(user_id, reply_text)

# Generar respuesta personalizada
def get_reply(message_text):
    if "hola" in message_text.lower():
        return "¡Hola! ¿Cómo puedo ayudarte hoy? 😊"
    elif "precio" in message_text.lower():
        return "Nuestros precios son: $100 por sesión. Más información aquí: https://example.com/precios"
    elif "contacto" in message_text.lower():
        return "Puedes contactarnos al correo soporte@example.com o al teléfono +123456789."
    elif "gracias" in message_text.lower():
        return "¡De nada! Estoy aquí para ayudarte. 🙌"
    return "Lo siento, no entendí tu mensaje. Por favor, intenta con otras palabras clave. 🙏"

# Enviar respuesta
def send_reply(user_id, message_text):
    url = "https://graph.facebook.com/v16.0/me/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_type": "RESPONSE",
        "recipient": {"id": user_id},
        "message": {"text": message_text},
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        print("Respuesta enviada:", response.status_code, response.text)
    except Exception as e:
        print("Error al enviar la respuesta:", e)

if __name__ == '__main__':
    print("Iniciando el servidor Flask...")
    app.run(host="0.0.0.0", port=8080)
