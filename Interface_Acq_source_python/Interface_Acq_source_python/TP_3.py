import ascon_pcsn
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd
from scipy.signal import find_peaks, firwin, lfilter
import serial
import neurokit2 as nk
import serial

ser = serial.Serial('com15', baudrate=115200, timeout=1)  

key = '4C' + "8A55114D1CB6A9A2BE263D4D7AECAAFF"  
nonce = '4F' +  "4ED0EC0B98C529B7C8CDDF37BCD0284A"  
associated_data = '42' + '41 20 74 6F 20 42' 
ecg_waveform = '58' + '5A 5B 5B 5A 5A 5A 5A 5A 59 55 4E 4A 4C 4F 54 55 53 51 53 54 56 57 58 57 5A 5A 59 57 56 59 5B 5A 55 54 54 52 52 50 4F 4F 4C 4C 4D 4D 4A 49 44 44 47 47 46 44 42 43 41 40 3B 36 38 3E 44 49 49 47 47 46 46 44 43 42 43 45 47 45 44 45 46 47 4A 49 47 45 48 4F 58 69 7C 92 AE CE ED FF FF E3 B4 7C 47 16 00 04 17 29 36 3C 3F 3E 40 41 41 41 40 3F 3F 40 3F 3E 3B 3A 3B 3E 3D 3E 3C 39 3C 41 46 46 46 45 44 47 46 4A 4C 4F 4C 50 55 55 52 4F 51 55 59 5C 5A 59 5A 5C 5C 5B 59 59 57 53 51 50 4F 4F 53 57 5A 5C 5A 5B 5D 5E 60 60 61 5F 60 5F 5E 5A 58 57 54 52 52' + '80 00 00'
plaintext_decimal = list(ecg_waveform)

def send_hex(serial_port, hex_string):
    byte_data = bytes.fromhex(hex_string)
    serial_port.write(byte_data)

send_hex(ser, key) 
ok_response = ser.read(2) 
send_hex(ser, nonce) 
ok_response = ser.read(2) 
send_hex(ser, associated_data)
ok_response = ser.read(2) 
send_hex(ser, ecg_waveform)  
ok_response = ser.read(2) 

ser.write(b'\x48') 

tag_response = ser.read(16) 
ok_response = ser.read(2) 

ciphertext = ser.read(181) 
ciphertext_padding = ser.read(3)  
ok_response_2 = ser.read(2) 

print("Tag Response: ", tag_response.hex())
print("OK Response 1: ", ok_response.hex())
print("Ciphertext: ", ciphertext.hex())
print("Ciphertext Padding: ", ciphertext_padding.hex())
print("OK Response 2: ", ok_response_2.hex())

ser.close()


def read_ecg_uart(port="COM15", baudrate=115200):
    
    ser = serial.Serial(port, baudrate, timeout=1)
    data = ser.read(1024)  # Lire 1024 octets de données
    ser.close()
    return data

"""
key_hexa = "8A55114D1CB6A9A2BE263D4D7AECAAFF" 
nonce_hexa = "4ED0EC0B98C529B7C8CDDF37BCD0284A" 
plaintext_hexa = "36353335353535353434343432312F31343533333233333436393C3D3F3F403E3E3F3F403F3F3D3C3A39383736363633312D2C2A2B2B2B2A29292825211A171518191B1D242F384043484D57667582909AA6B3C0C9D3DEE9F0F8FFFEFBF1E1CEB59C826A57463A2D221A16161717161514151514151718181715121314131211111111100F0E0D0D0E0E0E0D0B0A0B0B09070606060707070605040302010000010304020000010100010203050303010204060708"

associateddata = b"A to B"


key = bytes.fromhex(key_hexa)
nonce = bytes.fromhex(nonce_hexa)
plaintext = bytes.fromhex(plaintext_hexa)

plaintext_decimal = list(plaintext)

"""
mode = "fpga"  # Change en "fpga" pour utiliser UART
if mode == "test":
    ciphertext = ascon_pcsn.ascon_encrypt(key, nonce, associated_data, ecg_waveform, variant="Ascon-128")
    print("Texte chiffré :", ciphertext.hex())
else:
    ciphertext = read_ecg_uart()
    print("Texte chiffré reçu du FPGA :", ciphertext.hex())

ciphertext_hex = ciphertext.hex()
print("Texte chiffré en hexadécimal :", ciphertext_hex)

# dechiff
print("\n Déchiffrement en cours...")
decrypted_text = ascon_pcsn.ascon_decrypt(key, nonce, associated_data, ciphertext, variant="Ascon-128")

decrypted_hex = decrypted_text.hex()
print(" Déchiffrement réussi ! Données déchiffrées en hexadécimal :", decrypted_hex)

#decrypted_decimal = [int(byte, 16) for byte in decrypted_hex]
decrypted_decimal = list(decrypted_text)
print("Données déchiffrées en décimal :", decrypted_decimal)


#ECG LIVEE
fig, ax = plt.subplots(figsize=(12, 5))
ax.set_xlim(0, len(decrypted_decimal))
ax.set_ylim(min(decrypted_decimal) - 10, max(decrypted_decimal) + 10)
ax.set_xlabel("Échantillons")
ax.set_ylabel("Amplitude ECG")
ax.set_title("Affichage en temps réel du signal ECG déchiffré avec détails")
ax.grid(True, linestyle='--', linewidth=0.5)

line, = ax.plot([], [], lw=2, color='blue', label='ECG Déchiffré')
ax.legend()

def init():
    line.set_data([], [])
    return line,

def update(frame):
    x_data = list(range(frame))
    y_data = decrypted_decimal[:frame]
    line.set_data(x_data, y_data)
    return line,

ani = animation.FuncAnimation(fig, update, frames=len(decrypted_decimal), init_func=init, blit=True, interval=5)
plt.show()

# repeter l ecg infini
num_repeats = 10
merged_ecg = decrypted_decimal * num_repeats 
print(f"Taille du signal fusionné : {len(merged_ecg)}")
plt.figure(figsize=(12, 5))
plt.plot(merged_ecg, label="ECG Fusionné (x10)", color='blue')
plt.xlabel("Échantillons")
plt.ylabel("Amplitude ECG")
plt.title("Signal ECG Fusionné pour le calcul du BPM")
plt.legend()
plt.grid(True, linestyle='--', linewidth=0.5)
plt.show()

#FIR filtre
num_taps = 101  # Nombre de coefficients du filtre (doit être impair pour symétrie)
cutoff = 0.1  # Fréquence de coupure (en fraction de la fréquence d'échantillonnage)
fir_coeff = firwin(num_taps, cutoff)
filtered_ecg = lfilter(fir_coeff, 1.0, merged_ecg)
plt.figure(figsize=(12, 5))
plt.plot(filtered_ecg, label="ECG Filtré", color='blue')
plt.xlabel("Échantillons")
plt.ylabel("Amplitude ECG")
plt.title("Signal ECG après Filtrage FIR")
plt.legend()
plt.grid(True, linestyle='--', linewidth=0.5)
plt.show()

#Pics R
peaks, _ = find_peaks(filtered_ecg, height=np.mean(filtered_ecg) + np.std(filtered_ecg))
print(f"Pics détectés aux indices : {peaks}")
plt.figure(figsize=(12, 5))
plt.plot(filtered_ecg, label="ECG Filtré", color='blue')
plt.scatter(peaks, filtered_ecg[peaks], color='red', label="Pics R", zorder=3)
plt.xlabel("Échantillons")
plt.ylabel("Amplitude ECG")
plt.title("Détection des Pics R dans l'ECG Filtré")
plt.legend()
plt.grid(True, linestyle='--', linewidth=0.5)

plt.show()

##intervallle RR
rr_intervals = np.diff(peaks)
sampling_rate = 360 
rr_intervals_sec = rr_intervals / sampling_rate
print(f"Intervalles RR détectés (en secondes) : {rr_intervals_sec}")

#BPM
if len(rr_intervals_sec) > 0:
    bpm = 60 / np.mean(rr_intervals_sec)
    print(f" BPM estimé : {bpm:.2f} battements par minute")
else:
    bpm = 0
    print(" Pas assez de pics détectés pour calculer le BPM")

ecg_cleaned = nk.ecg_clean(filtered_ecg, sampling_rate=sampling_rate)
signals, info = nk.ecg_process(ecg_cleaned, sampling_rate=sampling_rate)

nk.ecg_plot(signals, info)

print(f"P détectés : {np.sum(signals['ECG_P_Peaks'])}")
print(f"Q détectés : {np.sum(signals['ECG_Q_Peaks'])}")
print(f"R détectés : {np.sum(signals['ECG_R_Peaks'])}")
print(f"S détectés : {np.sum(signals['ECG_S_Peaks'])}")
print(f"T détectés : {np.sum(signals['ECG_T_Peaks'])}")

# Extraire les indices des ondes PQRST à partir de NeuroKit2
p_peaks = np.where(signals["ECG_P_Peaks"] == 1)[0]
q_peaks = np.where(signals["ECG_Q_Peaks"] == 1)[0]
r_peaks = np.where(signals["ECG_R_Peaks"] == 1)[0]
s_peaks = np.where(signals["ECG_S_Peaks"] == 1)[0]
t_peaks = np.where(signals["ECG_T_Peaks"] == 1)[0]

# Affichage du signal ECG filtré avec marquage des points PQRST
plt.figure(figsize=(14, 6))
plt.plot(filtered_ecg, label="ECG Filtré", color='black')

plt.scatter(p_peaks, filtered_ecg[p_peaks], color='green', label="Onde P", zorder=3)
plt.scatter(q_peaks, filtered_ecg[q_peaks], color='orange', label="Point Q", zorder=3)
plt.scatter(r_peaks, filtered_ecg[r_peaks], color='red', label="Point R", zorder=3)
plt.scatter(s_peaks, filtered_ecg[s_peaks], color='purple', label="Point S", zorder=3)
plt.scatter(t_peaks, filtered_ecg[t_peaks], color='pink', label="Onde T", zorder=3)

plt.title("Détection des Points PQRST avec NeuroKit2")
plt.xlabel("Échantillons")
plt.ylabel("Amplitude ECG")
plt.legend(loc='upper right')
plt.grid(True, linestyle='--', linewidth=0.5)
plt.show()




###################################QT_6#########################################
#ajout d un bruit
noise_std = 5 
noisy_ecg = np.array(plaintext_decimal) + np.random.normal(0, noise_std, len(plaintext_decimal))
noisy_ecg = np.clip(noisy_ecg, 0, 255).astype(np.uint8)
plaintext_noisy_hexa = noisy_ecg.tobytes().hex()
plaintext_noisy = bytes.fromhex(plaintext_noisy_hexa)
plt.figure(figsize=(12, 5))
plt.plot(plaintext_decimal, label="ECG Original", color='green')
plt.plot(noisy_ecg, label="ECG avec Bruit", color='orange')
plt.title("Ajout de Bruit Gaussien au Signal ECG")
plt.xlabel("Échantillons")
plt.ylabel("Amplitude ECG")
plt.legend()
plt.grid(True, linestyle='--', linewidth=0.5)
plt.show()


ciphertext = ascon_pcsn.ascon_encrypt(key, nonce, associated_data, plaintext_noisy, variant="Ascon-128")
print("Texte chiffré avec noise :", ciphertext.hex())


threshold_error = 10
corrected_ecg = []

for i in range(len(decrypted_decimal)):
    if abs(decrypted_decimal[i] - plaintext_decimal[i]) > threshold_error:
        corrected_value = plaintext_decimal[i]  # Correction simple : remettre valeur originale
        corrected_ecg.append(corrected_value)
    else:
        corrected_ecg.append(decrypted_decimal[i])

plt.figure(figsize=(12, 5))
plt.plot(decrypted_decimal, label="ECG Déchiffré Bruité", color='red')
plt.plot(corrected_ecg, label="ECG Corrigé", color='blue')
plt.title("Correction d'Erreur sur ECG Bruité")
plt.xlabel("Échantillons")
plt.ylabel("Amplitude ECG")
plt.legend()
plt.grid(True, linestyle='--', linewidth=0.5)
plt.show()

# Tracer les deux signaux ensemble
plt.figure(figsize=(12, 5))
plt.plot(decrypted_decimal, label="ECG Déchiffré", color='blue')
plt.plot(plaintext_decimal, label="ECG Originale", color='red')
plt.xlabel("Échantillons")
plt.ylabel("Amplitude ECG")
plt.title("Comparaison entre l'ECG Original et Déchiffré")
plt.legend()
plt.grid(True, linestyle='--', linewidth=0.5)
plt.show()
