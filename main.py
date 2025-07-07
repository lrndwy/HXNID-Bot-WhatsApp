import os
import requests
import base64
import hmac
import hashlib
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from bot_logic import BotLogic

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

GO_WA_API_URL = os.getenv("GO_WA_API_URL")
GO_WA_API_USERNAME = os.getenv("GO_WA_API_USERNAME")
GO_WA_API_PASSWORD = os.getenv("GO_WA_API_PASSWORD")
PYTHON_WEBHOOK_SECRET = os.getenv("PYTHON_WEBHOOK_SECRET")
ALLOW_SELF_MESSAGE = os.getenv("ALLOW_SELF_MESSAGE", "false").lower() == "true"

# Global list to store webhook logs
webhook_logs = []

class WhatsAppClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.auth_header = self._generate_auth_header(username, password)

    def _generate_auth_header(self, username, password):
        credentials = f"{username}:{password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return {"Authorization": f"Basic {encoded_credentials}"}

    def _send_request(self, method, endpoint, params=None, json_data=None, files=None, data=None):
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(
                method, url, params=params, json=json_data, files=files, headers=self.auth_header, data=data
            )
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during API request to {url}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response content: {e.response.text}")
            return {"code": "ERROR", "message": str(e)}

    # App Endpoints

    def app_devices(self):
        return self._send_request("GET", "/app/devices")

    # User Endpoints
    def user_info(self, phone):
        return self._send_request("GET", "/user/info", params={"phone": phone})

    def user_avatar(self, phone, is_preview=None, is_community=None):
        params = {"phone": phone}
        if is_preview is not None:
            params["is_preview"] = is_preview
        if is_community is not None:
            params["is_community"] = is_community
        return self._send_request("GET", "/user/avatar", params=params)

    def user_change_avatar(self, avatar_file):
        files = {"avatar": avatar_file}
        return self._send_request("POST", "/user/avatar", files=files)

    def user_change_pushname(self, push_name):
        json_data = {"push_name": push_name}
        return self._send_request("POST", "/user/pushname", json_data=json_data)

    def user_my_privacy(self):
        return self._send_request("GET", "/user/my/privacy")

    def user_my_groups(self):
        return self._send_request("GET", "/user/my/groups")

    def user_my_newsletters(self):
        return self._send_request("GET", "/user/my/newsletters")

    def user_my_contacts(self):
        return self._send_request("GET", "/user/my/contacts")

    def user_check(self, phone):
        return self._send_request("GET", "/user/check", params={"phone": phone})

    # Send Endpoints
    def send_message(self, phone, message, reply_message_id=None, is_forwarded=False):
        json_data = {
            "phone": phone,
            "message": message,
            "is_forwarded": is_forwarded
        }
        if reply_message_id:
            json_data["reply_message_id"] = reply_message_id
        return self._send_request("POST", "/send/message", json_data=json_data)

    def send_image(self, phone, image_file=None, image_url=None, caption=None, view_once=False, compress=False, is_forwarded=False):
        files = {}
        if image_file:
            # If image_file is a file object, requests will handle it correctly
            # Explicitly set content type for image
            files["image"] = (image_file.name, image_file, "image/jpeg")

        data_for_form = {
            "phone": phone,
            "view_once": str(view_once).lower(),
            "compress": str(compress).lower(),
            "is_forwarded": str(is_forwarded).lower()
        }
        if caption:
            data_for_form["caption"] = caption
        if image_url:
            data_for_form["image_url"] = image_url

        return self._send_request("POST", "/send/image", data=data_for_form, files=files)

    def send_audio(self, phone, audio_file, is_forwarded=False):
        # Explicitly set content type for audio
        files = {"audio": (audio_file.name, audio_file, "audio/wav")}
        data_for_form = {
            "phone": phone,
            "is_forwarded": str(is_forwarded).lower()
        }
        return self._send_request("POST", "/send/audio", data=data_for_form, files=files)

    def send_file(self, phone, file_obj, caption=None, is_forwarded=False):
        files = {"file": file_obj}
        data_for_form = {
            "phone": phone,
            "is_forwarded": str(is_forwarded).lower()
        }
        if caption:
            data_for_form["caption"] = caption
        return self._send_request("POST", "/send/file", data=data_for_form, files=files)

    def send_video(self, phone, video_file, caption=None, view_once=False, compress=False, is_forwarded=False):
        # Explicitly set content type for video
        files = {"video": (video_file.name, video_file, "video/mp4")}
        data_for_form = {
            "phone": phone,
            "view_once": str(view_once).lower(),
            "compress": str(compress).lower(),
            "is_forwarded": str(is_forwarded).lower()
        }
        if caption:
            data_for_form["caption"] = caption

        return self._send_request("POST", "/send/video", data=data_for_form, files=files)

    def send_contact(self, phone, contact_name, contact_phone, is_forwarded=False):
        json_data = {
            "phone": phone,
            "contact_name": contact_name,
            "contact_phone": contact_phone,
            "is_forwarded": is_forwarded
        }
        return self._send_request("POST", "/send/contact", json_data=json_data)

    def send_link(self, phone, link, caption=None, is_forwarded=False):
        json_data = {
            "phone": phone,
            "link": link,
            "is_forwarded": is_forwarded
        }
        if caption:
            json_data["caption"] = caption
        return self._send_request("POST", "/send/link", json_data=json_data)

    def send_location(self, phone, latitude, longitude, is_forwarded=False):
        json_data = {
            "phone": phone,
            "latitude": str(latitude),
            "longitude": str(longitude),
            "is_forwarded": is_forwarded
        }
        return self._send_request("POST", "/send/location", json_data=json_data)

    def send_poll(self, phone, question, options, max_answer):
        json_data = {
            "phone": phone,
            "question": question,
            "options": options,
            "max_answer": max_answer
        }
        return self._send_request("POST", "/send/poll", json_data=json_data)

    def send_presence(self, type): # is_forwarded is not a parameter for send_presence in Go API
        json_data = {
            "type": type,
        }
        return self._send_request("POST", "/send/presence", json_data=json_data)

    # Message Endpoints
    def message_revoke(self, message_id, phone):
        json_data = {"phone": phone}
        return self._send_request("POST", f"/message/{message_id}/revoke", json_data=json_data)

    def message_delete(self, message_id, phone):
        json_data = {"phone": phone}
        return self._send_request("POST", f"/message/{message_id}/delete", json_data=json_data)

    def message_reaction(self, message_id, phone, emoji):
        json_data = {"phone": phone, "emoji": emoji}
        return self._send_request("POST", f"/message/{message_id}/reaction", json_data=json_data)

    def message_update(self, message_id, phone, message):
        json_data = {"phone": phone, "message": message}
        return self._send_request("POST", f"/message/{message_id}/update", json_data=json_data)

    def message_read(self, message_id, phone):
        json_data = {"phone": phone}
        return self._send_request("POST", f"/message/{message_id}/read", json_data=json_data)

    def message_star(self, message_id, phone):
        json_data = {"phone": phone}
        return self._send_request("POST", f"/message/{message_id}/star", json_data=json_data)

    def message_unstar(self, message_id, phone):
        json_data = {"phone": phone}
        return self._send_request("POST", f"/message/{message_id}/unstar", json_data=json_data)

    # Group Endpoints
    def group_join_with_link(self, link):
        json_data = {"link": link}
        return self._send_request("POST", "/group/join-with-link", json_data=json_data)

    def group_leave(self, group_id):
        json_data = {"group_id": group_id}
        return self._send_request("POST", "/group/leave", json_data=json_data)

    def group_create(self, name, participants):
        json_data = {"name": name, "participants": participants}
        return self._send_request("POST", "/group", json_data=json_data)

    def group_add_participants(self, group_id, participants):
        json_data = {"group_id": group_id, "participants": participants}
        return self._send_request("POST", "/group/participants", json_data=json_data)

    def group_remove_participant(self, group_id, participant):
        json_data = {"group_id": group_id, "participant": participant}
        return self._send_request("POST", "/group/participants/remove", json_data=json_data)

    def group_promote_participant(self, group_id, participant):
        json_data = {"group_id": group_id, "participant": participant}
        return self._send_request("POST", "/group/participants/promote", json_data=json_data)

    def group_demote_participant(self, group_id, participant):
        json_data = {"group_id": group_id, "participant": participant}
        return self._send_request("POST", "/group/participants/demote", json_data=json_data)

    def group_list_requested_participants(self):
        return self._send_request("GET", "/group/participant-requests")

    def group_approve_requested_participant(self, group_id, participant):
        json_data = {"group_id": group_id, "participant": participant}
        return self._send_request("POST", "/group/participant-requests/approve", json_data=json_data)

    def group_reject_requested_participant(self, group_id, participant):
        json_data = {"group_id": group_id, "participant": participant}
        return self._send_request("POST", "/group/participant-requests/reject", json_data=json_data)

    # Newsletter Endpoints
    def newsletter_unfollow(self, newsletter_id):
        json_data = {"newsletter_id": newsletter_id}
        return self._send_request("POST", "/newsletter/unfollow", json_data=json_data)


# Initialize WhatsAppClient and BotLogic
wa_client = WhatsAppClient(GO_WA_API_URL, GO_WA_API_USERNAME, GO_WA_API_PASSWORD)
bot_logic = BotLogic(wa_client, allow_self_message=ALLOW_SELF_MESSAGE)

@app.route("/")
def index():
    return "WhatsApp Bot Python Example is running!"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers.get("X-Hub-Signature-256")
    payload = request.data

    if not signature:
        print("Webhook: No signature provided.")
        return jsonify({"status": "error", "message": "No signature provided"}), 403

    # Verify the signature
    expected_signature = "sha256=" + hmac.new(
        PYTHON_WEBHOOK_SECRET.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected_signature, signature):
        print(f"Webhook: Invalid signature. Expected: {expected_signature}, Got: {signature}")
        return jsonify({"status": "error", "message": "Invalid signature"}), 403

    try:
        event_data = json.loads(payload)
        webhook_logs.append(event_data) # Store the incoming webhook data
        print(f"Received webhook event: {json.dumps(event_data, indent=2)}")

        # Assuming the webhook payload directly contains message data
        # Adjust these keys based on the actual webhook payload from go-wa-api
        raw_sender = event_data.get("from")
        message_content = event_data.get("message", {}).get("text")

        # Extract the user JID (e.g., "6285890392419@s.whatsapp.net")
        sender = None
        if raw_sender:
            # The format is "6285890392419:56@s.whatsapp.net in 6285890392419@s.whatsapp.net"
            # We need to extract the part before " in " and remove the device part ":56"
            parts = raw_sender.split(" in ")
            if len(parts) > 0:
                jid_with_device = parts[0]
                sender_parts = jid_with_device.split(":")
                if len(sender_parts) > 1 and "@s.whatsapp.net" in sender_parts[1]:
                    sender = sender_parts[0] + "@s.whatsapp.net"
                else:
                    sender = jid_with_device # Fallback if no device part

        # For now, we'll assume all messages are to be processed.
        # If 'is_self' is needed, we need to know how go-wa-api provides it in the webhook.
        is_self = False # Placeholder, as 'is_self' is not in the provided payload example

        if sender and message_content:
            print(f"New message from {sender} (self_message: {is_self}): {message_content}")
            bot_logic.handle_message(sender, message_content, is_self)
        else:
            # Handle other event types or incomplete message data
            print("Received non-message event or incomplete message data.")
            # You might want to add specific handling for 'qr' or 'connection' events if they are top-level
            # For example, if 'qr_link' is directly in event_data:
            # if event_data.get("qr_link"):
            #     print(f"New QR code received: {event_data['qr_link']}")
            # if event_data.get("status"): # For connection status
            #     print(f"Connection status changed: {event_data['status']}")

        return jsonify({"status": "success", "message": "Webhook received"}), 200
    except json.JSONDecodeError:
        print("Webhook: Invalid JSON payload.")
        return jsonify({"status": "error", "message": "Invalid JSON payload"}), 400
    except Exception as e:
        print(f"Webhook: An error occurred: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/logs")
def view_logs():
    return jsonify(webhook_logs)

if __name__ == "__main__":
    # To run the Flask app, you would typically use `flask run` or a WSGI server.
    # For this example, we'll use app.run for simplicity during development.
    # In production, use gunicorn or uWSGI.
    print(f"Starting Flask app on port {os.getenv('FLASK_RUN_PORT', 5000)}...")
    app.run(host="0.0.0.0", port=os.getenv("FLASK_RUN_PORT", 5000))
