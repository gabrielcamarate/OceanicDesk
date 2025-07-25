"""
Sistema de Métricas de Performance - OceanicDesk

IMPORTANTE: Este sistema mantém 100% da compatibilidade com as operações existentes.
Todas as funções e operações continuam funcionando exatamente igual.

Este módulo adiciona:
1. Coleta automática de métricas de performance sem impactar o sistema
2. Análise de gargalos e operações lentas
3. Relatórios de performance para otimização
4. Monitoramento de recursos do sistema
5. Integração com sistemas de logging e cache
"""

import time
import threading

# Import opcional do psutil
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable, Union
from datetime import datetime, timedelta
from functools import wraps
from collections import defaultdict, deque
import json
import statistics

# Import do sistema de logging (se disponível)
try:
    from utils.logger import log_operacao, log_performance, logger
    LOGGING_AVAILABLE = True
except ImportError:
    LOGGING_AVAILABLE = False

# Import do sistema de cache (se disponível)
try:
    from utils.cache import excel_cache
    CACHE_AVAILABLE = True
except ImportError:
    CACHE_AVAILABLE = False

# ============================================================================
# CONFIGURAÇÕES DAS MÉTRICAS
# ============================================================================

class MetricsConfig:
    """Configurações do sistema de métricas"""
    
    # Diretório para relatórios de métricas
    METRICS_DIR = Path.home() / ".oceanicdesk_metrics"
    
    # Intervalo de coleta de métricas do sistema (segundos)
    SYSTEM_METRICS_INTERVAL = 30
    
    # Número máximo de métricas em memória
    MAX_METRICS_IN_MEMORY = 1000
    
    # Threshold para operações lentas (ms)
    SLOW_OPERATION_THRESHOLD_MS = 1000
    
    # Threshold para operações muito lentas (ms)
    VERY_SLOW_OPERATION_THRESHOLD_MS = 5000
    
    # Categorias de operações para análise
    OPERATION_CATEGORIES = {
        "excel": ["load_workbook", "read_excel", "save", "write"],
        "cache": ["cache_hit", "cache_miss", "cache_save", "cache_load"],
        "automation": ["autosystem", "emsys", "pyautogui", "ocr"],
        "file": ["file_read", "file_write", "file_copy", "backup"],
        "validation": ["validate", "convert", "check"],
        "system": ["startup", "shutdown", "login", "export"]
    }


# ============================================================================
# COLETOR DE MÉTRICAS PRINCIPAL
# ============================================================================

class PerformanceMetrics:
    """
    Sistema principal de coleta de métricas de performance.
    Mantém compatibilidade total com operações existentes.
    """
    
    def __init__(self, metrics_dir: Optional[Path] = None):
        self.metrics_dir = metrics_dir or MetricsConfig.METRICS_DIR
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
        
        # Armazenamento em memória
        self._operation_metrics = defaultdict(list)
        self._system_metrics = deque(maxlen=MetricsConfig.MAX_METRICS_IN_MEMORY)
        self._slow_operations = deque(maxlen=100)
        
        # Controle de threading
        self._lock = threading.Lock()
        self._collecting = False
        self._collection_thread = None
        
        # Estatísticas agregadas
        self._stats = {
            "total_operations": 0,
            "slow_operations": 0,
            "very_slow_operations": 0,
            "average_duration_ms": 0.0,
            "cache_hit_rate": 0.0
        }
        
        # Log de inicialização
        if LOGGING_AVAILABLE:
            log_operacao("metrics_init", "INICIADO", {
                "metrics_dir": str(self.metrics_dir),
                "collection_interval": MetricsConfig.SYSTEM_METRICS_INTERVAL
            })
    
    def start_collection(self):
        """Inicia coleta automática de métricas do sistema"""
        if self._collecting:
            return
        
        self._collecting = True
        self._collection_thread = threading.Thread(target=self._collect_system_metrics, daemon=True)
        self._collection_thread.start()
        
        if LOGGING_AVAILABLE:
            log_operacao("metrics_collection", "INICIADO", {
                "interval_seconds": MetricsConfig.SYSTEM_METRICS_INTERVAL
            })
    
    def stop_collection(self):
        """Para coleta automática de métricas"""
        self._collecting = False
        if self._collection_thread:
            self._collection_thread.join(timeout=5)
        
        if LOGGING_AVAILABLE:
            log_operacao("metrics_collection", "PARADO", {})
    
    def _collect_system_metrics(self):
        """Coleta métricas do sistema em background"""
        while self._collecting:
            try:
                system_metric = {
                    "timestamp": datetime.now().isoformat()
                }

                # Coleta métricas do sistema se psutil estiver disponível
                if PSUTIL_AVAILABLE:
                    cpu_percent = psutil.cpu_percent(interval=1)
                    memory = psutil.virtual_memory()
                    disk = psutil.disk_usage('/')

                    # Métricas específicas do processo atual
                    process = psutil.Process()
                    process_memory = process.memory_info()

                    system_metric.update({
                        "cpu_percent": cpu_percent,
                        "memory_percent": memory.percent,
                        "memory_available_mb": memory.available / (1024 * 1024),
                        "disk_percent": disk.percent,
                        "process_memory_mb": process_memory.rss / (1024 * 1024),
                        "process_cpu_percent": process.cpu_percent()
                    })
                else:
                    # Métricas básicas sem psutil
                    system_metric.update({
                        "cpu_percent": 0.0,
                        "memory_percent": 0.0,
                        "memory_available_mb": 0.0,
                        "disk_percent": 0.0,
                        "process_memory_mb": 0.0,
                        "process_cpu_percent": 0.0,
                        "psutil_available": False
                    })
                
                # Adiciona métricas de cache se disponível
                if CACHE_AVAILABLE:
                    cache_stats = excel_cache.get_cache_stats()
                    system_metric.update({
                        "cache_files": cache_stats["total_files"],
                        "cache_size_mb": cache_stats["total_size_mb"]
                    })
                
                with self._lock:
                    self._system_metrics.append(system_metric)
                
                # Aguarda próxima coleta
                time.sleep(MetricsConfig.SYSTEM_METRICS_INTERVAL)
                
            except Exception as e:
                if LOGGING_AVAILABLE:
                    logger.warning(f"Erro na coleta de métricas do sistema: {e}")
                time.sleep(MetricsConfig.SYSTEM_METRICS_INTERVAL)
    
    def record_operation(self, operation: str, duration_ms: float, 
                        details: Optional[Dict[str, Any]] = None):
        """
        Registra métrica de uma operação.
        Complementa o sistema de logging existente.
        """
        metric = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "duration_ms": duration_ms,
            "duration_seconds": duration_ms / 1000,
            "details": details or {}
        }
        
        # Categoriza a operação
        category = self._categorize_operation(operation)
        metric["category"] = category
        
        # Marca operações lentas
        if duration_ms >= MetricsConfig.VERY_SLOW_OPERATION_THRESHOLD_MS:
            metric["performance_level"] = "very_slow"
            self._stats["very_slow_operations"] += 1
        elif duration_ms >= MetricsConfig.SLOW_OPERATION_THRESHOLD_MS:
            metric["performance_level"] = "slow"
            self._stats["slow_operations"] += 1
        else:
            metric["performance_level"] = "normal"
        
        with self._lock:
            # Armazena métrica
            self._operation_metrics[operation].append(metric)
            
            # Mantém apenas as últimas métricas para cada operação
            if len(self._operation_metrics[operation]) > 100:
                self._operation_metrics[operation] = self._operation_metrics[operation][-50:]
            
            # Adiciona a operações lentas se necessário
            if metric["performance_level"] in ["slow", "very_slow"]:
                self._slow_operations.append(metric)
            
            # Atualiza estatísticas
            self._update_stats(metric)
        
        # Log estruturado se disponível
        if LOGGING_AVAILABLE:
            log_performance(operation, duration_ms, details)
    
    def _categorize_operation(self, operation: str) -> str:
        """Categoriza uma operação baseada no nome"""
        operation_lower = operation.lower()
        
        for category, keywords in MetricsConfig.OPERATION_CATEGORIES.items():
            if any(keyword in operation_lower for keyword in keywords):
                return category
        
        return "other"
    
    def _update_stats(self, metric: Dict[str, Any]):
        """Atualiza estatísticas agregadas"""
        self._stats["total_operations"] += 1
        
        # Calcula média móvel da duração
        total_ops = self._stats["total_operations"]
        current_avg = self._stats["average_duration_ms"]
        new_duration = metric["duration_ms"]
        
        self._stats["average_duration_ms"] = (
            (current_avg * (total_ops - 1) + new_duration) / total_ops
        )
        
        # Calcula taxa de cache hit se disponível
        if CACHE_AVAILABLE and "cache" in metric["operation"]:
            cache_operations = [m for m in self._operation_metrics.values() 
                              for metric_list in m for m in metric_list 
                              if "cache" in m["operation"]]
            
            if cache_operations:
                cache_hits = len([m for m in cache_operations if "hit" in m["operation"]])
                self._stats["cache_hit_rate"] = cache_hits / len(cache_operations) * 100
    
    def get_operation_stats(self, operation: Optional[str] = None) -> Dict[str, Any]:
        """
        Retorna estatísticas de operações.
        """
        with self._lock:
            if operation:
                # Estatísticas de operação específica
                metrics = self._operation_metrics.get(operation, [])
                if not metrics:
                    return {"operation": operation, "metrics_count": 0}
                
                durations = [m["duration_ms"] for m in metrics]
                
                return {
                    "operation": operation,
                    "metrics_count": len(metrics),
                    "average_duration_ms": statistics.mean(durations),
                    "median_duration_ms": statistics.median(durations),
                    "min_duration_ms": min(durations),
                    "max_duration_ms": max(durations),
                    "std_deviation_ms": statistics.stdev(durations) if len(durations) > 1 else 0,
                    "slow_operations": len([m for m in metrics if m.get("performance_level") == "slow"]),
                    "very_slow_operations": len([m for m in metrics if m.get("performance_level") == "very_slow"]),
                    "category": metrics[0].get("category", "unknown")
                }
            else:
                # Estatísticas gerais
                return self._stats.copy()
    
    def get_slow_operations(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Retorna operações mais lentas"""
        with self._lock:
            slow_ops = list(self._slow_operations)
            slow_ops.sort(key=lambda x: x["duration_ms"], reverse=True)
            return slow_ops[:limit]
    
    def get_system_metrics(self, last_minutes: int = 60) -> List[Dict[str, Any]]:
        """Retorna métricas do sistema dos últimos minutos"""
        cutoff_time = datetime.now() - timedelta(minutes=last_minutes)
        
        with self._lock:
            recent_metrics = []
            for metric in self._system_metrics:
                metric_time = datetime.fromisoformat(metric["timestamp"])
                if metric_time >= cutoff_time:
                    recent_metrics.append(metric)
            
            return recent_metrics
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Retorna resumo completo de performance"""
        with self._lock:
            # Estatísticas por categoria
            category_stats = defaultdict(lambda: {"count": 0, "total_duration": 0, "avg_duration": 0})
            
            for operation_metrics in self._operation_metrics.values():
                for metric in operation_metrics:
                    category = metric.get("category", "other")
                    category_stats[category]["count"] += 1
                    category_stats[category]["total_duration"] += metric["duration_ms"]
            
            # Calcula médias por categoria
            for category, stats in category_stats.items():
                if stats["count"] > 0:
                    stats["avg_duration"] = stats["total_duration"] / stats["count"]
            
            # Operações mais comuns
            operation_counts = defaultdict(int)
            for operation, metrics in self._operation_metrics.items():
                operation_counts[operation] = len(metrics)
            
            most_common = sorted(operation_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            
            return {
                "general_stats": self._stats.copy(),
                "category_stats": dict(category_stats),
                "most_common_operations": most_common,
                "slow_operations_count": len(self._slow_operations),
                "system_metrics_count": len(self._system_metrics),
                "collection_active": self._collecting
            }
    
    def export_metrics_report(self, filename: Optional[str] = None) -> Path:
        """Exporta relatório completo de métricas"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"performance_report_{timestamp}.json"
        
        report_path = self.metrics_dir / filename
        
        # Gera relatório completo
        report = {
            "generated_at": datetime.now().isoformat(),
            "summary": self.get_performance_summary(),
            "slow_operations": self.get_slow_operations(50),
            "system_metrics": self.get_system_metrics(120),  # Últimas 2 horas
            "operation_details": {}
        }
        
        # Adiciona detalhes de operações principais
        with self._lock:
            for operation in list(self._operation_metrics.keys())[:20]:  # Top 20
                report["operation_details"][operation] = self.get_operation_stats(operation)
        
        # Salva relatório
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        if LOGGING_AVAILABLE:
            log_operacao("metrics_export", "SUCESSO", {
                "report_path": str(report_path),
                "report_size_kb": report_path.stat().st_size / 1024
            })
        
        return report_path


# ============================================================================
# INSTÂNCIA GLOBAL DE MÉTRICAS
# ============================================================================

# Instância global para uso em todo o sistema
performance_metrics = PerformanceMetrics()


# ============================================================================
# DECORATORS PARA COLETA AUTOMÁTICA DE MÉTRICAS
# ============================================================================

def measure_performance(operation_name: Optional[str] = None, 
                       category: Optional[str] = None,
                       auto_start_collection: bool = True):
    """
    Decorator para medição automática de performance.
    Mantém compatibilidade total com funções existentes.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Inicia coleta se necessário
            if auto_start_collection and not performance_metrics._collecting:
                performance_metrics.start_collection()
            
            # Nome da operação
            op_name = operation_name or f"{func.__module__}.{func.__name__}"
            
            # Medição de performance
            start_time = time.time()
            
            try:
                # Executa função original
                result = func(*args, **kwargs)
                
                # Calcula duração
                duration_ms = (time.time() - start_time) * 1000
                
                # Registra métrica
                details = {
                    "function": func.__name__,
                    "module": func.__module__,
                    "success": True
                }
                
                if category:
                    details["category"] = category
                
                performance_metrics.record_operation(op_name, duration_ms, details)
                
                return result
                
            except Exception as e:
                # Registra métrica de erro
                duration_ms = (time.time() - start_time) * 1000
                
                details = {
                    "function": func.__name__,
                    "module": func.__module__,
                    "success": False,
                    "error": str(e)
                }
                
                if category:
                    details["category"] = category
                
                performance_metrics.record_operation(f"{op_name}_error", duration_ms, details)
                
                # Re-raise para manter comportamento original
                raise
        
        return wrapper
    return decorator


def measure_excel_operation(operation_type: str = "excel"):
    """
    Decorator específico para operações Excel.
    """
    return measure_performance(category=operation_type, auto_start_collection=True)


def measure_automation_operation(operation_type: str = "automation"):
    """
    Decorator específico para operações de automação.
    """
    return measure_performance(category=operation_type, auto_start_collection=True)


# ============================================================================
# FUNÇÕES DE CONVENIÊNCIA PARA INTEGRAÇÃO
# ============================================================================

def record_operation_metric(operation: str, duration_ms: float,
                           details: Optional[Dict[str, Any]] = None):
    """
    Função de conveniência para registrar métrica de operação.
    Complementa o sistema existente sem substituí-lo.
    """
    performance_metrics.record_operation(operation, duration_ms, details)


def start_metrics_collection():
    """Inicia coleta automática de métricas do sistema"""
    performance_metrics.start_collection()


def stop_metrics_collection():
    """Para coleta automática de métricas"""
    performance_metrics.stop_collection()


def get_performance_stats(operation: Optional[str] = None) -> Dict[str, Any]:
    """Obtém estatísticas de performance"""
    return performance_metrics.get_operation_stats(operation)


def get_slow_operations_report(limit: int = 20) -> List[Dict[str, Any]]:
    """Obtém relatório de operações lentas"""
    return performance_metrics.get_slow_operations(limit)


def export_performance_report(filename: Optional[str] = None) -> Path:
    """Exporta relatório completo de performance"""
    return performance_metrics.export_metrics_report(filename)


# ============================================================================
# WRAPPERS PARA FUNÇÕES EXISTENTES
# ============================================================================

def enhance_with_metrics(original_func: Callable, operation_name: Optional[str] = None):
    """
    Melhora uma função existente com coleta de métricas sem modificá-la.
    Útil para migração gradual.
    """
    op_name = operation_name or f"enhanced_{original_func.__name__}"

    @wraps(original_func)
    def enhanced_wrapper(*args, **kwargs):
        start_time = time.time()

        try:
            # Executa função original
            result = original_func(*args, **kwargs)

            # Registra métrica de sucesso
            duration_ms = (time.time() - start_time) * 1000
            performance_metrics.record_operation(op_name, duration_ms, {
                "function": original_func.__name__,
                "success": True
            })

            return result

        except Exception as e:
            # Registra métrica de erro
            duration_ms = (time.time() - start_time) * 1000
            performance_metrics.record_operation(f"{op_name}_error", duration_ms, {
                "function": original_func.__name__,
                "success": False,
                "error": str(e)
            })

            # Re-raise para manter comportamento original
            raise

    return enhanced_wrapper


# ============================================================================
# SISTEMA DE ALERTAS DE PERFORMANCE
# ============================================================================

class PerformanceAlerts:
    """
    Sistema de alertas para problemas de performance.
    """

    def __init__(self):
        self._alert_thresholds = {
            "slow_operation_rate": 20,  # % de operações lentas
            "very_slow_operation_rate": 5,  # % de operações muito lentas
            "average_duration_threshold": 2000,  # ms
            "memory_usage_threshold": 80,  # %
            "cpu_usage_threshold": 90  # %
        }

        self._alerts_sent = set()

    def check_performance_alerts(self) -> List[Dict[str, Any]]:
        """Verifica e retorna alertas de performance"""
        alerts = []

        # Verifica estatísticas de operações
        stats = performance_metrics.get_performance_summary()
        general_stats = stats["general_stats"]

        # Taxa de operações lentas
        if general_stats["total_operations"] > 0:
            slow_rate = (general_stats["slow_operations"] / general_stats["total_operations"]) * 100
            very_slow_rate = (general_stats["very_slow_operations"] / general_stats["total_operations"]) * 100

            if slow_rate > self._alert_thresholds["slow_operation_rate"]:
                alert_key = f"slow_rate_{slow_rate:.1f}"
                if alert_key not in self._alerts_sent:
                    alerts.append({
                        "type": "slow_operations",
                        "severity": "warning",
                        "message": f"Taxa alta de operações lentas: {slow_rate:.1f}%",
                        "details": {"slow_rate": slow_rate, "threshold": self._alert_thresholds["slow_operation_rate"]}
                    })
                    self._alerts_sent.add(alert_key)

            if very_slow_rate > self._alert_thresholds["very_slow_operation_rate"]:
                alert_key = f"very_slow_rate_{very_slow_rate:.1f}"
                if alert_key not in self._alerts_sent:
                    alerts.append({
                        "type": "very_slow_operations",
                        "severity": "critical",
                        "message": f"Taxa alta de operações muito lentas: {very_slow_rate:.1f}%",
                        "details": {"very_slow_rate": very_slow_rate, "threshold": self._alert_thresholds["very_slow_operation_rate"]}
                    })
                    self._alerts_sent.add(alert_key)

        # Duração média alta
        avg_duration = general_stats["average_duration_ms"]
        if avg_duration > self._alert_thresholds["average_duration_threshold"]:
            alert_key = f"avg_duration_{avg_duration:.0f}"
            if alert_key not in self._alerts_sent:
                alerts.append({
                    "type": "high_average_duration",
                    "severity": "warning",
                    "message": f"Duração média alta: {avg_duration:.0f}ms",
                    "details": {"average_duration": avg_duration, "threshold": self._alert_thresholds["average_duration_threshold"]}
                })
                self._alerts_sent.add(alert_key)

        # Verifica métricas do sistema
        recent_system_metrics = performance_metrics.get_system_metrics(5)  # Últimos 5 minutos
        if recent_system_metrics:
            latest_metric = recent_system_metrics[-1]

            # Uso de memória alto
            if latest_metric["memory_percent"] > self._alert_thresholds["memory_usage_threshold"]:
                alert_key = f"memory_{latest_metric['memory_percent']:.1f}"
                if alert_key not in self._alerts_sent:
                    alerts.append({
                        "type": "high_memory_usage",
                        "severity": "warning",
                        "message": f"Uso alto de memória: {latest_metric['memory_percent']:.1f}%",
                        "details": {"memory_percent": latest_metric["memory_percent"], "threshold": self._alert_thresholds["memory_usage_threshold"]}
                    })
                    self._alerts_sent.add(alert_key)

            # Uso de CPU alto
            if latest_metric["cpu_percent"] > self._alert_thresholds["cpu_usage_threshold"]:
                alert_key = f"cpu_{latest_metric['cpu_percent']:.1f}"
                if alert_key not in self._alerts_sent:
                    alerts.append({
                        "type": "high_cpu_usage",
                        "severity": "critical",
                        "message": f"Uso alto de CPU: {latest_metric['cpu_percent']:.1f}%",
                        "details": {"cpu_percent": latest_metric["cpu_percent"], "threshold": self._alert_thresholds["cpu_usage_threshold"]}
                    })
                    self._alerts_sent.add(alert_key)

        return alerts

    def reset_alerts(self):
        """Reseta alertas enviados"""
        self._alerts_sent.clear()


# Instância global de alertas
performance_alerts = PerformanceAlerts()


# ============================================================================
# FUNÇÕES DE ANÁLISE E RELATÓRIOS
# ============================================================================

def analyze_performance_trends() -> Dict[str, Any]:
    """
    Analisa tendências de performance ao longo do tempo.
    """
    summary = performance_metrics.get_performance_summary()

    # Análise por categoria
    category_analysis = {}
    for category, stats in summary["category_stats"].items():
        if stats["count"] > 0:
            category_analysis[category] = {
                "average_duration_ms": stats["avg_duration"],
                "total_operations": stats["count"],
                "performance_level": "good" if stats["avg_duration"] < 500 else "slow" if stats["avg_duration"] < 2000 else "poor"
            }

    # Operações que precisam de otimização
    slow_operations = performance_metrics.get_slow_operations(10)
    optimization_candidates = []

    for op in slow_operations:
        optimization_candidates.append({
            "operation": op["operation"],
            "duration_ms": op["duration_ms"],
            "category": op.get("category", "unknown"),
            "optimization_priority": "high" if op["duration_ms"] > 5000 else "medium"
        })

    return {
        "category_analysis": category_analysis,
        "optimization_candidates": optimization_candidates,
        "general_health": "good" if summary["general_stats"]["average_duration_ms"] < 1000 else "needs_attention",
        "cache_effectiveness": summary["general_stats"].get("cache_hit_rate", 0),
        "alerts": performance_alerts.check_performance_alerts()
    }


def generate_performance_dashboard() -> Dict[str, Any]:
    """
    Gera dados para dashboard de performance.
    """
    summary = performance_metrics.get_performance_summary()
    trends = analyze_performance_trends()
    system_metrics = performance_metrics.get_system_metrics(30)  # Últimos 30 minutos

    return {
        "timestamp": datetime.now().isoformat(),
        "overview": {
            "total_operations": summary["general_stats"]["total_operations"],
            "average_duration_ms": summary["general_stats"]["average_duration_ms"],
            "slow_operations_rate": (summary["general_stats"]["slow_operations"] / max(summary["general_stats"]["total_operations"], 1)) * 100,
            "cache_hit_rate": summary["general_stats"].get("cache_hit_rate", 0),
            "health_status": trends["general_health"]
        },
        "top_operations": summary["most_common_operations"][:5],
        "slow_operations": performance_metrics.get_slow_operations(5),
        "system_status": system_metrics[-1] if system_metrics else {},
        "alerts": trends["alerts"],
        "optimization_suggestions": trends["optimization_candidates"][:3]
    }


# ============================================================================
# COMPATIBILIDADE COM SISTEMA EXISTENTE
# ============================================================================

# Aliases para manter compatibilidade
measure_operation = measure_performance
get_metrics = get_performance_stats

# Função para verificar se métricas estão disponíveis
def is_metrics_available() -> bool:
    """Verifica se sistema de métricas está disponível"""
    return True

# Função para desabilitar métricas temporariamente
_metrics_enabled = True

def disable_metrics():
    """Desabilita coleta de métricas temporariamente"""
    global _metrics_enabled
    _metrics_enabled = False
    performance_metrics.stop_collection()

def enable_metrics():
    """Reabilita coleta de métricas"""
    global _metrics_enabled
    _metrics_enabled = True
    performance_metrics.start_collection()

def is_metrics_enabled() -> bool:
    """Verifica se coleta de métricas está habilitada"""
    return _metrics_enabled
