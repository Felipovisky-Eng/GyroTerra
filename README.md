# Projeto de Aquisição de Dados com MPU-6050 e RTC

Este projeto realiza a leitura de dados do sensor **MPU-6050** e registra as informações em um **cartão SD**, utilizando um **RTC DS1307** para marcação precisa do tempo. O sistema conta com um botão para interrupção manual da gravação e LEDs para indicar o status da operação.

## 🚀 **Funcionamento**
- O sistema inicia a gravação ao ser ligado.
- A cada segundo, os dados do acelerômetro e giroscópio são lidos e armazenados no cartão SD.
- A cada 60 segundos, os dados são sincronizados no SD para evitar perda de informações.
- A gravação pode ser interrompida manualmente pressionando o botão.
- O sistema também para automaticamente após **48 horas** de gravação contínua.

## 🛠 **Componentes Utilizados**
- **Microcontrolador**: ATmega328P (Arduino ou similar)
- **Sensor de Movimento**: MPU-6050
- **Módulo RTC**: DS1307
- **Cartão SD** para armazenamento
- **Botão de parada** da gravação
- **LEDs de status**

## 🔌 **Pinagem**
### **Cartão SD**
| Sinal  | Pino no Microcontrolador |
|--------|-------------------------|
| **CS**  | 10 |
| **MOSI** | 11 |
| **MISO** | 12 |
| **SCK**  | 13 |

### **Botão e LEDs**
| Função  | Pino |
|---------|------|
| **Botão (Pull-up)** | 2 |
| **LED de Gravação** | 3 |
| **LED de Término** | 4 |

### **I2C - MPU-6050 e RTC**
| Sinal | Pino |
|-------|------|
| **SCL** | A5 |
| **SDA** | A4 |

> **Nota**: O **MPU-6050** deve estar configurado no **endereço `0x69`** (`AD0 = HIGH`), pois o **RTC DS1307** usa o endereço **`0x68`**.

## 📂 **Estrutura dos Dados Salvos**
Cada linha do arquivo salvo no SD segue o formato:

AAAA,MM,DD,HH,MM,SS,MS,AX,AY,AZ,GX,GY,GZ

Onde:
- **AAAA, MM, DD** → Ano, mês e dia
- **HH, MM, SS, MS** → Hora, minuto, segundo e milissegundos
- **AX, AY, AZ** → Aceleração nos eixos X, Y e Z
- **GX, GY, GZ** → Velocidade angular nos eixos X, Y e Z
