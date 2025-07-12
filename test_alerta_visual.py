import time
from utils.alerta_visual import mostrar_alerta_visual

if __name__ == "__main__":
    mostrar_alerta_visual("Sucesso!", "Seu backup foi realizado com sucesso.", tipo="success")
    time.sleep(2)
    mostrar_alerta_visual("Erro!", "Falha ao conectar ao banco de dados.", tipo="error")
    time.sleep(2)
    mostrar_alerta_visual("Informação", "Processando relatório mensal...", tipo="info")
    time.sleep(2)
    mostrar_alerta_visual("Log de desenvolvedor", "Variável X = 42", tipo="dev")
    time.sleep(2)
    mostrar_alerta_visual("Finalizado", "Todos os testes de alerta foram exibidos.", tipo="success")
    time.sleep(3) 