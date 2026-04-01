import customtkinter as ctk
import requests
import threading
import json

# --- API ANAHTARI ---
API_KEY = "AIzaSyCI9IRG-Hhs24E2b6eOacls4zhSJ6lvY_M"
# --------------------

def get_ai_response(event=None):
    user_input = entry_purpose.get()

    if not user_input.strip():
        update_ui_with_response("Please describe your purpose.")
        return

    button_submit.configure(state="disabled", text="Awaiting Response...")
    textbox_response.configure(state="normal")
    textbox_response.delete("1.0", "end")
    textbox_response.insert("1.0", "AI is preparing a response, please wait...\n")
    textbox_response.configure(state="disabled")

    def fetch_from_api():
        prompt_text = (
            f"The user wants to use AI for the following purpose: '{user_input}'. "
            "Provide 2-3 of the best AI tools for this purpose simply and directly, "
            "listing them with a brief description of their standout features. "
            "IMPORTANT: Your response MUST be in the exact same language that the user used for their purpose. "
            "ABSOLUTELY DO NOT use the '*' character or bold formatting in your response."
        )

        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=" + API_KEY
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": prompt_text}]}]
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
            response_data = response.json()

            if response.status_code == 200:
                ai_text = response_data["candidates"][0]["content"]["parts"][0]["text"]
                ai_text = ai_text.replace("*", "")
            else:
                error_msg = response_data.get("error", {}).get("message", "An unknown error occurred.")
                ai_text = f"API Error ({response.status_code}): {error_msg}"
        except Exception as e:
            ai_text = f"Connection error! Please check your internet.\nDetails: {str(e)}"

        app.after(0, update_ui_with_response, ai_text)

    threading.Thread(target=fetch_from_api, daemon=True).start()

def update_ui_with_response(response_text):
    textbox_response.configure(state="normal")
    textbox_response.delete("1.0", "end")
    textbox_response.insert("1.0", response_text)
    textbox_response.configure(state="disabled")
    button_submit.configure(state="normal", text="Get Recommendation")

# --- Arayüz Kurulumu ---
app = ctk.CTk()
app.title("Gemini AI Project Advisor")
app.geometry("800x600")
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

main_frame = ctk.CTkFrame(app)
main_frame.pack(fill="both", expand=True, padx=25, pady=25)

label_title = ctk.CTkLabel(main_frame, text="AI Recommendation Tool", font=ctk.CTkFont(size=22, weight="bold"))
label_title.pack(pady=(10, 20))

entry_purpose = ctk.CTkEntry(main_frame, placeholder_text="Enter your purpose", width=600, height=45)
entry_purpose.pack(pady=(0, 20))

app.bind("<Return>", get_ai_response)

button_submit = ctk.CTkButton(main_frame, text="Get Recommendation", command=get_ai_response, width=250, height=45, font=ctk.CTkFont(size=15, weight="bold"))
button_submit.pack(pady=(0, 20))

textbox_response = ctk.CTkTextbox(main_frame, width=700, height=350, wrap="word", font=ctk.CTkFont(size=14))
textbox_response.pack(padx=10, pady=(0, 10), fill="both", expand=True)
textbox_response.insert("1.0", "Welcome! Please enter what you want to use AI for above.")
textbox_response.configure(state="disabled")

if __name__ == "__main__":
    app.mainloop()