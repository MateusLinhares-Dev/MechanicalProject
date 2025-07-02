document.addEventListener('DOMContentLoaded', function() {
    // Estilizar os campos do formulário
    const formSelects = document.querySelectorAll('select');
    formSelects.forEach(select => {
      select.classList.add('form-select');
    });
    
    const formInputs = document.querySelectorAll('input');
    formInputs.forEach(input => {
      input.classList.add('form-control');
    });
    
    const formTextareas = document.querySelectorAll('textarea');
    formTextareas.forEach(textarea => {
      textarea.classList.add('form-control');
    });
    
    // Auto-preencher o preço quando o tipo de serviço é selecionado
    const serviceTypeSelect = document.getElementById('{{ form.service_type.id_for_label }}');
    const priceInput = document.getElementById('{{ form.price.id_for_label }}');
    
    if (serviceTypeSelect && priceInput) {
      serviceTypeSelect.addEventListener('change', function() {
        const selectedOption = this.options[this.selectedIndex];
        if (selectedOption.dataset.price) {
          priceInput.value = selectedOption.dataset.price;
        }
      });
    }
  });