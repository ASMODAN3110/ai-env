import unittest
from utilities.system_monitor import get_system_performance, pynvml


class TestSystemMonitor(unittest.TestCase):
    """Tests pour la fonction get_system_performance."""

    def test_cpu_percent(self) -> None:
        """Vérifie que l'utilisation du CPU est un pourcentage valide."""
        perf = get_system_performance()
        self.assertIn("cpu_percent", perf, "La clé 'cpu_percent' est absente")
        self.assertIsInstance(perf["cpu_percent"], float, "cpu_percent n'est pas un float")
        self.assertTrue(0 <= perf["cpu_percent"] <= 100, "cpu_percent hors des limites [0, 100]")

    def test_ram_percent(self) -> None:
        """Vérifie que l'utilisation de la RAM est un pourcentage valide."""
        perf = get_system_performance()
        self.assertIn("ram_percent", perf, "La clé 'ram_percent' est absente")
        self.assertIsInstance(perf["ram_percent"], float, "ram_percent n'est pas un float")
        self.assertTrue(0 <= perf["ram_percent"] <= 100, "ram_percent hors des limites [0, 100]")

    def test_gpu_with_pynvml(self) -> None:
        """Vérifie les métriques GPU si pynvml est installé et un GPU est disponible."""
        if pynvml is None:
            self.skipTest("pynvml n'est pas installé, test ignoré")

        perf = get_system_performance()
        self.assertIn("gpu_percent", perf, "La clé 'gpu_percent' est absente")
        self.assertIn("gpu_memory_percent", perf, "La clé 'gpu_memory_percent' est absente")

        try:
            pynvml.nvmlInit()
            device_count = pynvml.nvmlDeviceGetCount()
            pynvml.nvmlShutdown()
            if device_count > 0:
                self.assertIsInstance(perf["gpu_percent"], float, "gpu_percent n'est pas un float")
                self.assertIsInstance(perf["gpu_memory_percent"], float, "gpu_memory_percent n'est pas un float")
                self.assertTrue(0 <= perf["gpu_percent"] <= 100, "gpu_percent hors des limites [0, 100]")
                self.assertTrue(0 <= perf["gpu_memory_percent"] <= 100, "gpu_memory_percent hors des limites [0, 100]")
            else:
                self.assertIsNone(perf["gpu_percent"], "gpu_percent devrait être None sans GPU")
                self.assertIsNone(perf["gpu_memory_percent"], "gpu_memory_percent devrait être None sans GPU")
        except pynvml.NVMLError:
            self.assertIsNone(perf["gpu_percent"], "gpu_percent devrait être None en cas d'erreur")
            self.assertIsNone(perf["gpu_memory_percent"], "gpu_memory_percent devrait être None en cas d'erreur")


if __name__ == "__main__":
    unittest.main()