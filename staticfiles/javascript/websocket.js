document.addEventListener('DOMContentLoaded', function () {
    let notifications = JSON.parse(localStorage.getItem('notifications') || '[]');

    function updateMenu() {
        console.log('passando aqui')
        const menu = document.getElementById('notification-message-product');
        const notificationLowBox = document.getElementById('notification-low');
        const notificationContainerStockLow = document.getElementById('notification-container-stock-low');

        if (!menu || !notificationLowBox) {
            console.warn("Elementos de notificação não encontrados.");
            return;
        }

        let index = 0;
        if (notifications.length === 0) return;

        const interval = setInterval(() => {
            if (index >= notifications.length) {
                clearInterval(interval);
                notificationLowBox.classList.remove('visible');
                removeItemLocalStorage(10000)
                return;
            }
            notificationContainerStockLow.classList.add('active');
            notificationLowBox.classList.add('visible');
            
            const notif = notifications[index];
            const textContent = `O produto ${notif.message.name_product} está abaixo do estoque, quantidade: ${notif.message.quantity}`;
            menu.innerHTML = textContent;
            menu.className = `notification-message-product active`;

            index++;
        }, 2000);
    }

    function connectSocket() {
        notificationSocket = new WebSocket(
            (window.location.protocol === "https:" ? "wss://" : "ws://") + window.location.host + '/ws/notifications/'
        );

        notificationSocket.onopen = function () {
            console.log("WebSocket conectado");
        };

        notificationSocket.onmessage = function (e) {
            try {
                const data = JSON.parse(e.data);
                notifications = notifications.concat(data.notifications);
                localStorage.setItem('notifications', JSON.stringify(notifications));
                updateMenu();
            } catch (err) {
                console.error("Erro ao processar mensagem:", err);
            }
        };

        notificationSocket.onclose = function () {
            console.warn('WebSocket fechado, tentando reconectar em 5s...');
            setTimeout(() => {
                connectSocket();
            }, 5000);
        };

        notificationSocket.onerror = function (e) {
            console.error('Erro no WebSocket:', e);
        };
    }

    function removeItemLocalStorage(seconds) {
        setTimeout(() => {
            const notification = document.getElementById('notification-message-product');

            localStorage.removeItem('notifications');

            notifications = [];

            if (notification) {
                notification.innerHTML = '';
            }

            console.log('Notification removido');
        }, seconds);
    }

    connectSocket();
    updateMenu();
});
