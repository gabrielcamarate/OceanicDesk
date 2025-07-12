# Sistema de Alertas Visuais - OceanicDesk

## 📋 Visão Geral

O sistema de alertas visuais do OceanicDesk fornece feedback visual em tempo real para todas as operações do sistema, melhorando a transparência e usabilidade da aplicação.

## 🎯 Características Principais

### ✨ Design Moderno
- **Tema Dark**: Interface escura e elegante
- **Fade In/Out**: Animações suaves de entrada e saída
- **Opacidade Reduzida**: 92% de opacidade para não ser intrusivo
- **Sempre no Topo**: Alertas sempre visíveis sobre outras janelas

### 📍 Posicionamento
- **Canto Inferior Direito**: Posicionamento padrão
- **Empilhamento Inteligente**: Múltiplos alertas se organizam verticalmente
- **Posição Customizável**: Suporte a posicionamento específico

### 🔄 Controle de Threads
- **Thread-Safe**: Sistema seguro para múltiplas threads
- **Limite de Alertas**: Máximo de 3 alertas simultâneos
- **Controle de Concorrência**: Lock para evitar conflitos

## 🎨 Tipos de Alerta

### 1. **Success** (Sucesso)
- **Cor**: Verde (#1e2b1e)
- **Ícone**: ✔
- **Uso**: Operações concluídas com sucesso

### 2. **Error** (Erro)
- **Cor**: Vermelho (#2b1e1e)
- **Ícone**: ⚠
- **Uso**: Falhas e erros críticos

### 3. **Info** (Informação)
- **Cor**: Azul (#1e2230)
- **Ícone**: ℹ
- **Uso**: Informações gerais e status

### 4. **Warning** (Aviso)
- **Cor**: Amarelo (#2b2b1e)
- **Ícone**: ⚠
- **Uso**: Avisos e alertas importantes

### 5. **Dev** (Desenvolvedor)
- **Cor**: Roxo (#23232b)
- **Ícone**: ⚙
- **Uso**: Logs técnicos e debug

### 6. **Progress** (Progresso)
- **Cor**: Ciano (#1e2b2b)
- **Ícone**: ↻
- **Uso**: Operações em andamento com barra de progresso

## 🛠️ API de Uso

### Função Principal
```python
from interfaces.alerta_visual import mostrar_alerta_visual

mostrar_alerta_visual(
    titulo="Título do Alerta",
    descricao="Descrição detalhada",
    tipo="info",           # success, error, info, warning, dev, progress
    tempo=3000,           # Tempo de exibição em ms
    opacidade=0.92,       # Opacidade (0.0 a 1.0)
    posicao=None          # Posição específica (x, y) ou None para automático
)
```

### Função de Progresso
```python
from interfaces.alerta_visual import mostrar_alerta_progresso

mostrar_alerta_progresso(
    titulo="Processando...",
    descricao="Etapa 1 de 5",
    progresso=20          # Percentual (0-100)
)
```

### Funções de Progresso Dinâmico
```python
from interfaces.alerta_visual import atualizar_progresso, fechar_progresso

# Atualiza progresso existente ou cria novo
atualizar_progresso("Título", "Descrição", 50)

# Fecha alerta de progresso ativo
fechar_progresso()
```

## 📍 Posicionamento

### Automático (Padrão)
```python
# Posiciona no canto inferior direito
mostrar_alerta_visual("Título", "Descrição")
```

### Específico
```python
# Posição customizada
mostrar_alerta_visual("Título", "Descrição", posicao=(100, 100))
```

## 🔧 Configurações

### Variáveis Globais
```python
max_alerts = 3           # Máximo de alertas simultâneos
alert_positions = []     # Controle de posições
active_alerts = 0        # Contador de alertas ativos
alert_lock = threading.Lock()  # Lock thread-safe
```

### Cores e Estilos
```python
COLORS = {
    'success': '#1e2b1e',
    'error': '#2b1e1e',
    'info': '#1e2230',
    'dev': '#23232b',
    'warning': '#2b2b1e',
    'progress': '#1e2b2b',
}

BORDER_COLORS = {
    'success': '#4ade80',
    'error': '#f87171',
    'info': '#60a5fa',
    'dev': '#a78bfa',
    'warning': '#fbbf24',
    'progress': '#06b6d4',
}
```

## 🐛 Problemas Conhecidos

### 1. **Sobreposição Visual** ✅ RESOLVIDO
- **Descrição**: Alertas de sucesso podem sobrepor alertas de erro
- **Cenário**: Múltiplos alertas simultâneos (ex: COM errors)
- **Status**: Corrigido com sistema de progresso dinâmico

### 2. **Janela Oculta** ✅ RESOLVIDO
- **Descrição**: Janela principal fica oculta para não interferir
- **Solução**: Implementada com `root.withdraw()`
- **Status**: Resolvido

### 3. **Threads Excessivas** ✅ RESOLVIDO
- **Descrição**: Exceções de threads no terminal
- **Solução**: Sistema thread-safe implementado
- **Status**: Resolvido

## 🧪 Testes

### Executar Testes
```bash
python tests/test_alerta_visual.py
python tests/test_progresso_dinamico.py
```

### Testes Disponíveis
1. **Alertas Básicos**: Todos os tipos de alerta
2. **Alertas Simultâneos**: Simula bug do COM
3. **Alertas de Progresso**: Barra de progresso
4. **Alertas Rápidos**: Teste de sobrecarga
5. **Posicionamento**: Teste de posições
6. **Threads**: Teste de concorrência
7. **Bug Sobreposição**: Simulação do bug visual
8. **Progresso Dinâmico**: Teste de atualização em tempo real

## 📋 Integração no Projeto

### Arquivos Principais
- `interfaces/alerta_visual.py`: Módulo principal (movido de utils/)
- `run.py`: Inicialização e janela oculta
- `controllers/app_controller.py`: Alertas nas etapas
- `utils/etapas.py`: Alertas detalhados

### Padrões de Uso
```python
# Início de operação
mostrar_alerta_visual("Iniciando", "Operação em andamento...", tipo="info")

# Progresso dinâmico (recomendado para operações longas)
atualizar_progresso("Processando", "Etapa intermediária...", 50)

# Sucesso
mostrar_alerta_visual("Concluído", "Operação finalizada!", tipo="success")

# Erro
mostrar_alerta_visual("Erro", "Falha na operação", tipo="error")

# Log técnico
mostrar_alerta_visual("Debug", "Variável X = 42", tipo="dev")
```

## 🔄 Histórico de Versões

### v1.4.7 (Atual)
- ✅ Sistema de progresso dinâmico implementado
- ✅ Bug de sobreposição corrigido
- ✅ Movido para `interfaces/` para melhor modularização
- ✅ Funções `atualizar_progresso()` e `fechar_progresso()`
- ✅ Testes avançados de progresso dinâmico

### v1.4.6
- ✅ Posicionamento no canto inferior direito
- ✅ Sistema thread-safe
- ✅ Controle de alertas simultâneos
- ✅ Janela principal oculta
- ✅ Otimização de performance

### v1.4.5
- ✅ Sistema de alertas implementado
- ✅ Múltiplos tipos de alerta
- ✅ Integração completa no projeto

## 🎯 Melhorias Futuras

### Planejadas
- [ ] Som de notificação
- [ ] Animações mais suaves
- [ ] Alertas persistentes (não desaparecem)
- [ ] Sistema de prioridade de alertas

### Sugestões
- [ ] Alertas agrupados por categoria
- [ ] Histórico de alertas
- [ ] Configuração de cores personalizadas
- [ ] Alertas em modo noturno/diurno

## 📞 Suporte

Para dúvidas ou problemas com o sistema de alertas:
1. Verifique os logs em `logs/`
2. Execute os testes: `python tests/test_alerta_visual.py`
3. Consulte esta documentação
4. Reporte bugs com detalhes do cenário

---

**Desenvolvido para OceanicDesk v1.4.7**
*Sistema de alertas visuais moderno e responsivo* 