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
  });