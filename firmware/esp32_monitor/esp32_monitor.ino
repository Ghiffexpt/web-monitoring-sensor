// ESP32: baca LM35 (suhu) dan tegangan via pembagi, kirim ke server web monitoring.
// Isi WIFI_SSID, WIFI_PASS, dan SERVER_URL (IP komputer yang menjalankan server.py).
#include <WiFi.h>
#include <HTTPClient.h>

const char* WIFI_SSID  = "ISI_SSID";
const char* WIFI_PASS  = "ISI_PASSWORD";
const char* SERVER_URL = "http://192.168.1.10:8000/api/data";  // sesuaikan IP

const int PIN_LM35 = 34;   // LM35: 10 mV per derajat C
const int PIN_V    = 35;   // tegangan terukur lewat pembagi tegangan
const float VREF   = 3.3;  // ADC ESP32 tidak linear: kalibrasi dengan multimeter
const float DIV    = 1.0;  // faktor pembagi (mis. 2.0 untuk R1 = R2)

float bacaVolt(int pin) {
  long s = 0;
  for (int i = 0; i < 32; i++) s += analogRead(pin);  // rata-rata mengurangi derau
  return (s / 32.0) / 4095.0 * VREF;
}

void setup() {
  Serial.begin(115200);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print('.'); }
  Serial.println(WiFi.localIP());
}

void loop() {
  float suhu = bacaVolt(PIN_LM35) * 100.0;  // V -> derajat C
  float teg  = bacaVolt(PIN_V) * DIV;
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(SERVER_URL);
    http.addHeader("Content-Type", "application/json");
    String body = "{\"suhu_c\":" + String(suhu, 2) + ",\"tegangan_v\":" + String(teg, 3) + "}";
    int code = http.POST(body);
    Serial.printf("%s -> %d\n", body.c_str(), code);
    http.end();
  }
  delay(2000);
}
