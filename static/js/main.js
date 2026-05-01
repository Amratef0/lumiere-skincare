document.addEventListener("DOMContentLoaded", function () {

  const exploreBtn = document.querySelector('.hero .btn-primary');
  const storyBtn = document.querySelector('.hero .btn-ghost');
 
  const productCards = document.querySelectorAll('.product-card');

  //  Product click
  if (productCards.length > 0) {
    productCards.forEach(card => {
      card.addEventListener('click', (e) => {

       
        if (e.target.closest("form") || e.target.tagName === "BUTTON") return;

        const id = card.dataset.id;
        if (id) {
          window.location.href = `/product/${id}`;
        }
      });
    });
  }

  
  //  Explore button
  if (exploreBtn) {
    exploreBtn.addEventListener('click', () => {
      window.location.href = "/shop";
    });
  }
  
  //  Story button
  if (storyBtn) {
    storyBtn.addEventListener('click', () => {
      window.location.href = "/about";
    });
  }

});


