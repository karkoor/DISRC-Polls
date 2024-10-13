document.addEventListener('DOMContentLoaded', function() {
    const voteButtons = document.querySelectorAll('.submit-button');
  
    voteButtons.forEach(button => {
      if (!button.disabled) {
        button.addEventListener('click', function() {
          alert('Thank you for voting!');
        });
      }
    });
  });
  