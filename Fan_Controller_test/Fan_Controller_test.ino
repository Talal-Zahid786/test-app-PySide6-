#include <WiFi.h>
#include <WebServer.h>
#include <AsyncTCP.h>
#include <ArduinoJson.h>

const char* hostName = "fan-controller";
const char* ssid = "PTCLBBHOME";
const char* password = "Zahid@on987";

bool fanOn = false;
uint8_t fanSpeed = 0;
int fanPin =  2;

WebServer server(80);

TaskHandle_t Task1;

void setFanSpeed() {
  if (server.hasArg("plain") == false) {
    server.send(400, "text/plain", "Body not received");
    return;
  }

  String body = server.arg("plain");
  Serial.println("Received POST:");
  Serial.println(body);

  // Parse JSON
  StaticJsonDocument<200> doc;
  DeserializationError error = deserializeJson(doc, body);
  
  if (error) {
    Serial.println("JSON parse failed!");
    server.send(400, "text/plain", "Invalid JSON");
    return;
  }
  fanOn = doc["fan_on"];
  fanSpeed = doc["fan_speed"];
  Serial.printf("Fan-On: %d, Fan-Speed: %d\n", fanOn, fanSpeed);

  server.send(200, "application/json", "{\"status\":\"ok\"}");
}

void sendReadings() {

    StaticJsonDocument<256> doc;

    // Simulated meter values
    doc["temperature"] = random(0, 100);     // °C
    doc["voltage"] = random(0, 330);       // V
    doc["current"] = random(0, 30);          // A
    doc["power"] = random(0, 800);          // KW
    doc["energy"] = random(50, 1000);         // KWh

    char jsonString[256];
    serializeJson(doc, jsonString, sizeof(jsonString));
    server.send(200, "application/json", jsonString);
    Serial.println("Data Sent");
}

void TaskCode1(void *parameter) {
  while (true) {
    if(WiFi.isConnected())
    server.handleClient();
    delay(10);
  }
}

void setup() {
  Serial.begin(115200);
  WiFi.setHostname("fan-controller");
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("\nConnected!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  server.on("/fan-speed", HTTP_POST, setFanSpeed);
  server.on("/meters", HTTP_GET, sendReadings);
  server.begin();
  xTaskCreatePinnedToCore(
    TaskCode1,
    "Task1",
    10000,
    NULL,
    1,
    &Task1,
    0);
    ledcAttach(fanPin, 5000, 8);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(fanOn){
    ledcWrite(fanPin, fanSpeed);
  }
  else{
    ledcWrite(fanPin, 0);
  }
  delay(5);
}
