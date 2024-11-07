import requests
import tkinter as tk
from tkinter import ttk
from dotenv import load_dotenv
import os

# .env dosyasından API anahtarını yükleyin
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Football-Data.org API URL'si
url = "https://api.football-data.org/v4/matches"

# API'ye bağlanıp maçları çekme fonksiyonu
def get_matches():
    headers = {"X-Auth-Token": API_KEY}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        matches = response.json()['matches']
        return matches
    else:
        print("Veri alınamadı!")
        return []

# Skorları GUI üzerinde göstermek için fonksiyon
def show_matches():
    matches = get_matches()
    
    if not matches:
        print("Maç verisi bulunamadı!")
    
    for row in tree.get_children():
        tree.delete(row)

    for match in matches:
        home_team = match.get('homeTeam', {}).get('name', 'Bilgi Yok')
        away_team = match.get('awayTeam', {}).get('name', 'Bilgi Yok')
        home_score = match.get('score', {}).get('fullTime', {}).get('homeTeam', 'Bilgi Yok')
        away_score = match.get('score', {}).get('fullTime', {}).get('awayTeam', 'Bilgi Yok')

        tree.insert("", "end", values=(home_team, home_score, away_team, away_score))

# GUI oluşturma
root = tk.Tk()
root.title("Maç Skorları Uygulaması")

# Tam ekran yapma
root.attributes("-fullscreen", True)
root.configure(bg='#f0f0f0')

# Tam ekran modunu kapatma fonksiyonu
def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", False)
    root.quit()  # Pencereyi kapat

# Esc tuşuyla tam ekran modundan çıkma
root.bind("<Escape>", toggle_fullscreen)

# Stil ayarları
style = ttk.Style()
style.configure("Treeview",
                background="#e3e3e3",
                foreground="black",
                fieldbackground="#e3e3e3",
                font=('Arial', 10))
style.configure("Treeview.Heading", font=('Arial', 12, 'bold'), background="#4CAF50", foreground="white")
style.configure("Treeview.Cell", font=('Arial', 10))

# Tabloyu oluştur
columns = ("Ev Sahibi", "Ev Sahibi Skor", "Deplasman", "Deplasman Skor")
tree = ttk.Treeview(root, columns=columns, show="headings")

# Tablo başlıklarını ayarla
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150, anchor="center")

# Ekran boyutuna göre tabloyu yeniden boyutlandırma fonksiyonu
def resize_tree(event):
    width = event.width
    tree.column("Ev Sahibi", width=width // 4)
    tree.column("Ev Sahibi Skor", width=width // 4)
    tree.column("Deplasman", width=width // 4)
    tree.column("Deplasman Skor", width=width // 4)

# Ekran boyutunu izleme
root.bind("<Configure>", resize_tree)

# Tabloyu yerleştir
tree.pack(fill=tk.BOTH, expand=True, pady=20)

# "Yenile" butonu
refresh_button = tk.Button(root, text="Yenile", command=show_matches, bg="#4CAF50", fg="white", font=('Arial', 12, 'bold'))
refresh_button.pack(pady=10)

# Uygulamayı çalıştır
root.mainloop()
