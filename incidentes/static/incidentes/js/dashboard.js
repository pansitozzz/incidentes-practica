document.addEventListener("DOMContentLoaded", function () {
    fetch("/api/datos-dashboard/")
        .then((respuesta) => respuesta.json())
        .then((datos) => {
            const etiquetasPrioridad = Object.keys(datos.por_prioridad);
            const valoresPrioridad = Object.values(datos.por_prioridad);

            new Chart(document.getElementById("graficoPrioridad"), {
                type: "bar",
                data: {
                    labels: etiquetasPrioridad,
                    datasets: [
                        {
                            label: "Incidentes por prioridad",
                            data: valoresPrioridad,
                            backgroundColor: ["#dc2626", "#ea580c", "#ca8a04", "#16a34a"],
                        },
                    ],
                },
                options: { plugins: { legend: { display: false } } },
            });

            const etiquetasEstado = Object.keys(datos.por_estado);
            const valoresEstado = Object.values(datos.por_estado);

            new Chart(document.getElementById("graficoEstado"), {
                type: "doughnut",
                data: {
                    labels: etiquetasEstado,
                    datasets: [
                        {
                            data: valoresEstado,
                            backgroundColor: ["#2563eb", "#f59e0b", "#16a34a", "#6b7280"],
                        },
                    ],
                },
            });

            document.getElementById("valorTiempoPromedio").textContent =
                datos.tiempo_promedio_resolucion_horas;
        })
        .catch((error) => console.error("Error cargando datos del dashboard:", error));
});
