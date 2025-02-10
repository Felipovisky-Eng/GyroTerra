#include <Wire.h>     // MPU-6050
#include <MPU6050.h>  // MPU-6050
#include <SD.h>       // Cartão SD
#include <SPI.h>      // Cartão SD
#include <RTClib.h>   // RTC

MPU6050 mpu(0x69);  // Define o endereço I2C como 0x69
RTC_DS1307 rtc;
File dataFile;

DateTime startTime;                              // Variável para armazenar o tempo inicial
const long recordingDuration = 48L * 60L * 60L;  // 48 horas em segundos


int lastSecond = -1;  // Armazena o último segundo verificado

void setup() {
  Serial.begin(115200);

  pinMode(2, INPUT_PULLUP);  // Configura o botão com pull-up interno
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);

  Wire.begin();



  //----------------Verificação do funcionamento do MPU-6050 em duas etapas-------------------------//

  mpu.initialize();  // Verifica se o MPU não funcionou
  if (!mpu.testConnection()) {
    Serial.println("Erro ao iniciar o MPU-6050");
    while (1)
      ;
  }
  if (mpu.testConnection()) {  // Verifica se o MPU não funcionou  de novO só por garantia
    Serial.println("MPU INICIALIZADO");
  }



  //----------------Verificação do funcionamento do RTC em três etapas-------------------------//


  if (!rtc.begin()) {  // Verifica se o RTC não funcionou
    Serial.println("Erro ao iniciar o RTC");
    while (1)
      ;
  }
  if (rtc.begin()) {  // Verifica se o RTC não funcionou  de novO só por garantia
    Serial.println("RTC INICIALIZADO");

    ;
  }

  if (!rtc.isrunning()) {  // Verifica algum outro aspecto da conexão
    Serial.println("RTC não está rodando, ajustando a hora...");
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }




  //----------------Verificação do funcionamento do Cartão SD em três etapas-------------------------//

  if (!SD.begin(10)) {  // Verifica se ele não funcionou
    Serial.println("Erro ao inicializar o SD!");
    while (1)
      ;
  }
  if (SD.begin(10)) {  // verifica se ele funcionou
    Serial.println("SD INICIALIZADO");

    ;
  }
  dataFile = SD.open("datalog.txt", FILE_WRITE);

  if (!dataFile) {  // Verifica se o arquivo abriu
    Serial.println("Erro ao abrir o arquivo no SD!");
    while (1)
      ;
  }

  // Armazena a data/hora de início
  startTime = rtc.now();
  Serial.println(startTime.timestamp());
  Serial.println("Sistema pronto!");
}

//----------------Função que fecha o arquivo e salva os dados-------------------------//

void closeFile() {
  dataFile.close();
  Serial.println("Arquivo fechado corretamente.");
  digitalWrite(3, LOW);
  digitalWrite(4, HIGH);
  return;
}




//----------------Void loop-------------------------//

void loop() {


  DateTime now = rtc.now();

  long elapsedTime = now.unixtime() - startTime.unixtime();  // Tempo decorrido em segundos

  digitalWrite(3, HIGH);  // Led pra debug
  digitalWrite(4, LOW);   // Led pra debug

  //----------------Verifica se já se passou 48 horas-------------------------//

  if (elapsedTime >= recordingDuration) {
    closeFile();
  }

  //----------------Verifica o botão para encerrar a gravação antecipadamente -------------------------//

  if (digitalRead(2) == LOW) {  // LOW indica botão pressionado
    Serial.println("fim manual");
    closeFile();
    while (1)
      ;
  }


  //----------------Variaveis e coletas do MPU-6050-------------------------//
  int16_t ax, ay, az, gx, gy, gz;
  mpu.getAcceleration(&ax, &ay, &az);
  mpu.getRotation(&gx, &gy, &gz);


  char dataString[64];  // Ajuste o tamanho conforme necessário
  snprintf(dataString, sizeof(dataString), "%04d,%02d,%02d,%02d,%02d,%02d,%d,%d,%d,%d,%d,%d",
           now.year(), now.month(), now.day(), now.hour(), now.minute(), now.second(),
           ax, ay, az, gx, gy, gz);
  dataFile.println(dataString);


  dataFile.println(dataString);

  Serial.println(dataString);
  Serial.println(elapsedTime);


  // Verifica se um novo segundo começou
  if (now.second() != lastSecond) {
    lastSecond = now.second();  // Atualiza o último segundo registrado

    // A cada 60 segundos (mudança de minuto), grava os dados no SD
    if (now.second() % 60 == 0) {
      dataFile.flush();
      Serial.println("Dados sincronizados no SD.");
      digitalWrite(3, LOW);
    }
  }



  delay(1000);
}
