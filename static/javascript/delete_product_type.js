function DeleteProductTypeById(){ 
    const productTypeSelect = document.getElementById("productTypeSelect")
    const selectedValueId = productTypeSelect.value

    if (!selectedValueId) {
        alert('Nenhum produto selecionado, selecione algum produto para poder deletar!')
        return;
    }

    fetch(`/product/product_type_delete/${selectedValueId}`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Accept": "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        console.log('Resposta do servidor: ', data);
        if (data.status === "success") {
            location.reload();
        }
    })
    .catch(error => {
        console.error('Erro na requisição:', error);
        showMessage("Erro ao processar a requisição", "error");
    });

    
}

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

const select = document.getElementById('productTypeSelect');
const filterInput = document.getElementById('filterInput');

filterInput.addEventListener('input', () => {
    const filterText = filterInput.value.toLowerCase();

    select.querySelectorAll('option').forEach(option => {
    const optionText = option.textContent.toLowerCase(); 

    if (optionText.includes(filterText)) {
        option.style.display = '';
    } else {
        option.style.display = 'none';
    }
    });
});