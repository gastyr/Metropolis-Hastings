import random
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import numpy as np

def uniform01():
    return random.uniform(0, 1)
    

def function(x):
    y = [125, 18, 20, 34]
    return ((2 + x) ** y[0]) * ((1 - x) ** (y[1] + y[2])) * (x ** y[3])

def min(a, b):
    if a >= b:
        return b
    else:
        return a

def media(a):
    soma = 0
    for i in a:
        soma = soma + i
    tamanho = len(a)
    return soma / tamanho

class Amostras(object):
    def __init__(self, N, start):
        self.aceitos = [0] * N
        self.rejeitados = [0] * N
        self.todos = [0] * N

        self.aceitos[0] = self.rejeitados[0] = self.todos[0] = start
        

N = 2000
start = 0.5
aceitos, rejeitados = 1, 0
candidatos = Amostras(N, start)

print('Iniciando a simulacao MCMC\n...\n')
for i in range(1, N):
    x = uniform01()
    candidatos.todos[i] = x
    razao = function(x) / function(candidatos.aceitos[i-1])
    alpha = min(1, razao)
    if uniform01() < alpha:
        candidatos.aceitos[i] = x
        aceitos += 1
        candidatos.rejeitados[i] = candidatos.rejeitados[i-1]
    else:
        candidatos.aceitos[i] = candidatos.aceitos[i-1]
        candidatos.rejeitados[i] = x
        rejeitados += 1
print('Simulacao MCMC finalizada')

aceitos = (aceitos / N) * 100
rejeitados = (rejeitados / N) * 100

p1 = (media(candidatos.aceitos) / 4) + 0.5
p2 = (1 - media(candidatos.aceitos)) / 4
p3 = p2
p4 = media(candidatos.aceitos) / 4

print(f'Taxa aceita: {aceitos}')
print(f'Taxa rejeitada: {rejeitados}')
print(f'P1: {p1}')
print(f'P2: {p2}')
print(f'P3: {p3}')
print(f'P4: {p4}')


######## Grafico ########

colors = ['#3f3f3f', '#00bfff', '#ff7f00']

fig = make_subplots(
    rows=3, cols=2,
    column_widths=[0.58, 0.42],
    row_heights=[1., 1., 1.],
    specs=[[{"type": "scatter"}, {"type": "xy"}],
           [{"type": "scatter"}, {"type": "xy", "rowspan": 2}],
           [{"type": "scatter"},            None           ]])

fig.add_trace(
    go.Scatter(x = np.arange(1, N+1, 1), 
                y = candidatos.aceitos,
                hoverinfo = 'x+y',
                mode='lines',
                line=dict(color='#3f3f3f',
                width=1),
                showlegend=False,
                ),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(x = np.arange(1, N+1, 1), 
                y = candidatos.rejeitados,
                hoverinfo = 'x+y',
                mode='lines',
                line=dict(color='#00bfff',
                width=1),
                showlegend=False,
                ),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(x = np.arange(1, N+1, 1), 
                y = candidatos.todos,
                hoverinfo = 'x+y',
                mode='lines',
                line=dict(color='#ff7f00',
                width=1),
                showlegend=False,
                ),
    row=3, col=1
)

boxfig= go.Figure(data=[go.Box(x=candidatos.aceitos, showlegend=False, notched=True, marker_color="#3f3f3f", name='aceitos'),
                        go.Box(x=candidatos.rejeitados, showlegend=False, notched=True, marker_color="#00bfff", name='rejeitados'),
                        go.Box(x=candidatos.todos, showlegend=False, notched=True, marker_color="#ff7f00", name='todos')])

for k in range(len(boxfig.data)):
     fig.add_trace(boxfig.data[k], row=1, col=2)

group_labels = ['\u03B8 aceitos', '\u03B8 rejeitados', 'Todos os \u03B8']
hist_data = [candidatos.aceitos, candidatos.rejeitados, candidatos.todos]

distplfig = ff.create_distplot(hist_data, group_labels, colors=colors,
                         bin_size=.1, show_rug=False)

for k in range(len(distplfig.data)):
    fig.add_trace(distplfig.data[k],
    row=2, col=2
)
fig.update_layout(barmode='overlay', template='none')
fig.show()