# Web Monitoring Sensor

Sistem akuisisi data sederhana: sensor (ESP32) -> HTTP POST -> server Python + SQLite -> dashboard web real-time.
Mata kuliah Instrumentasi Elektronika (UNDIRA).

## Arsitektur
`ESP32 (LM35 + ADC)` -> `POST /api/data` -> `server.py (SQLite)` -> `static/index.html` (grafik, polling 2 detik)

## Menjalankan
```
python server.py          # buka http://localhost:8000
python simulator.py       # tanpa hardware: data tiruan tiap 2 detik
```
Dengan hardware: buka `firmware/esp32_monitor/esp32_monitor.ino`, isi WiFi dan IP server, upload dari Arduino IDE.

## Rangkaian
- LM35: VCC ke 3V3, OUT ke GPIO34, GND ke GND.
- Tegangan uji: lewat pembagi tegangan ke GPIO35 (maks 3,3 V).

## API
| Metode | Path | Keterangan |
|---|---|---|
| POST | /api/data | `{"suhu_c": 28.5, "tegangan_v": 3.12}` |
| GET | /api/data?limit=100 | data terbaru |

## Catatan
ADC ESP32 tidak linear; kalibrasi dengan multimeter sebelum mengambil data resmi.
