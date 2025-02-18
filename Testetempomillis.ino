#include <Wire.h>     // MPU-6050
#include <MPU6050.h>  // MPU-6050
#include <SD.h>       // Cartão SD
#include <SPI.h>      // Cartão SD

MPU6050 mpu(0x69);  // Define o endereço I2C como 0x69

File dataFile;

const unsigned long recordingDuration = 48L * 60L * 60L * 1000L;  // 48 horas em milissegundos
unsigned long startTime;  // Armazena o tempo inicial
unsigned long lastFlush = 0;  // Última vez que os dados foram sincronizados no SD
const unsigned long flushInterval = 60L * 1000L;  // Sincronizar a cada 60 segundos

void setup() {
  Serial.begin(115200);

  pinMode(2, INPUT_PULLUP);  // Configura o botão com pull-up interno
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);

  Wire.begin();

  //----------------Verificação do funcionamento do MPU-6050-------------------------//
  mpu.initialize();
  if (!mpu.testConnection()) {
    Serial.println("Erro ao iniciar o MPU-6050");
    while (1);
  }
  Serial.println("MPU INICIALIZADO");
  
   // Configurar a escala do acelerômetro para ±2g
   mpu.setFullScaleAccelRange(MPU6050_ACCEL_FS_2);

  // Configurar a escala do giroscópio para ±250°/s
   mpu.setFullScaleGyroRange(MPU6050_GYRO_FS_250);
  
  //----------------Verificação do funcionamento do Cartão SD-------------------------//
  if (!SD.begin(10)) {
    Serial.println("Erro ao inicializar o SD!");
    while (1);
  }
  Serial.println("SD INICIALIZADO");

  dataFile = SD.open("datalogmillis.txt", FILE_WRITE);
  if (!dataFile) {
    Serial.println("Erro ao abrir o arquivo no SD!");
    while (1);
  }

  // Armazena o tempo de início
  startTime = millis();
  Serial.println("Sistema pronto!");
}

//----------------Função que fecha o arquivo e salva os dados-------------------------//
void closeFile() {
  dataFile.close();
  Serial.println("Arquivo fechado corretamente.");
  digitalWrite(3, LOW);
  digitalWrite(4, HIGH);
  while (1);
}

//----------------Void loop-------------------------//
void loop() {
  digitalWrite(3, HIGH);  // LED de gravação ativa
  digitalWrite(4, LOW);   // LED de término apagado

  unsigned long elapsedTime = millis() - startTime;  // Tempo decorrido

  //----------------Verifica se já se passou 48 horas-------------------------//
  if (elapsedTime >= recordingDuration) {
    Serial.println("Tempo máximo atingido, encerrando gravação.");
    closeFile();
  }

  //----------------Verifica o botão para encerrar a gravação antecipadamente-------------------------//
  if (digitalRead(2) == LOW) {  // LOW indica botão pressionado
    Serial.println("Fim manual da gravação.");
    closeFile();
  }

  //----------------Coleta dados do MPU-6050-------------------------//
  int16_t ax, ay, az, gx, gy, gz;
  mpu.getAcceleration(&ax, &ay, &az);
  mpu.getRotation(&gx, &gy, &gz);

  unsigned long tempo_atual = millis();  // Captura o tempo em milissegundos

  // Formatar os dados para gravação
  char dataString[64];
  snprintf(dataString, sizeof(dataString), "%lu,%d,%d,%d,%d,%d,%d",
           tempo_atual, ax, ay, az, gx, gy, gz);

  dataFile.println(dataString);  // Salva no SD
  Serial.println(dataString);

  //----------------Sincroniza os dados no SD a cada 60 segundos-------------------------//
  if (millis() - lastFlush >= flushInterval) {
    dataFile.flush();
    lastFlush = millis();
    Serial.println("Dados sincronizados no SD.");
    digitalWrite(3, LOW);
  }

  delay(500);  // Pequeno atraso para reduzir a frequência de gravação
}
