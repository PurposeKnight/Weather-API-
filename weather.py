import customtkinter as ctk
import requests
from tkinter import messagebox


def get_weather():
    city = city_entry.get().strip()
    if city == "":
        messagebox.showwarning("Input Error", "Please enter a city name")
        return

    API_KEY = "c2a9880f91579fd266e751ef1fdbdf48" 
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

    params = {"q": city, "appid": API_KEY, "units": "metric"}

    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        data = response.json()

        if response.status_code == 401:
            messagebox.showerror("API Error", "❌ Invalid API Key!")
        elif response.status_code == 404:
            messagebox.showwarning("Not Found", f"🌍 City '{city}' not found.")
        elif response.status_code != 200:
            messagebox.showerror("Error", f"⚠️ {data.get('message', 'Unknown error')}")
        else:
            city_name = data["name"]
            country = data["sys"]["country"]
            temp = data["main"]["temp"]
            weather = data["weather"][0]["description"].title()

            result_label.configure(
                text=f"📍 {city_name}, {country}\n"
                     f"🌡️ {temp} °C\n"
                     f"⛅ {weather}"
            )
    except requests.exceptions.RequestException:
        messagebox.showerror("Network Error", "⚡ Check your internet connection.")


ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")  

root = ctk.CTk()
root.title("🌦️ Weather App")
root.geometry("400x500")

title = ctk.CTkLabel(root, text="Weather App",
                     font=ctk.CTkFont(size=24, weight="bold"))
title.pack(pady=20)


city_entry = ctk.CTkEntry(root, placeholder_text="Enter city name",
                          font=ctk.CTkFont(size=16), width=250, height=40)
city_entry.pack(pady=20)


btn = ctk.CTkButton(root, text="Get Weather",
                    font=ctk.CTkFont(size=16, weight="bold"),
                    width=200, height=40,
                    corner_radius=15,
                    command=get_weather)
btn.pack(pady=15)


result_label = ctk.CTkLabel(root, text="",
                            font=ctk.CTkFont(size=18, weight="bold"))
result_label.pack(pady=40)


footer = ctk.CTkLabel(root, text="Powered by OpenWeatherMap",
                      font=ctk.CTkFont(size=12))
footer.pack(side="bottom", pady=20)

root.mainloop()
