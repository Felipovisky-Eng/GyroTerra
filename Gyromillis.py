import pandas  as pd  #Análise dos dados
import tkinter as tk  #Interface Gráfica
import numpy   as np  #Calculos 
import os             # Para manipulação de caminhos
import matplotlib.pyplot as plt   # Plota os gráficos
import scipy.fft as fft                   # Transformada de Fourier


from tkinter import filedialog            # Busca arquivos
from scipy.interpolate import interp1d    # Calculo de interpolação

#
#
#
# Importaçao do arquivo .txt 
#
#
#

def selecionar_arquivo():     #Função vai permitir abrir a janela para selecionar o arquivo                      
    
    root = tk.Tk()                                   # Base para parte gráfica
    root.withdraw()                                  # Oculta a janela principal do Tkinter
    arquivo = filedialog.askopenfilename(            # Abre a janela de seleção
        title="Selecione o arquivo .txt",            # Titulo do arquivo
        filetypes=[("Arquivos de texto", "*.txt")]   # Tipo do arquivo
    )
    return arquivo # Retorna o caminho do arquivo com o titulo na variavel "arquivo"

#
#
#
# Separação do arquivo .txt usando a pandas
#
#
#

def carregar_dados(caminho_arquivo): # Lê o arquivo 
    
    dados = pd.read_csv(caminho_arquivo, delimiter=",", header=None) # Separa o arquivo em duas colunas usando o ","
    tempo   = dados[0]    # Primeira coluna
    AX      = dados[1]    # Setima coluna
    AY      = dados[2]    # Oitava coluna
    AZ      = dados[3]    # Nona coluna
    GX      = dados[4]    # Decima coluna
    GY      = dados[5]    # Decima primeira coluna
    GZ      = dados[6]    # Decima segunda coluna

    return tempo, AX, AY, AZ, GX, GY, GZ # Retorna primeiro as colunas de tempo depois as de valores 

if __name__ == "__main__":
    print("Selecione o arquivo .txt do arquivo sem o filtro no explorador de arquivos...")
    caminho = selecionar_arquivo() # Define o caminho para o arquivo com base na função anterior
    
    if caminho:
        print(f"Arquivo selecionado: {caminho}") # Imprime o caminho do arquivo
        tempo, AX, AY, AZ, GX, GY, GZ = carregar_dados(caminho) # Carrega as variaveis 
        nome_arquivo = os.path.basename(caminho) # Carrega em uma string o nome do arquivo
        print("\nDados carregados com sucesso!")
        #print("Tempo:", tempo.values)           # Imprime os dados do tempo no terminal
        #print("Valores:", valores.values)       # Imprime os dados do valor no terminal
        #print(f"Nome do arquivo: {nome_arquivo}")
    else:
        print("Nenhum arquivo foi selecionado.") # Caso não tenha selecionado nenhum arquivo
#
#
#
# Manipulaçao de dados
#
#
#

# Tratamento do nome do arquivo
Nome = nome_arquivo.replace(".txt", "") # Tira a extensão do arquivo (.txt) do nome dele
Nome = Nome.replace("_", " ") # Tira o "_" e subtitui por um espaço


# Converte os dados para numpy.ndarray com tipo float
tempo = tempo.to_numpy(dtype=float)  # Converte para numpy.ndarray
AX    = AX.to_numpy(dtype=float)     # Converte para numpy.ndarray
AY    = AY.to_numpy(dtype=float)     # Converte para numpy.ndarray
AZ    = AZ.to_numpy(dtype=float)     # Converte para numpy.ndarray
GX    = GX.to_numpy(dtype=float)     # Converte para numpy.ndarray
GY    = GY.to_numpy(dtype=float)     # Converte para numpy.ndarray
GZ    = GZ.to_numpy(dtype=float)     # Converte para numpy.ndarray

# Ajusta a escala do tempo
tempo = tempo - tempo[0]  # Inicia o tempo em zero
tempo = tempo * 1e-3      # Converte de milissegundos para segundos

# Calcula a frequência de amostragem
Diferenca = np.diff(tempo)       # Diferença entre amostras
Mdiferenca = np.mean(Diferenca)  # Média das diferenças
FS = 1 / Mdiferenca              # Frequência de amostragem

N = len(tempo) # Número de pontos

print(f"Frequência de amostragem estimada: {FS:.2f} Hz")          # Calcula a frequência de amostragem
print(f"Número de pontos: {N}")                                   # Calcula o número de pontos
print(f"Tempo total de gravação: {tempo[-1]:.2f} segundos")       # Calcula o tempo total de gravação

#
#
#
# Análise no domínio da frequência
#
#
#

# Função que divide e calcula a FFT dos sinais

def fft_segmentado(sinal, tamanho_pacote):
    # Calcular FFT para segmentos de tamanho 'tamanho_pacote'
    n = len(sinal)
    fft_total = np.zeros(n, dtype=complex)  # Array para armazenar o resultado final
    
    for i in range(0, n, tamanho_pacote):
        segmento = sinal[i:i + tamanho_pacote]
        if len(segmento) == tamanho_pacote:  # Verifica se o segmento tem o tamanho completo
            fft_total[i:i + tamanho_pacote] = fft.fft(segmento)  # Calcula a FFT do segmento
    return fft_total


# Calcula a FFT dos sinais

FFT_AX = fft_segmentado(AX, 1024) # Calcula a FFT do sinal de aceleração no eixo X
FFT_AY = fft_segmentado(AY, 1024) # Calcula a FFT do sinal de aceleração no eixo Y
FFT_AZ = fft_segmentado(AZ, 1024) # Calcula a FFT do sinal de aceleração no eixo Z

FFT_GX = fft_segmentado(GX, 1024) # Calcula a FFT do sinal de giroscópio no eixo X
FFT_GY = fft_segmentado(GY, 1024) # Calcula a FFT do sinal de giroscópio no eixo Y
FFT_GZ = fft_segmentado(GZ, 1024) # Calcula a FFT do sinal de giroscópio no eixo Z

# Calcula a frequência para cada ponto da FFT

frequencia = fft.fftfreq(len(tempo), Mdiferenca)

# Normaliza a FFT dividindo pelas magnitudes dos pontos

FFT_AX_norm = np.abs(FFT_AX) / N # Normaliza a FFT da aceleração de eixo X
FFT_AY_norm = np.abs(FFT_AY) / N # Normaliza a FFT da aceleração do eixo Y
FFT_AZ_norm = np.abs(FFT_AZ) / N # Normaliza a FFT da aceleração do eixo Z

FFT_GX_norm = np.abs(FFT_GX) / N # Normaliza a FFT da velocidade angular do eixo X
FFT_GY_norm = np.abs(FFT_GY) / N # Normaliza a FFT da velocidade angular do eixo Y
FFT_GZ_norm = np.abs(FFT_GZ) / N # Normaliza a FFT da velocidade angular do eixo Z

# Seleciona apenas as frequências positivas

idx_pos = np.where(frequencia > 0)  # Filtra os índices das frequências positivas

frequencia_pos = frequencia[idx_pos] # Frequências positivas
FFT_AX_pos = FFT_AX_norm   [idx_pos] # Componentes positivas da FFT do eixo X
FFT_AY_pos = FFT_AY_norm   [idx_pos] # Componentes positivas da FFT do eixo Y
FFT_AZ_pos = FFT_AZ_norm   [idx_pos] # Componentes positivas da FFT do eixo Z

FFT_GX_pos = FFT_GX_norm   [idx_pos] # Componentes positivas da FFT do giroscópio no eixo X
FFT_GY_pos = FFT_GY_norm   [idx_pos] # Componentes positivas da FFT do giroscópio no eixo Y
FFT_GZ_pos = FFT_GZ_norm   [idx_pos] # Componentes positivas da FFT do giroscópio no eixo Z


#
#
#
# Plotagem dos gráficos da fft
#
#
#


# Criação do gráfico com FFT normalizada para acelaração nos três eixos
fig, axs = plt.subplots(3, 1, figsize=(10, 8))

# Plot da FFT normalizada do eixo X
axs[0].plot(frequencia_pos, FFT_AX_pos)
axs[0].set_title('FFT Normalizada - Aceleração no Eixo X')
axs[0].set_xlabel('Frequência (Hz)')
axs[0].set_ylabel('Magnitude Normalizada')
axs[0].grid(True)

# Plot da FFT normalizada do eixo Y
axs[1].plot(frequencia_pos, FFT_AY_pos)
axs[1].set_title('FFT Normalizada - Aceleração no Eixo Y')
axs[1].set_xlabel('Frequência (Hz)')
axs[1].set_ylabel('Magnitude Normalizada')
axs[1].grid(True)

# Plot da FFT normalizada do eixo Z
axs[2].plot(frequencia_pos, FFT_AZ_pos)
axs[2].set_title('FFT Normalizada - Aceleração no Eixo Z')
axs[2].set_xlabel('Frequência (Hz)')
axs[2].set_ylabel('Magnitude Normalizada')
axs[2].grid(True)

# Ajuste para não sobrepor os subgráficos
plt.tight_layout()

# Exibe os gráficos
plt.show()


# Criação do gráfico com FFT normalizada para velocidade angular nos três eixos
# Criação do gráfico com FFT normalizada para acelaração nos três eixos
fig, axs = plt.subplots(3, 1, figsize=(10, 8))

# Plot da FFT normalizada do eixo X
axs[0].plot(frequencia_pos, FFT_GX_pos)
axs[0].set_title('FFT Normalizada - Aceleração no Eixo X')
axs[0].set_xlabel('Frequência (Hz)')
axs[0].set_ylabel('Magnitude Normalizada')
axs[0].grid(True)

# Plot da FFT normalizada do eixo Y
axs[1].plot(frequencia_pos, FFT_GY_pos)
axs[1].set_title('FFT Normalizada - Aceleração no Eixo Y')
axs[1].set_xlabel('Frequência (Hz)')
axs[1].set_ylabel('Magnitude Normalizada')
axs[1].grid(True)

# Plot da FFT normalizada do eixo Z
axs[2].plot(frequencia_pos, FFT_GZ_pos)
axs[2].set_title('FFT Normalizada - Aceleração no Eixo Z')
axs[2].set_xlabel('Frequência (Hz)')
axs[2].set_ylabel('Magnitude Normalizada')
axs[2].grid(True)

# Ajuste para não sobrepor os subgráficos
plt.tight_layout()

# Exibe os gráficos
plt.show()


#
#
#
# Converção dos dados dos sensores
#
#
#

G = 9.81  # Aceleração da gravidade (m/s²)

Escala_Acelerometro = (2 / 32768)* G  # Escala do acelerômetro (2g)
Escala_Giroscopio =  250 / 32768      # Escala do giroscópio (250°/s)

# Converte os dados do acelerômetro
AX = AX * Escala_Acelerometro  # Converte o acelerômetro no eixo X
AY = AY * Escala_Acelerometro  # Converte o acelerômetro no eixo Y
AZ = AZ * Escala_Acelerometro  # Converte o acelerômetro no eixo Z

# Converte os dados do giroscópio
GX = GX * Escala_Giroscopio  # Converte o giroscópio no eixo X
GY = GY * Escala_Giroscopio  # Converte o giroscópio no eixo Y
GZ = GZ * Escala_Giroscopio  # Converte o giroscópio no eixo

#
#
#
# Plotagem dos gráficos
#
#
#

# Criação do gráfico com aceleração nos três eixos
fig, axs = plt.subplots(3, 1, figsize=(10, 8))

# Plot da aceleração no eixo X
axs[0].plot(tempo, AX)
axs[0].set_title('Aceleração - Eixo X')
axs[0].set_xlabel('Tempo (s)')
axs[0].set_ylabel('Aceleração (m/s²)')
axs[0].grid(True)

# Plot da aceleração no eixo Y
axs[1].plot(tempo, AY)
axs[1].set_title('Aceleração - Eixo Y')
axs[1].set_xlabel('Tempo (s)')
axs[1].set_ylabel('Aceleração (m/s²)')
axs[1].grid(True)

# Plot da aceleração no eixo Z
axs[2].plot(tempo, AZ)
axs[2].set_title('Aceleração - Eixo Z')
axs[2].set_xlabel('Tempo (s)')
axs[2].set_ylabel('Aceleração (m/s²)')
axs[2].grid(True)

# Ajuste para não sobrepor os subgráficos
plt.tight_layout()

# Exibe os gráficos
plt.show()

# Criação do gráfico com velocidade angular nos três eixos
fig, axs = plt.subplots(3, 1, figsize=(10, 8))

# Plot da velocidade angular no eixo X
axs[0].plot(tempo, GX)
axs[0].set_title('Velocidade Angular - Eixo X')
axs[0].set_xlabel('Tempo (s)')
axs[0].set_ylabel('Velocidade Angular (°/s)')
axs[0].grid(True)

# Plot da velocidade angular no eixo Y
axs[1].plot(tempo, GY)
axs[1].set_title('Velocidade Angular - Eixo Y')
axs[1].set_xlabel('Tempo (s)')
axs[1].set_ylabel('Velocidade Angular (°/s)')
axs[1].grid(True)

# Plot da velocidade angular no eixo Z
axs[2].plot(tempo, GZ)
axs[2].set_title('Velocidade Angular - Eixo Z')
axs[2].set_xlabel('Tempo (s)')
axs[2].set_ylabel('Velocidade Angular (°/s)')
axs[2].grid(True)

# Ajuste para não sobrepor os subgráficos
plt.tight_layout()

# Exibe os gráficos
plt.show()

#
#
#
# Calculo da integral simples da velcidade angular em cada eixo
#
#
#

# Calcula a integral da velocidade angular para obter o ângulo

Ang_GX = np.cumsum(GX * Mdiferenca)  
Ang_GY = np.cumsum(GY * Mdiferenca)  
Ang_GZ = np.cumsum(GZ * Mdiferenca)

# Criação dos gráficos para deslocamento angular nos três eixos
fig, axs = plt.subplots(3, 1, figsize=(10, 8))

# Plot do deslocamento angular no eixo X
axs[0].plot(tempo, Ang_GX)
axs[0].set_title('Deslocamento Angular - Eixo X')
axs[0].set_xlabel('Tempo (s)')
axs[0].set_ylabel('Deslocamento Angular (° ou rad)')
axs[0].grid(True)

# Plot do deslocamento angular no eixo Y
axs[1].plot(tempo, Ang_GY)
axs[1].set_title('Deslocamento Angular - Eixo Y')
axs[1].set_xlabel('Tempo (s)')
axs[1].set_ylabel('Deslocamento Angular (° ou rad)')
axs[1].grid(True)

# Plot do deslocamento angular no eixo Z
axs[2].plot(tempo, Ang_GZ)
axs[2].set_title('Deslocamento Angular - Eixo Z')
axs[2].set_xlabel('Tempo (s)')
axs[2].set_ylabel('Deslocamento Angular (° ou rad)')
axs[2].grid(True)

# Ajuste para não sobrepor os subgráficos
plt.tight_layout()

# Exibe os gráficos
plt.show()

#
#
#
# Correção da orientação do giroscópio
#
#
#


# Calculando os ângulos de pitch e roll

pitch = np.arctan2 (AY, np.sqrt(AX**2 + AZ**2))  # Inclinação no eixo X
roll  = np.arctan2(-AX, np.sqrt(AY**2 + AZ**2))  # Inclinação no eixo Y

# Inicializando os ângulos corrigidos
alpha = 0.98  # Peso do giroscópio e do acelerômetro (filtro complementar)

angle_pitch_hist = np.zeros(len(tempo))
angle_roll_hist = np.zeros(len(tempo))

angle_pitch_hist[0] = pitch[0]
angle_roll_hist[0] = roll[0]

for i in range(1, len(tempo)):
    angle_pitch_hist[i] = alpha * (angle_pitch_hist[i - 1] + GY[i] * Mdiferenca) + (1 - alpha) * pitch[i]
    angle_roll_hist[i]  = alpha * (angle_roll_hist[i - 1]  + GX[i] * Mdiferenca) + (1 - alpha) * roll[i]



# Inicialização do estado
theta_kalman = 0  # Estimativa inicial do ângulo Yaw
bias_kalman = 0  # Viés estimado do giroscópio

# Incertezas (ajustáveis)
P = np.array([[1, 0], [0, 1]])  # Matriz de covariância
Q = np.array([[0.001, 0], [0, 0.003]])  # Ruído do modelo
R = 0.03  # Ruído da medição

# Vetores para armazenar os valores corrigidos
theta_kalman_hist = []

for i in range(len(tempo)):
    dt = Mdiferenca

    # Predição
    theta_kalman += (GZ[i] - bias_kalman) * dt
    P = P + Q

    # Medição simulada
    yaw_measurement = theta_kalman  

    # Cálculo do ganho de Kalman
    K = P[:, 0] / (P[0, 0] + R)

    # Atualização do estado corrigido
    theta_kalman += K[0] * (yaw_measurement - theta_kalman)
    bias_kalman   += K[1] * (0 - bias_kalman)  # Melhor correção do viés

    # Atualização da matriz de covariância
    P = (np.eye(2) - np.outer(K, [1, 0])) @ P

    theta_kalman_hist.append(theta_kalman)


# Plot do deslocamento angular corrigido
plt.plot(tempo, theta_kalman_hist, label="Yaw Corrigido (Filtro de Kalman)")
plt.plot(tempo, angle_pitch, label="Pitch Corrigido")
plt.plot(tempo, angle_roll, label="Roll Corrigido")
plt.xlabel("Tempo (s)")
plt.ylabel("Ângulo (°)")
plt.legend()
plt.grid()
plt.show()

ANG_GX_CORRIGIDO = angle_pitch
ANG_GY_CORRIGIDO = angle_roll
ANG_GZ_CORRIGIDO = theta_kalman_hist

#
#
#
# Análise da rotação da terra
#
#
#

rotacao_terra = 7.2921159e-5  * 180 / np.pi  # Velocidade angular da Terra (°/s)

Deslocamento_calculado = rotacao_terra * tempo[-1]  # Deslocamento esperado pela rotação da Terra

Deslocamento_esperado = 15 * (tempo / (3600))  # 15°/h convertido para segundos

print(f"Deslocamento esperado: {Deslocamento_calculado:.2f} ° ")            # Calcula o deslocamento esperado

print(f"Deslocamento real: {ANG_GZ_CORRIGIDO[-1]:.2f} ° ")                  # Calcula o deslocamento real

print(f"Erro: {ANG_GZ_CORRIGIDO[-1] - Deslocamento_calculado:.2f} ° ")      # Calcula o erro

# Criação do gráfico para o deslocamento angular no eixo Z
plt.figure(figsize=(10, 6))
plt.plot(tempo, ANG_GZ_CORRIGIDO,      color="k",   label='Deslocamento Real corrigido')
plt.plot(tempo, ANG_GZ,                color="b",   label='Deslocamento Real')
plt.plot(tempo, Deslocamento_esperado, color="r",   label='Deslocamento Esperado')
plt.title('Deslocamento Angular - Eixo Z')
plt.xlabel('Tempo (s)')
plt.ylabel('Deslocamento Angular (°)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

