document.addEventListener('DOMContentLoaded', function () {
    // Elementos de notificação
    const robotContainer = document.getElementById("robot-notification-container");
    const robotNotification = document.getElementById("robot-notification");
    const robotArm = document.getElementById("robot-arm");
    const robotMessage = document.getElementById("robot-message");
    
    // Elementos de notificação de estoque baixo
    const notificationContainerStockLow = document.getElementById("notification-container-stock-low");
    const notificationLow = document.getElementById("notification-low");
    const notificationMessageProduct = document.getElementById("notification-message-product");

    // Sistema de fila para notificações
    let messageQueue = [];
    let isShowingMessage = false;
    
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

        // Ativa as notificações do robô
        robotContainer.classList.add("active");
        robotArm.classList.add("active");
        robotNotification.classList.add("visible");

        robotMessage.innerHTML = `${type === "success" ? "✅" : "❌"} ${msg}`;
        robotMessage.className = `robot-message ${type}`;

        // Se for uma notificação de estoque baixo, também mostra no container específico
        if (type === "warning" || msg.includes("estoque baixo")) {
            showStockLowNotification(msg);
        }

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

    // Função específica para mostrar notificações de estoque baixo
    function showStockLowNotification(msg) {
        notificationContainerStockLow.classList.add("active");
        notificationLow.classList.add("visible");
        notificationMessageProduct.classList.add("active");
        notificationMessageProduct.textContent = msg;

        setTimeout(() => {
            notificationLow.classList.remove("visible");
            notificationContainerStockLow.classList.remove("active");
            
            setTimeout(() => {
                notificationMessageProduct.classList.remove("active");
            }, 500);
        }, 3000);
    }

    // Manipulador de eventos para botões de exclusão
    document.querySelectorAll('.btn-delete').forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const productId = this.getAttribute('data-id');

            if (confirm("Tem certeza que deseja deletar este produto?")) {
                fetch(`/product/products/delete_ajax/${productId}/`, {
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

    // Simular uma notificação de estoque baixo para teste
    setTimeout(() => {
        queueMessage("Produto com estoque baixo: Filtro de ar", "warning");
    }, 2000);

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
});