document.addEventListener('DOMContentLoaded', function() {

    const formSelects = document.querySelectorAll('select');
    formSelects.forEach(select => {
      select.classList.add('form-select');
    });
    
    const formInputs = document.querySelectorAll('input');
    formInputs.forEach(input => {
      input.classList.add('form-control');
    });
    
    // Auto-preencher o preço quando o produto é selecionado
    const productSelect = document.getElementById('{{ form.product.id_for_label }}');
    const unitPriceInput = document.getElementById('{{ form.unit_price.id_for_label }}');
    
    if (productSelect && unitPriceInput) {
      productSelect.addEventListener('change', function() {
        const selectedOption = this.options[this.selectedIndex];
        if (selectedOption.dataset.price) {
          unitPriceInput.value = selectedOption.dataset.price;
        }
      });
    }
  });