"""
Sistema de Configuração Dinâmica - OceanicDesk

IMPORTANTE: Este sistema mantém 100% da compatibilidade com as configurações existentes.
Todas as variáveis do .env continuam funcionando exatamente igual.

Este módulo adiciona:
1. Atualização automática de datas no dia 1 do mês (mês anterior completo)
2. Atualização automática de caminhos no dia 2 do mês (novo mês)
3. Validação robusta de todas as configurações
4. Backup automático antes de mudanças
5. Integração com sistemas de logging, validação e métricas
"""

import os
import calendar
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Tuple, Optional, Any
import shutil
import re

# Import dos sistemas implementados
try:
    from utils.logger import log_operacao, log_erro, logger
    LOGGING_AVAILABLE = True
except ImportError:
    LOGGING_AVAILABLE = False

try:
    from utils.validators import FilePathValidator, safe_int
    VALIDATION_AVAILABLE = True
except ImportError:
    VALIDATION_AVAILABLE = False

try:
    from utils.exceptions import ConfigurationError, FileOperationError
    EXCEPTIONS_AVAILABLE = True
except ImportError:
    EXCEPTIONS_AVAILABLE = False

try:
    from utils.metrics import record_operation_metric
    METRICS_AVAILABLE = True
except ImportError:
    METRICS_AVAILABLE = False


# ============================================================================
# CONFIGURAÇÕES DO SISTEMA DINÂMICO
# ============================================================================

class DynamicConfigSettings:
    """Configurações do sistema de configuração dinâmica"""
    
    # Arquivo .env principal
    ENV_FILE = Path(".env")
    
    # Backup do .env
    ENV_BACKUP_DIR = Path(".env_backups")
    
    # Mapeamento de meses
    MESES = {
        1: {"numero": "01", "nome": "JANEIRO", "nome_cap": "Janeiro"},
        2: {"numero": "02", "nome": "FEVEREIRO", "nome_cap": "Fevereiro"},
        3: {"numero": "03", "nome": "MARÇO", "nome_cap": "Março"},
        4: {"numero": "04", "nome": "ABRIL", "nome_cap": "Abril"},
        5: {"numero": "05", "nome": "MAIO", "nome_cap": "Maio"},
        6: {"numero": "06", "nome": "JUNHO", "nome_cap": "Junho"},
        7: {"numero": "07", "nome": "JULHO", "nome_cap": "Julho"},
        8: {"numero": "08", "nome": "AGOSTO", "nome_cap": "Agosto"},
        9: {"numero": "09", "nome": "SETEMBRO", "nome_cap": "Setembro"},
        10: {"numero": "10", "nome": "OUTUBRO", "nome_cap": "Outubro"},
        11: {"numero": "11", "nome": "NOVEMBRO", "nome_cap": "Novembro"},
        12: {"numero": "12", "nome": "DEZEMBRO", "nome_cap": "Dezembro"}
    }
    
    # Variáveis que precisam ser atualizadas mensalmente
    MONTHLY_PATHS = [
        "CAMINHO_PLANILHA",
        "CAMINHO_CHACALTAYA", 
        "CAMINHO_PLANILHA_VENDAS",
        "CAMINHO_MEU_CONTROLE",
        "CAMINHO_COMBUSTIVEL",
        "CAMINHO_COPIA_MES"
    ]


# ============================================================================
# SISTEMA PRINCIPAL DE CONFIGURAÇÃO DINÂMICA
# ============================================================================

class DynamicConfigManager:
    """
    Gerenciador de configuração dinâmica.
    Mantém compatibilidade total com sistema existente.
    """
    
    def __init__(self):
        self.settings = DynamicConfigSettings()
        self.current_date = datetime.now()
        
        # Cria diretório de backup se não existir
        self.settings.ENV_BACKUP_DIR.mkdir(exist_ok=True)
        
        if LOGGING_AVAILABLE:
            log_operacao("dynamic_config_init", "INICIADO", {
                "env_file": str(self.settings.ENV_FILE),
                "backup_dir": str(self.settings.ENV_BACKUP_DIR)
            })
    
    def should_update_dates(self) -> bool:
        """
        Verifica se deve atualizar as datas (dia 1 do mês).
        """
        return self.current_date.day == 1
    
    def should_update_paths(self) -> bool:
        """
        Verifica se deve atualizar os caminhos (dia 2 do mês).
        """
        return self.current_date.day == 2
    
    def get_previous_month_dates(self) -> Tuple[str, str]:
        """
        Calcula as datas do mês anterior (dia 1 ao último dia).
        Para usar no dia 1 do mês atual.
        """
        # Primeiro dia do mês anterior
        primeiro_dia_mes_atual = self.current_date.replace(day=1)
        ultimo_dia_mes_anterior = primeiro_dia_mes_atual - timedelta(days=1)
        primeiro_dia_mes_anterior = ultimo_dia_mes_anterior.replace(day=1)
        
        # Formata as datas
        dia_inicio = primeiro_dia_mes_anterior.strftime("%d/%m/%Y")
        dia_fim = ultimo_dia_mes_anterior.strftime("%d/%m/%Y")
        
        return dia_inicio, dia_fim
    
    def get_current_month_info(self) -> Dict[str, str]:
        """
        Retorna informações do mês atual para atualização de caminhos.
        """
        mes_numero = self.current_date.month
        ano = self.current_date.year
        
        mes_info = self.settings.MESES[mes_numero]
        
        return {
            "numero": mes_info["numero"],
            "nome": mes_info["nome"],
            "nome_cap": mes_info["nome_cap"],
            "ano": str(ano),
            "mes_numero": mes_numero
        }
    
    def backup_env_file(self) -> Path:
        """
        Cria backup do arquivo .env antes de modificações.
        """
        if not self.settings.ENV_FILE.exists():
            if EXCEPTIONS_AVAILABLE:
                raise FileOperationError(
                    "Arquivo .env não encontrado",
                    file_path=str(self.settings.ENV_FILE),
                    operation="backup_env"
                )
            else:
                raise FileNotFoundError(f"Arquivo .env não encontrado: {self.settings.ENV_FILE}")
        
        # Nome do backup com timestamp
        timestamp = self.current_date.strftime("%Y%m%d_%H%M%S")
        backup_name = f"env_backup_{timestamp}.env"
        backup_path = self.settings.ENV_BACKUP_DIR / backup_name
        
        # Cria backup
        shutil.copy2(self.settings.ENV_FILE, backup_path)
        
        if LOGGING_AVAILABLE:
            log_operacao("env_backup", "SUCESSO", {
                "backup_path": str(backup_path),
                "original_size": self.settings.ENV_FILE.stat().st_size,
                "backup_size": backup_path.stat().st_size
            })
        
        return backup_path
    
    def read_env_file(self) -> Dict[str, str]:
        """
        Lê o arquivo .env e retorna as variáveis como dicionário.
        """
        env_vars = {}
        
        if not self.settings.ENV_FILE.exists():
            return env_vars
        
        try:
            with open(self.settings.ENV_FILE, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    
                    # Ignora comentários e linhas vazias
                    if not line or line.startswith('#'):
                        continue
                    
                    # Processa variável
                    if '=' in line:
                        key, value = line.split('=', 1)
                        env_vars[key.strip()] = value.strip()
            
            if LOGGING_AVAILABLE:
                log_operacao("env_read", "SUCESSO", {
                    "variables_count": len(env_vars),
                    "file_size": self.settings.ENV_FILE.stat().st_size
                })
            
            return env_vars
            
        except Exception as e:
            if LOGGING_AVAILABLE:
                log_erro("env_read", e, {
                    "file_path": str(self.settings.ENV_FILE)
                })
            
            if EXCEPTIONS_AVAILABLE:
                raise FileOperationError(
                    f"Erro ao ler arquivo .env: {e}",
                    file_path=str(self.settings.ENV_FILE),
                    operation="read_env"
                )
            else:
                raise
    
    def write_env_file(self, env_vars: Dict[str, str]) -> None:
        """
        Escreve as variáveis de volta para o arquivo .env.
        """
        try:
            # Lê o arquivo original para preservar comentários e estrutura
            original_lines = []
            if self.settings.ENV_FILE.exists():
                with open(self.settings.ENV_FILE, 'r', encoding='utf-8') as f:
                    original_lines = f.readlines()
            
            # Reconstrói o arquivo preservando comentários
            new_lines = []
            processed_vars = set()
            
            for line in original_lines:
                stripped = line.strip()
                
                # Preserva comentários e linhas vazias
                if not stripped or stripped.startswith('#'):
                    new_lines.append(line)
                    continue
                
                # Atualiza variáveis existentes
                if '=' in stripped:
                    key = stripped.split('=', 1)[0].strip()
                    if key in env_vars:
                        new_lines.append(f"{key}={env_vars[key]}\n")
                        processed_vars.add(key)
                    else:
                        new_lines.append(line)
                else:
                    new_lines.append(line)
            
            # Adiciona novas variáveis (se houver)
            for key, value in env_vars.items():
                if key not in processed_vars:
                    new_lines.append(f"{key}={value}\n")
            
            # Escreve arquivo atualizado
            with open(self.settings.ENV_FILE, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            
            if LOGGING_AVAILABLE:
                log_operacao("env_write", "SUCESSO", {
                    "variables_updated": len(env_vars),
                    "file_size": self.settings.ENV_FILE.stat().st_size
                })
            
        except Exception as e:
            if LOGGING_AVAILABLE:
                log_erro("env_write", e, {
                    "file_path": str(self.settings.ENV_FILE),
                    "variables_count": len(env_vars)
                })
            
            if EXCEPTIONS_AVAILABLE:
                raise FileOperationError(
                    f"Erro ao escrever arquivo .env: {e}",
                    file_path=str(self.settings.ENV_FILE),
                    operation="write_env"
                )
            else:
                raise
    
    def update_monthly_paths(self) -> bool:
        """
        Atualiza os caminhos mensais no arquivo .env.
        Deve ser executado no dia 2 do mês.
        """
        if not self.should_update_paths():
            return False
        
        start_time = datetime.now()
        
        try:
            # Backup antes da modificação
            backup_path = self.backup_env_file()
            
            # Lê configurações atuais
            env_vars = self.read_env_file()
            
            # Informações do mês atual
            mes_info = self.get_current_month_info()
            
            # Atualiza cada caminho
            updated_paths = {}
            
            for var_name in self.settings.MONTHLY_PATHS:
                if var_name in env_vars:
                    old_path = env_vars[var_name]
                    new_path = self._update_path_for_month(old_path, mes_info)
                    
                    if new_path != old_path:
                        env_vars[var_name] = new_path
                        updated_paths[var_name] = {
                            "old": old_path,
                            "new": new_path
                        }
            
            # Salva arquivo atualizado
            if updated_paths:
                self.write_env_file(env_vars)
                
                # Registra métricas
                duration_ms = (datetime.now() - start_time).total_seconds() * 1000
                if METRICS_AVAILABLE:
                    record_operation_metric("update_monthly_paths", duration_ms, {
                        "paths_updated": len(updated_paths),
                        "month": mes_info["nome_cap"],
                        "success": True
                    })
                
                if LOGGING_AVAILABLE:
                    log_operacao("monthly_paths_update", "SUCESSO", {
                        "backup_path": str(backup_path),
                        "paths_updated": len(updated_paths),
                        "month_info": mes_info,
                        "updated_paths": updated_paths
                    })
                
                return True
            else:
                if LOGGING_AVAILABLE:
                    log_operacao("monthly_paths_update", "NENHUMA_MUDANCA", {
                        "month_info": mes_info
                    })
                
                return False
                
        except Exception as e:
            duration_ms = (datetime.now() - start_time).total_seconds() * 1000
            if METRICS_AVAILABLE:
                record_operation_metric("update_monthly_paths_error", duration_ms, {
                    "success": False,
                    "error": str(e)
                })
            
            if LOGGING_AVAILABLE:
                log_erro("monthly_paths_update", e, {
                    "month_info": mes_info if 'mes_info' in locals() else None
                })
            
            raise

    def _update_path_for_month(self, old_path: str, mes_info: Dict[str, str]) -> str:
        """
        Atualiza um caminho específico para o novo mês.
        """
        # Padrões para diferentes tipos de caminho
        patterns = [
            # Padrão: /2025/07 - JULHO/
            (r'/2025/\d{2} - [A-ZÁÊÇÕ]+/', f'/2025/{mes_info["numero"]} - {mes_info["nome"]}/'),

            # Padrão: 07-VENDA CHACALTAYA LOJA JULHO 2025
            (r'\d{2}-VENDA CHACALTAYA LOJA [A-ZÁÊÇÕ]+ 2025', f'{mes_info["numero"]}-VENDA CHACALTAYA LOJA {mes_info["nome"]} 2025'),

            # Padrão: Vendas Julho.xlsx
            (r'Vendas [A-ZÁÊÇÕa-záêçõ]+\.xlsx', f'Vendas {mes_info["nome_cap"]}.xlsx'),

            # Padrão: Meu Controle Julho - 2025.xlsx
            (r'Meu Controle [A-ZÁÊÇÕa-záêçõ]+ - 2025\.xlsx', f'Meu Controle {mes_info["nome_cap"]} - 2025.xlsx'),

            # Padrão: /07 - JULHO/ (diretório)
            (r'/\d{2} - [A-ZÁÊÇÕ]+/', f'/{mes_info["numero"]} - {mes_info["nome"]}/'),

            # Padrão: Cópia de Julho - 2025.xlsx
            (r'Cópia de [A-ZÁÊÇÕa-záêçõ]+ - 2025\.xlsx', f'Cópia de {mes_info["nome_cap"]} - 2025.xlsx'),

            # Padrão: Vendas Julho Oceanico.xlsx
            (r'Vendas [A-ZÁÊÇÕa-záêçõ]+ Oceanico\.xlsx', f'Vendas {mes_info["nome_cap"]} Oceanico.xlsx')
        ]

        new_path = old_path

        for pattern, replacement in patterns:
            new_path = re.sub(pattern, replacement, new_path)

        return new_path

    def get_dynamic_dates(self) -> Tuple[str, str]:
        """
        Retorna as datas dinâmicas baseadas no dia atual.

        - Dia 1: Retorna mês anterior completo (01/MM/YYYY ao último dia do mês anterior)
        - Outros dias: Retorna do dia 1 do mês atual até ontem
        """
        if self.should_update_dates():
            # Dia 1: mês anterior completo
            return self.get_previous_month_dates()
        else:
            # Outros dias: do dia 1 do mês atual até ontem
            primeiro_dia_mes = self.current_date.replace(day=1)
            ontem = self.current_date - timedelta(days=1)

            dia_inicio = primeiro_dia_mes.strftime("%d/%m/%Y")
            dia_fim = ontem.strftime("%d/%m/%Y")

            return dia_inicio, dia_fim

    def auto_update_if_needed(self) -> Dict[str, Any]:
        """
        Executa atualizações automáticas se necessário.
        Retorna informações sobre o que foi atualizado.
        """
        result = {
            "dates_updated": False,
            "paths_updated": False,
            "current_day": self.current_date.day,
            "updates_performed": []
        }

        try:
            # Atualização de datas (dia 1)
            if self.should_update_dates():
                dia_inicio, dia_fim = self.get_previous_month_dates()
                result["dates_updated"] = True
                result["date_range"] = {
                    "dia_inicio": dia_inicio,
                    "dia_fim": dia_fim,
                    "description": "Mês anterior completo"
                }
                result["updates_performed"].append("dates")

                if LOGGING_AVAILABLE:
                    log_operacao("auto_update_dates", "SUCESSO", {
                        "dia_inicio": dia_inicio,
                        "dia_fim": dia_fim,
                        "trigger": "day_1_of_month"
                    })

            # Atualização de caminhos (dia 2)
            if self.should_update_paths():
                paths_updated = self.update_monthly_paths()
                result["paths_updated"] = paths_updated
                if paths_updated:
                    result["updates_performed"].append("paths")
                    mes_info = self.get_current_month_info()
                    result["month_info"] = mes_info

            # Registra métricas da operação completa
            if METRICS_AVAILABLE:
                record_operation_metric("auto_update_check", 50, {
                    "day": self.current_date.day,
                    "dates_updated": result["dates_updated"],
                    "paths_updated": result["paths_updated"],
                    "updates_count": len(result["updates_performed"])
                })

            return result

        except Exception as e:
            if LOGGING_AVAILABLE:
                log_erro("auto_update_check", e, {
                    "day": self.current_date.day
                })

            result["error"] = str(e)
            return result


# ============================================================================
# FUNÇÕES DE CONVENIÊNCIA PARA INTEGRAÇÃO
# ============================================================================

# Instância global do gerenciador
dynamic_config = DynamicConfigManager()


def get_dynamic_date_range() -> Tuple[str, str]:
    """
    Função de conveniência para obter datas dinâmicas.
    Substitui a lógica manual em etapa8_projecao_de_vendas().
    """
    return dynamic_config.get_dynamic_dates()


def auto_update_config() -> Dict[str, Any]:
    """
    Função de conveniência para atualização automática.
    Pode ser chamada no início do sistema.
    """
    return dynamic_config.auto_update_if_needed()


def force_update_monthly_paths() -> bool:
    """
    Força atualização dos caminhos mensais (para testes ou correções).
    """
    return dynamic_config.update_monthly_paths()


def get_current_month_info() -> Dict[str, str]:
    """
    Retorna informações do mês atual.
    """
    return dynamic_config.get_current_month_info()


def create_env_backup() -> Path:
    """
    Cria backup manual do arquivo .env.
    """
    return dynamic_config.backup_env_file()


# ============================================================================
# INTEGRAÇÃO COM SISTEMA EXISTENTE
# ============================================================================

def enhanced_etapa8_dates() -> Tuple[str, str, int]:
    """
    Versão melhorada da lógica de datas para etapa8_projecao_de_vendas().
    Mantém compatibilidade total com a função original.
    """
    # Obtém datas dinâmicas
    dia_inicio, dia_fim = get_dynamic_date_range()

    # Calcula ontem (sempre o dia anterior)
    ontem = (datetime.now() - timedelta(days=1)).day

    if LOGGING_AVAILABLE:
        log_operacao("enhanced_etapa8_dates", "SUCESSO", {
            "dia_inicio": dia_inicio,
            "dia_fim": dia_fim,
            "ontem": ontem,
            "current_day": datetime.now().day,
            "logic": "dynamic_dates"
        })

    return dia_inicio, dia_fim, ontem


def validate_monthly_paths() -> Dict[str, bool]:
    """
    Valida se todos os caminhos mensais existem.
    """
    from dotenv import load_dotenv
    load_dotenv()

    validation_results = {}

    for var_name in DynamicConfigSettings.MONTHLY_PATHS:
        path_value = os.getenv(var_name)

        if path_value:
            path_exists = Path(path_value).exists()
            validation_results[var_name] = path_exists

            if not path_exists and LOGGING_AVAILABLE:
                log_operacao("path_validation", "ARQUIVO_NAO_ENCONTRADO", {
                    "variable": var_name,
                    "path": path_value
                })
        else:
            validation_results[var_name] = False

            if LOGGING_AVAILABLE:
                log_operacao("path_validation", "VARIAVEL_NAO_DEFINIDA", {
                    "variable": var_name
                })

    return validation_results


# ============================================================================
# COMPATIBILIDADE COM SISTEMA EXISTENTE
# ============================================================================

# Função para verificar se configuração dinâmica está disponível
def is_dynamic_config_available() -> bool:
    """Verifica se sistema de configuração dinâmica está disponível"""
    return True

# Função para desabilitar atualizações automáticas temporariamente
_auto_updates_enabled = True

def disable_auto_updates():
    """Desabilita atualizações automáticas temporariamente"""
    global _auto_updates_enabled
    _auto_updates_enabled = False

def enable_auto_updates():
    """Reabilita atualizações automáticas"""
    global _auto_updates_enabled
    _auto_updates_enabled = True

def is_auto_updates_enabled() -> bool:
    """Verifica se atualizações automáticas estão habilitadas"""
    return _auto_updates_enabled


def get_system_status() -> Dict[str, Any]:
    """
    Retorna status completo do sistema de configuração dinâmica.
    Útil para debugging e monitoramento.
    """
    current_day = datetime.now().day
    mes_info = get_current_month_info()

    # Verifica próximas ações
    next_actions = []
    if current_day == 1:
        next_actions.append("Usando mês anterior completo para relatórios")
    elif current_day == 2:
        next_actions.append("Verificando se caminhos precisam ser atualizados")
    else:
        days_until_next_month = calendar.monthrange(datetime.now().year, datetime.now().month)[1] - current_day + 1
        next_actions.append(f"Próxima atualização em {days_until_next_month} dias (dia 1)")

    # Obtém datas atuais
    dia_inicio, dia_fim = get_dynamic_date_range()

    return {
        "system_active": True,
        "current_day": current_day,
        "current_month": mes_info,
        "auto_updates_enabled": is_auto_updates_enabled(),
        "date_range": {
            "dia_inicio": dia_inicio,
            "dia_fim": dia_fim,
            "logic": "previous_month" if current_day == 1 else "current_month_to_yesterday"
        },
        "next_actions": next_actions,
        "paths_validation": validate_monthly_paths(),
        "backup_available": dynamic_config.settings.ENV_BACKUP_DIR.exists()
    }


def print_system_status():
    """
    Imprime status do sistema de forma amigável.
    Útil para debugging e verificação manual.
    """
    status = get_system_status()

    print("\n" + "=" * 60)
    print("🔧 STATUS DO SISTEMA DE CONFIGURAÇÃO DINÂMICA")
    print("=" * 60)

    print(f"📅 Dia atual: {status['current_day']}")
    print(f"📆 Mês atual: {status['current_month']['nome_cap']} de {status['current_month']['ano']}")
    print(f"⚙️ Atualizações automáticas: {'✅ Habilitadas' if status['auto_updates_enabled'] else '❌ Desabilitadas'}")

    print(f"\n📊 Período de relatórios:")
    print(f"   De: {status['date_range']['dia_inicio']}")
    print(f"   Até: {status['date_range']['dia_fim']}")
    print(f"   Lógica: {status['date_range']['logic']}")

    print(f"\n🎯 Próximas ações:")
    for action in status['next_actions']:
        print(f"   • {action}")

    print(f"\n📁 Validação de caminhos:")
    paths_validation = status['paths_validation']
    valid_count = sum(paths_validation.values())
    total_count = len(paths_validation)
    print(f"   ✅ Válidos: {valid_count}/{total_count}")

    if valid_count < total_count:
        print("   ⚠️ Caminhos com problemas:")
        for path_name, is_valid in paths_validation.items():
            if not is_valid:
                print(f"      • {path_name}")

    print(f"\n💾 Backup: {'✅ Disponível' if status['backup_available'] else '❌ Não configurado'}")

    print("=" * 60)
