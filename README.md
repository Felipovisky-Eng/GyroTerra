# Projeto de Aquisição de Dados com MPU-6050 e RTC

### Código C++ "Testetempo"

Este projeto realiza a leitura de dados do sensor **MPU-6050** e registra as informações em um **cartão SD**, utilizando um **RTC DS1307** para marcação precisa do tempo. O sistema conta com um botão para interrupção manual da gravação e LEDs para indicar o status da operação.

## 🚀 **Funcionamento**
- O sistema inicia a gravação ao ser ligado.
- A escala do Giroscópio é configurada para ``250°/s``.
- A escala so Acelerômetro é configurada para ``2g``.
- A cada segundos, os dados do acelerômetro e giroscópio são lidos e armazenados no cartão SD.
- A cada 60 segundos, os dados são sincronizados no SD para evitar perda de informações.
- A gravação pode ser interrompida manualmente pressionando o botão.
- O sistema também para automaticamente após **48 horas** de gravação contínua.

## 🛠 **Componentes Utilizados**
- **Microcontrolador**: ATmega328P (Arduino)
- **Sensor IMU**: MPU-6050
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

AAAA,MM,DD,HH,MM,SS,AX,AY,AZ,GX,GY,GZ

Onde:
- **AAAA, MM, DD** → Ano, mês e dia
- **HH, MM, SS, MS** → Hora, minuto e segundo
- **AX, AY, AZ** → Aceleração nos eixos X, Y e Z
- **GX, GY, GZ** → Velocidade angular nos eixos X, Y e Z
---
### Código C++ "Testetempomillis"

Este é um segundo código baseado na versão original, porém com uma **modificação importante**:  
➡ **O RTC foi removido**, e agora o código utiliza a função `millis()` para registrar o tempo.  

### 🔧 **Diferenças desta versão**  
✅ **RTC Removido** → O tempo agora é medido em milissegundos desde o início da execução.  
✅ **Registro contínuo dos dados** → A cada 0,5 segundos a leitura do **MPU-6050** é salva no cartão SD.  
✅ **Formato do arquivo de saída**:
```csv
tempo_ms, ax, ay, az, gx, gy, gz
````
✅ **Fechamento automático após 48 horas** → Se o tempo de execução ultrapassar esse limite, o arquivo é salvo e fechado.  
✅ **Sincronização periódica** → A cada 60 segundos, os dados são gravados no cartão SD para evitar perdas.  
✅ **Parada manual via botão** → Se o botão for pressionado, a gravação é interrompida e o arquivo é fechado corretamente.  

📜 Motivação para esta mudança
Na primeira versão, o código utilizava um RTC (Relógio de Tempo Real) para marcar a data e a hora de cada amostra. No entanto, como o objetivo era realizar coletas longas e garantir a integridade dos dados, optamos por usar a função millis(). Dessa forma, evitamos problemas de comunicação com o RTC e reduzimos o número de componentes necessários no projeto.Esta versão facilita o pós-processamento dos dados em Python, pois fornece um tempo contínuo baseado em milissegundos.



---
---

# Análise de Deslocamento Angular

## Código em python "Gyromillis"

### Descrição

Este código realiza a análise de deslocamento angular a partir dos dados coletados por sensores de movimento, como giroscópios e acelerômetros. O principal objetivo é medir a velocidade anglar da terra utilizando o giroscópio e acelerometro MPU-6050. O giroscópio irá medir a velocidade angular da terra e os dados do acelerometro serão utilizados para corrigir a inclinação do mesmo, futuramnte pode-se implementar um MPU-9265 com magnerômetro integrado para melhor correção de orientação. O código aplica filtros complementares e de Kalman para melhorar a precisão das estimativas e também considera o efeito da rotação da Terra, comparando o deslocamento real do sistema com o deslocamento esperado pela rotação do planeta.

### Funcionalidade

O código foi desenvolvido para realizar as seguintes operações:

1. **Cálculo do deslocamento angular nos eixos X, Y e Z**: A partir das velocidades angulares fornecidas pelos giroscópios, o código integra essas velocidades ao longo do tempo para obter os deslocamentos angulares.
  
2. **Correção dos ângulos de pitch e roll**: Um filtro complementar é aplicado para corrigir os ângulos de pitch e roll, combinando as medições do giroscópio e do acelerômetro. Isso ajuda a reduzir o erro acumulado ao longo do tempo.

3. **Correção do ângulo de yaw usando Filtro de Kalman**: O código implementa um filtro de Kalman para corrigir o ângulo de yaw, levando em consideração as incertezas tanto nos sensores quanto nas estimativas. O filtro de Kalman é particularmente útil para melhorar a precisão dos cálculos ao reduzir o impacto de ruídos nas medições.

4. **Cálculo e comparação com o deslocamento esperado pela rotação da Terra**: O código calcula o deslocamento angular esperado devido à rotação da Terra e compara com o deslocamento real estimado a partir dos sensores.

5. **Geração de gráficos**: O código gera gráficos para comparar os deslocamentos reais corrigidos com o deslocamento esperado, ajudando na visualização dos erros e na avaliação da precisão dos cálculos.

### Processamento de Dados

O processo de cálculo do deslocamento angular envolve a integração das velocidades angulares fornecidas pelos giroscópios. No caso do pitch e roll, utiliza-se um filtro complementar para corrigir os ângulos com base nos dados do acelerômetro e giroscópio. Já o ângulo de yaw é corrigido com a ajuda de um filtro de Kalman, que estima o valor do ângulo levando em consideração a incerteza nas medições.

### Resultados

O código gera gráficos que mostram a evolução do deslocamento angular nos três eixos (X, Y, Z) ao longo do tempo. Além disso, o gráfico final compara o deslocamento real corrigido com o deslocamento esperado pela rotação da Terra. Isso permite visualizar o erro acumulado durante o cálculo e verificar a precisão das estimativas.

### Requisitos

Para executar este código, é necessário ter as seguintes bibliotecas Python instaladas:

- `numpy`
- `matplotlib`
- `scipy`
- `pandas`
- `tkinter`

# Arquivos de Teste

No Githib estará disponível arquivos ``.txt`` para testes do código em ``Python`` *Gyromillis*, esses arquivos são originados das coletas do MPU-6050 utilizando o código em ``C++`` *Testetempomillis*.
