import pandas  as pd  #Análise dos dados
import tkinter as tk  #Interface Gráfica
import numpy   as np  #Calculos 
import os             # Para manipulação de caminhos
import matplotlib.pyplot as plt   # Plota os gráficos
import datetime  # Para manipulação de datas e tempos


from tkinter import filedialog            # Busca arquivos
from scipy.interpolate import interp1d    # Calculo de interpolação
from scipy.fftpack import fft, fftfreq

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
    
    dados = pd.read_csv(caminho_arquivo, delimiter=",", header=None) # Separa o arquivo em duas colunas usando o ";"
    ANO     = dados[0]    # Primeira coluna
    MES     = dados[1]    # Segunda coluna
    DIA     = dados[2]    # Terceira coluna
    HORA    = dados[3]    # Quarta coluna
    MINUTO  = dados[4]    # Quinta coluna
    SEGUNDO = dados[5]    # Sexta coluna
    AX      = dados[6]    # Setima coluna
    AY      = dados[7]    # Oitava coluna
    AZ      = dados[8]    # Nona coluna
    GX      = dados[9]    # Decima coluna
    GY      = dados[10]   # Decima primeira coluna
    GZ      = dados[11]   # Decima segunda coluna

    return ANO, MES, DIA, HORA, MINUTO, SEGUNDO, AX, AY, AZ, GX, GY, GZ # Retorna primeiro as colunas de tempo depois as de valores 

if __name__ == "__main__":
    print("Selecione o arquivo .txt do arquivo sem o filtro no explorador de arquivos...")
    caminho = selecionar_arquivo() # Define o caminho para o arquivo com base na função anterior
    
    if caminho:
        print(f"Arquivo selecionado: {caminho}") # Imprime o caminho do arquivo
        ANO, MES, DIA, HORA, MINUTO, SEGUNDO, AX, AY, AZ, GX, GY, GZ = carregar_dados(caminho) # Carrega as variaveis 
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

Nome = nome_arquivo.replace(".txt", "") # Tira a extensão do arquivo (.txt) do nome dele
Nome = Nome.replace("_", " ") # Tira o "_" e subtitui por um espaço

ANO     = ANO.values        # Converte pandas.Series para numpy.ndarray
MES     = MES.values        # Converte pandas.Series para numpy.ndarray
DIA     = DIAS.values       # Converte pandas.Series para numpy.ndarray
HORA    = HORA.values       # Converte pandas.Series para numpy.ndarray
MINUTO  = MINUTO.values     # Converte pandas.Series para numpy.ndarray
SEGUNDO = SEGUNDO.values    # Converte pandas.Series para numpy.ndarray
AX      = AX.values    # Converte pandas.Series para numpy.ndarray
AY      = AY.values    # Converte pandas.Series para numpy.ndarray
AZ      = AZ.values    # Converte pandas.Series para numpy.ndarray
GX      = GX.values    # Converte pandas.Series para numpy.ndarray
GY      = GY.values    # Converte pandas.Series para numpy.ndarray
GZ      = GZ.values    # Converte pandas.Series para numpy.ndarray  


# Criar timestamps absolutos
tempo_absoluto = [
    datetime.datetime(ANO[i], MES[i], DIA[i], HORA[i], MINUTO[i], SEGUNDO[i])
    for i in range(len(ANO))
]

# Calcular tempo relativo ao primeiro dado (início da gravação)
tempo_inicio = tempo_absoluto[0]  # Primeiro instante registrado
tempo_relativo = np.array([(t - tempo_inicio).total_seconds() for t in tempo_absoluto])

# Exibir os primeiros valores de tempo relativo
print("Primeiros valores de tempo relativo (s):", tempo_relativo[:10])



plt.figure(figsize=(10,5))
plt.plot(tempo_relativo, AX, label="Aceleração X")
plt.plot(tempo_relativo, AY, label="Aceleração Y")
plt.plot(tempo_relativo, AZ, label="Aceleração Z")
plt.xlabel("Tempo (s)")
plt.ylabel("Aceleração (g)")
plt.legend()
plt.title("Aceleração ao longo do tempo")
plt.grid()
plt.show()

# Calcular a frequência de amostragem
# Taxa de amostragem (estimada pelo tempo médio entre amostras)
delta_t = np.mean(np.diff(tempo_relativo))  # Diferença média entre amostras
fs = 1 / delta_t  # Frequência de amostragem (Hz)

# Aplicar FFT na aceleração X
n = len(AX)  # Número de pontos
fft_AX = fft(AX)  # FFT da aceleração X
freqs = fftfreq(n, d=delta_t)  # Frequências correspondentes

# Plotar FFT
plt.figure(figsize=(10,5))
plt.plot(freqs[:n//2], np.abs(fft_AX[:n//2]))  # Apenas metade positiva do espectro
plt.xlabel("Frequência (Hz)")
plt.ylabel("Magnitude")
plt.title("FFT da aceleração X")
plt.grid()
plt.show()
