import psutil
from typing import Dict, Optional

try:
    import pynvml
except ImportError:
    pynvml = None

def get_system_performance() -> Dict[str, Optional[float]]:
    """Récupère les performances actuelles de l'ordinateur.

    Cette fonction mesure l'utilisation du CPU, de la RAM, et, si disponible,
    du GPU (pour les cartes NVIDIA uniquement). Les valeurs sont exprimées en pourcentage.

    Returns:
        Dict[str, Optional[float]]: Dictionnaire avec les clés suivantes :
            - 'cpu_percent': Pourcentage d'utilisation du CPU.
            - 'ram_percent': Pourcentage d'utilisation de la RAM.
            - 'gpu_percent': Pourcentage d'utilisation du GPU (None si non disponible).
            - 'gpu_memory_percent': Pourcentage de mémoire GPU utilisée (None si non disponible).

    Examples:
        >>> perf = get_system_performance()
        >>> print(perf)
        {'cpu_percent': 45.2, 'ram_percent': 67.8, 'gpu_percent': 30.5, 'gpu_memory_percent': 25.0}
    """
    performance = {"cpu_percent": psutil.cpu_percent(interval=1)}

    # Mesurer l'utilisation du CPU (moyenne sur tous les cœurs)

    # Mesurer l'utilisation de la RAM
    ram = psutil.virtual_memory()
    performance["ram_percent"] = ram.percent

    # Mesurer l'utilisation du GPU (si disponible)
    performance["gpu_percent"] = 0
    performance["gpu_memory_percent"] = 0
    if pynvml is not None:
        try:
            pynvml.nvmlInit()
            device_count = pynvml.nvmlDeviceGetCount()
            if device_count > 0:
                # Prendre le premier GPU (peut être étendu pour plusieurs GPUs)
                handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                # Utilisation du GPU (en pourcentage)
                util = pynvml.nvmlDeviceGetUtilizationRates(handle)
                performance["gpu_percent"] = float(util.gpu)
                # Utilisation de la mémoire GPU
                mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
                performance["gpu_memory_percent"] = (mem_info.used / mem_info.total) * 100
            pynvml.nvmlShutdown()
        except pynvml.NVMLError:
            # Si une erreur survient (par exemple, pas de GPU NVIDIA), laisser None
            pass

    return performance
