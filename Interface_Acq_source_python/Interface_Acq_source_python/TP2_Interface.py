import ascon_pcsn
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd
from scipy.signal import find_peaks, firwin, lfilter
import serial

def read_ecg_uart(port="/dev/ttyUSB0", baudrate=115200):
    """
    Fonction pour lire les données ECG chiffrées envoyées par le FPGA via UART.
    """
    ser = serial.Serial(port, baudrate, timeout=1)
    data = ser.read(1024)  # Lire 1024 octets de données
    ser.close()
    return data


key_hexa = "8A55114D1CB6A9A2BE263D4D7AECAAFF" 
nonce_hexa = "4ED0EC0B98C529B7C8CDDF37BCD0284A" 
plaintext_hexa = "36353335353535353434343432312F31343533333233333436393C3D3F3F403E3E3F3F403F3F3D3C3A39383736363633312D2C2A2B2B2B2A29292825211A171518191B1D242F384043484D57667582909AA6B3C0C9D3DEE9F0F8FFFEFBF1E1CEB59C826A57463A2D221A16161717161514151514151718181715121314131211111111100F0E0D0D0E0E0E0D0B0A0B0B09070606060707070605040302010000010304020000010100010203050303010204060708"

associateddata = b"A to B"


key = bytes.fromhex(key_hexa)
nonce = bytes.fromhex(nonce_hexa)
plaintext = bytes.fromhex(plaintext_hexa)

#ciphertext = ascon_pcsn.ascon_encrypt(key, nonce, associateddata, plaintext, variant="Ascon-128")
#print("Texte chiffré :", ciphertext)
plaintext_decimal = list(plaintext)


mode = "test"  # Change en "fpga" pour utiliser UART
if mode == "test":
    ciphertext = ascon_pcsn.ascon_encrypt(key, nonce, associateddata, plaintext, variant="Ascon-128")
    print("Texte chiffré :", ciphertext.hex())
else:
    ciphertext = read_ecg_uart()
    print("Texte chiffré reçu du FPGA :", ciphertext.hex())
"""""
if mode == "test":
    ciphertext = ascon_pcsn.ascon_encrypt(key, nonce, associateddata, plaintext, variant="Ascon-128")
    print("Texte chiffré :", ciphertext.hex())
else:
    ciphertext = read_ecg_uart()
    print("Texte chiffré reçu du FPGA :", ciphertext.hex())
"""
ciphertext_hex = ciphertext.hex()
print("Texte chiffré en hexadécimal :", ciphertext_hex)

# dechiff
print("\n Déchiffrement en cours...")
decrypted_text = ascon_pcsn.ascon_decrypt(key, nonce, associateddata, ciphertext, variant="Ascon-128")

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

# repeter l ecg pour avoir un simulation cardiaque
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


def identify_pqrst(ecg_signal, peaks):
    """
    Identifie les segments PQRST en se basant sur les pics R détectés.
    """
    if len(peaks) < 3:
        print(" Trop peu de pics détectés pour une analyse fiable.")
        return [], [], [], [], []

    print("\nAnalyse améliorée des segments PQRST :")

    p_wave, q_wave, s_wave, t_wave = [], [], [], []

    for i in range(len(peaks) - 1):
        r_idx = peaks[i]  # Pic R actuel

        # Fenêtres de recherche pour les autres points
        pre_r_window = 20  # Fenêtre avant R
        post_r_window = 40  # Fenêtre après R

        # Trouver Q (avant R, minimum local)
        q_idx = r_idx - pre_r_window + np.argmin(ecg_signal[r_idx - pre_r_window:r_idx])
        q_wave.append(q_idx)

        # Trouver S (après R, minimum local)
        s_idx = r_idx + np.argmin(ecg_signal[r_idx:r_idx + post_r_window])
        s_wave.append(s_idx)

        # Trouver P (avant Q, maximum local)
        p_idx = q_idx - pre_r_window + np.argmax(ecg_signal[q_idx - pre_r_window:q_idx])
        p_wave.append(p_idx)

        # Trouver T (après S, maximum local)
        t_idx = s_idx + np.argmax(ecg_signal[s_idx:s_idx + post_r_window])
        t_wave.append(t_idx)

    # Tracer le signal ECG avec les points PQRST détectés
    plt.figure(figsize=(12, 5))
    plt.plot(ecg_signal, label="ECG Filtré", color='blue')
    plt.scatter(peaks, ecg_signal[peaks], color='red', label="Pics R")
    plt.scatter(q_wave, ecg_signal[q_wave], color='orange', label="Points Q")
    plt.scatter(s_wave, ecg_signal[s_wave], color='purple', label="Points S")
    plt.scatter(p_wave, ecg_signal[p_wave], color='green', label="Ondes P")
    plt.scatter(t_wave, ecg_signal[t_wave], color='pink', label="Ondes T")
    plt.xlabel("Échantillons")
    plt.ylabel("Amplitude ECG")
    plt.title("Correction de l'Identification des Segments PQRST")
    plt.legend()
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.show()

    return p_wave, q_wave, s_wave, t_wave

# Appliquer la nouvelle détection PQRST
p_wave, q_wave, s_wave, t_wave = identify_pqrst(filtered_ecg, peaks)


def analyze_ecg_anomalies(rr_intervals, p_wave, q_wave, s_wave, t_wave):
    """
    Analyse avancée des anomalies ECG basées sur PQRST.
    """
    print("\nDétection des anomalies ECG :")

    mean_rr = np.mean(rr_intervals)
    std_rr = np.std(rr_intervals)

    if std_rr > 0.15 * mean_rr:
        print("Possible arythmie détectée (irrégularité des intervalles RR)")

    if mean_rr > 1.2 * np.median(rr_intervals):
        print("Possible bradycardie (rythme cardiaque lent)")
    elif mean_rr < 0.6 * np.median(rr_intervals):
        print("Possible tachycardie (rythme cardiaque rapide)")

    if len(q_wave) > 0 and len(s_wave) > 0:
        qrs_durations = np.array(s_wave) - np.array(q_wave)
        mean_qrs = np.mean(qrs_durations)

        if mean_qrs > 120:
            print("Allongement du QRS détecté : possible infarctus ou problème de conduction.")

    if len(p_wave) > 0 and len(q_wave) > 0:
        pq_intervals = np.array(q_wave) - np.array(p_wave)
        mean_pq = np.mean(pq_intervals)

        if mean_pq > 200:
            print("Bloc cardiaque détecté : segment PQ trop long.")

    if len(t_wave) > 0 and len(s_wave) > 0:
        st_intervals = np.array(t_wave) - np.array(s_wave)
        mean_st = np.mean(st_intervals)

        if mean_st > 100:
            print("⚠️ Élévation du segment ST : possible ischémie ou infarctus.")

# Appliquer l'analyse des anomalies
analyze_ecg_anomalies(rr_intervals, p_wave, q_wave, s_wave, t_wave)

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


ciphertext = ascon_pcsn.ascon_encrypt(key, nonce, associateddata, plaintext_noisy, variant="Ascon-128")
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
