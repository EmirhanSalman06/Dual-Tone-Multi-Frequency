import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------------------------------
# 1. SYSTEM PARAMETERS & LOOKUP TABLE
# -------------------------------------------------------------------------
Fs = 8192.0         # Sampling rate in Hz
duration = 0.1      # Signal duration (100 ms)
N = int(Fs * duration)
n = np.arange(N)

# Keypad frequency mapping: (omega_row, omega_column) in radians/sample
DTMF_KEYPAD = {
    '1': (0.5346, 0.9273), '2': (0.5346, 1.0247), '3': (0.5346, 1.1328),
    '4': (0.5906, 0.9273), '5': (0.5906, 1.0247), '6': (0.5906, 1.1328),
    '7': (0.6535, 0.9273), '8': (0.6535, 1.0247), '9': (0.6535, 1.1328),
    '*': (0.7217, 0.9273), '0': (0.7217, 1.0247), '#': (0.7217, 1.1328)
}

# -------------------------------------------------------------------------
# 2. SIGNAL GENERATION FUNCTION
# -------------------------------------------------------------------------
def generate_dtmf_signal(key, sample_count=N):
    """
    Generates a dual-tone touch-tone signal for the specified key.
    Formula: d_k[n] = sin(omega_row * n) + sin(omega_column * n)
    """
    if key not in DTMF_KEYPAD:
        raise ValueError(f"Invalid key requested: {key}")
    
    w_row, w_col = DTMF_KEYPAD[key]
    time_indices = np.arange(sample_count)
    return np.sin(w_row * time_indices) + np.sin(w_col * time_indices), w_row, w_col

# -------------------------------------------------------------------------
# 3. DTMF DECODER FUNCTION
# -------------------------------------------------------------------------
def decode_dtmf_signal(signal_data, N_fft=2048):
    """
    Detects the pressed key by finding peak frequencies via FFT.
    """
    half_N = N_fft // 2
    omega_bins = np.linspace(0, np.pi, half_N)
    spectrum = np.abs(np.fft.fft(signal_data, N_fft)[:half_N])

    # Search for peak in low-frequency row band [0.45, 0.80] rad
    row_region = (omega_bins >= 0.45) & (omega_bins <= 0.80)
    detected_row = omega_bins[row_region][np.argmax(spectrum[row_region])]

    # Search for peak in high-frequency column band [0.85, 1.25] rad
    col_region = (omega_bins >= 0.85) & (omega_bins <= 1.25)
    detected_col = omega_bins[col_region][np.argmax(spectrum[col_region])]

    # Match against closest keypad entries
    detected_key = None
    min_dist = float("inf")
    for key, (r_val, c_val) in DTMF_KEYPAD.items():
        dist = np.hypot(detected_row - r_val, detected_col - c_val)
        if dist < min_dist:
            min_dist = dist
            detected_key = key

    return detected_key, detected_row, detected_col

# -------------------------------------------------------------------------
# 4. EXECUTION DEMO
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
    # Key Selection Configuration:
    # - Uncomment the static assignment below to bypass user interaction and
    #   directly analyze a preset key (e.g., '5', '4', '#').
    # - Alternatively, use the interactive input block to prompt the user at runtime
    #   and dynamically synthesize, decode, and plot the DTMF waveform.
    # -------------------------------------------------------------------------
    # target_key = '5'  # Static assignment
    

if __name__ == "__main__":
    # Key Selection Configuration:
    # Set statically (e.g., target_key = '5') to bypass interactive prompt, or leave dynamic:
    target_key = input("Enter a key from keypad (0-9, *, #): ").strip()
    
    # Input validation loop
    while target_key not in DTMF_KEYPAD:
        print("Invalid key! Please choose one of: 0-9, *, #")
        target_key = input("Enter a key: ").strip()

    # Signal synthesis
    signal, expected_w_row, expected_w_col = generate_dtmf_signal(target_key)
    
    # Compute FFT
    N_fft = 2048
    half_N = N_fft // 2
    magnitude_spectrum = np.abs(np.fft.fft(signal, N_fft)[:half_N]) / (N / 2)
    omega_axis = np.linspace(0, np.pi, half_N)

    # Decode the generated signal
    decoded_key, found_row, found_col = decode_dtmf_signal(signal, N_fft)
    print(f"\n--- DTMF Analysis for Key '{target_key}' ---")
    print(f"Expected Frequencies -> w_row: {expected_w_row:.4f}, w_col: {expected_w_col:.4f}")
    print(f"Detected Frequencies -> w_row: {found_row:.4f}, w_col: {found_col:.4f}")
    print(f"Decoded Key          -> '{decoded_key}' (Success: {decoded_key == target_key})")

    # Visualization
    plt.figure(figsize=(11, 7))

    # Time-domain plot
    plt.subplot(2, 1, 1)
    plt.plot(n[:120], signal[:120], 'b-', linewidth=1.5)
    plt.title(f"Time-Domain Waveform for Key '{target_key}' (First 120 Samples)")
    plt.xlabel("Sample Index n")
    plt.ylabel("Amplitude d[n]")
    plt.grid(True, linestyle="--", alpha=0.5)

    # Frequency-domain plot
    plt.subplot(2, 1, 2)
    plt.plot(omega_axis, magnitude_spectrum, 'r-', linewidth=1.5, label="Magnitude Spectrum")
    plt.axvline(expected_w_row, color='g', linestyle='--', label=f"Row Peak ({expected_w_row:.4f} rad)")
    plt.axvline(expected_w_col, color='m', linestyle='--', label=f"Column Peak ({expected_w_col:.4f} rad)")
    plt.title(f"DTFT Magnitude Spectrum |D(e^{{j\\omega}})| for Key '{target_key}'")
    plt.xlabel("Discrete Angular Frequency \\omega (rad/sample)")
    plt.ylabel("Normalized Magnitude")
    plt.xlim([0, np.pi])
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.show()