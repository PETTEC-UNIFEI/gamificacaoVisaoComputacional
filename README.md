# Touchless Quiz

Quiz interativo controlado pela câmera: em vez de usar mouse ou teclado, você
seleciona as respostas apontando o **dedo indicador** para o botão desejado e
esperando alguns segundos sobre ele. A detecção da mão é feita com o
MediaPipe HandLandmarker e a interface é renderizada com Pygame sobre o feed
da webcam (desfocado, como fundo).

## Como funciona

1. A webcam captura o vídeo continuamente (`vision/hand_tracking.py`).
2. O MediaPipe detecta a mão e extrai a posição da ponta do dedo indicador
   (landmark 8).
3. Essa posição é usada como um "cursor" na tela (`main.py`).
4. Ao manter o dedo sobre um botão por `TEMPO_SELECAO` segundos, a opção é
   selecionada (`ui/menu.py`, `ui/quiz.py`).
5. No quiz, cada resposta certa soma 1 ponto ao placar (`data/questions.py`
   tem as perguntas e respostas).

## Requisitos

- Python 3.10/3.11 recomendado (o `mediapipe` pode não ter build disponível
  para versões mais novas do Python).
- Uma webcam funcional.
- Pacotes Python: `pygame`, `opencv-python`, `mediapipe`, `numpy`.

## Instalação

```powershell
# na raiz do projeto
cd C:\gamificacaoVisaoComputacional-main

# ative o ambiente virtual (já existe uma venv pronta na pasta .venv)
.\.venv\Scripts\Activate.ps1

# instale as dependências (garante que vai para o Python da venv ativa)
python -m pip install pygame opencv-python mediapipe numpy
```

## Como rodar

Com a venv ativa e as dependências instaladas:

```powershell
python main.py
```

Isso abre a janela **"Touchless Quiz"**. No menu, aponte o dedo para
**Iniciar** e aguarde a barra de progresso preencher para começar o quiz.
Para sair, aponte para **Sair** ou feche a janela.

## Configuração (`config.py`)

| Variável        | Descrição                                                      | Valor atual |
|-----------------|------------------------------------------------------------------|-------------|
| `WIDTH`         | Largura da janela do jogo (px)                                  | `1280`      |
| `HEIGHT`        | Altura da janela do jogo (px)                                    | `720`       |
| `TEMPO_SELECAO` | Tempo (segundos) que o dedo precisa ficar sobre um botão para selecioná-lo | `3.0`       |
| `MODEL_PATH`    | Caminho do modelo do MediaPipe (`assets/hand_landmarker.task`)   | —           |

Esses valores foram ajustados a partir do padrão original do projeto
(`800x600` / `1.0s`) para deixar a janela maior e dar mais tempo para
confirmar a seleção com o dedo, já que 1 segundo estava muito rápido para
selecionar com precisão.

Como o layout das telas (`ui/menu.py`, `ui/quiz.py`) foi desenhado
originalmente para 800x600, os botões, textos e a logo agora são
reposicionados **proporcionalmente** com base em `WIDTH`/`HEIGHT`
(`SCALE_X = WIDTH / 800`, `SCALE_Y = HEIGHT / 600`). Isso significa que dá
para mudar `WIDTH`/`HEIGHT` em `config.py` para qualquer outra resolução que
o layout se ajusta automaticamente, sem precisar editar as posições dos
botões manualmente.

## Estrutura do projeto

```
main.py                 # loop principal do jogo (Pygame)
config.py               # configurações globais (resolução, tempo de seleção)
vision/hand_tracking.py # captura da webcam + detecção da mão (MediaPipe)
ui/menu.py               # tela de menu (Iniciar / Score / Sair)
ui/quiz.py               # tela do quiz (perguntas, alternativas, placar)
ui/button.py              # desenho de botões com barra de progresso do hover
data/questions.py        # banco de perguntas e respostas do quiz
assets/                  # modelo do MediaPipe e logo
```

## Solução de problemas

- **`ModuleNotFoundError: No module named 'pygame'`** — as dependências não
  foram instaladas no Python que a venv está expondo. Rode
  `python -m pip install pygame opencv-python mediapipe numpy` com a venv
  ativa (o `(.venv)` deve aparecer no prompt).
- **A câmera não abre / tela preta** — verifique se nenhum outro programa
  está usando a webcam e se o Windows deu permissão de câmera para o
  terminal/Python.
- **O dedo não é detectado** — garanta boa iluminação e que a mão esteja
  visível por inteiro no quadro da câmera.
