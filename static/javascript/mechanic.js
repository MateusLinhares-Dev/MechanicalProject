document.addEventListener('DOMContentLoaded', function () {
    const robotContainer = document.getElementById("robot-notification-container");
    const robotNotification = document.getElementById("robot-notification");
    const robotArm = document.getElementById("robot-arm");
    const robotMessage = document.getElementById("robot-message");

    let messageQueue = [];
    let isShowingMessage = false;
    
    function queueMessage(msg, type) {
        if (!msg || typeof msg !== 'string') {
            console.error('Mensagem inválida:', msg);
            return;
        }
        
        messageQueue.push({msg, type});
        console.log('Mensagem adicionada à fila:', messageQueue);
        processMessageQueue();
    }

    function processMessageQueue() {
        if (isShowingMessage || messageQueue.length === 0) return;
        
        isShowingMessage = true;
        const { msg, type } = messageQueue.shift();

        // Ativa as notificações do robô
        robotContainer.classList.add("active");
        robotArm.classList.add("active");
        robotNotification.classList.add("visible");

        robotMessage.innerHTML = `${type === "success" ? "✅" : type === "warning" ? "⚠️" : "❌"} ${msg}`;
        robotMessage.className = `robot-message ${type}`;


        setTimeout(() => {
            robotNotification.classList.remove("visible");
            robotArm.classList.remove("active");
            robotContainer.classList.remove("active");

            setTimeout(() => {
                isShowingMessage = false;
                processMessageQueue();
            }, 500);
        }, 2500);
    }

    document.querySelectorAll('.btn-delete').forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const productId = this.getAttribute('data-id');

            if (confirm("Tem certeza que deseja excluir este item?")) {
                let url = '';
                if (window.location.pathname.includes('product')) {
                    url = `/product/products/delete_ajax/${productId}/`;
                } else if (window.location.pathname.includes('vehicle')) {
                    url = `/vehicles/delete/${productId}/`;
                } else {
                    console.error('Contexto desconhecido para exclusão');
                    return;
                }

                fetch(url, {
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
                        // força atualização da página
                        location.reload();
                    }
                })
                .catch(error => {
                    console.error('Erro na requisição:', error);
                    queueMessage("Erro ao processar a requisição", "error");
                });
            }
        });
    });

    function checkLowStockProducts() {
        const products = document.querySelectorAll('tr[data-quantity]');
        products.forEach(product => {
            const quantity = parseInt(product.getAttribute('data-quantity'), 10);
            const name = product.getAttribute('data-name');
            
            if (quantity !== undefined && quantity <= 5 && name) {
                queueMessage(`O produto ${name} está com estoque baixo, quantidade: ${quantity}`, "warning");
            }
        });
    }

    // Executa a verificação de estoque baixo após um pequeno delay
    setTimeout(checkLowStockProducts, 1000);

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
