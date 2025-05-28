document.addEventListener('DOMContentLoaded', function () {
    // Elementos de notificação para veículos
    const robotContainer = document.getElementById("robot-notification-container");
    const robotNotification = document.getElementById("robot-notification");
    const robotArm = document.getElementById("robot-arm");
    const robotMessage = document.getElementById("robot-message");

    // Sistema de fila para notificações de veículos
    let messageQueue = [];
    let isShowingMessage = false;
    let vehicleNotifications = JSON.parse(localStorage.getItem('vehicle_notifications') || '[]');
    
    // Adiciona mensagem à fila
    function queueMessage(msg, type) {
        messageQueue.push({msg, type});
        console.log('Mensagem adicionada à fila:', messageQueue);
        processMessageQueue();
    }

    // Processa a fila de mensagens
    function processMessageQueue() {
        if (isShowingMessage || messageQueue.length === 0) return;
        
        isShowingMessage = true;
        const { msg, type } = messageQueue.shift();

        robotContainer.classList.add("active");
        robotArm.classList.add("active");
        robotNotification.classList.add("visible");

        robotMessage.innerHTML = `${type === "success" ? "✅" : "❌"} ${msg}`;
        robotMessage.className = `robot-message ${type}`;

        setTimeout(() => {
            robotNotification.classList.remove("visible");
            robotArm.classList.remove("active");
            robotContainer.classList.remove("active");

            setTimeout(() => {
                isShowingMessage = false;
                processMessageQueue(); // Chama a próxima mensagem na fila
            }, 500);
        }, 2500);
    }

    // Manipulador de eventos para botões de exclusão
    document.querySelectorAll('.btn-delete').forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const vehicleId = this.getAttribute('data-id');

            if (confirm("Tem certeza que deseja excluir este veículo?")) {
                fetch(`/vehicles/delete/${vehicleId}/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken"),
                        "Accept": "application/json"
                    }
                })
                .then(res => res.json())
                .then(data => {
                    console.log('Resposta do servidor:', data);
                    queueMessage(data.message, data.status === "success" ? "success" : "error");
                    if (data.status === "success") {
                        this.closest("tr").remove();
                    }
                })
                .catch(error => {
                    console.error('Erro na requisição:', error);
                    queueMessage("Erro ao processar a requisição", "error");
                });
            }
        });
    });

    // Conexão WebSocket para notificações de veículos
    function connectVehicleSocket() {
        const vehicleSocket = new WebSocket(
            (window.location.protocol === "https:" ? "wss://" : "ws://") + 
            window.location.host + 
            '/ws/vehicle_notifications/'
        );

        vehicleSocket.onopen = function () {
            console.log("WebSocket de veículos conectado");
        };

        vehicleSocket.onmessage = function (e) {
            try {
                const data = JSON.parse(e.data);
                if (data.type === 'vehicle') {
                    vehicleNotifications = vehicleNotifications.concat(data.notifications);
                    localStorage.setItem('vehicle_notifications', JSON.stringify(vehicleNotifications));
                    updateVehicleNotifications();
                }
            } catch (err) {
                console.error("Erro ao processar mensagem de veículo:", err);
            }
        };

        vehicleSocket.onclose = function () {
            console.warn('WebSocket de veículos fechado, tentando reconectar em 5s...');
            setTimeout(() => {
                connectVehicleSocket();
            }, 5000);
        };

        vehicleSocket.onerror = function (e) {
            console.error('Erro no WebSocket de veículos:', e);
        };
    }

    // Atualiza notificações de veículos na interface
    function updateVehicleNotifications() {
        if (vehicleNotifications.length === 0) return;
        
        // Aqui você pode implementar a lógica para exibir notificações de veículos
        // similar ao que foi feito para produtos
        vehicleNotifications.forEach(notif => {
            queueMessage(`Veículo ${notif.message.vehicle_name} precisa de manutenção`, "warning");
        });
    }

    // Função auxiliar para obter cookies (para CSRF)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Inicializa a conexão WebSocket para veículos
    try {
        connectVehicleSocket();
        updateVehicleNotifications();
    } catch (e) {
        console.error("Erro ao inicializar WebSocket de veículos:", e);
    }
});