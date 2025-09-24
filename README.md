This is a Digital Communication System project that focuses on key building blocks of modern communication techniques such as modulation, channel estimation, synchronization, encoding, and mapping.  
The system is designed to simulate how digital data is transmitted over a noisy channel, processed at the receiver, and reconstructed with error correction and synchronization.

---

## 🚀 Features

- **Modulation**  
  Implements digital modulation schemes for transmitting signals efficiently over a channel.

- **Encoding & Mapping**  
  Includes source and channel encoding with bit-to-symbol mapping for reliable transmission.

- **Synchronization**  
  Frame and symbol synchronization for aligning received signals in time and frequency.

- **Channel Estimation**  
  Estimates and compensates for channel impairments like noise, distortion, and fading.

- **Preambles**  
  Uses preambles for robust synchronization and detection.

---

## 📂 Project Structure

- `communicationSystem.py` – Main entry point that integrates all components of the system.  
- `modulation.py` – Functions for modulation and demodulation.  
- `encoding.py` – Handles encoding and decoding of data.  
- `mapping.py` – Symbol mapping and demapping functions.  
- `synchronization.py` – Implements synchronization techniques for received signals.  
- `channelEstimation.py` – Channel estimation and equalization algorithms.  
- `preambles.txt` – Preamble sequences used for synchronization.  
  
---

## 🛠️ Requirements

- Python 3.x  
- NumPy  
- SciPy  
- Matplotlib

